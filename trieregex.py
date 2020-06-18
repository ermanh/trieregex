from re import escape


def memoizer(func):
    cache = {}
    def function_wrapper(*arg):
        stringed = str(arg[1:])  # exclude self
        if stringed in cache:
            return cache[stringed]
        cache[stringed] = func(*arg)
        return cache[stringed]
    return function_wrapper


class TrieRegEx():

    def __init__(self, *words: str) -> None:
        self._trie = {}
        self.initial_chars = set()
        self.final_chars = set()
        self.regex = ""
        self.add(*words)
        
    def add(self, *words: str) -> None:
        for word in words:
            if word != '':
                self.initial_chars.add(word[0])
                self.final_chars.add(word[-1])
                trie = self._trie
                for char in word:
                    if char not in trie:
                        trie[char] = {}
                    trie = trie[char]
                trie['**'] = True
        self.regex = self._compose_regex(self._trie)
    
    def remove(self, *words: str) -> None:
        for word in words:
            for i in range(len(word), 0, -1):
                if self.has(word[:i]):
                    node = self._trie
                    for j in range(i-1):
                        node = node[word[j]]
                    if '**' in node[word[i-1]] or len(node[word[i-1]]) == 0:
                        del node[word[i-1]]
                break
        
        self.regex = self._compose_regex(self._trie)
        self.initial_chars = set(self._trie.keys())
        self._get_final_chars(self._trie)

    def has(self, word: str) -> bool:
        trie = self._trie
        for char in word:
            if char in trie:
                trie = trie[char]
            else:
                return False
        return True

    @memoizer
    def _compose_regex(self, trie: dict) -> str:
        if len(trie) == 0:
            return ''
        
        elif len(trie) == 1:
            key = list(trie.keys())[0]
            if (key == '**'):
                return ''
            return escape(key) + self._compose_regex(trie[key])        
        
        else:
            seqs = [escape(k) + self._compose_regex(trie[k]) 
                    for k in trie if k != '**']
            seqs.sort(key=lambda x: (-len(x), x))

            if len(seqs) == 1:
                result = f'(?:{seqs[0]})' if (len(seqs[0]) > 1) else seqs[0]
            elif len(seqs) == len(''.join(seqs)):
                result = '[{}]'.format(''.join(seqs))
            else:
                result = '(?:{})'.format('|'.join(seqs))

            result = f'{result}?' if ('**' in trie) else result
            return result
    
    def _get_final_chars(self, trie: dict, reset :bool = True) -> None:
        if reset:
            self.final_chars = set()
        for char in trie:
            if char != '**':
                if '**' in trie[char]:
                    self.final_chars.add(char)
                self._get_final_chars(trie[char], reset=False)
