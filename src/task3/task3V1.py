from datetime import datetime
#^ Import non-external library to allow the use of timestamps.
#^ used "from datetime" so don't have to call from datetime twice like "datetime.datetime.now()".
import os
#^ Import non-external library to allow the use opening, editing and creating text files for logs.
from pathlib import Path
#^ Allow paths work cross-platform - able to use on both Windows and Linux.
#^ Also allows in-built feature such as '.exists()'
import sys
#^ 'sys.exit()' allows for better termination of Python program than other alternatives like 'quit()'

#x IMPORTANT: This program made of mostly recycled and modified parts of task 2

#x Classes was used instead of functions as it allows OOP’s modularity to make code more organised -
#x methods grouped up into classes ‘Validation’, ‘Logging’, ‘RequestSystem’ and make it more
#x reusable/recyclable.

#x Many print statements used to satisfy Human-Computer Interaction (HCI) principle.

#x Use be terminal satisfies "Keep It Simple, Stupid" (KISS) principle.

#x Assume each file name has no spaces (replaced with underscores) for compatability with legacy linux OSs.

class Validation:
    validExtentions = [".pdf",".docx"]
    sizeLimit = 5 * 1024 * 1024
    #^ '1024' because 5MB instead of 5MiB.

    def fileMetadata(self, filePath):
        extention = os.path.basename(filePath).rsplit('.', 1)[-1]
        #^ Gets characters after last dot in string.
        #^ If no dots then it returns the string - no errors.
        if extention not in self.validExtentions:
            #^ Check if file name has none of the file extentions.
            #^ Far simpler alternative than a for-loop.
            print("Invalid file type - can only use PDFs or Microsoft Word files (.pdf or .docx)")
            return False
        if os.path.getsize(filePath) > self.sizeLimit:
            print("Invalid file size - file size is above 50MB")
            return False
        return True

    def isDuplicate(self, filePath):
        filename = filePath.rsplit('/', 1)[-1]
        pass

    def validSubmission(self, filePath):
        if " " in os.path.basename(filePath):
            print(f"Error - file name cannot have white-spaces. Inputted filepath - {filePath}")
        if not filePath.exists():
            print(f"Error - file path does not exist. Inputted filepath - {filePath}")
            return False
        if not self.fileMetadata(filePath): return False
        if not self.isDuplicate(self, filePath): return False
        return True

class Logging:
    logFile = Path("./submission_log.txt")
    submissionDir = Path("./submissions/")

    #: Modified and reused from task 2 ('Logging.appendEntry')
    def appendEntry(self, entry: str):
        #* syntax 'with' is used to make code simpler - don't have to flush the buffer then close file client.
        if not os.path.exists(self.logFile):
            with open(self.logFile, "w") as file: file.write("")
            #^ Create text file if does not exist.
            #^ 'w' argument means write mode.
        with open(self.logFile, "a") as file: file.write(entry+"\n")
        #^ Append entry to file.
        #^ New line to indicate new entry.

    #: Modified and reused from task 2 ('Logging.appendLog')
    def appendLog(self, filename: str):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        #^ For when the action was done for the log.
        entry += f"Sumitted file: {filename} - timestamp of submission: {timestamp}"
        #^ Creating entry based on action, data/details, and current timestamp of action.
        #^ Structure - filename then submission timestamp.
        self.appendEntry(self,entry)
        #^ Does the appending operation.

    def getSubmissions(self):
        #* More reliable to check sumbitted files themselves rather than 'submission_log.txt' because it may say something is there or not
        #* when infact its the opposite (CAN ONLY HAPPEN IN DIRECTORY'S OR LOG FILE'S CONTENT ARE MANUALLY ALTERED IN ANY WAY).
        #* Reliability > computational time.
        results = []
        if not os.path.isdir(self.submissionDir): return results
        #^ If file cannot be found, assume no submissions have been make.
        #^ Return empty list if directory cannot be found.
        results = [str(file.name) for file in self.submissionDir.iterdir() if file.is_file()]
        #^ Make a list that contains every file in the submission directory.
        return results

    def getSubmissionLogs(self):
        #* Uses submission_log.txt because timestamps (of submissions) are required.
        results = []
        if not os.path.exists(self.logFile): results
        #^ If file cannot be found, assume no submissions have been made.
        with open(self.logFile, "r") as file:
            #^ 'r' argument means read mode.
            for line in file:
                #^ Each line is a single submission.
                if line == "": return []
                #^ If file exist but empty, then return nothing.
                #^ Assume that user has not tampered with text file by leaving empty lines.
                sublist = line.strip().split(" -")
                #^ Each element is saperated, by a space whitespace and dash ("- ").
                results.append(sublist)
                #^ Add sub-list of elements to 2D list.
        return results

class submissionInterface:
    logging = Logging
    validation = Validation

    #: Modified and reused from task 2 ('RequestSystem.menu')
    def menu(self):
        #^ The 'self' argument is a referance to the class instance to allow modifying/reading fields and call other methods.
        #^ The 'self' argument in only needed in the method definition and not in its call.
        #^ Source - https://www.w3schools.com/python/gloss_python_self.asp .
        options = "\nEnter one of the following numbers for the corrosponding option:\n1 - Submit assaignment.\n2 - View all submitted assaignments.\n3 - Check if assaignment has been assaigned.\n4 - Exit.\n: "
        #^ Just like Bash, '\n' means new line.
        #^ ": " indicates for user input.
        #^ Empty line at top to help saperate from console messages of past commands/options.
        while True:
            #^ Python boolean has the first letter of the syntax capitalised.
            option = input(options).strip()
            #^ '.strip()' to remove any whitespaces to reduce the number of possible validation errors.
            #^ Did not need to convert to integer because that would require more complex validation.
            #: Using if-statements because Python does not support switch statements ( https://en.wikipedia.org/wiki/Switch_statement )
            if option == "1": self.submit()
            elif option == "2": self.viewAll()
            elif option == "3": self.isSubmitted()
            elif option == "4": self.confirmExit()
            else: print (f"option '{option}' does not exist, has to be an integer in between the range 1 to 4")
            #^ Deals with invalid option inputs (any string that is not '1', '2', '3', or '4')

    def confirmExit():
        while True:
            confimation = input("Are you sure you want to exit [Y/N]").strip().upper()
            if confimation == "Y":
                print("Conformed exit.\nBye!")
                sys.exit()
            if confimation == "N":
                #^ No need 'elif' as program will exit if satisfied previous is-statement.
                print("Returning to main menu.")
                break
            print(f"Error - unexpected input.\nInput must either be Y or N (your input: '{confimation}').\nPlease try again.")
            #^ Deals with unexpected input.

    def viewAll(self):
        submissions = self.logging.getSubmissions()
        print("Timestamp | File name (with extention)")
        for submission in submissions:
            print (f"{submission[0]} | {submission[1]}")

    def isSubmitted(self, FileName: str):
        submissions = self.logging.getSubmissions()
        if submissions == []: return False
        if not FileName in submissions: return False
        #^ Far easier to use 'in' than a whole for-loop.
        return True

    def submit(self):
        filePath = Path(input("Enter file path here: ").strip())
        if not self.validation.validSubmission(filePath): return


