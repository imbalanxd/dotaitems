import json, os, time

SEP = os.path.sep;

def main():
	indexData = getIndexData()
	for entry in indexData:
		if("time" not in indexData[entry]):
			indexData[entry]["time"] = os.stat("itemdata/"+indexData[entry]["id"]).st_mtime;
	saveIndexData(indexData)

def getIndexData():
	raw = open("index.json", encoding="utf-8")
	return json.loads(raw.read())

def saveIndexData(indexData):
	writeDictionaryToFile(indexData, "index.json")

def writeDictionaryToFile(dict, file):
	file = open(file, "w")
	file.write(json.dumps(dict, indent=4, sort_keys=True))
	file.closed

if __name__ == "__main__":
	main()