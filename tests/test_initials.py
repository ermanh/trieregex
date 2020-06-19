# TODO: TO BE COMPLETED

from trieregex.trieregex import TrieRegEx as TRE
import unittest


class TestInitials(unittest.TestCase):
    """Tests for TrieRegEx().initials() and TrieRegEx()._initials
    """

    def setUp(self):
        self.words = ['heart', 'healthy', 'pear', 'peach',
                      'lark', 'look', 'change']
        self.tre = TRE(*self.words)

    def test_initials_variable(self):
        assert self.tre._initials == {'c': 1, 'h': 2, 'l': 2, 'p': 2}

    def test_initials(self):
        assert self.tre.initials() == ['c', 'h', 'l', 'p']


if __name__ == '__main__':
    unittest.main()
