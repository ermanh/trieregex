# TODO: TO BE COMPLETED

from trieregex.trieregex import TrieRegEx as TRE
import unittest


class TestRemove(unittest.TestCase):
    """Tests for TrieRegEx().remove()
    """

    def setUp(self):
        self.words = ['heart', 'healthy', 'pear', 'peach',
                      'lark', 'look', 'change']
        self.tre = TRE(*self.words)

    def test_remove(self):
        self.tre.remove('healthy', 'change')
        assert self.tre._trie == {
            'l': {'a': {'r': {'k': {'**': {}}}},
                  'o': {'o': {'k': {'**': {}}}}},
            'h': {'e': {'a': {'r': {'t': {'**': {}}}}}},
            'p': {'e': {'a': {'c': {'h': {'**': {}}},
                              'r': {'**': {}}}}}
        }

if __name__ == '__main__':
    unittest.main()
