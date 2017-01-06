import tkinter
from tkinter.font import Font
from time import sleep
import requests
import calendar
from datetime import datetime
from datetime import timedelta
import time
import collections

def getDeltaTimeInMinutes(time):
    now = datetime.now()

    currentYear = now.year
    currentDay = now.day
    currentMonth = now.month
    currentHour = now.hour
    currentMinute = now.minute

    timeSplit = time.split(":")
    hour = timeSplit[0]
    minute = timeSplit[1]

    busDate = str(currentYear) + "-" + str(currentMonth) + "-" + str(currentDay) + " " + hour + ":" + minute

    busDateTime = datetime.strptime(busDate, "%Y-%m-%d %H:%M")

    seconds = (busDateTime - now).seconds / 60
    h = int(round(seconds))

    if h > 1000:
        return 0

    return h

def correctTimeFromShittyFormat(time):

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

def compareBusTimeToCurrentTime(time, date):

    now = datetime.now()
    #nowMock = datetime.strptime('Jan 5 2017 23:40', '%b %d %Y %H:%M')

    busDateYear = date[:4]
    busDateMonth = date[4:6]
    busDateDay = date[6:8]

    busDateString = busDateYear + "-" + busDateMonth + "-" + busDateDay  + " " + time

    busDateTime = datetime.strptime(busDateString, "%Y-%m-%d %H:%M")

    return now > busDateTime

def update_txt(event = None): # base logic for update_txt function inspired by https://www.reddit.com/r/learnpython/comments/2rpk0k/how_to_update_your_gui_in_tkinter_after_using/
    r = requests.get(url='http://localhost/bus.php')
    data = r.json()

    data = collections.OrderedDict(reversed(sorted(data.items())))

    txt.configure(background='black')

    txt.tag_configure("makehaste", foreground="yellow")
    txt.tag_configure("toolate", foreground="red")
    txt.tag_configure("future", foreground="white")

    txt.delete("1.0", "end")

    for key, value in data.items():

        time = key[:5]
        date = value[:8]
        bus = value[9:]

        print(time, date, bus)

        correctedTime = correctTimeFromShittyFormat(time)
        deltaTimeInMinutes = getDeltaTimeInMinutes(correctedTime)

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

        isBusTimeOld = compareBusTimeToCurrentTime(correctedTime, date)

        if deltaTimeInMinutes >= 0 and deltaTimeInMinutes <= 2:
            txt.insert('1.0', correctedTime + " " + bus + " ------> " + str(deltaTimeInMinutes) + " min" + '\n', "toolate")
        elif deltaTimeInMinutes > 2 and deltaTimeInMinutes <= 5:
            txt.insert('1.0', correctedTime + " " + bus + " ------> " + str(deltaTimeInMinutes) + " min" + '\n', "makehaste")
        elif deltaTimeInMinutes < 60:
            txt.insert('1.0', correctedTime + " " + bus + " ------> " + str(deltaTimeInMinutes) + " min" + '\n', "future")
        else:
            txt.insert('1.0', correctedTime + " " + bus + " ------> " + str(deltaTimeInHoursAndMinutes) + " min" + '\n', "future")

    print('\n')
    txt.update_idletasks()
    main.after(10000, update_txt)

main = tkinter.Tk()
screen_width = main.winfo_screenwidth()
screen_height = main.winfo_screenheight()
resolution = str(screen_width) + "x" + str(screen_height)
main.geometry(resolution) 
txt = tkinter.Text(main)
txt.configure(font=Font(size=32, family="Default sans-serif"))
txt.pack()
main.after(0, update_txt)

# sleep until next starting minute
# print("Starting on next full minute...")
# sleeptime = 60 - datetime.utcnow().second
# time.sleep(sleeptime)

main.mainloop()