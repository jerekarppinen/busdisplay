import tkinter
from tkinter.font import Font
from time import sleep
import requests

# base logic for this inspired by https://www.reddit.com/r/learnpython/comments/2rpk0k/how_to_update_your_gui_in_tkinter_after_using/

def update_txt(event = None):
    r = requests.get(url='http://10.10.15.50/bus.php?')
    data = r.json()

    txt.delete('1.0','end')
    print(data)
    for time in reversed(data):

        txt.insert('1.0', time + '\n')
        txt.update_idletasks()

    main.after(60000, update_txt)

main = tkinter.Tk()
txt = tkinter.Text(main)
myFont = Font(family="Helvetica", size=32)
txt.configure(font=myFont)
txt.pack()
main.after(0, update_txt)
main.mainloop()