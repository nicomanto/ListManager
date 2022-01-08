
import os
from pymongo import MongoClient

# connect to mongo
cluster = MongoClient(
    os.environ.get('MONGO_URI', None))
db = cluster.ListManager
collection = db.UserLists


class ListManager:
    def getAllChatId(self):
        return [x["_id"] for x in collection.find()]

    def createNewUser(self, chat_id):
        collection.insert_one(
            {"_id": chat_id, "lists": {}})

    def chatIsPresent(self, chat_id):
        if not collection.find_one({"_id":chat_id}):
            return False

        return True

    def deleteChat(self, chat_id):
        collection.delete_one(
            {"_id": chat_id})

    def getMyLists(self, chat_id):
        return collection.find_one({"_id":chat_id}).get("lists").keys()

    def listIsPresent(self, chat_id, listName):
        return listName in self.getMyLists(chat_id)

    def createNewList(self, chat_id, listName):
        collection.update_one(
            {"_id": chat_id}, {"$set": {f"lists.{listName}": []}})

    def emptyList(self, chat_id, listName):
        collection.update_one(
            {"_id": chat_id}, {"$set": {f"lists.{listName}": []}})

    def deleteList(self, chat_id, listName):
        collection.update_one(
            {"_id": chat_id}, {"$unset": {f"lists.{listName}": ""}})

    def elementIsPresent(self, chat_id, listName, element):
        return element in collection.find_one({"_id":chat_id}).get("lists").get(listName)

    def removeElementFromList(self, chat_id, listName, element):
        collection.update_one(
            {"_id": chat_id}, {"$pull": {f"lists.{listName}": element}})

    def addElementToList(self, chat_id, listName, element):
        collection.update_one(
            {"_id": chat_id}, {"$push": {f"lists.{listName}": {"$each": element}}})

    def getElementsFromList(self, chat_id, listName):
        return collection.find_one({"_id":chat_id}).get("lists").get(listName)
