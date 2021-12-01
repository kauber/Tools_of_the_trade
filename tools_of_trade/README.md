# Fuzzy Matcher

Often confronted with the need to perform fuzzy matching, be it for duplicate records removal
or entity resolution tasks, I build a simple helper package to speed up and simplify part of the job.

The package wraps together a set of helper functions that can come handy when having to perform fuzzy matching.

First, let's import the package:

```
from fuzzy_matcher.fuzzy_tools import FuzzyMatcher
```

We can the initialize a fuzzy match session:

```
fuzzy_match = FuzzyMatcher(column1=df.column1,
                           column2=df.column2,
                           matcher=fuzz.partial_ratio,
                           first_chars=0,
                           similarity_threshold=60)
```

We pass the columns we want to match using fuzzy string matching, we specify which
function from the fuzzywuzzy package we want: default will be fuzz.ratio, but we can pass fuzz.partial_ratio or fuzz.token_ratio.
Documentation can be found [here](https://pypi.org/project/fuzzywuzzy/).

The *first char* parameter specifies whether we want to only match strings starting with a n amount
of overlapping characters. This feature might be useful if we have a very large number of matches: in fact, let's consider that if
we have a list of n strings to match with a list of m strings, the total matches the algorithm will perform is n * m, i.e. matching 2 lists of  1000 strings
with 1000 strings will require 1 million matches. 
Only matching strings that start with the same character (n = 1) will save a lot of 
potentially useless matches, and reduce the computational load.

The *similarity threshold* parameter specifies which matches we will keep for inspection. The parameter is passed to the
*post_processor* method after the fuzzy matching. Setting the threshold to 60 means we will only keep matches that returned a similarity score of
60 or more.





