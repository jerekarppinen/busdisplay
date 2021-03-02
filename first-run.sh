sudo apt-get update && sudo apt-get upgrade -y
sudo apt-get install php -y
pip3 install rpi-backlight
(crontab -l ; echo "0 23 * * * /home/pi/.local/bin/rpi-backlight -b 10") | crontab -
(crontab -l ; echo "0 8 * * *  /home/pi/.local/bin/rpi-backlight -b 100") | crontab -
pip3 install pytz
php -S localhost:8080 -t /home/pi/busdisplay/php/ > /dev/null 2>&1 &
export DISPLAY=:0
python3 display.py > /dev/null 2>&1 &
