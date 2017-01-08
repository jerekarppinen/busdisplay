import unittest
from datetime import datetime
from display import Display

class TestBusDisplayMethods(unittest.TestCase):

    def test_correctTimeFromShittyFormat(self):
        self.assertEqual('00:01', Display.correctTimeFromShittyFormat(self, '00:01'))
        self.assertEqual('01:01', Display.correctTimeFromShittyFormat(self, '25:01'))
        self.assertEqual('23:01', Display.correctTimeFromShittyFormat(self, '23:01'))
        self.assertEqual('04:01', Display.correctTimeFromShittyFormat(self, '28:01'))

    def test_compareBusTimeToCurrentTime(self):
        mockDate = datetime.strptime('Jan 7 2017 00:00', '%b %d %Y %H:%M')
        self.assertEqual(False, Display.isCurrentTimeBiggerThanBusDepartureTime(self, '00:01', '20170107', mockDate))

        mockDate = datetime.strptime('Jan 7 2017 00:02', '%b %d %Y %H:%M')
        self.assertEqual(True, Display.isCurrentTimeBiggerThanBusDepartureTime(self, '00:01', '20170107', mockDate))

        mockDate = datetime.strptime('Jan 7 2017 23:59', '%b %d %Y %H:%M')
        self.assertEqual(False, Display.isCurrentTimeBiggerThanBusDepartureTime(self, '00:00', '20170207', mockDate))

    def test_getDeltaTimeInMinutes(self):
        mockDate = datetime.strptime('Jan 7 2017 21:50', '%b %d %Y %H:%M')
        self.assertEqual(10, Display.getDeltaTimeInMinutes(self, '22:00', mockDate))
        mockDate = datetime.strptime('Jan 7 2017 23:59', '%b %d %Y %H:%M')
        self.assertEqual(2, Display.getDeltaTimeInMinutes(self, '00:01', mockDate))

if __name__ == '__main__':
    unittest.main()