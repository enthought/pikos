import StringIO
import unittest

from pikos.recorders.text_stream_recorder import TextStreamRecorder
from pikos.recorders.abstract_recorder import RecorderError
from pikos.tests.compat import TestCase
from pikos.tests.dummy_record import DummyRecord


class TestTextStreamRecorder(TestCase):

    def setUp(self):
        self.temp = StringIO.StringIO()
        self.maxDiff = None

    def tearDown(self):
        self.temp.close()

    def test_prepare(self):
        header = 'one two three\n-------------\n'
        recorder = TextStreamRecorder(self.temp)
        recorder.prepare(DummyRecord)

        # the first call writes the header
        self.assertMultiLineEqual(self.temp.getvalue(), header)
        recorder.prepare(DummyRecord)
        # all calls after that do nothing
        for x in range(10):
            recorder.prepare(DummyRecord)
        self.assertMultiLineEqual(self.temp.getvalue(), header)

    def test_finalize(self):
        header = 'one two three\n-------------\n'
        recorder = TextStreamRecorder(self.temp)
        # all calls do nothing
        recorder.prepare(DummyRecord)
        for x in range(10):
            recorder.finalize()
        self.assertMultiLineEqual(self.temp.getvalue(), header)

    def test_record(self):
        record = DummyRecord(5, 'pikos', 'apikos')
        output = 'one two three\n-------------\n5 pikos apikos\n'
        recorder = TextStreamRecorder(self.temp)
        recorder.prepare(DummyRecord)
        recorder.record(record)
        self.assertMultiLineEqual(self.temp.getvalue(), output)

    def test_filter(self):
        records = [
            DummyRecord(5, 'pikos', 'apikos'),
            DummyRecord(12, 'emilios', 'milo')]
        output = 'one two three\n-------------\n12 emilios milo\n'

        def not_pikos(values):
            return not ('pikos' in values)

        recorder = TextStreamRecorder(self.temp, filter_=not_pikos)
        recorder.prepare(DummyRecord)
        for record in records:
            recorder.record(record)
        self.assertMultiLineEqual(self.temp.getvalue(), output)

    def test_exceptions(self):
        record = DummyRecord(5, 'pikos', 'apikos')
        recorder = TextStreamRecorder(self.temp)

        with self.assertRaises(RecorderError):
            recorder.record(record)

        with self.assertRaises(RecorderError):
            recorder.finalize()

    def test_formatter_with_namedtuples(self):
        record = DummyRecord(5, 'pikos', 'apikos')
        output = 'one   two   three\n-----------------\n5     pikos apikos\n'
        recorder = TextStreamRecorder(self.temp, formatted=True)
        recorder.prepare(DummyRecord)
        recorder.record(record)
        self.assertMultiLineEqual(self.temp.getvalue(), output)

    def test_formatter_with_tuples(self):
        record = (5, 'pikos', 'apikos')
        output = '5 pikos apikos\n'
        recorder = TextStreamRecorder(self.temp, formatted=True)
        recorder.prepare(tuple)
        recorder.record(record)
        self.assertMultiLineEqual(self.temp.getvalue(), output)


if __name__ == '__main__':
    unittest.main()
