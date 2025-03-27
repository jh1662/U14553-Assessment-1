from datetime import datetime
#^ Import non-external library to allow the use of timestamps.
#^ used "from datetime" so don't have to call from datetime twice like "datetime.datetime.now()".
import os
#^ Import non-external library to allow the use opening, editing and creating text files for logs.
from pathlib import Path
#^ Allow paths work cross-platform - able to use on both Windows and Linux.
#^ Also allows in-built features such as '.exists()'
import sys
#^ 'sys.exit()' allows for better termination of Python program than other alternatives like 'quit()'
import shutil
#^ Allows the manipulation of files themselves.

#: imports used just for the 'PlagiarismChecker' class
import re
#^ Import non-external library to allow the use of regular expressions (regex).
#^ Regex is extremely useful as it allows validations and modifications of strings to take a single short line instead of an enitre for-loop block of code!
import zipfile
#^ For opening and reeading '.docx' files due to thier compressed nature.
#^ Offical source for zip file import - https://docs.python.org/3/library/zipfile.html .
import xml.etree.ElementTree as ET
#^ Allows parsing of XML elements to extract the relevant text from '.docx' files.
#^ Offical source for element tree import - https://docs.python.org/3/library/xml.etree.elementtree.html .
import difflib
#^ Does the comparison/detection for plagiarism.
#^ Offical source for difflib import - https://docs.python.org/3/library/difflib.html .

#x IMPORTANT: This program made of mostly recycled and modified parts of task 2

#x Classes was used instead of functions as it allows OOP’s modularity to make code more organised -
#x methods grouped up into classes ‘Validation’, ‘Logging’, ‘RequestSystem’ and make it more
#x reusable/recyclable.

#x Many print statements used to satisfy Human-Computer Interaction (HCI) principle.

#x Use be terminal satisfies "Keep It Simple, Stupid" (KISS) principle.

#x Assume each file name has no spaces (replaced with underscores) for compatability with legacy linux OSs.

#x Due to class needing each other (both ways), such as Validation calling Logging, they have been made static for simpler communication.

