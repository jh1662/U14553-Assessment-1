from datetime import datetime
#^ Import non-external library to allow the use of timestamps.
#^ used "from datetime" so don't have to call from datetime twice like "datetime.datetime.now()".
import os
#^ Import non-external library to allow the use opening, editing and creating text files for logs.

#x This program is made to be used by a admin instead of a student thus the ability of making requests and processing next request by specified method.

class Validation:
    #* Used to store the various validation methods for different data (like name, id, etc).
    def integerLimit(self, input, limit = 999999):
        #^ Use of default parameter values - https://www.w3schools.com/python/gloss_python_function_default_parameter.asp .
        #^ Assume that the limit for students ids is in range from 0 to 999,999 (6 digits) because the highest student count, at a UK university, is 129,420 - https://en.wikipedia.org/wiki/List_of_universities_in_the_United_Kingdom_by_enrolment .
        #* Used for student IDs and priorites.
        #* No print statements as they are handled by called due do validating a multiple kinds of integers/inputs.
        if (not input.isdigit()): return False
            #^ '.isdigit()' checks if its a positive integer (because it does not accept '-' or '.' in string) - https://www.w3schools.com/python/ref_string_isdigit.asp .
            #^ Invalid if not an integer
        if int(input) > limit: return False
            #^ 'int()' converts string to integer for comparison.
            #^ InValid if it is above the upper limit, assume the lower limit is zero.
        return True
        #^ Valid.

    def bookId(self, input, books):
        #: book id has more ways of beinf invalid than student id so each reason for invalidity is explained to the user.
        if not input.isdigit():
            #^ Uses 'not' instead of '!'
            print(f"Invalid book ID '{input}'- book ID must be a positive integer")
            return False
            #^ Invalid
        book = next((book for book in books if book[0] == int(input)), [])
        #^ Much simpler to do than a for-loop block and a full if-statement - https://www.w3schools.com/python/ref_func_next.asp .
        if book != []: return True
        #^ Book (by ID) got found - valid
        #: Invalid because book ID was not found
        print(f"Invalid book ID '{input}'- no book with that ID. To see all books, type option 1")
        return False

    def uniqueRequest(self,studentID,bookID,requests):
        #* Purposefullt made it to pass request list instead of calling 'logging.getRequests' because that would require this class
        #* to have the logging instance referance passed into this class constructor which will defeat one of the main purposes of OOP
        #* which is modulality and code being reusable.
        request =  next((request for request in requests if requests[1] == studentID and requests[2] == bookID), [])
        #^ Python uses 'and' instead of '&&' for AND logical operator - https://www.w3schools.com/python/gloss_python_logical_operators.asp .
        if request == []: True
        #^ If not found then request is unique.
        #: Not unique.
        print(f"Invalid request - student {studentID} has already requested for book {bookID}.")
        return False

class Logging:
    #* Used to log activity by writing to text files.
    #: File paths can be easily editied by other developers
    pathLogs = "library_log.txt"
    pathRequests = "book_requests.txt"

    def getRequests(self):
        results = []
        if not os.path.exists(self.pathRequests): return []
        #^ If file cannot be found, assume no requests have been make
        with open(self.pathRequests, "r") as file:
            #^ 'r' argument means read mode
            for line in file:
                #^ Each line is a sub-list which is a single request.
                if line == "": return []
                #^ If file exist but empty, then return nothing.
                #^ Assume that user has not tampered with text file by leaving empty lines.
                sublist = line.strip().split(", ")
                #^ Each element is saperated, by a comma and a space whitespace (", ").
                results.append(sublist)
                #^ Add sub-list of elements to 2D list.
        return results
        #^ Returns queue as 2D list that to serve either Priority Scheduling, FIFO or just to view all requests.
        #^ Returns all requests for FIFO instead of the first one because can only borrow books that are currently availible - not always the first is processed.

    def appendRequest(self, priority, studentId, bookId):
        entry = f"{priority}, {studentId}, {bookId}"
        #^ Structure - priority, Student ID, and Book ID.
        #^ No need for time as entries are appended in order of time - their index/linenumber shows the earliest request.
        self.appendEntry(self.pathRequests, entry)

    def dequeueRequest(self, index):
        #* return popped/dequeued entry as list, otherwise return 'False' if not possible.
        #* Note that request ID/index start from 0.
        #* Is somewhat validated before but filed can be edited/deleted before actual file writing/reading operations.
        if not os.path.exists(self.pathRequests):
            #* Cannot requeue a queue that does not exist (not existing means a request has not been made yet).
            print("Error - book_requests.txt does not exist. Make a request to create file.")
            return False
        with open(self.pathRequests, "r") as file: entires = file.readlines()
        #^ Store text file content as 1D list as only index is needed.
        #: More validation
        if entires == []:
            #* Cannot requeue a queue that is currently empty.
            print ("Error - No requests has been made yet. Please make atleast one to process them")
            return []
        if len(entires) <= index:
            #* Index out-of-bounds
            print ("Error - request ID/index is out of current bounds, view requests to double check.")
            return []

        dequeuedEntry = str(index)+", "+entires.pop(index).replace("\n","")
        #^ Remove entry and store to variable with index.
        #^ Using replace is much easier for developers to understand its purpose than just slicing the last two characters off.
        with open(self.pathRequests, "w") as file: file.writelines(entires)
        #^ Overwrite list of requests with the modified requests lists (with one entry dequeued).
        return dequeuedEntry
        #^ return request as string to show to user.


    def appendLog(self, index, isFIFO, priority, studentId, bookId):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        #^ For when the action was done for the log.
        if isFIFO: entry = "Request processed by FIFO (first come, first serve) - "
        #^ If action is making a book request.
        else: entry = "Request processed by highest priority value - "
        #^ If action is processing a book request.
        entry += f"request index: {index}, priority: {priority}, student ID: {studentId}, book ID: {bookId} - {timestamp}"
        #^ Creating entry based on action, data/details, and current timestamp of action.
        #^ Structure - priority, Student ID, Book ID, and timestamp.
        self.appendEntry(self.pathLogs,entry)
        #^ Does the appending operation.

    def appendEntry(self, path, entry):
        #* syntax 'with' is used to make code simpler - don't have to flush the buffer then close file client.
        if not os.path.exists(path):
            with open(path, "w") as file: file.write("")
            #^ Create text file if does not exist.
            #^ 'w' argument means write mode.
        with open(path, "a") as file: file.write(entry+"\n")
        #^ Append entry to file.
        #^ New line to indicate new entry.


