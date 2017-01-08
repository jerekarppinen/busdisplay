import tkinter
from tkinter.font import Font
from time import sleep
import requests
import calendar
from datetime import datetime
from datetime import timedelta
import time
import collections


class Display():
	def __init__(self):

		self.main = tkinter.Tk()
		screen_width = self.main.winfo_screenwidth()
		screen_height = self.main.winfo_screenheight()
		resolution = str(screen_width) + "x" + str(screen_height)
		self.main.geometry(resolution) 
		self.txt = tkinter.Text(self.main)
		self.txt.configure(font=Font(size=32, family="Default sans-serif"))
		self.txt.pack()

		self.main.after(0, self.update_txt)

		#sleep until next starting minute
		self.sleepUntilNextMinute()

		self.main.mainloop()

	def sleepUntilNextMinute(self):
		print('Starting on next full minute...')
		sleeptime = 60 - datetime.utcnow().second
		print('Starting in ' + str(sleeptime) + ' seconds.')
		time.sleep(sleeptime)

	def getDeltaTimeInMinutes(self, time, now=None):

		if now is None:
			now = datetime.now()

		currentYear = now.year
		currentDay = now.day
		currentMonth = now.month
		currentHour = now.hour
		currentMinute = now.minute

		timeSplit = time.split(':')
		hour = timeSplit[0]
		minute = timeSplit[1]

		busDate = str(currentYear) + '-' + str(currentMonth) + '-' + str(currentDay) + ' ' + hour + ':' + minute

		busDateTime = datetime.strptime(busDate, '%Y-%m-%d %H:%M')

		minutes = (busDateTime - now).seconds / 60
		h = int(round(minutes))

		# if it is close enough to present time, h validates to over 1000 for some reason
		if h > 1000:
		  return 0

		return h

	def correctTimeFromShittyFormat(self, time):

		timeSplit = time.split(":")
		hour = timeSplit[0]
		minute = timeSplit[1]

		intHour = int(hour)

		if intHour >= 24:
			intHour = intHour - 24

			hour = str(intHour)
			hour = "0" + hour

			return hour + ":" + minute
		else:
			return time

	def isCurrentTimeBiggerThanBusDepartureTime(self, time, date, now=None):

		if now is None:
			now = datetime.now()

		busDateYear = date[:4]
		busDateMonth = date[4:6]
		busDateDay = date[6:8]

		busDateString = busDateYear + '-' + busDateMonth + '-' + busDateDay  + ' ' + time

		busDateTime = datetime.strptime(busDateString, '%Y-%m-%d %H:%M')

		# print('now: ' + str(now), 'bus: ' + str(busDateTime))
		# print('now is bigger ' + str(now > busDateTime))

		return now > busDateTime

	def update_txt(self, event = None): # base logic for update_txt function inspired by https://www.reddit.com/r/learnpython/comments/2rpk0k/how_to_update_your_gui_in_tkinter_after_using/
		r = requests.get(url='http://localhost/crawler.php')
		data = r.json()

		data = collections.OrderedDict(reversed(sorted(data.items())))

		self.txt.delete("1.0", "end")

		for key, value in data.items():
			time = value['time']
			date = value['date']
			bus = value['bus']

			self.txt.configure(background='black')

			self.txt.tag_configure("makehaste", foreground="yellow")
			self.txt.tag_configure("toolate", foreground="red")
			self.txt.tag_configure("future", foreground="white")


			print(time, date, bus)

			correctedTime = self.correctTimeFromShittyFormat(time)
			deltaTimeInMinutes = self.getDeltaTimeInMinutes(correctedTime)

			# make waiting times over 60 minutes look prettier on the screen
			if deltaTimeInMinutes >= 60:

				over60 = str(timedelta(minutes=deltaTimeInMinutes))
				over60List = over60.split(":")
				over60ListMinutes = str(over60List[1])

				if len(over60ListMinutes) == 2 and over60ListMinutes[0] == "0":
					over60ListMinutes = over60ListMinutes[1]

				deltaTimeInHoursAndMinutes = str(over60List[0]) + " h " + over60ListMinutes

			# in case I need these afterwards
			# hours, remainder = divmod(deltaTimeInSeconds, 3600)
			# minutes, seconds = divmod(remainder, 60)

			isBusTimeOld = self.isCurrentTimeBiggerThanBusDepartureTime(correctedTime, date)

			if isBusTimeOld is False: # do not show past times

				if deltaTimeInMinutes >= 0 and deltaTimeInMinutes <= 2:
					self.txt.insert('1.0', correctedTime + " " + bus + " ------> " + str(deltaTimeInMinutes) + " min" + '\n', "toolate")
				elif deltaTimeInMinutes > 2 and deltaTimeInMinutes <= 5:
					self.txt.insert('1.0', correctedTime + " " + bus + " ------> " + str(deltaTimeInMinutes) + " min" + '\n', "makehaste")
				elif deltaTimeInMinutes < 60:
					self.txt.insert('1.0', correctedTime + " " + bus + " ------> " + str(deltaTimeInMinutes) + " min" + '\n', "future")
				else:
					self.txt.insert('1.0', correctedTime + " " + bus + " ------> " + str(deltaTimeInHoursAndMinutes) + " min" + '\n', "future")

		print('\n')
		self.txt.update_idletasks()
		self.main.after(30000, self.update_txt)

if __name__ == '__main__':
	Display()
