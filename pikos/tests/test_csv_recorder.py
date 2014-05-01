import StringIO
import unittest

from pikos.recorders.csv_recorder import CSVRecorder
from pikos.recorders.abstract_recorder import RecorderError
from pikos.tests.compat import TestCase
from pikos.tests.dummy_record import DummyRecord


class TestCSVRecorder(TestCase):

    def setUp(self):
        self.temp = StringIO.StringIO()

    def tearDown(self):
        self.temp.close()

    def test_prepare_with_namedtuple(self):
        header = 'one,two,three\r\n'
        recorder = CSVRecorder(self.temp)
        recorder.prepare(DummyRecord)

        # the first call writes the header
        self.assertMultiLineEqual(self.temp.getvalue(), header)
        recorder.prepare(DummyRecord)
        # all calls after that do nothing
        for x in range(10):
            recorder.prepare(DummyRecord)
        self.assertMultiLineEqual(self.temp.getvalue(), header)

    def test_prepare_with_tuple(self):
        recorder = CSVRecorder(self.temp)
        recorder.prepare(tuple)

        # there is no header in this case
        self.assertMultiLineEqual(self.temp.getvalue(), '')
        recorder.prepare(tuple)
        # all calls do nothing
        for x in range(10):
            recorder.prepare(tuple)
        self.assertMultiLineEqual(self.temp.getvalue(), '')

    def test_finalize(self):
        header = 'one,two,three\r\n'
        recorder = CSVRecorder(self.temp)
        # all calls do nothing
        recorder.prepare(DummyRecord)
        for x in range(10):
            recorder.finalize()
        self.assertMultiLineEqual(self.temp.getvalue(), header)

    def test_record_with_namedtuple(self):
        record = DummyRecord(5, 'pikos', 'apikos')
        output = 'one,two,three\r\n5,pikos,apikos\r\n'
        recorder = CSVRecorder(self.temp)
        recorder.prepare(DummyRecord)
        recorder.record(record)
        self.assertMultiLineEqual(self.temp.getvalue(), output)

    def test_record_with_tuple(self):
        record = (5, 'pikos', 'apikos')
        output = '5,pikos,apikos\r\n'
        recorder = CSVRecorder(self.temp)
        recorder.prepare(tuple)
        recorder.record(record)
        self.assertMultiLineEqual(self.temp.getvalue(), output)

    def test_filter(self):
        records = [
            DummyRecord(5, 'pikos', 'apikos'),
            DummyRecord(12, 'emilios', 'milo')]
        output = 'one,two,three\r\n12,emilios,milo\r\n'

        def not_pikos(records):
            return all('pikos' != record for record in records)

        recorder = CSVRecorder(self.temp, filter_=not_pikos)
        recorder.prepare(DummyRecord)
        for record in records:
            recorder.record(record)
        self.assertMultiLineEqual(self.temp.getvalue(), output)

    def test_dialect(self):
        records = [
            DummyRecord(5, 'pikos', 'apikos'),
            DummyRecord(12, 'emilios', 'milo')]
        output = 'one,two,three^5,pikos,apikos^12,emilios,milo^'
        recorder = CSVRecorder(self.temp, lineterminator='^')
        recorder.prepare(DummyRecord)
        for record in records:
            recorder.record(record)
        self.assertMultiLineEqual(self.temp.getvalue(), output)

    def test_exception_when_no_prepare(self):
        records = [DummyRecord(5, 'pikos', 'apikos')]
        recorder = CSVRecorder(self.temp)

        with self.assertRaises(RecorderError):
            recorder.record(records)

        with self.assertRaises(RecorderError):
            recorder.finalize()

if __name__ == '__main__':
    unittest.main()
