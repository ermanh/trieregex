from re import escape
from collections import defaultdict
from typing import Any, Callable, Dict, List


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
            remove_word = False
            for i in range(len(word), 0, -1):
                is_end = i == len(word)
                if is_end and self.has(word[:i]):  #, removal_check=True):
                    remove_word = True
                    self._initials[word[-1]] -= 1
                    self._finals[word[-1]] -= 1
                if remove_word:
                    node = self._trie
                    for j in range(i-1):
                        node = node[word[j]]
                    penult_node = node[word[i-1]]
                    if is_end:
                        if '**' in penult_node:
                            if len(penult_node) == 1:
                                del node[word[i-1]]
                            else:
                                del penult_node['**']
                    else:
                        if len(penult_node) == 0:
                            del node[word[i-1]]
                else:
                    break

    def has(self, word: str) -> bool:  #, removal_check: bool = False) -> bool:
        trie = self._trie
        for char in word:
            if char in trie:
                trie = trie[char]
            else:
                return False
        # if not removal_check:
        if '**' not in trie:
            return False
        return True

    def initials(self) -> List[str]:
        result = [key for key in self._initials if self._initials[key] > 0]
        return sorted(result)

    def finals(self) -> List[str]:
        result = [key for key in self._finals if self._finals[key] > 0]
        return sorted(result)

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
