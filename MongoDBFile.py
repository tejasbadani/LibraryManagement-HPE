import pymongo
import uuid
from bson.objectid import ObjectId
import dns
import json,ast
import random
# myclient = pymongo.MongoClient("mongodb+srv://tejasbadani:20AoCd9LDQbagCvg@cluster0-hondi.mongodb.net/test?retryWrites=true&w=majority")
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
myDB = myclient["Library2"]
# db_names = myclient.list_database_names()
# print(db_names)
# if "Library" in db_names:
#     # Do nothing
#     print('Nothing')
# else:
#     print('Failed to create db')
#
#
# db_names_collection = myDB.list_collection_names()
# bookBorrowedDict = {"bookID": bookID, "dateOfBorrow": "Sample",
#                     "returnDate": "Sample", "counter": "0", "returnTime": "8","userID":"Sample"}
# bookHistory = {"bookID": bookID, "Dateissue": "Sample Date"}
# section = {
#     "books": bookID
# }
# booksDict = {
#     "bookID": bookID,
#     "name": "Tejas",
#     "author": "Sample",
#     "location": "Bock B",
#     "noOfPeople": "13",
#     "isBorrowed": False,
#     "borrowedUsers" : ["uuid1"]
# }
#
# libDict = {"Section 1": section, "Section 2 ": section}
# uniqueID = str(uuid.uuid4())
# userDict = {"userID": uniqueID, "booksBorrowed": "0"}

# x = users.insert_one(userDict)
# x1 = books.insert_one(booksDict)
# x2 = library.insert_one(libDict)

# y = users.find_one()
# print(y)
# y = books.find_one()
# print(y)
# y = library.find_one()
# print(y)
# if "users" in db_names_collection:
#     # Do nothing
#     print('Nothing')
# else:
#     print('Failed to create Collection')

