import os
import StringIO
import unittest

from collections import namedtuple

from pikos.recorders.text_stream_recorder import TextStreamRecorder
from pikos.recorders.abstract_recorder import RecorderError


class MockRecord(namedtuple('MockRecord', ('one', 'two', 'three'))):

    @classmethod
    def header(cls):
        return '{:<5} {:<5} {:<5}{newline}'.format(*cls._fields,
                                                   newline=os.linesep)

    def line(self):
        return '{:<5} {:<5} {:<5}{newline}'.format(*self, newline=os.linesep)


class TestTextStreamRecorder(unittest.TestCase):

    def setUp(self):
        self.temp = StringIO.StringIO()
        self.maxDiff = None

    def tearDown(self):
        self.temp.close()

    def test_prepare(self):
        header = 'one two three{newline}-------------{newline}'.\
                 format(newline=os.linesep)
        recorder = TextStreamRecorder(self.temp)
        recorder.prepare(MockRecord)

        # the first call writes the header
        self.assertMultiLineEqual(self.temp.getvalue(), header)
        recorder.prepare(MockRecord)
        # all calls after that do nothing
        for x in range(10):
            recorder.prepare(MockRecord)
        self.assertMultiLineEqual(self.temp.getvalue(), header)

    def test_finalize(self):
        header = 'one two three{newline}-------------{newline}'.\
                 format(newline=os.linesep)
        recorder = TextStreamRecorder(self.temp)
        # all calls do nothing
        recorder.prepare(MockRecord)
        for x in range(10):
            recorder.finalize()
        self.assertMultiLineEqual(self.temp.getvalue(), header)

    def test_record(self):
        record = MockRecord(5, 'pikos', 'apikos')
        output = ('one two three{newline}-------------{newline}'
                  '5 pikos apikos{newline}'.format(newline=os.linesep))
        recorder = TextStreamRecorder(self.temp)
        recorder.prepare(MockRecord)
        recorder.record(record)
        self.assertMultiLineEqual(self.temp.getvalue(), output)

    def test_filter(self):
        records = [MockRecord(5, 'pikos', 'apikos'),
                 MockRecord(12, 'emilios', 'milo')]
        output = ('one two three{newline}-------------{newline}'
                  '12 emilios milo{newline}'.format(newline=os.linesep))

        def not_pikos(values):
            return not 'pikos' in values

        recorder = TextStreamRecorder(self.temp, filter_=not_pikos)
        recorder.prepare(MockRecord)
        for record in records:
            recorder.record(record)
        self.assertMultiLineEqual(self.temp.getvalue(), output)

    def test_exceptions(self):
        record = MockRecord(5, 'pikos', 'apikos')
        recorder = TextStreamRecorder(self.temp)

        with self.assertRaises(RecorderError):
            recorder.record(record)

        with self.assertRaises(RecorderError):
            recorder.finalize()

    def test_formater(self):
        record = MockRecord(5, 'pikos', 'apikos')
        output = ('one   two   three{newline}-----------------{newline}'
                  '5     pikos apikos{newline}'.format(newline=os.linesep))
        recorder = TextStreamRecorder(self.temp, formated=True)
        recorder.prepare(MockRecord)
        recorder.record(record)
        self.assertMultiLineEqual(self.temp.getvalue(), output)


if __name__ == '__main__':
    unittest.main()