class PlagiarismChecker:
    #* Due to to immense complexity of analysing complex files types (PDF and MS-word), the plagiarism checker has been made its own class.

    def textExtractionPDF(filePath):
        #* Extracts text form PDF by using the 'latin1' decryption.
        #* IMPORTANT - we assume only simple PDFs are used as it is very difficult to understand complex PDFs such as https://doompdf.pages.dev/doom.pdf .
        #* IMPORTANT - due to complexity 100% of the content is not guarenteed tobe fetch but the simpler the PDF the more likely all text content can be extracted.
        try:
            #* Using complex file type with too much viarity make is very possible for unexpected errors -  hence the try statement
            with open(filePath, "rb") as file:
                #^ Due to the complexity of the PDF file, program has to read the binary itself.
                #^ 'rb' source - https://www.w3schools.com/python/python_file_handling.asp .
                content = file.read().decode("latin1", errors="ignore")
                #^ Decodes using 'latin1' encryption.
                texts = re.findall(r'\((.*?)\)', content)
                #^ Uses regex to extract text inside parentheses - where the text is stored
                text = "\n".join(texts)
                return text
        except Exception as error:
            print(f'Error reading PDF file "{os.path.basename(filePath)}": {error}')
            #^ Shows details regarding the unexpected error.
            return None
            #^ Returning 'None' allows caller to know that an error happened (and not just an empty file - "").


    def textExtractionMSWord(filePath):
        #* Extracts text form PDF by using the decompressing and XML parsing decryption.
        #* MS-Word ('.docx') extraxtion requires more steps then PDFs due to having to decompress first.
        text = ""
        try:
            with zipfile.ZipFile(filePath) as decompressed:
                #^ Decompresses file.
                #* Decompress, open, parse then read.
                with decompressed.open("word/document.xml") as file:
                    #^ Opens file.
                    tree = ET.parse(file)
                    #^ Parses data into XML structure
                    root = tree.getroot()
                    #^ moves all XML tags into list to iterate over.
                    texts = []
                    #^ To store the text in
                    for XMLEle in root.iter():
                        #^ Iterates via each XML tag
                        if XMLEle.tag.endswith("}t") and XMLEle.text:
                            texts.append(XMLEle.text)
                    text = "\n".join(texts)
        except Exception as error:
            #* Exact some purpose and justification as the one in PDF but this includes errors for decompression as well.
            print(f'Error reading PDF file "{os.path.basename(filePath)}": {error}')
            return None
        return text

    def extracText(filepath):
        #* choses how to extract text from file, depending of file type, by file extention and returns the result.
        ext = os.path.splitext(filepath)[1]
        #^ Can use '.splitext' on os.path instances -  https://docs.python.org/3/library/os.path.html#os.path.splitext .
        #^ '[1]' fetches the file extention.
        if ext == ".pdf": return PlagiarismChecker.textExtractionPDF(filepath)
        elif ext == ".docx": return PlagiarismChecker.textExtractionMSWord(filepath)
        else:
            print("Error - invalid file in uploaded submission folder: " + filepath)
            return None

    def PlagiarismCheck(filePath, submissionDir):
        #* Checks for plagurism by comparing with other submitted files.
        #* If similarity reaches 90% or above then concider as plagurism.
        threshold = 0.9
        #^ Dictates that is simularity is 90% or above then condcider it as plagiarism.
        #^ Easily editable by other developers - easy maintainbility of code.

        #: Cannot check plagiarism is there is no file to compare with.
        if not os.path.isdir(Logging.submissionDir):
            print("Error - no uploaded files to compare with for plagiarism check. Please upload atleast one file to check plagiarism.")
            return None

        targetFileText = PlagiarismChecker.extracText(filePath)
        #^ Try to extract file from targeted file
        #: Errors relating to extracting from targetted file
        if not targetFileText.strip():
            print("Warning: No extractable text from the target file.")
            return None

        #: Loop via every PDF and MS-Word files in the uploaded submissions directory.
        for file in os.listdir(submissionDir):
            submittedFilePath = os.path.join(submissionDir, file)
            #^ Get file path from directory path and file name.
            if os.path.abspath(submittedFilePath) == os.path.abspath(filePath): continue
            #^ Cannot compare file with its self - if checking file is in the submission directory (by name).
            submittedFileText = PlagiarismChecker.extracText(submittedFilePath)
            if not submittedFileText.strip(): continue
            #^ Do not bother comparing to file with no text - empty file.
            similarity = difflib.SequenceMatcher(None, targetFileText, submittedFileText).ratio()
            #^ To simply code, a internal library method is used to determine the similarity.
            if similarity >= threshold:
                print(f"Plagarism detected - File '{os.path.basename(filePath)}' is plagiarised compared to '{os.path.basename(submittedFilePath)}' with similarity {similarity * 100:.2f}%.")
                print(f"Because of this, the file will not be submitted!")
                return True
        print(f"Plagarism check - no plagiarism detected for '{os.path.basename(filePath)}'.")
        return False


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
        if not Validation.hasNoPlagiarism(filePath): return False
        return True

    def hasNoPlagiarism(filePath):
        #* Caller mathod, because it relates to file validation and 'Validation' having the needed field.
        return not PlagiarismChecker.PlagiarismCheck(filePath, Logging.submissionDir)
        #^ If is plagiarised then catches true resulting in returning false.
        #^ If is not plagiarised then catches false resulting in returning true.

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
        if submissions == []:
            print("No files have been uploaded yet, therefore file is unique.")
            return
        if not fileName in submissions:
            print("File not found in submissions - is unique.")
            return
        #^ Far easier to use 'in' than a whole for-loop.
        print("File found in submissions - is not unique (has duplicate)")

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