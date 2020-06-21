import unittest
from collections import defaultdict

from trieregex import TrieRegEx as TRE


class TestFinals(unittest.TestCase):
    """Tests for TrieRegEx().finals() and TrieRegEx()._finals
    """

    def setUp(self):
        self.words = ['all', 'the', 'stars', 'we', 'steal', 'from',
                      'night', 'sky', 'will', 'never', 'be', 'enough']
        self.tre = TRE(*self.words)

    def test_finals_variable(self):
        self.assertEqual(               # "hard" check
            self.tre._finals,
            {'l': 3, 'e': 3, 's': 1, 'm': 1, 't': 1, 'y': 1, 'r': 1, 'h': 1}
        )
        finals = defaultdict(int)       # "soft" check
        for w in self.words:
            finals[w[-1]] += 1
        self.assertEqual(self.tre._finals, finals)

    def test_finals(self):
        self.assertEqual(               # "hard" check
            self.tre.finals(),
            ['e', 'h', 'l', 'm', 'r', 's', 't', 'y']
        )
        self.assertEqual(               # "soft" check
            self.tre.finals(),
            sorted(list(set([w[-1] for w in self.words])))
        )

    def test_add_existing_word_will_not_change_counts(self):
        self.tre.add('the')
        self.assertEqual(
            self.tre._finals,
            {'l': 3, 'e': 3, 's': 1, 'm': 1, 't': 1, 'y': 1, 'r': 1, 'h': 1},
            "key-value pairs should remain the same"
        )

    def test_add_new_word_increase_frequency(self):
        self.tre.add('spotlights')
        self.assertEqual(
            self.tre._finals,
            {'l': 3, 'e': 3, 's': 2, 'm': 1, 't': 1, 'y': 1, 'r': 1, 'h': 1},
            "'s' should be set to 2 (up from 1)"
        )

    def test_add_new_final(self):
        self.tre.add('echoing')
        self.assertEqual(
            self.tre._finals,
            {'l': 3, 'e': 3, 's': 1, 'm': 1, 't': 1, 'y': 1, 'r': 1, 'h': 1,
             'g': 1},
            "new key 'g' should have a value of 1"
        )

    def test_add_new_escaped_char(self):
        self.tre.add('newline\n')
        self.assertEqual(
            self.tre._finals,
            {'l': 3, 'e': 3, 's': 1, 'm': 1, 't': 1, 'y': 1, 'r': 1, 'h': 1,
             '\n': 1},
            "new key '\n' should have a value of 1"
        )

    def test_add_new_special_char(self):
        self.tre.add('lå')
        self.assertEqual(
            self.tre._finals,
            {'l': 3, 'e': 3, 's': 1, 'm': 1, 't': 1, 'y': 1, 'r': 1, 'h': 1,
             'å': 1},
            "new key 'å' should have a value of 1"
        )

    def test_remove_word_lower_frequency(self):
        self.tre.remove('stars')
        self.assertEqual(
            self.tre._finals,
            {'l': 3, 'e': 3, 's': 0, 'm': 1, 't': 1, 'y': 1, 'r': 1, 'h': 1},
            "'s' should have a value of 0 (down from 1)"
        )

    def test_zero_frequency_should_not_appear(self):
        self.tre.remove('stars')
        self.assertEqual(
            self.tre.finals(),
            ['e', 'h', 'l', 'm', 'r', 't', 'y'],
            "'s' should not appear in the list"
        )

    def test_remove_nonexisting_final_with_zero_frequency(self):
        self.tre.remove('stars')  # set 's': 1 -> 't': 0
        self.tre.remove('spotlights')  # attempt removal of nonexisting word
        self.assertEqual(
            self.tre._finals,
            {'l': 3, 'e': 3, 's': 0, 'm': 1, 't': 1, 'y': 1, 'r': 1, 'h': 1},
            "'s' should still have a value of 0"
        )

    def test_remove_all(self):
        self.tre.remove(*self.words)
        self.assertEqual(
            self.tre._finals,
            {'l': 0, 'e': 0, 's': 0, 'm': 0, 't': 0, 'y': 0, 'r': 0, 'h': 0},
            "All keys should be set to a value of 0"
        )


if __name__ == '__main__':
    unittest.main()
