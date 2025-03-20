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
import shutil
#^ Allows the manipulation of files themselves.

#x IMPORTANT: This program made of mostly recycled and modified parts of task 2

#x Classes was used instead of functions as it allows OOP’s modularity to make code more organised -
#x methods grouped up into classes ‘Validation’, ‘Logging’, ‘RequestSystem’ and make it more
#x reusable/recyclable.

#x Many print statements used to satisfy Human-Computer Interaction (HCI) principle.

#x Use be terminal satisfies "Keep It Simple, Stupid" (KISS) principle.

#x Assume each file name has no spaces (replaced with underscores) for compatability with legacy linux OSs.

#x Due to class needing each other, such as Validation calling Logging, they have been made static for simpler communication.

class Validation:
    validExtentions = [".pdf",".docx"]
    sizeLimit = 5 * 1024 * 1024
    #^ '1024' because 5MB instead of 5MiB.

    def fileMetadata(filePath):
        name = os.path.basename(filePath)
        if not "." in name:
            #* Need dot to know file type and prevent getting past the next validation with filenames like just "pdf".
            print("Invalid file type - must have atleast one dot inside")
            return False
        extention = "." + name.rsplit('.', 1)[-1]
        #^ Gets characters after last dot in string.
        #^ If no dots then it returns the string - no errors.
        if extention not in Validation.validExtentions:
            #^ Check if file name has none of the file extentions.
            #^ Far simpler alternative than a for-loop.
            print("Invalid file type - can only use PDFs or Microsoft Word files (.pdf or .docx)")
            return False
        if os.path.getsize(filePath) > Validation.sizeLimit:
            print("Invalid file size - file size is above 50MB")
            return False
        return True

    def isDuplicate(filePath):
        #* Check if file has already been uploaded.
        filename = os.path.basename(filePath)
        #^ Get file name for comparison.
        existingSubmissions = Logging.getSubmissions()
        if filename in existingSubmissions:
            #* If filename is found then it is a dupilcate
            print("File with name has been found in uploaded sumbissions!")
            return True
        return False

    def validSubmission(filePath):
        if " " in os.path.basename(filePath):
            #* Cannot upload a file with whitespaces within for code integrity purposes.
            print(f"Error - file name cannot have white-spaces. Inputted filepath - {filePath}")
        if not filePath.exists():
            #* Cannot upload duplicates
            print(f"Error - file path does not exist. Inputted filepath - {filePath}")
            return False
        #: Other valdiation methods.
        if not Validation.fileMetadata(filePath): return False
        if Validation.isDuplicate(filePath): return False

        return True

class Logging:
    logFile = Path("./submission_log.txt")
    submissionDir = Path("./submissions/")

    #: Modified and reused from task 2 ('Logging.appendEntry')
    def appendEntry(entry: str):
        #* syntax 'with' is used to make code simpler - don't have to flush the buffer then close file client.
        if not os.path.exists(Logging.logFile):
            with open(Logging.logFile, "w") as file: file.write("")
            #^ Create text file if does not exist.
            #^ 'w' argument means write mode.
        with open(Logging.logFile, "a") as file: file.write(entry+"\n")
        #^ Append entry to file.
        #^ New line to indicate new entry.

    #: Modified and reused from task 2 ('Logging.appendLog')
    def appendLog(filename: str):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        #^ For when the action was done for the log.
        entry = f"Sumitted file: {filename} - timestamp of submission: {timestamp}"
        #^ Creating entry based on action, data/details, and current timestamp of action.
        #^ Structure - filename then submission timestamp.
        Logging.appendEntry(entry)
        #^ Does the appending operation.

    def getSubmissions():
        #* More reliable to check sumbitted files themselves rather than 'submission_log.txt' because it may say something is there or not
        #* when infact its the opposite (CAN ONLY HAPPEN IN DIRECTORY'S OR LOG FILE'S CONTENT ARE MANUALLY ALTERED IN ANY WAY).
        #* Reliability > computational time.
        results = []
        if not os.path.isdir(Logging.submissionDir): return results
        #^ If file cannot be found, assume no submissions have been make.
        #^ Return empty list if directory cannot be found.
        results = [str(file.name) for file in Logging.submissionDir.iterdir() if file.is_file()]
        #^ Make a list that contains every file in the submission directory.
        return results

    def getSubmissionLogs():
        #* Uses submission_log.txt because timestamps (of submissions) are required.
        results = []
        if not os.path.exists(Logging.logFile): results
        #^ If file cannot be found, assume no submissions have been made.
        with open(Logging.logFile, "r") as file:
            #^ 'r' argument means read mode.
            for line in file:
                #^ Each line is a single submission.
                if line == "": return []
                #^ If file exist but empty, then return nothing.
                #^ Assume that user has not tampered with text file by leaving empty lines.
                results.append(line)
                #^ Add sub-list of elements to list.
        return results

    def uploadSubmission(path):
        os.makedirs(Logging.submissionDir, exist_ok=True)
        #^ If submission folder does not exist then make it exist.
        fileName = os.path.basename(path)
        #^ Get file name for destination path.
        shutil.copy(path, os.path.join(Logging.submissionDir, fileName))
        #^ The copy operation.
        print("File uploaded successfully")

class SubmissionInterface:
    logging = Logging
    validation = Validation

    #: Modified and reused from task 2 ('RequestSystem.menu')
    def menu():
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
            if option == "1": SubmissionInterface.submit()
            elif option == "2": SubmissionInterface.viewAll()
            elif option == "3": SubmissionInterface.isSubmitted()
            elif option == "4": SubmissionInterface.confirmExit()
            else: print (f"option '{option}' does not exist, has to be an integer in between the range 1 to 4")
            #^ Deals with invalid option inputs (any string that is not '1', '2', '3', or '4')

    def confirmExit():
        while True:
            confimation = input("Are you sure you want to exit [Y/N]").strip().upper()
            #^ User's confimation as input.
            #^ '.upper()' to make comparison easier.
            if confimation == "Y":
                print("Conformed exit.\nBye!")
                sys.exit()
            if confimation == "N":
                #^ No need 'elif' as program will exit if satisfied previous is-statement.
                print("Returning to main menu.")
                break
            print(f"Error - unexpected input.\nInput must either be Y or N (your input: '{confimation}').\nPlease try again.")
            #^ Deals with unexpected input.

    def viewAll():
        submissions = Logging.getSubmissionLogs()
        if submissions == []:
            #* No point viewing if there are no uploaded submissions.
            print("No submissions so far!")
            return
        print("All submission logs: VVV")
        for submission in submissions:
            print (submission)
            #^ Printed without column headers because each log has labels for both file name and timestamp.

    def isSubmitted():
        fileName = input("Enter file name (case sensitive)").strip()
        submissions = Logging.getSubmissions()
        if submissions == []: return False
        if not fileName in submissions: return False
        #^ Far easier to use 'in' than a whole for-loop.
        return True

    def submit():
        filePath = Path(input("Enter file path here: ").strip())
        if not Validation.validSubmission(filePath): return
        #^ Called method calls other validation methods as well - fileMetadata and isDuplicate.
        Logging.uploadSubmission(filePath)
        #^ Does the submission operation.
        Logging.appendLog(os.path.basename(filePath))
        #^ Logs upload.

SubmissionInterface.menu()
#^ Starts the program.