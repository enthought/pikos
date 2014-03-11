# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
#  Package: Pikos toolkit
#  File: monitors/test_focused_line_monitor.py
#  License: LICENSE.TXT
#
#  Copyright (c) 2012, Enthought, Inc.
#  All rights reserved.
#------------------------------------------------------------------------------
import StringIO
import unittest

from pikos.monitors.focused_line_memory_monitor import (
    FocusedLineMemoryMonitor)
from pikos.recorders.list_recorder import ListRecorder
from pikos.tests.compat import TestCase


class TestFocusedLineMemoryMonitor(TestCase):

    def setUp(self):
        self.filename = __file__.replace('.pyc', '.py')
        self.maxDiff = None
        self.stream = StringIO.StringIO()
        self.recorder = ListRecorder()

    def test_focus_on_function(self):

        def gcd(x, y):
            while x > 0:
                x, y = internal(x, y)
            return y

        def internal(x, y):
            boo()
            return y % x, x

        def boo():
            pass

        recorder = self.recorder
        logger = FocusedLineMemoryMonitor(recorder, functions=[gcd])

        @logger.attach
        def container(x, y):
            boo()
            result = gcd(x, y)
            boo()
            return result

        boo()
        result = container(12, 3)
        boo()
        self.assertEqual(result, 3)

        filename = self.filename
        expected = [
            "0 gcd 30             while x > 0: {0}".format(filename),
            "1 gcd 31                 x, y = internal(x, y) {0}".format(filename),
            "2 gcd 30             while x > 0: {0}".format(filename),
            "3 gcd 31                 x, y = internal(x, y) {0}".format(filename),
            "4 gcd 30             while x > 0: {0}".format(filename),
            "5 gcd 32             return y {0}".format(filename)]
        records = self.get_records(recorder)
        self.assertEqual(records, expected)

    def test_focus_on_functions(self):

        def gcd(x, y):
            while x > 0:
                x, y = internal(x, y)
            return y

        def internal(x, y):
            return y % x, x

        def boo():
            pass

        def foo():
            boo()
            boo()

        recorder = self.recorder
        logger = FocusedLineMemoryMonitor(recorder, functions=[gcd, foo])

        @logger.attach
        def container(x, y):
            boo()
            result = gcd(x, y)
            boo()
            foo()
            return result

        boo()
        result = container(12, 3)
        boo()
        self.assertEqual(result, 3)
        filename = self.filename
        expected = [
            "0 gcd 70             while x > 0: {0}".format(filename),
            "1 gcd 71                 x, y = internal(x, y) {0}".format(filename),
            "2 gcd 70             while x > 0: {0}".format(filename),
            "3 gcd 71                 x, y = internal(x, y) {0}".format(filename),
            "4 gcd 70             while x > 0: {0}".format(filename),
            "5 gcd 72             return y {0}".format(filename),
            "6 foo 81             boo() {0}".format(filename),
            "7 foo 82             boo() {0}".format(filename)]
        records = self.get_records(recorder)
        self.assertEqual(records, expected)

    def test_focus_on_recursive(self):

        def gcd(x, y):
            foo()
            return x if y == 0 else gcd(y, (x % y))

        def boo():
            pass

        def foo():
            pass

        recorder = self.recorder
        logger = FocusedLineMemoryMonitor(recorder, functions=[gcd])

        @logger.attach
        def container(x, y):
            boo()
            result = gcd(x, y)
            boo()
            foo()
            return result

        boo()
        result = container(12, 3)
        boo()
        self.assertEqual(result, 3)
        filename = self.filename
        expected = [
            "0 gcd 115             foo() {0}".format(filename),
            "1 gcd 116             return x if y == 0 else gcd(y, (x % y)) {0}".format(filename),
            "2 gcd 115             foo() {0}".format(filename),
            "3 gcd 116             return x if y == 0 else gcd(y, (x % y)) {0}".format(filename)]
        records = self.get_records(recorder)
        self.assertEqual(records, expected)

    def test_focus_on_decorated_recursive_function(self):

        def foo():
            pass

        recorder = self.recorder
        logger = FocusedLineMemoryMonitor(recorder)

        @logger.attach(include_decorated=True)
        def gcd(x, y):
            foo()
            return x if y == 0 else gcd(y, (x % y))

        result = gcd(12, 3)
        self.assertEqual(result, 3)
        filename = self.filename
        expected = [
            "0 gcd 158             foo() {0}".format(filename),
            "1 gcd 159             return x if y == 0 else gcd(y, (x % y)) {0}".format(filename),
            "2 gcd 158             foo() {0}".format(filename),
            "3 gcd 159             return x if y == 0 else gcd(y, (x % y)) {0}".format(filename)]
        records = self.get_records(recorder)
        self.assertEqual(records, expected)

    def test_focus_on_decorated_function(self):

        def internal(x, y):
            return y % x, x

        def boo():
            pass

        recorder = self.recorder
        logger = FocusedLineMemoryMonitor(recorder)

        @logger.attach(include_decorated=True)
        def gcd(x, y):
            while x > 0:
                x, y = internal(x, y)
            return y

        boo()
        result = gcd(12, 3)
        boo()
        self.assertEqual(result, 3)
        filename = self.filename
        expected = [
            "0 gcd 185             while x > 0: {0}".format(filename),
            "1 gcd 186                 x, y = internal(x, y) {0}".format(filename),
            "2 gcd 185             while x > 0: {0}".format(filename),
            "3 gcd 186                 x, y = internal(x, y) {0}".format(filename),
            "4 gcd 185             while x > 0: {0}".format(filename),
            "5 gcd 187             return y {0}".format(filename)]
        records = self.get_records(recorder)
        self.assertEqual(records, expected)

    def test_focus_on_function(self):

        def gcd(x, y):
            while x > 0:
                x, y = internal(x, y)
            return y

        def internal(x, y):
            boo()
            return y % x, x

        def boo():
            pass

        recorder = self.recorder
        logger = FocusedLineMemoryMonitor(
            recorder, record_type=tuple, functions=[gcd])

        @logger.attach
        def container(x, y):
            boo()
            result = gcd(x, y)
            boo()
            return result

        boo()
        result = container(12, 3)
        boo()
        self.assertEqual(result, 3)

        filename = self.filename
        expected = [
            "0 gcd 207             while x > 0: {0}".format(filename),
            "1 gcd 208                 x, y = internal(x, y) {0}".format(filename),
            "2 gcd 207             while x > 0: {0}".format(filename),
            "3 gcd 208                 x, y = internal(x, y) {0}".format(filename),
            "4 gcd 207             while x > 0: {0}".format(filename),
            "5 gcd 209             return y {0}".format(filename)]
        records = self.get_records(recorder)
        self.assertEqual(records, expected)

    def get_records(self, recorder):
        """ Remove the memory related fields.
        """
        records = []
        for record in recorder.records:
            filtered = record[:3] + record[5:]
            records.append(
                ' '.join([str(item).rstrip() for item in filtered]))
        return records


if __name__ == '__main__':
    unittest.main()
