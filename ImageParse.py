import os, sys, urllib.request, json, vdf, copy, time

def main():
	os.chdir(sys.path[0])
	indexData = getIndexData();
	for key in indexData.keys():
		parseImagesForVersion(indexData[key]["id"]);
		fillImageGapsForVersion(indexData[key]["id"])
		# break;
	# fillImageGapsForVersion("27bd269df7e649742028321d950f2b0f25f0239c")


def parseImagesForVersion(versionId):
	itemData = {};

	if(os.path.exists("itemdata/"+versionId+"/itemimages.json")):
		print("skipping " + versionId)
		return;

	if(os.path.exists("itemdata/"+versionId+"/newitemlist.json")):
		itemData = open("itemdata/"+versionId+"/newitemlist.json", encoding="utf-8");
	elif(os.path.exists("itemdata/"+versionId+"/itemlist.json")):
		itemData = open("itemdata/"+versionId+"/itemlist.json", encoding="utf-8");

	itemDict = json.loads(itemData.read());
	imageDict = {};
	for key in itemDict.keys():
		for item in itemDict[key].keys():
			if(item == "count"):
				break
			imageInventoryName = os.path.basename(itemDict[key][item]["image_inventory"])
			imageDict[imageInventoryName] = {}
			imageDict[imageInventoryName]["normal"] = getImageUrlForItem(imageInventoryName, False);
			imageDict[imageInventoryName]["large"] = getImageUrlForItem(imageInventoryName, True);
			print(imageDict[imageInventoryName])
	writeDictionaryToFile(imageDict, "itemdata/"+versionId+"/itemimages.json")

def fillImageGapsForVersion(versionId):
	print("Version " + versionId)
	imageData = readDictionaryFromFile("itemdata/"+versionId+"/itemimages.json")
	dataUpdated = False;
	for key in imageData.keys():
		if(len(imageData[key]["normal"]) == 0):
			dataUpdated = True
			print(key + " missing normal image. Requesting...")
			imageData[key]["normal"] = getImageUrlForItem(key, False)
			print("Done: " + imageData[key]["normal"])
		if(len(imageData[key]["large"]) == 0):
			dataUpdated = True
			print(key + " missing large image. Requesting...")
			imageData[key]["large"] = getImageUrlForItem(key, True)
			print("Done: " + imageData[key]["large"])
	if(dataUpdated):
		writeDictionaryToFile(imageData, "itemdata/"+versionId+"/itemimages.json")


def getImageUrlForItem(imageInventory, large):
	time.sleep(1.0);
	iconPath = "https://api.steampowered.com/IEconDOTA2_570/GetItemIconPath/v1?key=47C349E7AFF79D6FA40805A3726484DD&iconname=" + imageInventory
	if(large):
		iconPath = iconPath + "&iconType=1"
	try:
		with urllib.request.urlopen(iconPath) as url:
			data = json.loads(url.read().decode("utf-8"))
			if("error" in data["result"]):
				return ""
			return data["result"]["path"]
	except:
		return ""

def getIndexData():
	raw = open('index.json', encoding="utf-8")
	indexData = json.loads(raw.read())
	return indexData

def writeDictionaryToFile(dict, file):
	file = open(file, "w")
	file.write(json.dumps(dict, indent=0, sort_keys=True))
	file.closed

def readDictionaryFromFile(file):
	raw = open(file, encoding="utf-8")
	data = json.loads(raw.read())
	return data


if __name__ == "__main__": 
	main()