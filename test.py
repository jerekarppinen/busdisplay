import unittest
from datetime import datetime
from display import Display

# class TestBusDisplayMethods(unittest.TestCase):

#     def test_isCurrentTimeBiggerThanBusDepartureTime(self):
#         mockDate = datetime.strptime('Jan 7 2017 00:00', '%b %d %Y %H:%M')
#         self.assertEqual(False, Display.isCurrentTimeBiggerThanBusDepartureTime(self, '00:01', mockDate))

#         mockDate = datetime.strptime('Jan 7 2017 00:02', '%b %d %Y %H:%M')
#         self.assertEqual(True, Display.isCurrentTimeBiggerThanBusDepartureTime(self, '00:01', mockDate))

#         mockDate = datetime.strptime('Jan 7 2017 23:59', '%b %d %Y %H:%M')
#         self.assertEqual(False, Display.isCurrentTimeBiggerThanBusDepartureTime(self, '00:00', mockDate))

#     def test_getDeltaTimeInMinutes(self):
#         mockDate = datetime.strptime('Jan 7 2017 21:50', '%b %d %Y %H:%M')
#         self.assertEqual(10, Display.getDeltaTimeInMinutes(self, '22:00', mockDate))
#         mockDate = datetime.strptime('Jan 7 2017 23:59', '%b %d %Y %H:%M')
#         self.assertEqual(2, Display.getDeltaTimeInMinutes(self, '00:01', mockDate))

# if __name__ == '__main__':
#     unittest.main()