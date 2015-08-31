import sys
import os
sys.path.append(sys.path.append(\
  os.sep.join(os.getcwd().split(os.sep)[:os.getcwd().split(os.sep).index('pyparse')]+['pyparse' + os.sep]))) #fixing python path


from src.qmodel import Tree
import unittest

class ModelTestCase(unittest.TestCase):

    faultyInput = [
        #[[('master')]], # missing attributes
        #[[('master', 'class')]], # wrong attributes types
        #[[('master', {'blink': 'blink'})]], # misses type
        #[[('master', {'type': 'class'}), []]] # empty level
        ['master'], # list should have children, missing tuple
    ]

    def setUp(self):
        self.tree = Tree([[('master', {'type': 'class'})]], '~/filename.py')

    def test_setBranches(self):
        # Ill formatted tree
        for fi in range(len(self.faultyInput)):
            with self.subTest(i=fi):
                with self.assertRaises((TypeError, KeyError, IndexError, ValueError)):
                    self.tree.setBranches(self.faultyInput[fi])

if __name__ == '__main__':
    unittest.main()
