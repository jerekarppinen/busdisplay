<!-- ![Build status](https://circleci.com/gh/jerekarppinen/busdisplay.svg?style=shield&circle-token=aa56f1b333e444e1e3fb68741845690509be96de) -->

## Purpose of the project

- The purpose is to display next departing times for buses near my place, I run this on Raspberry Pi 7" touch screen

## Development Environment

- Developed with Python 3.x (should install python3-tk to get Tkinter)

- Run docker commands which are in docker-commands.txt and you will get api.php running

- Run: python3 display.py, the gui will start in next full minute (to properly refresh the view every new minute and 30s past)

## Testing

- python3 test.py

![Alt text](https://github.com/jerekarppinen/busdisplay/blob/development/bussiaikataulu.jpg?raw=true "Raspberry Project")

## Keep screen on

- Open /etc/lightdm/lightdm.conf
- Look for the line #xserver-command=X. Change it to xserver-command=X -s 0 dpms
- Save and reboot.

## Use this to dim and bright the screen if necessary
- https://github.com/linusg/rpi-backlight