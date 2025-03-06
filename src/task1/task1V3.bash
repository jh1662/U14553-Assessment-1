#!/bin/bash
#^ Shebang line tells to execute this file using the Bash shell.

#x Function returns works differently to other languages.
#x Opposite to others, in BASH, a returned 0 means success and a returned 1 is fail (contrasting the 1=true and 0=false).
#x This is because BASH returns are for status codes rather then boolean.
#x Source: https://labex.io/tutorials/shell-bash-function-return-values-391153#understanding-function-return-codes .
#x This is important to know because if-statments will only return true if called function returns 0.

#x Used ShellCheck (https://www.shellcheck.net/) to help enforce good BASH programming practice.

#x Developer made sure to add semi-colon at the end of all appropiate lines a stricter but better programming practice.

menu(){
    clear
    #^ Makes is easier for user be clearing everyting else in the current terminal.
    echo "Hi!"
    #^ Friendly indication that the program has started.
    displayMenu;
    #^ Display commands.
    while true; do
        read -p "Please enter a command ('help' for commands):" -r option;
        #^ "-r" argument prevents backslashes ('\') from being interpreted as special characters such as new line ('\n') (SC2162 - https://www.shellcheck.net/wiki/SC2162).
        #^ "-p" argument displays text to terminal before waiting for user input - like 'echo' before but on the same line/
        case $option in
            "list") list ;;
            "move") move ;;
            "rename") rename ;;
            "delete") delete ;;
            "backup") backup ;;
            "exit") confirmExit ;;
            "help") displayMenu ;;
            *) printf "Error - unknown command try again.\nType 'help' to view all script commands." ;;
            #^ 'printf' allows formatting of special characters such as '\n' to new line character.
        esac
    done

}
#region Command functions
#: Command functions - one function per command.
displayMenu(){
    #* Executes on start and when command 'help' is used.
    #* Function purposely not called 'help' to not call the bash in-built function instead.
    #: Easier to use multiple echo commands than printf for this ASCII menu display.
    echo "===================================================================================================="
    echo "Intelligent File Manager - Main Menu"
    echo "===================================================================================================="
    echo "> list [directory path] - List all files in a directory"
    echo "> move [file path] [directory path]- Move a file to a different folder"
    echo "> rename [file path] [new name] - Rename a file"
    echo "> delete [file path] - delete a file"
    echo "> backup [file path] - manually backup a file"
    echo "> exit - exit the program"
    echo "> help - View the main menu"
    echo "===================================================================================================="

}
list(){
    read -p "Please enter directory path" -r dirPath;
    echo "RESULT $(! validation "$dirPath" 1)";
    if ! validation "$dirPath" 1; then return; fi
    #^ If validation fails, then exit function.
    #^ Does not work with square brackets ('[' and ']').

    printf "Permissions\tLinks\tOwner\t\tGroup\t\tSize\tLast Modified\t\tName\n";
    #^ '\t' means tab - to allow spacing between toe column labels
    echo "===================================================================================================="
    ls -lht "$dirPath" | grep -v "^total" | while read -r permissions links owner group size date time name; do
        printf "%-12s\t%-5s\t%-15s\t%-15s\t%-4s\t%-20s\t%s\n" "$permissions" "$links" "$owner" "$group" "$size" "$date $time" "$name"
    done
    #^ Takes the result 'ls -lht "$dirPath"' and pipe the result into the grep command and then into awk command.
    #^ For 'ls', the following arguments: 'l' - provide extra details, 'h' - prints storage sizes in human-readable format, and '-t' sort rows by latest modification timestamps.
    #^ Numbers after '%-' (and before 's') means the number of characters they occupy (regardless of string being under or over that count).
    #^ For example: '%-12s' mean that string must occuppy 12 charaters.
    #^ This allows the columns to alaign with the tab seperated headings.
    #^ Not allowed to use the 'awk' command so will use a while-loop instead.

    backupLog "Listed directory - $(realpath "$dirPath")";
    #^ log command to 'backup_log.txt' with the absolute directory path instead of relative one.
}
delete(){
    read -p "Please enter file path" -r filePath;
    if ! validation "$filePath" 0; then return; fi
    #^ Check if path exist and leads the a file.
    if confirm "Are you sure you want to delete file at path: $filePath ?"; then
        #^ Ask for user's confirmation
        backupFile "$filePath";
        #^ automatically back file before deletion.
        rm "$filePath";
        #^ Deletion operation.
        echo "File deleted.";
        #^ Notify user of success.
        if [ ! "$(realpath "$(dirname "$filePath")")" == "$(realpath "./backup/")" ]; then
            #^ All in same line to save space and also because is not needed again in function afterwards.
            #^ Comparing as absolute paths incase user uses absolute path to delete
            backupLog "Deleted file - $(realpath "$filePath")";
        fi
    fi
    echo "File deletion cancelled."
    #^ Send message when user cancel file deletion
}
move(){
    read -p "Please enter file path to move" -r filePath;
    read -p "Please enter destination directory path to move to" -r dirPath;
    if validatation "$filePath" 0 -o validate "$dirPath" 1; then return; fi
    #^ No need to return status code as it will not be needed by caller function.
    mv "$filePath" "$dirPath";
    #^ The moving operation.
}
rename(){
    #: Gather inputs.
    read -p "Please enter file path to rename" -r filePath;
    read -p "Please enter new name" -r newName;

    if validatation "$(dirname "$filePath")/$newName;" 0 -o ; then return; fi
    #^ Cannot rename a non-existing file.
    mv -i "$filePath" "$(dirname "$filePath")/$newName";
    #^ Use the move command ('mv') to move to exact same director but with different name.
    #^ Not move's main purpose but works perfectly fine and is still good practice.
}
confirmExit(){
    #* Executes when command 'exit' is used.
    #* Confirm if user wated to exit or not, if no yes ('Y') or no ('N'), state it and then ask again.
    #* Function purposely not called 'exit' to not call the bash in-built function instead.
    if confirm "Are you sure you want to exit [Y/N]"; then
        printf "Conformed exit.\nBye!";
        backupLog "Exited program";
        exit 0;
        #^ Ends program.
    fi
    echo "Returning to main menu";
    #^ display message when user does not want to exit.
}
#endregion
#region Common functions
#: Common functions - functions used by one or more command functions.
confirm(){
    #* To be used for exit and deleting files
    prompt="$1";
        while true; do
        read -p "$prompt" -r confirmation;
        confirmation=$(echo "$confirmation" | tr '[:lower:]' '[:upper:]' | tr -d '[:space:]');
        #^ Parsing it - convert all to uppercase then remove any whitespaces.
            if [ "$confirmation" == "Y" ]; then
                #^ 'confirmation' inside double quotes to prevent globbing and word splitting (SC2086 - https://www.shellcheck.net/wiki/SC2086 ).
                echo "Confirmed success";
                return 0;
        elif [ "$confirmation" == "N" ]; then
                echo "Confirmed fail";
                return 1;
            else
                #* Users submit an unexpected input.
                printf "Error - unexpected input.\nInput must either be Y or N (your input: '%s').\nPlease try again.\n" "$confirmation";
                #^ Apparently it is better use '%s' instead of '$confirmation'.
                #^ Unlike 'echo', need to add new line ('\n') at end or the next output will be on same line.
            fi
    done
}
validation(){
    #* Checks if path exist and if it leads to a file or directory.
    local path=$1;
    local isFile=$2;
    //local isLoud=$3;
        echo "Checking path of: $(realpath "$path")";
        #^ 'realpath' feature informs user of the absolute version of the path incase they got confused with the relative path.
        if [ -e "$path" ]; then
            #^ Does path exist?
            if [ "$isFile" -eq 0 ]; then
                #^ Should path lead to a file?
                if [ -f "$path" ]; then
                    #^ Does path lead actually to a file?
                    echo "File found."
                    return 0;
                    #^ In bash, 'return 0' means returning true.
                else
                    printf "Error - path '%s' does not lead to a file (to a directory intead)" "$path";
                    return 1;
                    #^ In bash, 'return 1' means returning true.
                fi
            else
                if [ -d "$path" ]; then
                    echo "Directory found."
                    #^ Does path lead actually to a directory?
                    return 0;
                else
                    printf "Error - path '%s' does not lead to a directory (to a file intead)" "$path";
                    return 1;
                fi
            fi
        else
            printf "Error - non-existant path - the path '%s' leads to a file instead of a directory" "$path";
        return 0;
        fi
}
backupLog(){
    operation="$1"
    #^ describing what happened - command used and inputs (such as filepath).
    echo "Date: $(date +"%Y-%m-%d %H:%M:%S") | command: $operation " >> backup_log.txt
    #^ Construct string (the log) and append ('>>') it to file 'backup_log.txt'.
    #^ If 'backup_log.txt' does not exist, then create it then append log to it.
    #^ File name convension is different to usual because it was specified in assaignment.
}
backupFile(){
    #* No need to validate paths here because they will be already be validated by caller function.
    filePath="$1";
    #^ To know which file to make a back up of.
    fileName=$(basename "$filePath - $(date +"%Y-%m-%d-%H:%M:%S")");
    #^ More compact, yet still simple.
    #^ Far simplier, than manually finding where slice and slice the string file path thanks to 'basename'.
    #^ Source: https://www.tutorialspoint.com/unix_commands/basename.htm .
    #^ Checked and it is allowed to have colons in linux file names (ext[2-4]) - https://stackoverflow.com/questions/4814040/allowed-characters-in-filename .
    backupDir="./backup/";
    #^ Decalred to own variable because is referanced more than once.
    if validation "$backupDir"; then mkdir "$backupDir"; fi
    #^ Create back up directory if does not already exist.
    #^ Due to its simplicity, its compressed into a single line.
    cp -i "$filePath" "$backupDir$fileName";
    #^ 'cp' allows specifying new name whe copying file over - as mentioned in source: https://linuxize.com/post/cp-command-in-linux/ .
    #^ '-i' is for confimation if back up was to overwite another file but near impossible that will happen because of use of timestamps in the file name.
    totalSize=$(du -sm "backupDir" | cut -f1)
    #^ 'du' command stands for disk usage and shows infomation regarding sizes of subjected directory.
    #^ Argument '-s' only fetched the total size of the directory.
    #^ Argument '-m' shows size in MB.
    #^ Not using '-h' because value will be compared against.
    #^ 'cut' command fetches the first column ('-f1') of the result - displaying "[size]MB" instead of "[size]MB ./backupDir".
    #^ 'du' command source - https://www.tutorialspoint.com/unix_commands/du.htm
    #^ 'cut' command source - https://www.tutorialspoint.com/unix_commands/cut.htm
    if [ "$totalSize" -gt 500 ]; then
        #^ '-gt' argument is same as greater than ('>').
        echo "Warning - contents of backup directory exceeds 500 MB (currently $totalSize MB). Concider deleting some files.";
    fi
}
#endregion
menu;

