<!-- ![Build status](https://circleci.com/gh/jerekarppinen/busdisplay.svg?style=shield&circle-token=aa56f1b333e444e1e3fb68741845690509be96de) -->

## Development Environment

- Developed with Python 3.x

- Place globals.php into php folder with variables $user and $pass having your hsl api credentials.

- Run docker commands which are in docker-commands.txt and you will get crawler.php running

- Run: python3 display.py, the gui will start in next full minute (to properly refresh the view every new minute and 30s past)

## Testing

- python3 test.py

## Other stuff

- crawler.py is obsolete at the moment