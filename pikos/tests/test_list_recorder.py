import unittest

from pikos.recorders.list_recorder import ListRecorder


class TestListRecorder(unittest.TestCase):

    def test_prepare(self):
        fields = ('one', 'two', 'three')
        output = []
        recorder = ListRecorder()
        recorder.prepare(fields)
        self.assertSequenceEqual(recorder.records, output)
        recorder.prepare(fields)

    def test_finalize(self):
        fields = ('one', 'two', 'three')
        output = []
        recorder = ListRecorder()
        recorder.prepare(fields)
        for x in range(10):
            recorder.finalize()
        self.assertSequenceEqual(recorder.records, output)

    def test_record(self):
        fields = ('one', 'two', 'three')
        values = (5, 'pikos', 'apikos')
        output = [(5, 'pikos', 'apikos')]
        recorder = ListRecorder()
        recorder.prepare(fields)
        recorder.record(values)
        self.assertSequenceEqual(recorder.records, output)

    def test_filter(self):
        fields = ('one', 'two', 'three')
        values = [(5, 'pikos', 'apikos'), (12, 'emilios', 'milo')]
        output = [(12, 'emilios', 'milo')]

        def not_pikos(values):
            return not 'pikos' in values

        recorder = ListRecorder(filter_=not_pikos)
        recorder.prepare(fields)
        for record in values:
            recorder.record(record)
        self.assertSequenceEqual(recorder.records, output)

if __name__ == '__main__':
    unittest.main()
