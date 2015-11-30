import json, os, time

SEP = os.path.sep;

def main():
	indexData = getIndexData()
	for entry in indexData:
		# print(time.strftime('%Y-%m-%d %H:%M:%S', 
			# time.localtime(os.stat(indexData[entry]["id"]).st_mtime)) +" "+indexData[entry]["id"])
		indexData[entry]["time"] = os.stat(indexData[entry]["id"]).st_mtime;
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