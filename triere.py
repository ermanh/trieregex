import re

import collections
import functools

class memoized(object):
   '''Decorator. Caches a function's return value each time it is called.
   If called later with the same arguments, the cached value is returned
   (not reevaluated).
   '''
   def __init__(self, func):
      self.func = func
      self.cache = {}
   def __call__(self, *args):
      args2 = str(args)
      if not isinstance(args, collections.Hashable):
         # uncacheable. a list, for instance.
         # better to not cache than blow up.
         return self.func(*args)
      if args2 in self.cache:
         return self.cache[args2]
      else:
         value = self.func(*args)
         self.cache[args2] = value
         return value
   def __repr__(self):
      '''Return the function's docstring.'''
      return self.func.__doc__
   def __get__(self, obj, objtype):
      '''Support instance methods.'''
      return functools.partial(self.__call__, obj)

class Trieify_Regex():

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

    def regex(self, boundary=''):
        if type(boundary) == str:
            return '{}{}{}'.format(boundary, self.trace(self._trie), boundary)
        elif type(boundary) == list:
            if len(boundary) != 2 or any([type(b) != str for b in boundary]):
                raise ValueError('list item passed in to arg `boundary` \
                    must contain 2 strings')
            return '{}{}{}'.format(
                boundary[0], self.trace(self._trie), boundary[1])

    @memoized
    def trace(self, trie: dict, seq: str=''):
        if type(trie) == bool:
            return ''
        if len(trie) == 0:
            return ''
        if len(trie) == 1:
            seq += self._trace_single(trie, seq)
        else:
            seq += self._trace_multi(trie, seq)
        return seq

    def _trace_single(self, trie: dict, seq: str):
        t = trie
        key = list(t.keys())[0]

        if key == '**':
            return seq
        else:
            if len(t[key]) == 1:
                t = t[key]
                seq += re.escape(key)
                return self._trace_single(t, seq)
            else:
                return self._trace_multi(t, seq)

    def _trace_multi(self, trie: dict, preseq: str):
        t = trie
        subseqs = []

        for key in t:
            if key != '**':
                seq = re.escape(key)
                seq += self.trace(t[key])
                subseqs += [seq]

        # first sort alphabetically
        # then sort by length (ignoring group/set/or special chars)
        subseqs.sort()
        # subseqs.sort(key=lambda x: len(x), reverse=True)
        subseqs.sort(key=lambda x: len(re.findall('\(\?:|[\[\|\?\+]', x)))

        are_single_chars = [len(i) == 1 for i in subseqs]
        if all(are_single_chars):
            joined = ''.join(subseqs)
            if len(joined) == 1:
                return preseq + joined[0] + '?' if '**' in t else joined[0]
            else:
                if any([joined in s for s in self._ORDERED]):
                    return '{}[{}-{}]'.format(preseq, joined[0], joined[-1])
                else:
                    return '{}[{}]'.format(preseq, joined)
        else:
            if sum(are_single_chars) > 1:
                ones = [s for s in subseqs if len(s) == 1]
                multis = [s for s in subseqs if len(s) > 1]
                seq = '(?:{}|[{}])'.format('|'.join(multis), ''.join(ones))
            else:
                seq = '(?:{})'.format('|'.join(subseqs))
            seq = seq + '?' if "**" in t else seq
            return preseq + seq


'''
timeit('m.trace(m.trie, "")', setup="import my_trie_regex as m", number=1000)
'''
