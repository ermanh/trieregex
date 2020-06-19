# TODO: TO BE COMPLETED

from trieregex.trieregex import TrieRegEx as TRE
import unittest


class TestFinals(unittest.TestCase):
    """Tests for TrieRegEx().finals() and TrieRegEx()._finals
    """

    def setUp(self):
        self.words = ['heart', 'healthy', 'pear', 'peach',
                      'lark', 'look', 'change']
        self.tre = TRE(*self.words)

    def test_finals(self):
        assert self.tre.finals() == ['e', 'h', 'k', 'r', 't', 'y']


if __name__ == '__main__':
    unittest.main()
