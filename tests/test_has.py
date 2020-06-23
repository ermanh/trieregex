import unittest

from trieregex import TrieRegEx as TRE


class TestHas(unittest.TestCase):
    """Tests for TrieRegEx.has()"""

    def setUp(self):
        self.words = ['heal', 'health', 'healthy', 'healthier', 'healthiest']
        self.tre = TRE(*self.words)

    def test_existing_longest_word(self):
        self.assertTrue(self.tre.has('healthiest'))

    def test_existing_substring_word(self):
        self.assertTrue(self.tre.has('health'))
        self.assertTrue(self.tre.has('heal'))

    def test_nonexisting(self):
        self.assertFalse(self.tre.has('wound'))
    
    def test_nonword_substring_of_existing_word(self):
        self.assertFalse(self.tre.has('he'))

    def test_nonexisting_after_removed(self):
        """Also a test of the TrieRegEx.remove() function
        """
        self.assertTrue(
            self.tre.has('healthy'), 
            "'healthy' must first exist in trie"
        )
        self.tre.remove('healthy')
        self.assertFalse(self.tre.has('healthy'))

    def test_existing_after_added(self):
        """Also a test of the TrieRegEx.add() function
        """
        self.assertFalse(
            self.tre.has('settled'),
            "'settled' must first NOT exist in trie"
        )
        self.tre.add('settled')
        self.assertTrue(self.tre.has('settled'))

    def test_empty_string(self):
        self.assertFalse(self.tre.has(''))
