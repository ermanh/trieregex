# TODO: TO BE COMPLETED
 
from trieregex.trieregex import TrieRegEx as TRE
import unittest


class TestRegex(unittest.TestCase):
    """Tests for TrieRegEx().regex()
    """

    def setUp(self):
        self.words = ['heart', 'healthy', 'pear', 'peach',
                      'lark', 'look', 'change']
        self.tre = TRE(*self.words)

    def test_regex(self):
        assert (self.tre.regex() ==
                "(?:hea(?:lthy|rt)|l(?:ark|ook)|pea(?:ch|r)|change)")


if __name__ == '__main__':
    unittest.main()
