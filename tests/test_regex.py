# TODO: TO BE COMPLETED
 
from trieregex.trieregex import TrieRegEx as TRE
import unittest
import re
from typing import List


class TestRegex(unittest.TestCase):
    """Tests for TrieRegEx().regex()
    """

    def setUp(self):
        self.tre = TRE()
        self.words = ['p', 'pe', 'pea', 'pear']

    def findall(self, string: str, boundary: str) -> List[str]:
        """Helper function. The TrieRegEx.regex() function is called here and 
        the result of regex matching is also returned here
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
    
    def test_added_word_reflected_in_new_regex_call(self):
        self.tre.add(*self.words)
        self.assertEqual(self.tre.regex(), 'p(?:e(?:ar?)?)?')
        
        self.tre.add('peak')
        self.assertEqual(self.tre.regex(), 'p(?:e(?:a[kr]?)?)?')


if __name__ == '__main__':
    unittest.main()
