sudo apt-get update && sudo apt-get upgrade -y
sudo apt-get install php -y
pip3 install rpi-backlight
pip3 install pytz
php -S localhost:8080 -t /home/pi/busdisplay/php/ > /dev/null 2>&1 &
export DISPLAY=:0
python3 display.py > /dev/null 2>&1 &
