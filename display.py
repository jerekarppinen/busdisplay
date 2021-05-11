from time import sleep
from time import gmtime, strftime
from pytz import timezone
from datetime import datetime
from datetime import timedelta
import time
import collections
import logging
import config


class Display():
	def __init__(self):

		logging.basicConfig(filename='display.log',level=logging.DEBUG)
		logging.info('\n\n')

		self.main = tkinter.Tk()
		screen_width = self.main.winfo_screenwidth()
		screen_height = self.main.winfo_screenheight()
		resolution = str(screen_width) + "x" + str(screen_height)
		self.main.geometry(resolution) 
		self.txt = tkinter.Text(self.main, padx=10)
		self.txt.configure(font=Font(size=32, family="Default sans-serif"))
		self.txt.pack()

		self.main.after(0, self.update_txt)

		if config.waitUntilNextFullMinute == 1:
			#sleep until next starting minute
			self.sleepUntilNextMinute()

		self.main.mainloop()

	def sleepUntilNextMinute(self):
		print('Starting on next full minute...')
		logging.info('Starting on next full minute...')
		sleeptime = 60 - datetime.utcnow().second
		print('Starting in ' + str(sleeptime) + ' seconds.')
		logging.info('Starting in ' + str(sleeptime) + ' seconds.')
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

		# if it is close enough to present time, h resolves to over 1000 for some reason
		if h > 1000:
		  return 0

		return h

	def getPossibleError(self, r):

		data = []
		error = None

		now_utc = datetime.now(timezone('UTC'))
		now_helsinki = now_utc.astimezone(timezone('Europe/Helsinki'))
		fmt = "%H:%M:%S"
		currentTime = now_helsinki.strftime(fmt)

		if r.status_code != requests.codes.ok:
			error = "Status code returned: " + str(r.status_code)

		if error is None:
			try:
				data = r.json()
			except ValueError as verr:
				error = "Value Error: " + str(verr)

		if error is None and len(data) > 0:
			try:
				self.items = data.items()
			except ValueError as verr:
				error = "Value Error: " + str(verr)

		if len(data) == 0:
			error = "Empty object returned"

		if error is None:
			for key, value in self.items:
				if key == "departures":
					if len(value) == 0 or value is None:
						error = str(currentTime) + " Empty response"

		return error

	def update_txt(self, event = None): # base logic for update_txt function inspired by https://www.reddit.com/r/learnpython/comments/2rpk0k/how_to_update_your_gui_in_tkinter_after_using/

		error = False
		r = requests.get(url='http://localhost:8080/api.php')
		data = r.json()

		error = self.getPossibleError(r)

		if error is not None:
			self.txt.insert('1.0', error + '\n', "toolate")
			self.main.after(10000, self.update_txt)


		else:

			self.txt.configure(background='black')

			self.txt.tag_configure("makehaste", foreground="yellow")
			self.txt.tag_configure("toolate", foreground="red")
			self.txt.tag_configure("future", foreground="white")
			self.txt.tag_configure("title", foreground="lightgreen")

			self.txt.delete("1.0", "end")

			stopName = data['stopname']
			departures = data['departures']

			for departure in reversed(departures):


				destination = departure['destination']
				time = departure['time']
				line =  "(" + departure['line'] + ")"

				# logging.info('Destination: ' + () + ', Line: ' + line + ', Stopname: ' + stopName + ', Time: ' + time)


				# print('Destination: ' + () + ', Line: ' + line + ', Stopname: ' + stopName + ', Time: ' + time)

				deltaTimeInMinutes = self.getDeltaTimeInMinutes(time)
				logging.debug('DeltaTimeInMinutes: ' + str(deltaTimeInMinutes))

				# make waiting times over 60 minutes look prettier on the screen
				if deltaTimeInMinutes >= 60:

					over60 = str(timedelta(minutes=deltaTimeInMinutes))
					over60List = over60.split(":")
					over60ListMinutes = str(over60List[1])

					if len(over60ListMinutes) == 2 and over60ListMinutes[0] == "0":
						over60ListMinutes = over60ListMinutes[1]

					deltaTimeInHoursAndMinutes = str(over60List[0]) + " h " + over60ListMinutes

				empty_space = "          "

				if len(destination) == 8:
					empty_space = "                 "

				if deltaTimeInMinutes >= 0 and deltaTimeInMinutes <= 2:
					self.txt.insert('1.0', time + " " + destination + " " + line + empty_space + str(deltaTimeInMinutes) + " min" + '\n', "toolate")
				elif deltaTimeInMinutes > 2 and deltaTimeInMinutes <= 5:
					self.txt.insert('1.0', time + " " + destination + " " + line + empty_space + str(deltaTimeInMinutes) + " min" + '\n', "makehaste")
				elif deltaTimeInMinutes < 60:
					self.txt.insert('1.0', time + " " + destination + " " + line + empty_space + str(deltaTimeInMinutes) + " min" + '\n', "future")
				else:
					self.txt.insert('1.0', time + " " + destination + " " + line + empty_space + str(deltaTimeInHoursAndMinutes) + " min" + '\n', "future")

			print('\n')
			self.txt.update_idletasks()
			self.main.after(30000, self.update_txt)	

	# if config.showStopAndDestination == 1:
	# 	self.txt.insert('1.0', stopName + '  --------------->  ' + destination +  '\n', "title")

if __name__ == '__main__':
	import tkinter
	from tkinter.font import Font
	import requests
	Display()
