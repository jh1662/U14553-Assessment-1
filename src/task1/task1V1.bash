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
            "list") echo "list" ;;
            "move") echo "move" ;;
            "rename") echo "rename" ;;
            "delete") echo "delete" ;;
            "backup") echo "backup" ;;
            "exit") confirmExit ;;
            "help") displayMenu ;;
            *) printf "Unknown command try again.\nType 'help' to view all script commands." ;;
            #^ 'printf' allows formatting of special characters such as '\n' to new line character.
        esac
    done

}
#region Command functions
#: Command functions - one function per command.

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
                printf "Error - unexpected input./nInput must either be Y or N (your input: "%s").\nPlease try again." "$confirmation";
                #^ apparently it is better use '%s' instead of '$confirmation'
            fi
    done
}
displayMenu(){
    #* Executes on start and when command 'help' is used.
    #* Function purposely not called 'help' to not call the bash in-built function instead.
    #: Easier to use multiple echo commands than printf for this ASCII menu display.
    echo "===================================================================================="
    echo "Intelligent File Manager - Main Menu"
    echo "===================================================================================="
    echo "list [directory path] - List all files in a directory"
    echo "move [file path] [directory path]- Move a file to a different folder"
    echo "rename [file path] [new name] - Rename a file"
    echo "delete [file path] - delete a file"
    echo "backup [file path] - manually backup a file"
    echo "exit - exit the program"
    echo "help - View the main menu"
    echo "===================================================================================="
    echo "Either call command by number or name"
    echo "===================================================================================="

}
#endregion
menu