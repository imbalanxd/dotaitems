import os, sys, urllib.request, json, copy, IndexPatch

steamLogin = '76561197961979008%7C%7C486F1FDA2E04217F7396B9196BFCD3C6694459EB'
steamSecureLogin = '76561197961979008%7C%7C295970FE1C686C48FE55D7AC243E46F302A60C3C'
priceHistoryData = None

def main():
	getData("Adornment%20of%20Omen's%20Embrace");

def getData(itemName):
	getPriceHistoryData(urllib.parse.quote(itemName))
	itemData = {}
	itemData["history"] = compilePriceHistory(priceHistoryData['prices'])
	return itemData

# def compileItemsSoldHistory(priceHistoryData):


def compilePriceHistory(priceHistoryData):
	HISTORY_SIZE_DAYS = 30
	history = []
	index = len(priceHistoryData)
	currentDate = ''
	paidTotal = 0;
	countTotal = 0;
	for i in range(index-1, 0, -1):
		thisDate = priceHistoryData[i][0][:priceHistoryData[i][0].index(" ", 4)]
		if(currentDate != thisDate):
			if(len(currentDate) > 0):
				history.append(paidTotal/countTotal)
				HISTORY_SIZE_DAYS = HISTORY_SIZE_DAYS - 1
				if(HISTORY_SIZE_DAYS == 0):
					return list(reversed(history))
			currentDate = thisDate
			count = int(priceHistoryData[i][2])
			paidTotal = priceHistoryData[i][1] * count
			countTotal = count
		else:
			count = int(priceHistoryData[i][2])
			paidTotal += priceHistoryData[i][1] * count
			countTotal += count
	for i in range(0, HISTORY_SIZE_DAYS, 1):
		history.append(0)
	return list(reversed(history))


	# fullDayReached = False
	# totalPaidDay = 0
	# totalSoldCount = 0
	# for pricePoint in reversed(priceHistoryData):


def getPriceHistoryData(itemName):
	global priceHistoryData;
	print("https://steamcommunity.com/market/pricehistory/?country=ZA&currency=28&appid=570&market_hash_name=" + itemName);
	req = urllib.request.Request("https://steamcommunity.com/market/pricehistory/?country=ZA&currency=28&appid=570&market_hash_name=" + itemName,
	    headers={
			'Cookie' : 'steamLogin=' + steamLogin + '; steamLoginSecure=' + steamSecureLogin
	    })
	with urllib.request.urlopen(req) as url:
		priceHistoryData = json.loads(url.read().decode("utf-8"))
	
if __name__ == "__main__":
	main()