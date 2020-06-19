# TODO: TO BE COMPLETED

from trieregex.trieregex import TrieRegEx as TRE
import unittest


class TestTrieRegEx(unittest.TestCase):
    """Tests for TrieRegEx().add()
    """

    def setUp(self):
        self.words = ['heart', 'healthy', 'pear', 'peach',
                      'lark', 'look', 'change']
        self.tre = TRE(*self.words)

    def test_base_case(self):
        assert self.tre._trie == {
            'c': {'h': {'a': {'n': {'g': {'e': {'**': {}}}}}}},
            'l': {'a': {'r': {'k': {'**': {}}}},
                  'o': {'o': {'k': {'**': {}}}}},
            'h': {'e': {'a': {'l': {'t': {'h': {'y': {'**': {}}}}},
                              'r': {'t': {'**': {}}}}}},
            'p': {'e': {'a': {'c': {'h': {'**': {}}},
                              'r': {'**': {}}}}}
        }
    
    def test_add(self):
        pass


if __name__ == '__main__':
    unittest.main()
