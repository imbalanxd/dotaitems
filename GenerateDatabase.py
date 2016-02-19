import ItemParse, json, ItemEconomy
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
	dbItems = list();
	for alphaNumericCategory in allItems:
		categoryDict = allItems[alphaNumericCategory]
		del categoryDict["count"]
		for item in categoryDict:
			wearableItem = categoryDict[item]
			economyData = ItemEconomy.getData(wearableItem['name'])
			print(economyData)
			wearableItem["_id"] = wearableItem["name"]
			flatItem = {	'_id':wearableItem["name"], 
							'hero':list(wearableItem["used_by_heroes"].keys())[0],
							'slot':wearableItem["item_slot"] if "item_slot" in wearableItem.keys() else "main_weapon",
							'rarity':wearableItem["item_rarity"] if "item_rarity" in wearableItem.keys() else "common"};
			dbItems.append(flatItem);
	ItemParse.writeDictionaryToFile({'items':dbItems}, "firebase.json")
	# result = db[dbWearable].insert_one({"items": dbItems})

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