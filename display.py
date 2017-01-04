import tkinter
from tkinter.font import Font
from time import sleep
import requests
import datetime

# base logic for this inspired by https://www.reddit.com/r/learnpython/comments/2rpk0k/how_to_update_your_gui_in_tkinter_after_using/

def compareBusTimeToCurrentTime(time):

    now = datetime.datetime.now()

    currentYear = now.year
    currentDay = now.day
    currentMonth = now.month
    currentHour = now.hour
    currentMinute = now.minute

    timeSplit = time.split(":")
    hour = timeSplit[0]
    minute = timeSplit[1]

    hourInt = int(hour)
    # hsl api returns weird shit after midnight
    if hourInt >= 24:
        return False

    busDate = str(currentYear) + "-" + str(currentMonth) + "-" + str(currentDay) + " " + hour + ":" + minute

    busDateTime = datetime.datetime.strptime(busDate, "%Y-%m-%d %H:%M")

    return now > busDateTime

def update_txt(event = None):
    r = requests.get(url='http://localhost/bus.php')
    data = r.json()

    reversedData = reversed(data)

    txt.configure(background='black')

    txt.tag_configure("old", foreground="yellow")
    txt.tag_configure("future", foreground="white")

    txt.delete("1.0", "end")

    for time in reversedData:

        isBusTimeOld = compareBusTimeToCurrentTime(time[:5])

        if isBusTimeOld:
            txt.insert('1.0', time + '\n', "old")
            print("Is bus time old: " + str(isBusTimeOld)  + " " + time)
        else:
            txt.insert('1.0', time + '\n', "future")
            print("Is bus time old: " + str(isBusTimeOld)  + " " + time)

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