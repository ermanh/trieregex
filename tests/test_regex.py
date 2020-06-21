import re
from typing import List
import unittest

from trieregex import TrieRegEx as TRE


class TestRegex(unittest.TestCase):
    """Tests for TrieRegEx().regex()
    """

    def setUp(self):
        self.tre = TRE()
        self.words = ['p', 'pe', 'pea', 'pear']
        self.more_words = [
            'orange', 'kumquat', 'tangerine', 'mandarin', 'pomelo', 'yuzu', 
            'grapefruit', 'lemon', 'lime', 'bergamot', 'citron', 'clementine', 
            'satsuma', 'tangelo', 'mikan', 'tangor',
            'mint', 'peppermint', 'spearmint', 'basil', 'cilantro',
            'coriander', 'chives', 'parsley', 'oregano', 'rosemary', 'thyme', 
            'scallion', 'ginger', 'garlic', 'onion', 'galangal'
        ]

    def findall(self, string: str, boundary: str) -> List[str]:
        """Helper function. The TrieRegEx.regex() function is called here and 
        the result of regex matching is returned
        """
        pattern = re.compile(f'{boundary}{self.tre.regex()}{boundary}')
        return sorted(pattern.findall(string))

    def test_match_all_incrementals(self):
        self.tre.add(*self.words)
        found = self.findall(' '.join(self.words), '\\b')

        self.assertEqual(found, sorted(self.words))

    def test_does_not_match_larger_string(self):
        self.tre.add('p')
        found = self.findall('pe', '\\b')

        self.assertEqual(found, [])

    def test_does_not_match_substring(self):
        my_words = self.words[1:]  # leave out 'p'
        self.tre.add(*my_words)
        found = self.findall(' '.join(self.words), '\\b')

        self.assertEqual(
            found, 
            sorted(my_words), 
            "'p' should not be captured"
        )

    def test_empty_trie_returns_empty_string_regex(self):
        self.assertEqual(self.tre.regex(), '')
    
    def test_match_all_words(self):
        self.tre.add(*self.more_words)
        found = self.findall(' '.join(sorted(self.more_words)), '\\b')
        self.assertEqual(found, sorted(self.more_words))

    def test_match_all_words_surrounded_by_spaces(self):
        words = sorted(self.more_words)
        self.tre.add(*words)
        found = re.findall(f"(?<= ){'|'.join(words)}(?= )", ' '.join(words))
        self.assertEqual(
            found,
            words[1:-1],
            'First and last item in sorted words list should not be matched.'
        )

    def test_added_word_reflected_in_new_regex_call(self):
        self.tre.add(*self.words)
        self.assertEqual(
            self.tre.regex(), 
            'p(?:e(?:ar?)?)?', 
            'Setup for the real test in the next assertEqual'
        )
        self.tre.add('peak')
        self.assertEqual(self.tre.regex(), 'p(?:e(?:a[kr]?)?)?')

    def test_removed_word_reflected_in_new_regex_call(self):
        expanded = self.words + ['peak']
        self.tre.add(*expanded)
        self.assertEqual(
            self.tre.regex(), 
            'p(?:e(?:a[kr]?)?)?',
            'Setup for the real test in the next assertEqual'
        )
        self.tre.remove('peak')
        self.assertEqual(self.tre.regex(), 'p(?:e(?:ar?)?)?')

    def test_multiple_adding_removing_reflected(self):
        """This test also checks that the memoizer cache clearing is called
        in the right places so that .add(), .remove(), and .regex() run
        correctly as expected
        """
        self.tre.add(*self.words)
        self.assertEqual(
            self.tre.regex(),
            'p(?:e(?:ar?)?)?',
            'Setup for the real test in the next assertEqual'
        )
        self.tre.add('peak')
        self.tre.remove('pe')
        self.tre.add('river')
        self.tre.add('rich')
        self.tre.remove('pea')
        self.tre.remove('peak')
        self.assertEqual(
            self.tre.regex(),
            '(?:ri(?:ver|ch)|p(?:ear)?)'
        )
        self.tre.add('peak')
        self.tre.remove('peak')
        self.tre.remove('pear')
        self.tre.add(*self.words)
        self.assertEqual(
            self.tre.regex(),
            '(?:p(?:e(?:ar?)?)?|ri(?:ver|ch))'
        )


if __name__ == '__main__':
    unittest.main()
