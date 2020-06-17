import re
from .memoize import memoize


class TrieRE():

    def __init__(self, *words: str):
        self._trie = {}
        self._ORDERED = ['0123456789', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
                         'abcdefghijklmnopqrstuvwxyz']
        for word in words:
            self.insert(word)

    def insert(self, *words: str):
        for word in words:
            trie = self._trie
            for char in word:
                if char not in trie:
                    trie[char] = {}
                trie = trie[char]
            trie['**'] = True

    def regex(self, boundaries=''):
        if type(boundaries) == str:
            return '{}{}{}'.format(
                boundaries, self.trace(self._trie), boundaries)
        elif type(boundaries) == list:
            if (len(boundaries) != 2 or any([type(b) != str for b in boundaries])):
                raise ValueError('list item passed in to arg `boundaries` \
                    must contain 2 strings')
            return '{}{}{}'.format(
                boundaries[0], self.trace(self._trie), boundaries[1])

    @memoize
    def trace(self, trie: dict):
        if len(trie) == 1:
            return self._trace_single(trie)
        return self._trace_multi(trie)

    def _trace_single(self, trie: dict):
        key = list(trie.keys())[0]

        if key == '**':
            return ''

        return re.escape(key) + self.trace(trie[key])

    def _trace_multi(self, trie: dict): 
        t = trie
        result = ''
        subseqs = []

        for key in t:
            if key != '**':
                seq = re.escape(key)
                seq += self.trace(t[key])
                subseqs += [seq]

        if len(subseqs) == 1:
            result = subseqs[0]
        elif len(subseqs) == len(''.join(subseqs)):
            result = '[{}]'.format(''.join(sorted(subseqs)))
        else:
            result = '(?:{})'.format('|'.join(subseqs))
        
        if len(result) > 1 and result[0] not in '([':
            result = '(?:{})'.format(result)

        if ('**' in t):  
            result += '?'
        
        return result
