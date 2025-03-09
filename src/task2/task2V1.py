import datetime
#^ Import non-external library to allow use of timestamps.

#x This program is made to be used by a admin instead of a student thus the ability of making requests and processing next request by specified method.

class Validation():
    #* Used to store the various validation methods for different data (like name, id, etc).
    pass

class Logging():
    #* Used to log activity by writing to text files.
    pass

class RequestSystem():
    #* Is main class, hence other classes are aggregate classes (stoered inside this class).
    availableBooks = [
        #* Books are identified by index because its easier than combination of book name and author.
        #* Author's name is stored as well because two books can have the same name.
        ["book1","author1"],
        ["BOOK2","AUTHOR2"],
        ["B0 O K3"," AUTHor3  "],
        #^ Variety of data.
        ["4","4"],
        #^ Book with same name and author.
        ["BOOK3","AUTHOR1"]
        #^ Same book, different author.
    ]
    queue = []
    #^ 2D list can both serve as FIFO or Priority Scheduling.

    def menu(self):
        #^ The 'self' argument is a referance to the class instance to allow modifying/reading fields and call other methods.
        #^ The 'self' argument in only needed in the method definition and not in its call.
        #^ Source - https://www.w3schools.com/python/gloss_python_self.asp .
        options = """
            Enter for following numbers for the corrosponding option:
            1 - View all books.
            2 - Request book.
            3 - View all requests.
            4 - Process next request.
        """
        while True:
            #^ Python boolean has the first letter of the syntax capitalised.
            option = input(options).strip()
            #^ '.strip()' to remove any whitespaces to reduce the number of possible validation errors.
            #^ Did not need to convert to integer because that would require more complex validation.
            #: Using if-statements because Python does not support switch statements ( https://en.wikipedia.org/wiki/Switch_statement )
            if option == "1":
                self.viewBooks()
            elif option == "2":
                self.requestBook()
            elif option == "3":
                self.viewRequests()
            elif option == "4":
                self.processRequest()
            else:
                #* Deals with invalid option inputs (any string that is not '1', '2', '3', or '4')
                print (f'option "{option}" does not exist, has to be an integer in between the range 1 to 4')




    def requestBook(self):
        studentId = int(input("Enter your Id: ").strip())
        #^ Make all inputs devoid of whitespaces for less validation or logic errors.
        #^ Better store as integer because it make sure that info is inputted correctly.
        #^ Used instead of student names because unlike names, Ids are unique.
        priority = int(input("Enter priority (1-10)").strip())
        #^ For priority scheduling.
        bookId = int(input("Enter ID").strip())
        #^ Much easier for both user and program to find book
        self.queue.append([priority, studentId, bookId])
        #^ Dictionary keys can be integers, keys are the priority.

    def viewBooks(self):
        print("Index (ID), Book name, Author name:")
        #^ displaying column headers.
        for index in range(0,len(self.availableBooks)):
            print(f"{index}, {self.availableBooks[index][0]}, {self.availableBooks[index][1]}")
            #^ 'f' is similar to bash's printf - allows formatting.

    def viewRequests(self):
        if (len(self.queue) == 0):
            #* tell user that there is no requests instead of showing an empty/umpopulated table
            print("There are currently no requests.")
            return
        print("Index (ID of request), priority ,Student ID, Book ID, Book name")
        #^ displaying column headers.
        for index in range(0,len(self.queue)):
            print(f"{index}, {self.queue[index][0]}, {self.queue[index][1]}, {self.queue[index][2]}, {self.availableBooks[index][0]}")
            #^ Also display book name incase user forgot what book is the book ID

    def processRequest(self):
        method = int(input("Enter 1 to process next book by first order (FIFO)\nEnter 2 to process by priority scheduling").strip())
        #^ Simpler to do boolean instead of integer '1' or '2', but inputting integers is much easier for the user.
        if method == 1:
            pass
        elif method == 2:
            pass
        else:
            pass

    def requestFirst(self):

        pass

    def requestSecond(self):

        pass


requestSystem = RequestSystem()
requestSystem.menu()