#!/bin/bash
#^ Shebang line tells to execute this file using the Bash shell.

#: constants for easier communication between functions
validExtensions=(.pdf .docx);
#^ Allowed file extensions for assignment submissions.
sizeLimit=$((50 * 1024 * 1024));
#^ Maximum file size allowed is 50 MB.
submissionLog="./submission_log.txt";
#^ Log file for assignment submissions.
submissionDir="./submissions";
#^ Directory where submitted assignment files are stored.

#x Due to the sheer amount of functions, nested regions are used to keep code organised.

menu(){
    #* Taken from Task 1 and modified to fit needs.
    clear;
    #^ Clear the terminal to start with a fresh interface.
    echo "Hi!";
    #^ Friendly greeting to the user.
    displayMenu;
    while true; do
        read -p "Please enter a command ('help' for commands): " -r option;
        option=$(echo "$option" | tr '[:lower:]' '[:upper:]');
        case $option in
            "SUBMIT") submit ;;
            "LOGS") logs ;;
            "CHECK") check ;;
            "EXIT") confirmExit ;;
            "HELP") displayMenu ;;
            *) printf "Error - unknown command '%s', try again.\nType 'help' to view all script commands.\n" "$option";;
        esac;
    done;
}

#region Command Functions
#: functions are in order in accordance to the switch-statement in the 'menu()' function
#region write-to functions
submit(){
    #* Manage the overall submission process.
    read -p "Please enter file path: " -r filePath;
    validSubmission "$filePath"; if [ $? -ne 0 ]; then return; fi;
    uploadSubmission "$filePath";
    appendLog "$(basename "$filePath")";
}
logs(){
    #* Display all assignment submission logs.
    logsContent="$(getSubmissionLogs)";
    if [ -z "$logsContent" ]; then
        echo "No submissions so far!";
        return;
    fi;
    echo "All submission logs:";
    echo "$logsContent";
}
#endregion
#region read-from only functions
check(){
    #* Allow the user to verify if a file has been submitted.
    read -p "Please enter file name (case sensitive): " -r fileName;
    if echo "$fileName" | grep -q " "; then
        #^ 'grep' command source - https://www.tutorialspoint.com/unix_commands/grep.htm
        #* Check for white-spaces in the file name.
        printf "Error - file name cannot have white-spaces. Inputted filepath - %s\n" "$filePath";
        return 1;
    fi;
    if [ -d "$submissionDir" ]; then
        if [ -f "$submissionDir/$fileName" ]; then
            echo "File '$fileName' exists in submissions.";
            return 0;
        fi;
    fi;
    echo "File '$fileName' has not been submitted.";
    return 1;
}
confirmExit(){
    #* Function taken from Task 2 (modified - removed logging part as Task 3 does not says to include it)
    #* Executes when command 'exit' is used.
    #* Confirm if user wated to exit or not, if no yes ('Y') or no ('N'), state it and then ask again.
    #* Function purposely not called 'exit' to not call the bash in-built function instead.
    if confirm "Are you sure you want to exit [Y/N]"; then
        printf "Conformed exit.\nBye!";
        exit 0;
        #^ Ends program.
    fi
    echo "Returning to main menu";
    #^ display message when user does not want to exit.
}
displayMenu(){
    #* Show the complete list of available commands for both systems.
    echo "===================================================================================================="
    echo "Composite System - Assignment Submission & File Manager"
    echo "===================================================================================================="
    echo "> submit - Submit an assignment"
    echo "> logs - View submission logs"
    echo "> check - Check if an assignment has been submitted"
    echo "> exit - Exit the program"
    echo "> help - View this menu"
    echo "===================================================================================================="
}
#endregion
#endregion
#region Utility Functions (called by command functions)
#region logging functions
getSubmissionLogs(){
    #* Retrieve and display assignment submission logs.
    if [ -f "$submissionLog" ]; then
        cat "$submissionLog";
    else
        echo "";
    fi;
}
appendLog(){
    #* Log the file submission with a timestamp.
    filename=$1;
    timestamp=$(date "+%Y-%m-%d %H:%M:%S");
    #^ 'date' command source - https://www.tutorialspoint.com/unix_commands/date.htm
    entry="Submitted file: ${filename} - timestamp of submission: ${timestamp}";
    echo "$entry" >> "$submissionLog";
}
#endregion
#region validation functions
validation(){
    #* Function taken from Task 1 (not modified)
    #* Checks if path exist and if it leads to a file or directory.
    path=$1;
    isFile=$2;
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
                    printf "Error - path '%s' does not lead to a file (to a directory intead)\n" "$path";
                    return 1;
                    #^ In bash, 'return 1' means returning false.
                fi
            else
                if [ -d "$path" ]; then
                    echo "Directory found."
                    #^ Does path lead actually to a directory?
                    return 0;
                else
                    printf "Error - path '%s' does not lead to a directory (to a file intead)\n" "$path";
                    return 1;
                fi
            fi
        else
            printf "Error - non-existant path - the path '%s' leads to a file instead of a directory\n" "$path";
        return 1;
        fi
}
validateMetadata(){
    #* Validate the submission file's name and properties.
    #* Checks for: white-spaces, presence of a dot in the filename, valid extension, file existence, and file size.
    filePath=$1;
    #^ The complete path of the file to validate.
    baseName=$(basename "$filePath");
    #^ Extracts just the file name.
    #^ 'basename' command source - https://www.tutorialspoint.com/unix_commands/basename.htm
    if echo "$baseName" | grep -q " "; then
        #^ 'grep' command source - https://www.tutorialspoint.com/unix_commands/grep.htm
        #* Check for white-spaces in the file name.
        printf "Error - file name cannot have white-spaces. Inputted filepath - %s\n" "$filePath";
        return 1;
    fi;
    if [[ "$baseName" != *.* ]]; then
        #* Ensure the file name contains at least one dot separating name and extension.
        printf "Invalid file type - must have at least one dot inside\n";
        return 1;
    fi;

    ext=".${baseName##*.}"
    #^ Extract the file extension using Bash parameter expansion.
    #^ Extension is extracted by removing everything up to the last dot.
    #^ Alternative to 'awk'.
    #^ Source - https://www.gnu.org/software/bash/manual/html_node/Shell-Parameter-Expansion.html .

    allowed=0;
    #^ 'allowed' is a flag (0: not allowed, 1: allowed).
    for valid in "${validExtensions[@]}"; do
        if [ "$ext" == "$valid" ]; then
            allowed=1;
            break;
        fi;
    done;
    if [ $allowed -eq 0 ]; then
        printf "Invalid file type - can only use PDFs or Microsoft Word files (.pdf or .docx)\n";
        return 1;
    fi;
    if [ ! -f "$filePath" ]; then
        #* Verify that the file exists.
        printf "Error - file path does not exist: %s\n" "$filePath";
        return 1;
    fi;
    fileSize=$(stat -c%s "$filePath");
    #^ Check that the file size does not exceed the allowed limit.
    #^ 'stat' command source - https://www.tutorialspoint.com/unix_commands/stat.htm
    if [ "$fileSize" -gt "$sizeLimit" ]; then
        printf "Invalid file size - file size is above 5MB\n";
        return 1;
    fi;
    return 0;
}
checkDuplicate(){
    #*Prevent duplicate submissions by checking if a file with the same name already exists.
    filePath=$1;
    baseName=$(basename "$filePath");
    if [ -d "$submissionDir" ]; then
        if [ -f "$submissionDir/$baseName" ]; then
            printf "File with name has been found in uploaded submissions!\n";
            return 1;
        fi;
    fi;
    return 0;
}
validSubmission(){
    #* Run all validations on the file for submission.
    filePath=$1;
    validateMetadata "$filePath"; if [ $? -ne 0 ]; then return 1; fi;
    checkDuplicate "$filePath"; if [ $? -ne 0 ]; then return 1; fi;
    return 0;
}
#endregion
uploadSubmission(){
    #* Copy the validated file to the submissions directory.
    filePath=$1;
    mkdir -p "$submissionDir";
    #^ 'mkdir' command source - https://www.tutorialspoint.com/unix_commands/mkdir.htm
    cp "$filePath" "$submissionDir/$(basename "$filePath")";
    #^ 'cp' command usage reference - https://linuxize.com/post/cp-command-in-linux/
    echo "File uploaded successfully";
}
confirm(){
    #* Prompt the user for Y/N confirmation.
    #* Function taken Task 1 and is unmodified.
    prompt="$1";
        while true; do
        read -p "$prompt: " -r confirmation;
        confirmation=$(echo "$confirmation" | tr '[:lower:]' '[:upper:]');
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

#endregion
menu;
#^ Finally, start the composite menu and wait for user input.
