php -S localhost:8080 -t /home/pi/busdisplay/php/ > /dev/null 2>&1 &
export DISPLAY=:0
python3 display.py > /dev/null 2>&1 &
