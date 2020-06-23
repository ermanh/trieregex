# trieregex

[**trieregex**](https://github.com/ermanh/trieregex/) create efficient [regular expressions](https://en.wikipedia.org/wiki/Regular_expression) (regexes) by storing a list of words in a [trie](https://en.wikipedia.org/wiki/Trie) structure, and translating the trie into a more compact pattern.

The speed performance of these trie-based regexes (e.g. `r'(?:under(?:stand|take|go)?)'`), compared to a straightforward regex union (i.e., `r'(?:understand|undertake|undergo)'`, becomes evident when using extremely large word lists and especially when more specific or complicated contexts are specified at the boundaries. 

This package is also implemented with [memoization](https://en.wikipedia.org/wiki/Memoization) to cut down on its own processing time.

## Installation

```shell
pip install trieregex
```

## Usage

```py
import re
from trieregex import TrieRegEx as TRE

words = ['lemon', 'lime', 'pomelo', 'orange', 'citron']
more_words = ['grapefruit', 'grape', 'tangerine', 'tangelo']

# Initialize class instance
tre = TRE()

# Add word(s)
tre = TRE(*words)  # word(s) can be added upon instance creation...
tre.add('kumquat')  # add one word (... or after)
tre.add(*more_words)  # add a list of words 

# Remove word(s)
tre.remove('citron')  # remove one word
tre.remove(*words)  # remove a list of words

# Check if a word exists in the trie
tre.has('citron')  # Returns: False
tre.has('tangerine')  # Returns: True

# Create regex pattern from the trie
tre.regex()  # Returns: '(?:tange(?:rine|lo)|grape(?:fruit)?|kumquat)'
pattern = re.compile(f'\\b{tre.regex()}\\b')  # OR rf'\b{tre.regex()}\b'
pattern  # Returns: re.compile('\\b(?:tange(?:rine|lo)|grape(?:fruit)?|kumquat)\\b')
pattern.findall("A kumquat is tastier than a loquat")  # Returns: ['kumquat']

# Inspect initial characters of the words in the trie
tre.initials()  # Returns: ['g', 'k', 't']

# Inspect final characters of the words in the trie
tre.finals()  # Returns: ['e', 'o', 't']
```

The last two methods may be useful for determining what boundaries to set (or avoid) in the final regex to be used (see below).

## Boundaries

**trieregex** does not include any default boundaries (such as `r'\b'`) in the pattern returned from its `TrieRegEx.regex()` method, and leaves it to the user to determine what is appropriate per use case. 

Consider a fictitious brand name, `!Citrus`, with an exclamation mark at the beginning:

```py
import re

string = 'I love !Citrus products!'
re.findall(r'\b(!Citrus)\b', string)  # Returns: []
```

The `re.findall()` call returns an empty list because the first `r'\b'` is not matched. `r'\b'` stands for the boundary between a word character and a non-word character, but the "boundary" between the exclamation mark and its preceding space character is that between two non-word characters, thus resulting in no matches.

An appropriate regex for catching `'!Citrus'` may be as follows, where the context before the exclamation mark can be either start-of-string (`r'^'`) or a non-word character (`r'[^\w]'`): 

```py
re.findall(r'(?:^|[^\w])(!Citrus)\b', string)  # Returns: ['!Citrus']
```

**trieregex** was designed to allow any pattern in its trie, not just normal words bound by space and punctuation, so that the user can define their own regex context, and have the option to avoid unwanted data normalization.

## Python version comptability

This package is only comptible with Python versions >=3.6 because of the use of [f-strings](https://www.python.org/dev/peps/pep-0498/) and type hints. Those using Python versions >=2.7 <3.6 may consider installing backports (such as [`future-fstrings`](https://pypi.org/project/future-fstrings/) and [`typing`](https://pypi.org/project/typing/)).
