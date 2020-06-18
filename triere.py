from re import escape
from triere.memoizer import memoizer
from typing import Callable

class TrieRE():

    def __init__(self, *words: str):
        self._trie = {}
        self._trie_changed = False 
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

    def has(self, word: str) -> bool:
        trie = self._trie
        for char in word:
            if char in trie:
                trie = trie[char]
            else:
                return False
        return True

    def boundary_helper(self):
        """
        Helper function(s) for the `boundaries` arg in self.regex()
        - for validating/error-checking `boundaries` arg passed in
        - alert whether there are chars in the first level nodes or leaves 
          in the trie that are incompatible with r'\b'
        """
        pass

    def regex(self, boundaries='') -> str:
        result = ''
        if type(boundaries) == str:
            result = '{}{}{}'.format(
                boundaries, self.trace(self._trie), boundaries)
        elif type(boundaries) == list:
            if (len(boundaries) != 2 or any([type(b) != str for b in boundaries])):
                raise ValueError('list item passed in to arg `boundaries` \
                    must contain 2 strings')
            result = '{}{}{}'.format(
                boundaries[0], self.trace(self._trie), boundaries[1])
        return result

    @memoizer
    def trace(self, trie: dict) -> str:
        if len(trie) == 0:
            return ''
        
        elif len(trie) == 1:
            key = list(trie.keys())[0]
            return '' if (key == '**') else escape(key) + self.trace(trie[key])        
        
        else:
            keys = [key for key in trie if key != '**']
            subseqs = [escape(key) + self.trace(trie[key]) for key in keys]
            subseqs.sort()
            subseqs.sort(key=lambda x: len(x), reverse=True)

            if len(subseqs) == 1:
                result = subseqs[0]
                result = f'(?:{result})' if len(result) > 1 else result
            elif len(subseqs) == len(''.join(subseqs)):
                result = '[{}]'.format(''.join(subseqs))
            else:
                result = '(?:{})'.format('|'.join(subseqs))

            result = f'{result}?' if ('**' in trie) else result
            return result