class RequestSystem:
    #* Is main class, hence other classes are aggregate classes (stoered inside this class).
    books = [
        #* Books are identified by index because its easier than combination of book name and author.
        #* Author's name is stored as well because two books can have the same name.
        #* Entry/column structure: book id, book name, book author, avaibility.
        #* ID is not index because if book get removed, then all books after that will have their IDs changed.
        [0,"book1","author1", True],
        [1,"BOOK2","AUTHOR2", True],
        [2,"B0 O K3"," AUTHor3  ", False],
        #^ Variety of data - book is registered at library but curretly missing
        [3,"4","4",True],
        #^ Book with same name and author.
        [4,"BOOK3","AUTHOR1",True]
        #^ Same book, different author.
    ]
    validation = Validation()
    logging = Logging()

    def menu(self):
        #^ The 'self' argument is a referance to the class instance to allow modifying/reading fields and call other methods.
        #^ The 'self' argument in only needed in the method definition and not in its call.
        #^ Source - https://www.w3schools.com/python/gloss_python_self.asp .
        options = "\nEnter one of the following numbers for the corrosponding option:\n1 - View all books.\n2 - Request book.\n3 - View all requests.\n4 - Process next request.\n: "
        #^ Just like Bash, '\n' means new line.
        #^ ": " indicates for user input.
        #^ Empty line at top to help saperate from console messages of past commands/options.
        while True:
            #^ Python boolean has the first letter of the syntax capitalised.
            option = input(options).strip()
            #^ '.strip()' to remove any whitespaces to reduce the number of possible validation errors.
            #^ Did not need to convert to integer because that would require more complex validation.
            #: Using if-statements because Python does not support switch statements ( https://en.wikipedia.org/wiki/Switch_statement )
            if option == "1": self.viewBooks()
            elif option == "2": self.requestBook()
            elif option == "3": self.viewRequests()
            elif option == "4": self.processRequest()
            else: print (f"option '{option}' does not exist, has to be an integer in between the range 1 to 4")
            #^ Deals with invalid option inputs (any string that is not '1', '2', '3', or '4')

    def requestBook(self):
        studentId = input("Enter your student ID: ").strip()
        #^ Make all inputs devoid of whitespaces for less validation or logic errors.
        #^ Better store as integer because it make sure that info is inputted correctly.
        #^ Used instead of student names because unlike names, Ids are unique.
        priority = input("Enter priority (1-10). 1 is lowest priority and 10 is highest: ").strip()
        #^ For priority scheduling.
        bookId = input("Enter book ID: ").strip()
        #^ Much easier for both user and program to find book
        #: validation
        if not self.validation.integerLimit(studentId):
            print (f"Invalid student ID '{studentId}' - must be an integer between the range of 0 to 999,999")
            return
        if not self.validation.integerLimit(priority):
            #^ No need to use 'elif' because privious if-statement has the 'return' syntax inside.
            print (f"Invalid priority value '{priority}' - must be an integer between the range of 1 to 10")
            return
        if not self.validation.bookId(bookId,self.books): return
        #^ No print statement because that is done in the 'validation.bookId' method.
        if not self.validation.uniqueRequest(studentId, bookId, self.logging.getRequests()): return
        #^ "self.logging.getRequests()" is used as argument because its not used elseware in this function.
        self.logging.appendRequest(priority, studentId, bookId)
        #^ Sucessful request is appendix to file.

    def viewBooks(self):
        print("Book ID, Book name, Author name, Is availible")
        #^ displaying column headers.
        for index in range(0,len(self.books)): print(self.books[index])

    def viewRequests(self):
        requests = self.logging.getRequests()
        if len(requests) == 0:
            print("Cannot view requests - there are currently no book requests. Type option 2 to make a request")
            return
        print("Index (ID of request), priority ,Student ID, Book ID:")
        #^ displaying column headers.
        for index in range(0,len(requests)): print(f"{index}, {requests[index][0]}, {requests[index][1]}, {requests[index][2]}")
        #^ 'f' is similar to bash's printf - allows formatting.
        #^ Also display book name incase user forgot what book is the book ID.

    def processRequest(self):
        requests = self.logging.getRequests()
        if len(requests) == 0:
            print("Cannot process next request - there are currently no book requests.")
            return
        method = input("Enter 1 to process next book by first order (FIFO)\nEnter 2 to process by priority scheduling\n: ").strip()
        #^ Simpler to do boolean instead of integer '1' or '2', but inputting integers is much easier for the user.
        #: Another wanna-be switch-statement
        if method == "1": print(self.requestFIFO())
        elif method == "2": print(self.requestPriority())
        else: print(f"Invalid option - choose either 1 or 2.")


    def requestFIFO(self):
        requests = self.logging.getRequests()
        #^ Get list of requests from book_requests.txt
        for index in range(len(requests)):
            #* Gets the first request where the requested book is availible.
            if not self.processBook(index): continue
            #^ Cannot lend book to student when book as already borrowed by somebody else.
            processedRequest = self.logging.dequeueRequest(index).split(", ")
            #^ Pop request from file
            self.logging.appendLog(True,processedRequest[0],processedRequest[1],processedRequest[2],processedRequest[3])
            #^ Log processed request
            return "Processed request - Priority value (1-10), Student ID, Book ID: " +  ", ".join(processedRequest)
            #^ Indicate success and which request got processed according do FIFO.
            #^ '.join' to convert list into string.
        return "Cannot process request - there are no availible books for request(s) (all borrowed)"
        #^ If all books requested are unavailible/borrowed currently.

    def requestPriority(self):
        requests = self.logging.getRequests()
        for priority in range(10,0,-1):
            #^ does not include '0', counts downwards.
            #* Prioritieses requests higher priority values
            for index in range(len(requests)):
                #* Gets the first request where the requested book is availible.
                print(requests[index][0])
                if requests[index][0] != str(priority): continue
                #^ Cannot lend book to student request with unequality to current priority value.
                #^ Converting to int instead may cause unexpected errors such as manually editing book_requests.txt to change number to something else which would cause error from int parse
                #^ meanwhile 'str' will work for whatever number.
                if not self.processBook(index): continue
                processedRequest = self.logging.dequeueRequest(index).split(", ")
                self.logging.appendLog(False,processedRequest[0],processedRequest[1],processedRequest[2],processedRequest[3])
                return "Processed request - Priority value (1-10), Student ID, Book ID: " + ", ".join(processedRequest)
                #^ indicate success and which request got processed according do priority scheduling.
        return "Cannot process request - there are no availible books (all borrowed)"

    def processBook(self,bookId):
        #* Check if book (by ID is availible), if so then make it unavailible then return true otherwise return false.
        #* Both checks and does the book processing due to the computational time it takes to find book by ID - O(n) where n = number of books.
        #* so if done saperately then Big O notation time will be O(2n) in total.
        index = next((index for index, book in enumerate(self.books) if book[0] == bookId), -1)
        #^ Far simpler syntax than a for-loop block.
        #^ "enumerate" gives both the sub-array for checking and index for return when satisfied - https://www.w3schools.com/python/ref_func_enumerate.asp .
        #^ Better practice for function return options to all be the same data type, hence replaced "False" with "-1".
        if index == -1: return False
        #^ Should never happen because request cannot be made for a non-registered book but is there for code integrety for unexpected errors such as memory leaks.
        if self.books[index][3] == False: return False
        #^ Cannot process request if book is currently unavailable.
        #: Book unavailable so can process request.
        self.books[index][3] == False
        return True

requestSystem = RequestSystem()
requestSystem.menu()