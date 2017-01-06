import tkinter
from tkinter.font import Font
from time import sleep
import requests
import calendar
from datetime import datetime



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

def compareBusTimeToCurrentTime(time):

    now = datetime.now()
    #nowMock = datetime.strptime('Jan 5 2017 23:40', '%b %d %Y %H:%M')

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

    return now > busDateTime

def update_txt(event = None): # base logic for update_txt function inspired by https://www.reddit.com/r/learnpython/comments/2rpk0k/how_to_update_your_gui_in_tkinter_after_using/
    r = requests.get(url='http://localhost/bus.php')
    data = r.json()

    print(data)

    reversedData = reversed(data)

    txt.configure(background='black')

    txt.tag_configure("old", foreground="yellow")
    txt.tag_configure("future", foreground="white")

    txt.delete("1.0", "end")

    for time in reversedData:

        correctedTime = correctTimeFromShittyFormat(time[:5])

        print(correctedTime)

        isBusTimeOld = compareBusTimeToCurrentTime(correctedTime)

        if isBusTimeOld:
            txt.insert('1.0', correctedTime + '\n', "old")
            print("Is bus time old: " + str(isBusTimeOld)  + " " + correctedTime)
        else:
            txt.insert('1.0', correctedTime + '\n', "future")
            print("Is bus time old: " + str(isBusTimeOld)  + " " + correctedTime)

    print("\n")
    txt.update_idletasks()
    main.after(30000, update_txt)

main = tkinter.Tk()
screen_width = main.winfo_screenwidth()
screen_height = main.winfo_screenheight()

resolution = str(screen_width) + "x" + str(screen_height)
main.geometry(resolution) 
txt = tkinter.Text(main)
txt.configure(font=Font(size=32, family="Default sans-serif"))
txt.pack()
main.after(0, update_txt)
main.mainloop()