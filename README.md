# trieregex

[![pypi Version](https://img.shields.io/pypi/v/trieregex.svg?logo=pypi&logoColor=white)](https://pypi.org/project/trieregex/)
[![python](https://img.shields.io/pypi/pyversions/trieregex.svg?logo=python&logoColor=white)](https://pypi.org/project/trieregex/)

[**trieregex**](https://github.com/ermanh/trieregex/) creates efficient regular expressions (regexes) by storing a list of words in a [trie](https://en.wikipedia.org/wiki/Trie) structure, and translating the trie into a more compact pattern.

The speed performance of a trie-based regex (e.g., `r'under(?:sta(?:nd|te)|take|go)'`) -- compared to a flat regex union (i.e., `r'(?:understand|understate|undertake|undergo)'`) -- becomes apparent when using extremely large word lists, and especially when more specific or complicated contexts are specified at the boundaries. The processing time of this package itself is also minimized with [memoization](https://en.wikipedia.org/wiki/Memoization).

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
tre = TRE(*words)  # word(s) can be added upon instance creation, or after
tre.add('kumquat')  # add one word
tre.add(*more_words)  # add a list of words 

# Remove word(s)
tre.remove('citron')  # remove one word
tre.remove(*words)  # remove a list of words

# Check if a word exists in the trie
tre.has('citron')  # Returns: False
tre.has('tangerine')  # Returns: True

# Create regex pattern from the trie
tre.regex()  # Returns: '(?:tange(?:rine|lo)|grape(?:fruit)?|kumquat)'

# Add boundary context and compile for matching
pattern = re.compile(f'\\b{tre.regex()}\\b')  # OR rf'\b{tre.regex()}\b'
pattern  # Returns: re.compile('\\b(?:tange(?:rine|lo)|grape(?:fruit)?|kumquat)\\b')
pattern.findall("A kumquat is tastier than a loquat")  # Returns: ['kumquat']

# Inspect unique initial characters in the trie
tre.initials()  # Returns: ['g', 'k', 't']

# Inspect unique final characters in the trie
tre.finals()  # Returns: ['e', 'o', 't']
```

The last two methods are intended for checking what boundary contexts are appropriate for the final regex for pattern matching (discussed below).

## (No) Boundaries

**trieregex** does not include any default boundaries (such as `r'\b'`) in the pattern returned from its `TrieRegEx.regex()` method, that way the user can determine what is appropriate for each particular use case. 

Consider a fictitious brand name `!Citrus` with an exclamation mark at the beginning, and trying to catch it in a target string by using `r'\b'` for its boundaries in the regex:

```py
string = 'I love !Citrus products!'
re.findall(r'\b(!Citrus)\b', string)  # Returns: []
```

The `re.findall()` call returns an empty list because the first `r'\b'` is not matched. While `r'\b'` stands for the boundary between a word character and a non-word character, the exclamation mark and its preceding space character are both non-word characters. 

An appropriate regex for catching `'!Citrus'` can be written as follows, where the context before the exclamation mark is either start-of-string (`r'^'`) or a non-word character (`r'[^\w]'`): 

```py
re.findall(r'(?:^|[^\w])(!Citrus)\b', string)  # Returns: ['!Citrus']
```

This package is designed to allow any pattern to be added to its trie, not just normal words bound by space and punctuation, so that the user can define their own boundaries in the regex, and have the option to leave the data unnormalized when desired.

## Python version comptability

Due to [f-strings](https://www.python.org/dev/peps/pep-0498/) and type hints, this package is only compatible with Python versions >=3.6. 

For Python versions >=2.7, <3.6, backports such as [`future-fstrings`](https://pypi.org/project/future-fstrings/) and [`typing`](https://pypi.org/project/typing/) are available.
