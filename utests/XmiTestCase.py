import sys
import os
sys.path.append(sys.path.append(\
  os.sep.join(os.getcwd().split(os.sep)[:os.getcwd().split(os.sep).index('pyparse')]+['pyparse' + os.sep]))) #fixing python path


from src.exporter import Xmi
import unittest

class XmiTestCase(unittest.TestCase):

    faultyInput = [
        [[('master')]], # missing attributes
        [[('master', 'class')]], # wrong attributes types
        [[('master', {'blink': 'blink'})]], # misses type
        [[('master', {'type': 'class'}), []]] # empty level
    ]

    def setUp(self):
        self.xmi = Xmi()

    def test_setTree(self):
        # Ill formatted tree
        for fi in range(len(self.faultyInput)):
            with self.subTest(i=fi):
                with self.assertRaises((TypeError, KeyError, IndexError)):
                    self.xmi.setTree(self.faultyInput[fi])

    def test_write(self):
        # No tree set
        with self.assertRaises(RuntimeError):
            self.xmi.write('filename')
        # Missing argument
        with self.assertRaises(TypeError):
            self.xmi.write()


if __name__ == '__main__':
    unittest.main()
