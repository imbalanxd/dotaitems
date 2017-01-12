import os, sys, urllib.request, json, vdf, copy, time

def main():
	os.chdir(sys.path[0])
	indexData = getIndexData();
	for key in indexData.keys():
		parseImagesForVersion(indexData[key]["id"]);


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
			time.sleep(1.5);
			imageDict[imageInventoryName]["large"] = getImageUrlForItem(imageInventoryName, True);
			time.sleep(1.5);
			print(imageDict[imageInventoryName])
	writeDictionaryToFile(imageDict, "itemdata/"+versionId+"/itemimages.json")


def getImageUrlForItem(imageInventory, large):
	iconPath = "https://api.steampowered.com/IEconDOTA2_570/GetItemIconPath/v1?key=47C349E7AFF79D6FA40805A3726484DD&iconname=" + imageInventory
	if(large):
		iconPath = iconPath + "&iconType=1"

	print(iconPath)
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


if __name__ == "__main__": 
	main()