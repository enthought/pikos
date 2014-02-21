import os
import shutil
import tempfile
import sys

from pikos.recorders.api import (
    TextStreamRecorder, TextFileRecorder, CSVFileRecorder)
from pikos.tests import compat

def my_filter(record):
    return False

class TestPikosRecorderFactories(compat.TestCase):

    def setUp(self):
        self.directory = tempfile.mkdtemp()
        self.filename = os.path.join(self.directory, 'mylog')

    def tearDown(self):
        shutil.rmtree(self.directory)

    def test_screen(self):
        from pikos.api import screen

        # default usage
        recorder = screen()
        self.assertIsInstance(recorder, TextStreamRecorder)
        self.assertIs(recorder._stream, sys.stdout)

        # with a filter
        recorder = screen(filter_=my_filter)
        self.assertIsInstance(recorder, TextStreamRecorder)
        self.assertIs(recorder._stream, sys.stdout)
        self.assertIs(recorder._filter, my_filter)

    def test_textfile(self):
        from pikos.api import textfile

        # default usage
        recorder = textfile()
        self.assertIsInstance(recorder, TextFileRecorder)
        self.assertEqual(recorder._filename, 'monitor_records.log')
        self.assertIsNone(recorder._stream)

        # with a filter
        recorder = textfile(self.filename, filter_=my_filter)
        self.assertIsInstance(recorder, TextFileRecorder)
        self.assertEqual(recorder._filename, self.filename)
        self.assertIsNone(recorder._stream)
        self.assertIs(recorder._filter, my_filter)

    def test_csvfile(self):
        from pikos.api import csvfile

        # default usage
        recorder = csvfile()
        self.assertIsInstance(recorder, CSVFileRecorder)
        self.assertEqual(recorder._filename, 'monitor_records.csv')
        self.assertIsNone(recorder._handle)

        # with a filter
        recorder = csvfile(self.filename, filter_=my_filter)
        self.assertIsInstance(recorder, CSVFileRecorder)
        self.assertEqual(recorder._filename, self.filename)
        self.assertIs(recorder._filter, my_filter)


if __name__ == '__main__':
    import unittest
    unittest.main()
