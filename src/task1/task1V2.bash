#!/bin/bash
#^ Shebang line tells to execute this file using the Bash shell.
menu(){
    clear
    #^ Makes is easier for user be clearing everyting else in the current terminal.
    echo "Hi!"
    #^ Friendly indication that the program has started.
    displayMenu;
    #^ Display commands.
    while true; do
        read -p "Please enter a command ('help' for commands):" -r option;
        #^ "-r" argument prevents backslashes ('\') from being interpreted as special characters such as new line ('\n') (SC2162).
        #^ "-p" argument displays text to terminal before waiting for user input - like 'echo' before but on the same line/
        case $option in
            "list") list ;;
            "move") echo "move" ;;
            "rename") echo "rename" ;;
            "delete") echo "delete" ;;
            "backup") echo "backup" ;;
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
    echo "===================================================================================="
    echo "Intelligent File Manager - Main Menu"
    echo "===================================================================================="
    echo "> list [directory path] - List all files in a directory"
    echo "> move [file path] [directory path]- Move a file to a different folder"
    echo "> rename [file path] [new name] - Rename a file"
    echo "> delete [file path] - delete a file"
    echo "> backup [file path] - manually backup a file"
    echo "> exit - exit the program"
    echo "> help - View the main menu"
    echo "===================================================================================="

}
list(){
    read -p "Please enter directory path" -r filePath;
    if validation "$filePath" 0; then return; fi
    #^ If validation fails, then exit function.
    #^ Does not work with square brackets ('[' and ']').

    printf "Permissions\tLinks\tOwner\t\tGroup\t\tSize\tLast Modified\t\tName\n";
    #^ '\t' means tab - to allow spacing between toe column labels
    echo "===================================================================================="
    ls -lht "$filePath" | grep -v "^total" | awk '{printf "%-12s\t%-5s\t%-15s\t%-15s\t%-8s\t%-20s\t%s\n", $1, $2, $3, $4, $5, $6 " " $7 " " $8, $9}'
    #^ Takes the result 'ls -lht "$filePath"' and pipe the result into the grep command and then into awk command.
    #^ For 'ls', the following arguments: 'l' - provide extra details, 'h' - prints storage sizes in human-readable format, and '-t' sort rows by latest modification timestamps.
    #^ Numbers after '%-' (and before 's') means the number of characters they occupy (regardless of string being under or over that count).
    #^ For example: '%-12s' mean that string must occuppy 12 charaters.
    #^ This allows the columns to alaign with the tab seperated headings.
}
#endregion
#region Common functions
#: Common functions - functions used by one or more command functions.
confirmExit(){
    #* Executes when command 'exit' is used.
    #* Confirm if user wated to exit or not, if no yes ('Y') or no ('N'), state it and then ask again.
    #* Function purposely not called 'exit' to not call the bash in-built function instead.
    while true; do
        read -p "Are you sure you want to exit [Y/N]" -r confirmation;
        confirmation=$(echo "$confirmation" | tr '[:lower:]' '[:upper:]' | tr -d '[:space:]');
        #^ Parsing it - convert all to uppercase then remove any whitespaces.
            if [ "$confirmation" == "Y" ]; then
                #^ 'confirmation' inside double quotes to prevent globbing and word splitting (SC2086).
                printf "Confirmed exit.\nBye!";
                exit 0;
        elif [ "$confirmation" == "N" ]; then
                echo "Returning to main menu";
                break;
            else
                #* Users submit an unexpected input.
                printf "Error - unexpected input./nInput must either be Y or N (your input: '%s').\nPlease try again." "$confirmation";
                #^ apparently it is better use '%s' instead of '$confirmation'
            fi
    done
}
validation(){
    #* Checks if path exist and if it leads to a file or directory.
    local path=$1;
    local isFile=$2;
        if [ -e "$path" ]; then
            #^ Does path exist?
            if [ "$isFile" -eq 1 ]; then
                #^ Should path lead to a file?
                if [ -f "$path" ]; then
                    #^ Does path lead actually to a directory?
                    return 1;
                else
                    printf "Error - path '%s' does not lead to a file (to a directory intead)" "$path";
                    return 0;
                fi
            else
                if [ -d "$path" ]; then
                    #^ Does path lead actually to a directory?
                    return 1;
                else
                    printf "Error - path '%s' does not lead to a directory (to a file intead)" "$path";
                    return 0;
                fi
            fi
        else
            printf "Error - non-existant path - the path '%s' leads to a file instead of a directory" "$path";
        return 0;
        fi
}
#endregion
menu;