from datetime import datetime
#^ Import non-external library to allow the use of timestamps.
#^ used "from datetime" so don't have to call from datetime twice like "datetime.datetime.now()".
import os
#^ Import non-external library to allow the use opening, editing and creating text files for logs.

#x IMPORTANT: This program made of mostly recycled and modified parts of task 2

#x Classes was used instead of functions as it allows OOP’s modularity to make code more organised -
#x methods grouped up into classes ‘Validation’, ‘Logging’, ‘RequestSystem’ and make it more
#x reusable/recyclable.

#x Many print statements used to satisfy Human-Computer Interaction (HCI) principle.

#X Use be terminal satisfies "Keep It Simple, Stupid" (KISS) principle.

class Validation:
    logFile = "submission_log.txt"
    validExtentions = [".pdf",".docx"]
    sizeLimit = 5 * 1024 * 1024
    #^ '1024' because 5MB instead of 5MiB.

    def fileMetadata(self, filePath):
        extention = filePath.rsplit('.', 1)[-1]
        #^ Gets characters after last dot in string.
        #^ If no dots then it returns the string - no errors.
        if extention not in self.validExtentions:
            #^ Check if file name has none of the file extentions.
            #^ Far simpler alternative than a for-loop.
            print("Invalid file type - can only upload .pdf or .docx")
            return False
        if os.path.getsize(filePath) > self.sizeLimit:
            print("Invalid file size - file size is above 50MB")
            return False
        return True

    def isDuplicate(self, filepath):
        filename = filepath.rsplit('/', 1)[-1]
        pass



class Logging:
    submissionDir = "./submissions/"

    #: Modified and reused from task 2 ('Logging.appendEntry')
    def appendEntry(self, entry):
        #* syntax 'with' is used to make code simpler - don't have to flush the buffer then close file client.
        if not os.path.exists(self.logFile):
            with open(self.logFile, "w") as file: file.write("")
            #^ Create text file if does not exist.
            #^ 'w' argument means write mode.
        with open(self.logFile, "a") as file: file.write(entry+"\n")
        #^ Append entry to file.
        #^ New line to indicate new entry.

    #: Modified and reused from task 2 ('Logging.appendLog')
    def appendLog(self, filename):
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
        results = []
        if not os.path.isdir(self.submissionDir): return results
        #^ If file cannot be found, assume no submissions have been make.
        #^ Return empty list if directory cannot be found.
        results = [str(file.name) for file in self.submissionDir.iterdir() if file.is_file()]
        #^ Make a list that contains every file in the submission directory.
        return results



