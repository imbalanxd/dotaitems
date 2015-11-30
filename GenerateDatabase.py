import ItemParse, json
from pymongo import MongoClient

dbName = "outfitter"
dbWearable = "wearable"
client = MongoClient()
db = client[dbName]

def main():
	indexData = ItemParse.getIndexData()
	#Generate the wearable collection in the database from the latest data
	generateFromLatestVersion(indexData)
	#Assign created dates based on history
	generateFoundDates(indexData)

def generateFromVersionId(versionId):
	db[dbWearable].drop()
	allItems = ItemParse.getWearableItemsForVersionId(versionId)
	for alphaNumericCategory in allItems:
		categoryDict = allItems[alphaNumericCategory]
		del categoryDict["count"]
		for item in categoryDict:
			wearableItem = categoryDict[item]
			wearableItem["_id"] = wearableItem["name"]
			result = db[dbWearable].insert_one(wearableItem)

def generateFromLatestVersion(indexData):
	generateFromVersionId(ItemParse.getCurrentVersionId(indexData))

def generateFoundDates(indexData):
	for versionIndex in indexData:
		versionData = indexData[versionIndex]
		if(versionData["id"] != "default"):
			generateFoundDateForVersionAndEpoch(versionData["id"], versionData["time"])

def generateFoundDateForVersionAndEpoch(versionId, epoch):
	newItems = ItemParse.getNewWearableItemsForVersionId(versionId)
	for alphaNumericCategory in newItems:
		categoryDict = newItems[alphaNumericCategory]
		for item in categoryDict:
			wearableItem = categoryDict[item]
			db[dbWearable].update({"_id": wearableItem["name"]}, {"$set": {"found_date": epoch}})



if __name__ == "__main__":
	main()