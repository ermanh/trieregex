from trieregex.trieregex import TrieRegEx as TRE
import unittest


class TestTrieRegEx(unittest.TestCase):
    """Tests for TrieRegEx().add()
    """

    def setUp(self):
        self.words = ['heart', 'healthy', 'pear', 'peach',
                      'lark', 'look', 'change']
        self.tre = TRE()

    def test_one_word(self):
        self.tre.add('pear')
        self.assertEqual(
            self.tre._trie,
            {'p': {'e': {'a': {'r': {'**': {}}}}}}
        )

    def test_two_words_together(self):
        self.tre.add('pear', 'peach')
        self.assertEqual(
            self.tre._trie,
            {'p': {'e': {'a': {'c': {'h': {'**': {}}},
                               'r': {'**': {}}}}}}
        )

    def test_two_words_added_separately(self):
        self.tre.add('pear')
        self.tre.add('peach')
        self.assertEqual(
            self.tre._trie,
            {'p': {'e': {'a': {'c': {'h': {'**': {}}},
                               'r': {'**': {}}}}}}
        )

    def test_two_words_different_initials(self):
        self.tre.add('pear', 'heart')
        self.assertEqual(
            self.tre._trie,
            {
                'p': {'e': {'a': {'r': {'**': {}}}}},
                'h': {'e': {'a': {'r': {'t': {'**': {}}}}}}
            }
        )

    def test_three_words_different_prefix_length_matching(self):
        self.tre.add('pear', 'peach', 'perth')
        self.assertEqual(
            self.tre._trie,
            {
                'p': {'e': {'r': {'t': {'h': {'**': {}}}},
                            'a': {'r': {'**': {}},
                                  'c': {'h': {'**': {}}}}}}
            }
        )

    def test_add_empty_string_changes_nothing(self):
        self.tre.add('')
        self.assertEqual(
            self.tre._trie, 
            {}, 
            'Add empty string to empty trie should yield empty trie'
        )
        
        self.tre.add('pear')
        pear_trie = self.tre._trie
        self.tre.add('')
        self.assertEqual(
            pear_trie,
            self.tre._trie,
            'Add empty string to populated trie should yield same trie'
        )

    def test_add_nonword_chars(self):
        self.tre.add('!wow', 'ask?')
        self.assertEqual(
            self.tre._trie,
            {
                '!': {'w': {'o': {'w': {'**': {}}}}},
                'a': {'s': {'k': {'?': {'**': {}}}}}
            }
        )

    def test_add_special_chars(self):
        self.tre.add('\nline', '\ttab', ' space')
        self.assertEqual(
            self.tre._trie,
            {
                '\n': {'l': {'i': {'n': {'e': {'**': {}}}}}},
                '\t': {'t': {'a': {'b': {'**': {}}}}},
                ' ': {'s': {'p': {'a': {'c': {'e': {'**': {}}}}}}}
            }
        )

    def test_add_incremental_words(self):
        self.tre.add('a', 'an', 'ana', 'anat', 'anath', 'anathe', 'anathem',
            'anathema')
        self.assertEqual(
            self.tre._trie,
            {
                'a': {'**': {},
                      'n': {'**': {},
                            'a': {'**': {},
                                  't': {'**': {},
                                        'h': {'**': {},
                                              'e': {'**': {},
                                                    'm': {'**': {},
                                                          'a': {'**': {}}
                                                    }}}}}}}
            }
        )


if __name__ == '__main__':
    unittest.main()
