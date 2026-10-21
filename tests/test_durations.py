import unittest
from datetime import time, timedelta
from excel_to_prism import duration_seconds, prepare_column

class DurationTests(unittest.TestCase):
    def test_fraction_and_long_duration(self):
        self.assertAlmostEqual(duration_seconds('0:36:15.760'),2175.76)
        self.assertEqual(duration_seconds('25:00:00'),90000)
        self.assertEqual(duration_seconds(time(0,0,9,880000)),9.88)
        self.assertEqual(duration_seconds(timedelta(seconds=61)),61)
    def test_invalid_duration(self):
        for v in ['0:60:00','1:20','P001',0.5]:
            with self.assertRaises(ValueError): duration_seconds(v)
    def test_units_and_blanks(self):
        title,values=prepare_column(['0:01:00',None,'0:02:00'],'Time','s','A','minutes')
        self.assertEqual(title,'Time (minutes)')
        self.assertEqual(values,['1',None,'2'])
    def test_strict_default(self):
        with self.assertRaises(ValueError): prepare_column(['0:01:00'],'Time','s','A','none')
    def test_numeric_not_rescaled(self):
        self.assertEqual(prepare_column([60,None,120],'Time in Seconds','s','C','minutes'),
                         ('Time in Seconds',['60',None,'120']))
    def test_mixed_values_rejected(self):
        with self.assertRaisesRegex(ValueError,'A3'):
            prepare_column(['0:01:00',60],'Time','s','A','seconds')
