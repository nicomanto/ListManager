
import os
from pymongo import MongoClient

# connect to mongo
cluster = MongoClient(
    os.environ.get('MONGO_URI', None))
db = cluster.ListManager
collection = db.UserLists


class ListManager:
    dictChatList = {x["_id"]: x["lists"] for x in collection.find()}

    def createNewUser(self, chat_id):
        self.dictChatList[chat_id] = {}
        # insert in db
        collection.insert_one(
            {"_id": chat_id, "lists": {}})

    def chatIsPresent(self, chat_id):
        return chat_id in self.dictChatList

    def deleteChat(self, chat_id):
        del self.dictChatList[chat_id]
        # delete in db
        collection.delete_one(
            {"_id": chat_id})

    def getMyLists(self, chat_id):
        return self.dictChatList[chat_id].keys()

    def listIsPresent(self, chat_id, listName):
        return listName in self.dictChatList[chat_id]

    def createNewList(self, chat_id, listName):
        self.dictChatList[chat_id].update({listName: []})
        # update in db
        collection.update_one(
            {"_id": chat_id}, {"$set": {f"lists.{listName}": []}})

    def emptyList(self, chat_id, listName):
        self.dictChatList[chat_id][listName] = []
        # update in db
        collection.update_one(
            {"_id": chat_id}, {"$set": {f"lists.{listName}": []}})

    def deleteList(self, chat_id, listName):
        del self.dictChatList[chat_id][listName]
        # update in db
        collection.update_one(
            {"_id": chat_id}, {"$unset": {f"lists.{listName}": ""}})

    def elementIsPresent(self, chat_id, listName, element):
        return element in self.dictChatList[chat_id][listName]

    def removeElementFromList(self, chat_id, listName, element):
        self.dictChatList[chat_id][listName].remove(element)
        # update in db
        collection.update_one(
            {"_id": chat_id}, {"$pull": {f"lists.{listName}": element}})

    def addElementToList(self, chat_id, listName, element):
        self.dictChatList[chat_id][listName] = element + \
            self.dictChatList[chat_id].setdefault(listName, [])
        # update in db
        collection.update_one(
            {"_id": chat_id}, {"$push": {f"lists.{listName}": {"$each": element}}})

    def getElementsFromList(self, chat_id, listName):
        return self.dictChatList[chat_id][listName]
