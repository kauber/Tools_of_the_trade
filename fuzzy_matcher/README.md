# Fuzzy Matching in Python made eas(ier)

Often confronted with the need to perform fuzzy matching, be it for removing duplicate records or
doing entity resolution, I built a simple helper package to speed up and simplify part of the job.

The package is a wrapper around the fuzzywuzzy package, and puts together a set of helper methods that can come handy when performing fuzzy matching.
The three main methods after initializing an instance of the fuzzy matcher class are:
<ol>
  <li> string_normalizer </li>
  <li> fuzzy_matcher </li>
  <li> post_processor </li>
</ol>

The *string_normalizer* implements some transformations on the strings we want to match, such as transforming to lower case,
removing non alpha-numeric characters, or removing substrings we don't need; an example might be removing
all instances of __limited__ or __ltd__ from company names. This is because limited (or ltd) might affect fuzzy matching if the naming
convention differs between lists, so *dummy transports ltd* and *dummy transports limited* will produce a lower similarity
score, despite being most likely the same company.

The *fuzzy_matcher* method is the method performing the fuzzy matching.

The *post_processor* method performs some operations on the output of the fuzzy matcher to tidy up the results.

### Demo

First, let's import the package:

```
from fuzzy_matcher.fuzzy_tools import FuzzyMatcher
```

We can initialize a fuzzy match session with:

```
fuzzy_match = FuzzyMatcher(column1=df.column1,
                           column2=df.column2,
                           matcher=fuzz.partial_ratio,
                           first_chars=0,
                           similarity_threshold=60)
```

We pass the columns we want to match using fuzzy string matching, we specify which
function from the fuzzywuzzy package we want: default will be fuzz.ratio, but we can pass fuzz.partial_ratio or fuzz.token_ratio.
Documentation on these algorithms can be found [here](https://pypi.org/project/fuzzywuzzy/).

The *first_chars* parameter specifies whether we want to only match strings starting with a n amount
of overlapping characters. Default will be 0 (i.e, all strings will be matched). This feature might be useful if we have a very large number of matches: in fact, let's consider that if
we have a list of n strings to match with a list of m strings, the total matches the algorithm will perform is n * m, i.e. matching 2 lists of
1000 strings will require 1 million matches. 
Only matching strings that start with the same character (first_chars = 1) will save a lot of 
potentially useless matches, and reduce the computational load.

The *similarity threshold* parameter specifies which matches we will keep for inspection. The parameter is passed to the
*post_processor* method after the fuzzy matching. Setting the threshold to 60 means we will only keep matches that returned a similarity score of
60 or more.

Then, we can call the name_normalizer method:
```
new_df = fuzzy_match.string_normalizer(do_replace=True, 
                                       replace_list=substrings, 
                                       colname1='test1',
                                       colname2='test2')
```

*do_replace* determines whether we want to replace some substrings from the strings. If set to True, we
have to pass a list to the *replace_list* argument. For instance, if we want to remove "ltd" and "limited", we can create a list

```
remove_list = ['ltd','limited']
```

and pass it to the argument *replace_list*. *colname1* and *colname2* are the names we want to assign to the columns
of the resulting dataframe.

Then, we can implement the actually fuzzy matching by calling the method:

```
res = fuzzy_match.fuzzy_matcher(first_col=new_df.test1, 
                                second_col=new_df.test2, 
                                match_track=25)
```

Here we specify which columns we want to match, and the *match_track*, that is the number
of matches to be performed before we get a notification printed on the screen.

Finally, we can call the *name_processor* method to tidy up the results.

```
fin_res = fuzzy_match.post_processor(res, highest_matches=False)
```

Calling this method will do two main things: if we have a *similarity_threshold* defined, 
the output will be a dataframe that only has matches equal or above the threshold (e.g., only
matches with a similarity score of 60 or more).

*highest_matches* is an argument that determines whether we want to keep only the highest matches
by string. 
</br>
Suppose a string is matched against 3 other strings, and they all produce high similarity scores, for instance:
84, 93, 89. 
<br>
In most cases, the match with the 93 similarity score will be the correct one, so 
*highest_matches* will remove the other two matches and only keep the one with 93.
<br>
This feature might be useful if we need to merge the output to other dataframes, and we don't want
unnecessary duplication.



