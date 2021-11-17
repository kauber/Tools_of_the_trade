import pandas as pd
from fuzzy_matcher.fuzzy_tools import FuzzyMatcher

list1 = ['dunno how', 'cantsee if', 'Wontwork maybe', 'willwork surely', 'stucklimited']
list2 = ['dunnowhy99&', 'cantsee If', 'wontwork maybe', 'see', 'stuckltd']
zip_list = zip(list1, list2)

df = pd.DataFrame(zip_list, columns=['column1', 'column2'])

fuzzy_match = FuzzyMatcher(normalization=True, column1=df.column1, column2=df.column2, matcher='fuzz.ratio',
                           first_chars=False)

substrings = ['ltd', 'limited']

new_df = fuzzy_match.name_normalizer(sreplace=True, replace_list=substrings)  # we already initialized the cols, so
# we should not have to pass them to this method

# post processor keep highest similarity score when multiple matches

# option to pass a list with strings to remove

# vectorised version
