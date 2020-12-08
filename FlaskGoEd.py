from flask import Flask
from flask import request
from flask import render_template
# from .MongoDBFile import MgDB
import pymongo
import uuid
from bson.objectid import ObjectId
import dns
import json,ast
import random
app=Flask(__name__)

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
myDB = myclient["Library2"]
users = myDB['users']
books = myDB['books']
library = myDB['lib']
borrowedBook = myDB['borrow']
orderHistory = myDB['orderHistory']
@app.route('/')
def home():
    #retrieve data from Mongo DB server
    # print(MgDB.viewAllBooks())
    # print(obj.viewAllBooks())
    bookName = []
    bookID = []
    authorName = []
    bookStatus = []
    for aBookU in books.find({},{"_id" :0}):
        bookName.append(aBookU["name"])
        bookID.append(aBookU["bookID"])
        authorName.append(aBookU["author"])
        bookStatus.append(aBookU["isBorrowed"])
    length = len(bookID)
        # print(aBookU["bookID"])
    # print(array[0]['bookID'])
    
    return render_template('index.html',result1 = bookID,result2 = bookName,result3 = authorName,result4 = bookStatus,length = length)

@app.route('/addBook',methods=['POST','GET'])
def next():
    if request.method=='POST':
        # bookname = request.form['BookName']
        bookAuthor = request.form['BookAuthor']
        bookName = request.form['BookName']
        location = request.form['Location']
        bID = str(uuid.uuid4())
        bDict = {
            "bookID": bID,
            "name": bookName,
            "author": bookAuthor,
            "location": location,
            "noOfPeople": "0",
            "isBorrowed": False
            }
        insertBook = books.insert_one(bDict)
        bookName = []
        bookID = []
        authorName = []
        bookStatus = []
        for aBookU in books.find({},{"_id" :0}):
            bookName.append(aBookU["name"])
            bookID.append(aBookU["bookID"])
            authorName.append(aBookU["author"])
            bookStatus.append(aBookU["isBorrowed"])
        length = len(bookID)
        # print(aBookU["bookID"])
    # print(array[0]['bookID'])

        return render_template('index.html',result1 = bookID,result2 = bookName,result3 = authorName,result4 = bookStatus,length = length)
#This is cool
#This is the best thing on this planet

	
