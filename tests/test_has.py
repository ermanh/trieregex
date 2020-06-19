# TODO: TO BE COMPLETED

from trieregex.trieregex import TrieRegEx as TRE
import unittest


class TestHas(unittest.TestCase):
    """Tests TrieRegEx().has()
    """

    def setUp(self):
        self.words = ['heart', 'healthy', 'pear', 'peach',
                      'lark', 'look', 'change']
        self.tre = TRE(*self.words)

    def test_has(self):
        non_existing = ['hear', 'ear', 'each', 'hang', 'ok', 'heal', 'pa']
        assert (
            all([self.tre.has(word) for word in self.words]) and
            not all([self.tre.has(word) for word in non_existing])
        )


if __name__ == '__main__':
    unittest.main()
