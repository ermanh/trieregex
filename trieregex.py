from re import escape
from collections import defaultdict
from typing import Dict, List
from functools import partial


class Memoizer:

    def __init__(self, func):
        self.func = func
        self.cache = {}

    def __call__(self, *args):
        stringed = str(args)
        if stringed not in self.cache:
            self.cache[stringed] = self.func(*args)
        return self.cache[stringed]

    def __get__(self, obj, objtype):
          fn = partial(self.__call__, obj)
          fn.clear_cache = self._clear_cache
          return fn

    def _clear_cache(self):
        self.cache.clear()


class TrieRegEx():

    def __init__(self, *words: str) -> None:
        self._trie = {}  # type: Dict[str: dict]
        self._initials = defaultdict(int)
        self._finals = defaultdict(int)
        self.add(*words)
    
    @Memoizer
    def add(self, *words: str) -> None:
        self.regex.clear_cache()  # better performance to clear just once
        for word in words:
            if word != '' and not self.has(word):
                self.adjust_initials_finals(word)
                trie = self._trie
                for char in word:
                    if char not in trie:
                        trie[char] = {}
                    trie = trie[char]
                trie['**'] = {}
        # self.add.reset()

    def adjust_initials_finals(self, word, increase=True):
        if increase:
            self._initials[word[0]] += 1
            self._finals[word[-1]] += 1
        else:
            self._initials[word[0]] -= 1
            self._finals[word[-1]] -= 1

    def remove(self, *words: str) -> None:
        self.add.clear_cache()    # better performance to clear just once
        self.regex.clear_cache()
        for word in words:
            remove_word = False
            for i in range(len(word), 0, -1):
                is_end = i == len(word)
                if is_end and self.has(word[:i]):
                    remove_word = True
                    self.adjust_initials_finals(word, increase=False)
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

    def has(self, word: str) -> bool:
        trie = self._trie
        for char in word:
            if char in trie:
                trie = trie[char]
            else:
                return False
        if '**' not in trie:
            return False
        return True

    def initials(self) -> List[str]:
        result = [key for key in self._initials if self._initials[key] > 0]
        return sorted(result)

    def finals(self) -> List[str]:
        result = [key for key in self._finals if self._finals[key] > 0]
        return sorted(result)

    @Memoizer
    def regex(self, trie: dict = None, reset: bool = True) -> str:
        if reset:
            trie = self._trie

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
