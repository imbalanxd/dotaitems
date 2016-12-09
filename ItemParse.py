import os, sys, urllib.request, json, vdf, copy, IndexPatch

demo = False
currentVersionId = None
latestVersionId = None
indexData = None

def main():
	os.chdir(sys.path[0])
	getIndexData()
	currentVersionId = getCurrentVersionId(indexData)
	latestVersionId = getLatestVersionId();
	
	updateState = {}
	if(currentVersionId == latestVersionId):
		updateState["update"] = 0;
		print(json.dumps(updateState))
	else:
		updateState["update"] = 1;
		updateState["id"] = latestVersionId;
		print(json.dumps(updateState))
		if(demo):
			gameItemsDict = getFullDataFromFile()
		else:
			os.makedirs("itemdata/"+latestVersionId)
			gameItemsDict = getFullData(getSchemaURL())
			saveFullItemDataForVersionId(gameItemsDict, latestVersionId)
		latestWearableItems = getWearableItems(getItemsDict(gameItemsDict))
		saveWearableItemDataForVersionId(latestWearableItems, latestVersionId)
		currentWearableItems = getWearableItemsForVersionIdNew(currentVersionId)
		saveNewWearableItemDataForVersionId(findNewWearableItems(currentWearableItems, latestWearableItems), latestVersionId)
		if(not demo):
			latestVersion = {}
			latestVersion["id"] = latestVersionId
			indexData[str(len(indexData) + 1)] = latestVersion
			saveIndexData(indexData)
	IndexPatch.main();
	
def getIndexData():
	global indexData;
	if indexData is None:
		raw = open('index.json', encoding="utf-8")
		indexData = json.loads(raw.read())
	return indexData

def saveIndexData(indexData):
	writeDictionaryToFile(indexData, "index.json")

def getIndexForVersionId(versionId):
	global indexData;
	for version in indexData:
		if(indexData[version]["id"] == versionId):
			return version

def getVersionIdForIndex(index):
	global indexData
	return indexData[str(index)]["id"]

def getCurrentVersionId(indexDict=None):
	if(indexDict is None):
		indexDict = getIndexData()
	return indexDict[str(len(indexDict))]["id"]

def getLatestVersionId(schemaUrl = None):
	if(demo):
		return "demo"
	else:
		return (getSchemaURL() if schemaUrl is None else schemaUrl).replace("http://cdn.dota2.com/apps/570/scripts/items/items_game.", "").replace(".txt", "")

def getSchemaURL():
	if(latestVersionId is not None):
		return "http://cdn.dota2.com/apps/570/scripts/items/items_game." + latestVersionId + ".txt"
	schemaWS = "http://api.steampowered.com/IEconItems_570/GetSchemaURL/v0001/?key=47C349E7AFF79D6FA40805A3726484DD"
	with urllib.request.urlopen(schemaWS) as url:
		data = json.loads(url.read().decode("utf-8"))
		if(data["result"]["status"] is 1):
			return data["result"]["items_game_url"]

def getFullData(fullItemUrl):
	with urllib.request.urlopen(fullItemUrl) as url:
		return vdf.loads(url.read().decode("utf-8"))

def getFullDataFromFile():
	raw = open("demo/items_game.txt", encoding="utf-8")
	return vdf.loads(raw.read())

def getItemsDict(fullDict):
	return fullDict["items_game"]["items"]

def writeDictionaryToFile(dict, file):
	file = open(file, "w")
	file.write(json.dumps(dict, indent=0, sort_keys=True))
	file.closed

def saveFullItemDataForVersionId(fullDict, versionId):
	writeDictionaryToFile(fullDict, "itemdata/"+versionId+"/items_game.txt")

def saveWearableItemDataForVersionId(wearableDict, versionId):
	writeDictionaryToFile(wearableDict, "itemdata/"+versionId+"/itemlist.json")

def saveNewWearableItemDataForVersionId(newWearableDict, versionId):
	writeDictionaryToFile(newWearableDict, "itemdata/"+versionId+"/newitemlist.json")

#Old method
#Cannot be used with a new pull of the project
def getWearableItemsForVersionId(versionId):
	raw = open("itemdata/"+versionId+"/itemlist.json", encoding="utf-8")
	return json.loads(raw.read())

#New method
#Only requires default file with full starting item list, then constructs full list
def getWearableItemsForVersionIdNew(versionId):
	verIndex = int(getIndexForVersionId(versionId))
	wearableDict = json.loads(open("itemdata/default/itemlist.json", encoding="utf-8").read())
	for i in range (2, verIndex + 1):
		newDict = json.loads(open("itemdata/"+getVersionIdForIndex(i)+"/newitemlist.json", encoding="utf-8").read())
		for alpha in newDict:
			if(alpha in wearableDict):
				wearableDict[alpha].update(newDict[alpha])
			else:
				wearableDict[alpha] = newDict[alpha]
	return wearableDict

def getNewWearableItemsForVersionId(versionId):
	raw = open("itemdata/"+versionId+"/newitemlist.json", encoding="utf-8")
	return json.loads(raw.read())

def getWearableItems(itemsDict):
	wearableDict = {}
	for item in itemsDict.items():
		if("prefab" in item[1] and item[1]["prefab"] == "wearable"):
			alpha = item[1]["name"][0]
			if(alpha not in wearableDict):
				wearableDict[alpha] = {};
				wearableDict[alpha]["count"] = 0;
			wearableDict[alpha][item[1]["name"]] = item[1]
			wearableDict[alpha]["count"] = wearableDict[alpha]["count"] + 1;
			if("portraits" in wearableDict[alpha][item[1]["name"]]):
				del wearableDict[alpha][item[1]["name"]]["portraits"]
	return wearableDict

def findNewWearableItems(oldDict, newDict):
	diffDict = copy.deepcopy(newDict)
	for key in newDict.keys():
		if(key in oldDict):
			if(newDict[key]["count"] == oldDict[key]["count"]):
				del diffDict[key]
			else:
				for item in newDict[key].keys():
					if(item in oldDict[key]):
						del diffDict[key][item]
	return diffDict

if __name__ == "__main__": 
	main()