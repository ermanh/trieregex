from trieregex.trieregex import TrieRegEx as TRE
import unittest
from collections import defaultdict


class TestInitials(unittest.TestCase):
    """Tests for TrieRegEx().initials() and TrieRegEx()._initials
    """

    def setUp(self):
        self.words = ['all', 'the', 'stars', 'we', 'steal', 'from',
                      'night', 'sky', 'will', 'never', 'be', 'enough']
        self.tre = TRE(*self.words)

    def test_initials_variable(self):
        self.assertEqual(               # "hard" check
            self.tre._initials,
            {'a': 1, 't': 1, 's': 3, 'w': 2, 'f': 1, 'n': 2, 'b': 1, 'e': 1}
        )
        initials = defaultdict(int)     # "soft" check
        for w in self.words:
            initials[w[0]] += 1
        self.assertEqual(self.tre._initials, initials)

    def test_initials(self):
        self.assertEqual(               # "hard" check
            self.tre.initials(), 
            ['a', 'b', 'e', 'f', 'n', 's', 't', 'w']
        )
        self.assertEqual(               # "soft" check
            self.tre.initials(),
            sorted(list(set([w[0] for w in self.words])))
        )

    def test_add_existing_word_will_not_change_counts(self):
        self.tre.add('the')
        self.assertEqual(
            self.tre._initials,
            {'a': 1, 't': 1, 's': 3, 'w': 2, 'f': 1, 'n': 2, 'b': 1, 'e': 1},
            "key-value pairs should remain the same"
        )
    
    def test_add_new_word_increase_frequency(self):
        self.tre.add('spotlights')
        self.assertEqual(
            self.tre._initials,
            {'a': 1, 't': 1, 's': 4, 'w': 2, 'f': 1, 'n': 2, 'b': 1, 'e': 1},
            "'s' should be set to 4 (up from 3)"
        )
    
    def test_add_new_initial(self):
        self.tre.add('dream')
        self.assertEqual(
            self.tre._initials,
            {'a': 1, 't': 1, 's': 3, 'w': 2, 'f': 1, 'n': 2, 'b': 1, 'e': 1,
             'd': 1},
            "new key 'd' should have a value of 1"
        )
    
    def test_add_new_escaped_char(self):
        self.tre.add('\nnewline')
        self.assertEqual(
            self.tre._initials,
            {'a': 1, 't': 1, 's': 3, 'w': 2, 'f': 1, 'n': 2, 'b': 1, 'e': 1,
             '\n': 1},
            "new key '\n' should have a value of 1"
        )

    def test_add_new_special_char(self):
        self.tre.add('åll')
        self.assertEqual(
            self.tre._initials,
            {'a': 1, 't': 1, 's': 3, 'w': 2, 'f': 1, 'n': 2, 'b': 1, 'e': 1,
             'å': 1},
            "new key 'å' should have a value of 1"
    )

    def test_remove_word_lower_frequency(self):
        self.tre.remove('the')
        self.assertEqual(
            self.tre._initials,
            {'a': 1, 't': 0, 's': 3, 'w': 2, 'f': 1, 'n': 2, 'b': 1, 'e': 1},
            "'t' should have a value of 0 (down from 1)"
        )

    def test_zero_frequency_should_not_appear_in_function_call(self):
        self.tre.remove('the')
        self.assertEqual(
            self.tre.initials(),
            ['a', 'b', 'e', 'f', 'n', 's', 'w'],
            "'t' should not appear in the list"
        )

    def test_remove_nonexisting_word_initial_with_zero_frequency(self):
        self.tre.remove('the')  # set 't': 1 -> 't': 0
        self.tre.remove('table')  # attempt removal of nonexisting word
        self.assertEqual(
            self.tre._initials,
            {'a': 1, 't': 0, 's': 3, 'w': 2, 'f': 1, 'n': 2, 'b': 1, 'e': 1},
            "'t' should still have a value of 0"
        )

    def test_remove_all(self):
        self.tre.remove(*self.words)  
        self.assertEqual(
            self.tre._initials,
            {'a': 0, 't': 0, 's': 0, 'w': 0, 'f': 0, 'n': 0, 'b': 0, 'e': 0},
            "All keys should be set to a value of 0"
        )


if __name__ == '__main__':
    unittest.main()
