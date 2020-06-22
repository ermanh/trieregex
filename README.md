# trieregex

[**trieregex**](https://github.com/ermanh/trieregex/) composes efficient [regular expressions](https://en.wikipedia.org/wiki/Regular_expression) (regexes) by storing a list of words in a [trie](https://en.wikipedia.org/wiki/Trie) structure, and translating the trie into a more compact pattern.

The speed performance of these trie-based regex patterns (e.g. `r'(?:under(?:statement|stand|take|go)?)'`), compared to a straightforward regex union (i.e., `r'(?:understatement|understand|undertake|undergo)'`, becomes evident when using extremely large word lists and _especially_ when more specific or complicated contexts are specified at the boundaries. 

This package is implemented with [memoization](https://en.wikipedia.org/wiki/Memoization) to further cut down on processing time.

## Usage

```py
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

# Inspect initial characters of the words in the trie
tre.initials()  # Returns: ['g', 'k', 't']

# Inspect final characters of the words in the trie
tre.finals()  # Returns: ['e', 'o', 't']

```

### Boundary agnostic

**trieregex** does not include any default boundaries (such as `r'\b'`) in the pattern returned from its `TrieRegEx.regex()` method, and leaves it to the user to determine what is appropriate per use case. This ensures the tool stays versatile, rather than force users to normalize everything to fit the tool.

Consider a fictitious brand name called `!Citrus` with an obligatory exclamation mark at the beginning:

```py
import re

string = 'I love !Citrus products!'
re.findall(r'\b(!Citrus)\b', string)  # Returns: []
```

The `re.findall()` call returns an empty list because the first `r'\b'` is not matched. `r'\b'` stands for the boundary between a word character (all letters and digits plus the underscore) and a non-word character, but the "boundary" between the exclamation mark and its preceding space character is that between two non-word characters, thus resulting in no match.

A more desirable regex for the above example might be as follows, where the context before the exclamation mark can be either start-of-string or a non-word character: 

```py
re.findall(r'(?:^|[^\w])(!Citrus)\b', string)  # Returns: ['!Citrus']
```

**trieregex** therefore allows the inclusion of any pattern in its trie, not just natural language words normally bounded by space or punctuation. The regex patterns it produces can similarly be expanded for seaching/matching patterns in any context within the string.