class MgDB():
    def __init__(self):
       
        self.users = myDB['users']
        self.books = myDB['books']
        self.library = myDB['lib']
        self.borrowedBook = myDB['borrow']
        self.orderHistory = myDB['orderHistory']
        db_names = myclient.list_database_names()
        print(db_names)
        if "Library2" in db_names:
            # Do nothing
            print('DB Present')
        else:
            print('Failed to create db')


    def insertNewBook(self, bookName, author, location):
        print('EXECUTING')
        bID = str(uuid.uuid4())
        bDict = {
            "bookID": bID,
            "name": bookName,
            "author": author,
            "location": location,
            "noOfPeople": "0",
            "isBorrowed": False
            }
        insertBook = self.books.insert_one(bDict)

    def createUser(self):
        print("creating user")
        uid = str(uuid.uuid4())

        uDict = {
            "userID": uid,
            "booksBorrowed": "0",
            }
        self.users.insert_one(uDict)

    def deleteBook(self,bookID):
        print(self.borrowedBook.find_one({"bookID": bookID}))
        if (self.borrowedBook.find_one({"bookID": bookID}) == None):
            self.books.delete_one({"bookID": bookID})
        else:
            print('Cannot remove')

    # bookBorrowedDict.remove({"bookID":bookID})


    def borrowBook(self,userID, bookID, returnt, dateBorrow, dateRet):
    # increment borrowed books by 1
        if (self.books.find_one({"bookID":bookID})["isBorrowed"] == False):
            borrowDict = {
                "bookID": bookID,
                "dateOfBorrow": dateBorrow,
                "returnDate": dateRet,
                "counter": "0",
                "returnTime": returnt,
                "userID": userID
                }
            bBook = self.borrowedBook.insert_one(borrowDict)
            self.books.update_one({"bookID": bookID}, {"$set": {"isBorrowed": True}})

    def returnBook(self,bookID):
    # Get the userID from the borrowedBooks
    # Add it to the history
    # remove from borrow
        if (self.borrowedBook.find_one({"bookID":bookID}) != None):
            print("Exists")
            self.books.update_one({"bookID": bookID}, {"$set": {"isBorrowed": False}})
            borrowedBookDict =  self.borrowedBook.find_one({"bookID":bookID})
            uid = borrowedBookDict['userID']
            dateBorrow = borrowedBookDict['dateOfBorrow']
            returnDate = borrowedBookDict['returnDate']
            print("USER ID ")
            print(uid)
            self.borrowedBook.delete_one({"bookID":bookID})
            orderDict = {
                "userID": uid,
                "bookID": bookID,
                "dateOfBorrow": dateBorrow,
                "returnDate": returnDate
                }
            print(uid)
            print(bookID)
            print(dateBorrow)
            print(returnDate)
            print(orderDict)
            ordNo = self.orderHistory.insert_one(orderDict)
            print(ordNo)
    def viewAllBooks(self):
        print('View all books and their status')
        array = []
        for aBookU in self.books.find({},{"_id" :0}):
            # bookDict = {
            #     "bookID": id,
            #     "name": aBookU["name"],
            #     "author": aBookU["author"],
            #     "location": aBookU["location"],
            #     "noOfPeople": aBookU["noOfPeople"],
            #     "isBorrowed": aBookU["isBorrowed"]
            # }
            # aBook = ast.literal_eval(json.dumps(aBookU))
            array.append(aBookU)
            print(aBookU["bookID"])
        print(array[0]['bookID'])
        return array
    def viewAllBorrowedBook(self):
        print('View all borrowed books')
        array = []
        bookID =[]
        for aBook in self.borrowedBook.find({},{"_id":0}):
            print(aBook)
            print(type(aBook))
            anID = aBook["bookID"]
            bookID.append(anID)
        for anID in bookID:
            foundBook = self.books.find_one({"bookID":anID},{"_id":0})
            if ( foundBook != None):
                array.append(foundBook)
        print(array)
        return array
    def getHistoryUser(self,userID):
        print('Getting user History')
        bHistory = []
        for book in self.orderHistory.find({"userID": userID},{"_id":0}):
            # print(book)

            bookDetails =  self.books.find_one({"bookID": book["bookID"]},{"_id":0})
            hDict = {
                    "name": bookDetails["name"],
                    "author": bookDetails["author"],
                    "dateOfBorrow": book['dateOfBorrow'],
                    "returnDate": book["returnDate"]
                }
            bHistory.append(hDict)
        print(bHistory)

    def addDataToBorrow(self):
        print('Calling borrow')
        idArray = []
        for data in self.books.find().limit(40):
            idArray.append(data["bookID"])
        userIDs = ["aeda9c77-b476-4210-b8d6-40db2bb318ea","b936da0b-1ce4-4dfb-8782-0ab76d38d926","c8300b03-6946-45ba-be1b-cb8f560e6cd9","344b700f-7ec4-49d5-a1f2-1b32b6da91cc"]
        for value in range(30):
            rand = random.randint(0,3)
            randV = random.randint(0,39)
            self.borrowBook(userIDs[rand],idArray[randV],6,"15.05.2019","21.05.2019")

        # borrowBook()
    def returnFewBooks(self):
        print("Return book")
        idArray = []
        for data in self.borrowedBook.find().limit(10):
            idArray.append(data["bookID"])
            self.returnBook(data['bookID'])



a = MgDB()
#a.createUser()
# a.insertNewBook("Tintin","James","Block 2")

a.returnFewBooks()
# x = range (50)
# a.addDataToBorrow()
# for n in x :
#     rand = random.randint(1,8)
#     a.insertNewBook(f'Book {n}',f'Author {n}',f'Block {rand}')

# for n in x:
#     a.createUser()


# **** #
# create multiple borrows from a single user 


# print(books.find())
# a.borrowBook("aeda9c77-b476-4210-b8d6-40db2bb318ea","",5,"Jan 1","Jan 6")
# deleteBook("0e8e38fb-60f1-46c5-90d8-5018cdf63121")
# a.returnBook("bdd13709-fb69-4f63-832b-09e261d36910")
# a.getHistoryUser("aeda9c77-b476-4210-b8d6-40db2bb318ea")
# users.delete_one({"_id" : ObjectId("5d0e7b2464d1c7d1f264b26b")})
# books.delete_one({"_id" : ObjectId("5d0e7b2464d1c7d1f264b26c")})
# borrowBook("aeda9c77-b476-4210-b8d6-40db2bb318ea","bdd13709-fb69-4f63-832b-09e261d36910",5,"Jan 2","Jan 7")
# a.viewAllBorrowedBook()
# a.viewAllBooks()