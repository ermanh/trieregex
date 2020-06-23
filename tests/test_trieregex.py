import unittest

from trieregex import TrieRegEx as TRE


class TestTrieRegEx(unittest.TestCase):
    """Basic tests for each function in the trieregex.TrieRegEx class. 
    More in-depth tests are located in files bearing their function names.
    """

    def setUp(self):
        self.words = ['heart', 'healthy', 'pear', 'peach', 
                      'lark', 'look', 'change']
        self.tre = TRE(*self.words)

    def test_add(self):
        self.assertEqual(
            self.tre._trie, 
            {
                'c': {'h': {'a': {'n': {'g': {'e': {'**': {}}}}}}},
                'l': {'a': {'r': {'k': {'**': {}}}}, 
                    'o': {'o': {'k': {'**': {}}}}},
                'h': {'e': {'a': {'l': {'t': {'h': {'y': {'**': {}}}}},
                                'r': {'t': {'**': {}}}}}},
                'p': {'e': {'a': {'c': {'h': {'**': {}}}, 
                                'r': {'**': {}}}}}
            }, 
            "Words were not added to the trie (._trie) properly"
        )

    def test_remove(self):
        self.tre = TRE(*self.words)
        self.tre.remove('healthy', 'change')
        self.assertEqual(
            self.tre._trie,
            {
                'l': {'a': {'r': {'k': {'**': {}}}},
                    'o': {'o': {'k': {'**': {}}}}},
                'h': {'e': {'a': {'r': {'t': {'**': {}}}}}},
                'p': {'e': {'a': {'c': {'h': {'**': {}}},
                                'r': {'**': {}}}}}
            },
            "'healthy' and 'change' were not properly removed from the trie"
        )

    def test_has(self):
        for word in self.words:
            self.assertTrue(
                self.tre.has(word),
                f"'{word}' should be searchable in trie"
            )
        non_existing = ['hear', 'ear', 'each', 'hang', 'ok', 'heal', 'pa']
        for word in non_existing:
            self.assertFalse(
                self.tre.has(word),
                f"'{word}' should not be searchable in trie"
            )

    def test_initials_variable(self):
        self.assertEqual(
            self.tre._initials,
            {'c': 1, 'h': 2, 'l': 2, 'p': 2},
        )

    def test_initials(self):
        self.assertEqual(
            self.tre.initials(),
            ['c', 'h', 'l', 'p']
        )

    def test_finals_variable(self):
        self.assertEqual(
            self.tre._finals,
            {'e': 1, 'h': 1, 'k': 2, 'r': 1, 't': 1, 'y': 1}
        )

    def test_finals(self):
        self.assertEqual(
            self.tre.finals(),
            ['e', 'h', 'k', 'r', 't', 'y']
        )

    def test_regex(self):
        self.assertEqual(
            self.tre.regex(),
            "(?:hea(?:lthy|rt)|l(?:ark|ook)|pea(?:ch|r)|change)"
        )
