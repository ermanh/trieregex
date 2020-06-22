# trieregex

**trieregex** composes time- and space-saving regular expressions (regexes) by storing a list of words as a [trie](https://en.wikipedia.org/wiki/Trie) structure, and translating it into a more compact pattern. Memoization has also been implemented to speed up internal methods.

## Usage

```py
from trieregex import TrieRegEx as TRE

words = ['lemon', 'lime', 'pomelo', 'orange', 'oro_blanco', 'citron']
more_words = ['grapefruit', 'grape', 'tangerine', 'tangelo']

# Initialize class instance
tre = TRE()

# Add word(s)
tre = TRE(*words)  # word(s) can be added upon instance creation
tre.add('kumquat')  # add one word
tre.add(*more_words)  # add a list of words 

# Remove word(s)
tre.remove('citron')  # remove one word
tre.remove(*words)  # remove a list of words

# Check if a word exists in the trie
tre.has('citron')  # Returns: False

# Create regex pattern from the trie
tre.regex()  # Returns: '(?:tange(?:rine|lo)|grape(?:fruit)?|kumquat)'

# Inspect initial characters of the words in the trie
tre.initials()  # Returns: ['g', 'k', 't']

# Inspect final characters of the words in the trie
tre.finals()  # Returns: ['e', 'o', 't']

```

### Inspecting initial and final characters for nuanced regex creation

Not all users necessarily want to normalize their words/patterns to exclude non-word characters (and in some cases may also want to match patterns surrounded by contexts that are not whitespace or punctuation). 

Consider a fictitious brand name called `!Citrus` with an obligatory exclamation mark at the beginning:

```py
import re

string = 'I love !Citrus products!'
re.findall(r'\b(!Citrus)\b', string)  # Returns: []
re.findall(r' (!Citrus)\b', string)  # Returns: ['!Citrus']
```

The first `re.findall()` call returns an empty list is because `r'\b'` stands for the boundary between a word character (all letters and digits, and the underscore) and a non-word character, but the boundary between the exclamation mark and its preceding space in `'I love !Citrus products!'` is that between two non-word characters, resulting in no match.

For this reason, **trieregex** does not include any default boundary conditions (such as `r'\b'`) in its `TrieRegEx.regex()` method, and leaves it to users to determine what is appropriate per their use case.
