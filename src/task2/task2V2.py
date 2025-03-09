import datetime
#^ Import non-external library to allow the use of timestamps.
import re
#^ Import non-external library to allow the use of regular expressions (regex).
#^ Regex is extremely useful as it allows validations and modifications of strings to take a single short line instead of an enitre for-loop block of code!
import os
#^ Import non-external library to allow the use opening, editing and creating text files for logs.

#/ result = next((sublist for sublist in self.books if sublist[1] == priority), None)
#^ Python uses 'and' instead of '&&' for AND logical operator - https://www.w3schools.com/python/gloss_python_logical_operators.asp .

#x This program is made to be used by a admin instead of a student thus the ability of making requests and processing next request by specified method.

class Validation():
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

    def bookId(self,input, books):
        #: book id has more ways of beinf invalid than student id so each reason for invalidity is explained to the user.
        if not input.isdigit:
            #^ Uses 'not' instead of '!'
            print(f"Invalid book ID '{input}'- book ID must be a positive integer")
            return False
            #^ Invalid
        book = next((book for book in books if book[0] == int(input)), None)
        #^ Much simpler to do than a for-loop block and a full if-statement - https://www.w3schools.com/python/ref_func_next.asp .
        if book != None: return True
        #^ Book (by ID) got found - valid
        #: Invalid because book ID was not found
        print(f"Invalid book ID '{input}'- no book with that ID. To see all books, type option 1")
        return False

class Logging():
    #* Used to log activity by writing to text files.
    #: File paths can be easily editied by other developers
    pathLogs = "library_log.txt"
    pathRequests = "book_requests.txt"

    def getRequests(self):
        results = []
        if not os.path.exists(self.pathRequests): return []
        #^ If file cannot be found, assume no requests have been make
        with open(self.pathRequests, "r") as file:
            for line in file:
                #^ Each line is a sub-list which is a single request.
                if line == "": return []
                #^ If file exist but empty, then return nothing.
                sublist = line.strip().split(", ")
                #^ Each element is saperated, by a comma and a space whitespace (", ").
                results.append(sublist)
                #^ Add sub-list of elements to 2D list.
        return results


    def appendRequest(self, priority, studentId, bookId):
        entry = f"{priority}, {studentId}, {bookId}"
        self.appendEntry(self.pathRequests, entry)

    def appendLog(self, isProcessed, priority, studentId, bookId):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        #^ For when the action was done for the log.
        if isProcessed: entry = "Request made - "
        #^ If action is making a book request.
        else: entry = "Request processed - "
        #^ If action is processing a book request.
        entry += f"priority: {priority}, student ID: {studentId}, book ID: {bookId} - {timestamp}"
        #^ Creating entry based on action, data/details, and current timestamp of action.
        self.appendEntry(self.pathLogs,entry)

    def appendEntry(self, path, entry):
        #* syntax 'with' is used to make code simpler - don't have to flush the buffer then close file client.
        if not os.path.exists(path):
            with open(path, "w") as file: file.write("")
            #^ Create text file if does not exist.
        with open(path, "a") as file: file.write(entry)
        #^ Append entry to file.


class RequestSystem():
    #* Is main class, hence other classes are aggregate classes (stoered inside this class).
    books = [
        #* Books are identified by index because its easier than combination of book name and author.
        #* Author's name is stored as well because two books can have the same name.
        #* entry/column structure: book id, book name, book author, avaibility
        [0,"book1","author1", True],
        [1,"BOOK2","AUTHOR2", True],
        [2,"B0 O K3"," AUTHor3  ", False],
        #^ Variety of data.
        [3,"4","4",True],
        #^ Book with same name and author.
        [4,"BOOK3","AUTHOR1",True]
        #^ Same book, different author.
    ]
    queue = []
    #^ 2D list can both serve as FIFO or Priority Scheduling.
    #^ Structure - priority, Student ID, Book ID
    #^ Priority scheduling is done by reading the priority column, while FIFO takes index 0 (basically '.pop(0)') - https://www.w3schools.com/python/ref_list_pop.asp
    validation = Validation()

    def menu(self):
        #^ The 'self' argument is a referance to the class instance to allow modifying/reading fields and call other methods.
        #^ The 'self' argument in only needed in the method definition and not in its call.
        #^ Source - https://www.w3schools.com/python/gloss_python_self.asp .
        options = "Enter one of the following numbers for the corrosponding option:\n1 - View all books.\n2 - Request book.\n3 - View all requests.\n4 - Process next request."
        #^ Just like Bash, '\n' means new line.
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
        priority = input("Enter priority (1-10). 1 is lowest priority and 10 is highest").strip()
        #^ For priority scheduling.
        bookId = input("Enter book ID").strip()
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
        self.queue.append([priority, studentId, bookId])
        #^ Sucessful request is added.

    def viewBooks(self):
        print("Book ID, Book name, Author name, Is availible")
        #^ displaying column headers.
        for index in range(0,len(self.books)): print(self.books[index])


    def viewRequests(self):
        if (len(self.queue) == 0):
            #* tell user that there is no requests instead of showing an empty/umpopulated table
            print("There are currently no requests.")
            return
        print("Index (ID of request), priority ,Student ID, Book ID, Book name")
        #^ displaying column headers.
        for index in range(0,len(self.queue)): print(f"{index}, {self.queue[index][0]}, {self.queue[index][1]}, {self.queue[index][2]}, {self.books[index][0]}")
        #^ 'f' is similar to bash's printf - allows formatting.
        #^ Also display book name incase user forgot what book is the book ID.

    def processRequest(self):
        if len(self.queue) == 0:
            print("Cannot process next request - there are currently no book requests.")
            return
        method = input("Enter 1 to process next book by first order (FIFO)\nEnter 2 to process by priority scheduling").strip()
        #^ Simpler to do boolean instead of integer '1' or '2', but inputting integers is much easier for the user.
        #: Another wanna-be switch-statement
        if method == "1": print(self.requestFIFO())
        elif method == "2": print(self.requestPriority())
        else: print(f"Invalid option - choose either 1 or 2.")


    def requestFIFO(self):
        for index in range(len(self.queue)):
            #* Gets the first request where the requested book is availible.
            if self.books[index][3] == False: continue
            #^ Cannot lend book to student when book as already borrowed by somebody else.
            self.books[index][3] == False
            return "Processed request - Priority value (1-10), Student ID, Book ID: " + ", ".join(self.queue.pop(index))
            #^ Indicate success and which request got processed according do FIFO.
            #^ '.join' to convert list into string.
        return "Cannot process request - there are no availible books (all borrowed)"

    def requestPriority(self):
        for priority in range(10,0,-1):
            #^ does not include '0'
            #* Prioritieses requests higher priority values
            for index in range(len(self.queue)):
                #* Gets the first request where the requested book is availible.
                if self.books[index][3] == False or self.queue[index][0] != priority: continue
                #^ Cannot lend book to student when book as already borrowed by somebody else or not specifically wanting that priority.
                self.books[index][3] == False
                return "Processed request - Priority value (1-10), Student ID, Book ID: " + ", ".join(self.queue.pop(index))
                #^ indicate success and which request got processed according do priority scheduling.
        return "Cannot process request - there are no availible books (all borrowed)"


requestSystem = RequestSystem()
requestSystem.menu()