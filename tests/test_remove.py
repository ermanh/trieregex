from trieregex.trieregex import TrieRegEx as TRE
import unittest


class TestRemove(unittest.TestCase):
    """Tests for TrieRegEx().remove()
    """

    def setUp(self):
        self.words = ['heart', 'healthy', 'pear', 'peach',
                      'lark', 'look', 'change']
        self.incrementals = ['p', 'pe', 'pea', 'pear']
        self.tre = TRE(*self.words)
        self.tre_incr = TRE(*self.incrementals)

    def test_remove_one(self):
        self.tre.remove('healthy')
        self.assertEqual(           # "hard" check
            self.tre._trie,
            {
                'c': {'h': {'a': {'n': {'g': {'e': {'**': {}}}}}}},
                'l': {'a': {'r': {'k': {'**': {}}}},
                    'o': {'o': {'k': {'**': {}}}}},
                'h': {'e': {'a': {'r': {'t': {'**': {}}}}}},
                'p': {'e': {'a': {'c': {'h': {'**': {}}},
                                'r': {'**': {}}}}}
            },
            "'healthy' should have been removed (hard check)"
        )
        self.assertEqual(           # "soft" check
            self.tre._trie,
            TRE(*[w for w in self.words if w != 'healthy'])._trie,
            "'healthy' should have been removed (soft check)"
        )

    def test_remove_two(self):
        self.tre.remove('healthy', 'change')
        self.assertEqual(           # "hard" check
            self.tre._trie,
            {
                'l': {'a': {'r': {'k': {'**': {}}}},
                    'o': {'o': {'k': {'**': {}}}}},
                'h': {'e': {'a': {'r': {'t': {'**': {}}}}}},
                'p': {'e': {'a': {'c': {'h': {'**': {}}},
                                'r': {'**': {}}}}}
            },
            "'healthy' and 'change' should have been removed (hard check)"
        )
        self.assertEqual(           # "soft" check
            self.tre._trie,
            TRE('lark', 'look', 'heart', 'peach', 'pear')._trie,
            "'healthy' and 'change' should have been removed (soft check)"
        )

    def test_remove_all(self):
        self.tre.remove(*self.words)
        self.assertEqual(self.tre._trie, {}, 'Trie should be empty')

    def test_remove_second_time(self):
        self.tre.remove(*self.words)
        self.tre.add(*self.words)
        self.tre.remove(*[w for w in self.words if w != 'pear'])
        self.assertEqual(           # "hard" check
            self.tre._trie,
            {'p': {'e': {'a': {'r': {'**': {}}}}}},
            "Only 'pear' should be in trie (hard check)"
        )
        self.assertEqual(           # "soft" check
            self.tre._trie, 
            TRE('pear')._trie,
            "Only 'pear' should be in trie (soft check)"
        )  
    
    def test_remove_first_in_incremental_words(self):
        self.tre_incr.remove('p')
        self.assertEqual(           # "hard" check
            self.tre_incr._trie,
            {'p': {'e': {'**': {},
                         'a': {'**': {},
                               'r': {'**': {}}}}}},
            "'p' should have been removed (hard check)"
        )
        self.assertEqual(           # "soft" check
            self.tre_incr._trie,
            TRE('pe', 'pea', 'pear')._trie,
            "'p' should have been removed (soft check)"
        )

    def test_remove_middle_in_incremental_words(self):
        self.tre_incr.remove('pea')
        self.assertEqual(           # "hard" check
            self.tre_incr._trie,
            {'p': {'**': {},
                   'e': {'**': {},
                         'a': {'r': {'**': {}}}}}},
            "'pea' should have been removed (hard check)"
        )
        self.assertEqual(           # "soft" check
            self.tre_incr._trie,
            TRE('p', 'pe', 'pear')._trie,
            "'pea' should have been removed (soft check)"
        )

    def test_remove_last_in_incremental_words(self):
        self.tre_incr.remove('pear')
        self.assertEqual(           # "hard" check
            self.tre_incr._trie,
            {'p': {'**': {},
                   'e': {'**': {},
                         'a': {'**': {}}}}},
            "'pear' should have been removed (hard check)"
        )
        self.assertEqual(           # "soft" check
            self.tre_incr._trie,
            TRE('p', 'pe', 'pea')._trie,
            "'pear' should have been removed (soft check)"
        )

    def test_remove_one_in_multiple_shared(self):
        tre = TRE('brander', 'brandy', 'brandless')
        tre.remove('brandless')
        self.assertEqual(           # "hard" check
            tre._trie,
            {'b': {'r': {'a': {'n': {'d': {'y': {'**': {}},
                                           'e': {'r': {'**': {}}}}}}}}},
            "'brandless' should have been removed (hard check)"
        )
        self.assertEqual(           # "soft" check
            tre._trie,
            TRE('brander', 'brandy')._trie,
            "'brandless' should have been removed (soft check)"
        )

    def test_remove_nonexisting_word(self):
        self.tre_incr.remove('riffraff')
        self.assertEqual(           # "hard" check
            self.tre_incr._trie,
            {'p': {'**': {},
                   'e': {'**': {},
                         'a': {'**': {},
                               'r': {'**': {}}}}}},
            "Trie should remain the same (hard check)"
        )
        self.assertEqual(           # "soft" check
            self.tre_incr._trie,
            TRE(*self.incrementals)._trie,
            "Trie should remain the same (soft check)"
        )


if __name__ == '__main__':
    unittest.main()
