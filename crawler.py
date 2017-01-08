import requests
import json
import collections
from collections import defaultdict
from globalVars import Globals

class Crawler():

	def getDepartures(self):

		user = Globals().getUserName()
		password = Globals().getPassword()
		url = "http://api.reittiopas.fi/hsl/prod/?request=stop&code=1491123&user=" + user + "&pass=" + password

		r = requests.get(url=url)

		data = r.json()

		prettyJsonString = json.dumps(data, indent=4, sort_keys=True)
		prettyJsonObject = json.loads(prettyJsonString)

		departures = prettyJsonObject[0]['departures']

		departuresList = defaultdict(list)

		i = 0

		for departure in departures:

			hour = str(departure['time'])[:2]
			minute = str(departure['time'])[2:]
			time = hour + ":" + minute

			bus = departure['code'][2:4]
			date = str(departure['date'])

			year = date[:4]
			month = date[4:6] 
			day = date[6:8]

			hour = int(hour) # shitty web service does not change day when clock goes beyond 24
			if hour > 23:
				day = int(day)
				day = day + 1
				day = str(day)
				if len(day) == 1:
					day = "0" + day

			date = year + month + day

			item = {"bus": bus, "date": date, "time": time}

			departuresList[departure['time']].append(item)

			i = i + 1


		return departuresList


	def __init__(self):
		pass

if __name__ == "__main__":
   Crawler()