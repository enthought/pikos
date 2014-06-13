import unittest

from pikos.recorders.list_recorder import ListRecorder
from pikos.tests.compat import TestCase
from pikos.tests.dummy_record import DummyRecord


class TestListRecorder(TestCase):

    def test_prepare(self):
        output = []
        recorder = ListRecorder()
        recorder.prepare(DummyRecord)
        self.assertSequenceEqual(recorder.records, output)
        recorder.prepare(DummyRecord)

    def test_finalize(self):
        output = []
        recorder = ListRecorder()
        recorder.prepare(DummyRecord)
        for x in range(10):
            recorder.finalize()
        self.assertSequenceEqual(recorder.records, output)

    def test_record(self):
        record = DummyRecord(5, 'pikos', 'apikos')
        output = [(5, 'pikos', 'apikos')]
        recorder = ListRecorder()
        recorder.prepare(DummyRecord)
        recorder.record(record)
        self.assertSequenceEqual(recorder.records, output)

    def test_filter(self):
        records = [
            DummyRecord(5, 'pikos', 'apikos'),
            DummyRecord(12, 'emilios', 'milo')]
        output = [(12, 'emilios', 'milo')]

        def not_pikos(values):
            return not ('pikos' in values)

        recorder = ListRecorder(filter_=not_pikos)
        recorder.prepare(DummyRecord)
        for record in records:
            recorder.record(record)
        self.assertSequenceEqual(recorder.records, output)

if __name__ == '__main__':
    unittest.main()
