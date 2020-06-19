from trieregex import trieregex
import unittest


class TestTrieRegEx(unittest.TestCase):
    """Basic tests for each function in the trieregex.TrieRegEx class. 
    More in-depth tests are located in files bearing their function names.
    """

    def setUp(self):
        self.words = ['heart', 'healthy', 'pear', 'peach', 
                      'lark', 'look', 'change']
        self.tre = trieregex.TrieRegEx(*self.words)

    def test_add(self):
        assert self.tre._trie == {
            'c': {'h': {'a': {'n': {'g': {'e': {'**': {}}}}}}},
            'l': {'a': {'r': {'k': {'**': {}}}}, 
                  'o': {'o': {'k': {'**': {}}}}},
            'h': {'e': {'a': {'l': {'t': {'h': {'y': {'**': {}}}}},
                              'r': {'t': {'**': {}}}}}},
            'p': {'e': {'a': {'c': {'h': {'**': {}}}, 
                              'r': {'**': {}}}}}
        }

    def test_has(self):
        non_existing = ['hear', 'ear', 'each', 'hang', 'ok', 'heal', 'pa']
        assert (
            all([self.tre.has(word) for word in self.words]) and
            not all([self.tre.has(word) for word in non_existing])
        )

    def test_remove(self):
        self.tre.remove('healthy', 'change')
        assert self.tre._trie == {
            'l': {'a': {'r': {'k': {'**': {}}}},
                  'o': {'o': {'k': {'**': {}}}}},
            'h': {'e': {'a': {'r': {'t': {'**': {}}}}}},
            'p': {'e': {'a': {'c': {'h': {'**': {}}},
                              'r': {'**': {}}}}}
        }

    def test_initials_variable(self):
        assert self.tre._initials == {'c': 1, 'h': 2, 'l': 2, 'p': 2}

    def test_initials(self):
        assert self.tre.initials() == ['c', 'h', 'l', 'p']

    def test_finals_variable(self):
        assert (self.tre._finals == 
                {'e': 1, 'h': 1, 'k': 2, 'r': 1, 't': 1, 'y': 1})

    def test_finals(self):
        assert self.tre.finals() == ['e', 'h', 'k', 'r', 't', 'y']

    def test_regex(self):
        assert (self.tre.regex() ==
                "(?:hea(?:lthy|rt)|l(?:ark|ook)|pea(?:ch|r)|change)")


if __name__ == '__main__':
    unittest.main()
