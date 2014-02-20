import contextlib
import os
import shutil
import tempfile
import unittest

from pikos.recorders.text_file_recorder import TextFileRecorder
from pikos.recorders.abstract_recorder import RecorderError
from pikos.tests.compat import TestCase
from pikos.tests.dummy_record import DummyRecord


class TestTextFileRecorder(TestCase):

    def setUp(self):
        self.directory = tempfile.mkdtemp()
        self.filename = os.path.join(self.directory, 'mylog')

    def tearDown(self):
        shutil.rmtree(self.directory)

    def test_prepare(self):
        header = 'one two three\n-------------\n'
        recorder = TextFileRecorder(filename=self.filename)

        with self.finalizer(recorder):
            recorder.prepare(DummyRecord)
        self.assertRecordedLines(header)

    def test_prepare_multiple_times(self):
        header = 'one two three\n-------------\n'
        recorder = TextFileRecorder(filename=self.filename)

        with self.finalizer(recorder):
            recorder.prepare(DummyRecord)
            # all calls after that do nothing
            for x in range(10):
                recorder.prepare(DummyRecord)
        self.assertRecordedLines(header)

    def test_finalize(self):
        header = 'one two three\n-------------\n'
        recorder = TextFileRecorder(filename=self.filename)
        # all calls do nothing
        with self.finalizer(recorder):
            recorder.prepare(DummyRecord)
            for x in range(10):
                recorder.finalize()
        self.assertRecordedLines(header)

    def test_record(self):
        record = DummyRecord(5, 'pikos', 'apikos')
        output = 'one two three\n-------------\n5 pikos apikos\n'
        print output
        recorder = TextFileRecorder(filename=self.filename)
        with self.finalizer(recorder):
            recorder.prepare(DummyRecord)
            recorder.record(record)
        self.assertRecordedLines(output)

    def test_filter(self):
        records = [
            DummyRecord(5, 'pikos', 'apikos'),
            DummyRecord(12, 'emilios', 'milo')]
        output = 'one two three\n-------------\n12 emilios milo\n'

        def not_pikos(record):
            return all('pikos' != field for field in record)

        recorder = TextFileRecorder(filename=self.filename, filter_=not_pikos)
        with self.finalizer(recorder):
            recorder.prepare(DummyRecord)
            for record in records:
                recorder.record(record)
        self.assertRecordedLines(output)

    def test_formatter(self):
        record = DummyRecord(5, 'pikos', 'apikos')
        output = 'one   two   three\n----------------\n5     pikos apikos\n'
        recorder = TextFileRecorder(
            filename=self.filename, formatted=True)
        with self.finalizer(recorder):
            recorder.prepare(DummyRecord)
            recorder.record(record)
        self.assertRecordedLines(output)

    def test_exception_when_no_prepare(self):
        records = [DummyRecord(5, 'pikos', 'apikos')]
        recorder = TextFileRecorder(filename=self.filename)

        with self.assertRaises(RecorderError):
            recorder.record(records)

        with self.assertRaises(RecorderError):
            recorder.finalize()

    @contextlib.contextmanager
    def finalizer(self, recorder):
        try:
            yield recorder
        finally:
            recorder.finalize()

    def assertRecordedLines(self, expected):
        with open(self.filename, 'Ur') as handle:
            lines = handle.readlines()
            self.assertMultiLineEqual(''.join(lines), expected)


if __name__ == '__main__':
    unittest.main()
