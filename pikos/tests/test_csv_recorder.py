import StringIO
import unittest

from pikos.recorders.csv_recorder import CSVRecorder
from pikos.recorders.abstract_recorder import RecorderError
from pikos.tests.compat import TestCase


class TestCSVRecorder(TestCase):

    def setUp(self):
        self.temp = StringIO.StringIO()

    def tearDown(self):
        self.temp.close()

    def test_prepare(self):
        fields = ('one', 'two', 'three')
        header = 'one,two,three\r\n'
        recorder = CSVRecorder(self.temp)
        recorder.prepare(fields)

        # the first call writes the header
        self.assertMultiLineEqual(self.temp.getvalue(), header)
        recorder.prepare(fields)
        # all calls after that do nothing
        for x in range(10):
            recorder.prepare(fields)
        self.assertMultiLineEqual(self.temp.getvalue(), header)

    def test_finalize(self):
        fields = ('one', 'two', 'three')
        header = 'one,two,three\r\n'
        recorder = CSVRecorder(self.temp)
        # all calls do nothing
        recorder.prepare(fields)
        for x in range(10):
            recorder.finalize()
        self.assertMultiLineEqual(self.temp.getvalue(), header)

    def test_record(self):
        fields = ('one', 'two', 'three')
        values = (5, 'pikos', 'apikos')
        output = 'one,two,three\r\n5,pikos,apikos\r\n'
        recorder = CSVRecorder(self.temp)
        recorder.prepare(fields)
        recorder.record(values)
        self.assertMultiLineEqual(self.temp.getvalue(), output)

    def test_filter(self):
        fields = ('one', 'two', 'three')
        values = [(5, 'pikos', 'apikos'), (12, 'emilios', 'milo')]
        output = 'one,two,three\r\n12,emilios,milo\r\n'

        def not_pikos(values):
            return not 'pikos' in values

        recorder = CSVRecorder(self.temp, filter_=not_pikos)
        recorder.prepare(fields)
        for record in values:
            recorder.record(record)
        self.assertMultiLineEqual(self.temp.getvalue(), output)

    def test_dialect(self):
        fields = ('one', 'two', 'three')
        values = [(5, 'pikos', 'apikos'), (12, 'emilios', 'milo')]
        output = 'one,two,three^5,pikos,apikos^12,emilios,milo^'
        recorder = CSVRecorder(self.temp, lineterminator='^')
        recorder.prepare(fields)
        for record in values:
            recorder.record(record)
        self.assertMultiLineEqual(self.temp.getvalue(), output)

    def test_exception_when_no_prepare(self):
        values = [(5, 'pikos', 'apikos')]
        recorder = CSVRecorder(self.temp)

        with self.assertRaises(RecorderError):
            recorder.record(values)

        with self.assertRaises(RecorderError):
            recorder.finalize()

if __name__ == '__main__':
    unittest.main()
