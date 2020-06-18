from re import escape
from typing import Any, Callable, Dict, List
from collections import defaultdict


def memoize(func: Callable) -> Callable:
    cache = {}  # type: Dict[str: dict]

    def memoizer(*arg: Any) -> dict:
        stringed = str(arg[1:])
        if stringed in cache:
            return cache[stringed]
        cache[stringed] = func(*arg)
        return cache[stringed]
    
    return memoizer


class TrieRegEx():

    def __init__(self, *words: str) -> None:
        self._trie = {}  # type: Dict[str: dict]
        self._initials = defaultdict(int)
        self._finals = defaultdict(int)
        self.add(*words)

    def add(self, *words: str) -> None:
        for word in words:
            if word != '':
                self._initials[word[0]] += 1
                self._finals[word[-1]] += 1
                trie = self._trie
                for char in word:
                    if char not in trie:
                        trie[char] = {}
                    trie = trie[char]
                trie['**'] = {}

    def remove(self, *words: str) -> None:
        for word in words:
            for i in range(len(word), 0, -1):
                if self.has(word[:i]):
                    self._initials[word[-1]] -= 1
                    self._finals[word[-1]] -= 1
                    node = self._trie
                    for j in range(i-1):
                        node = node[word[j]]
                    if '**' in node[word[i-1]] or len(node[word[i-1]]) == 0:
                        del node[word[i-1]]
                break

    def has(self, word: str) -> bool:
        trie = self._trie
        for char in word:
            if char in trie:
                trie = trie[char]
            else:
                return False
        return True

    def initials(self) -> List[str]:
        return [key for key in self._initials if self._initials[key] > 0]

    def finals(self) -> List[str]:
        return [key for key in self._finals if self._finals[key] > 0]

    @memoize
    def regex(self, trie: dict = None, reset: bool = True) -> str:
        trie = self._trie if reset else trie

        if len(trie) == 0:
            return ''

        elif len(trie) == 1:
            key = list(trie.keys())[0]
            if key == '**':
                return ''
            return escape(key) + self.regex(trie[key], False)

        else:
            sequences = [escape(key) + self.regex(trie[key], False)
                         for key in trie if key != '**']
            sequences.sort(key=lambda x: (-len(x), x))  # for easier inspection

            if len(sequences) == 1:
                result = sequences[0]
                if len(sequences[0]) > 1:
                    result = '(?:{})'.format(result)
            elif len(sequences) == len(''.join(sequences)):
                result = '[{}]'.format(''.join(sequences))
            else:
                result = '(?:{})'.format('|'.join(sequences))

            if '**' in trie:
                result = result + '?'
            return result
