import pandas as pd
from fuzzy_matcher.fuzzy_tools import FuzzyMatcher
from fuzzywuzzy import fuzz

list1 = ['dunno how', 'cantsee if', 'Wontwork maybe', 'willwork surely', 'stucklimited']
list2 = ['dunnowhy99&', 'cantsee If', 'wontwork maybe', 'see', 'stuckltd']

zip_list = zip(list1, list2)

df = pd.DataFrame(zip_list, columns=['column1', 'column2'])

fuzzy_match = FuzzyMatcher(column1=df.column1,
                           column2=df.column2,
                           matcher='fuzz.ratio',
                           first_chars=0)

substrings = ['ltd', 'limited']

new_df = fuzzy_match.name_normalizer(do_replace=True, replace_list=substrings)  # these arguments must be optional
res = fuzzy_match.fuzzy_matcher(first_col=new_df.col1, second_col=new_df.col2, match_track=5)

fuzzy_match2 = FuzzyMatcher(column1=df.column1,
                            column2=df.column2,
                            matcher='fuzz.ratio',
                            first_chars=1)

new_df2 = fuzzy_match2.name_normalizer(do_replace=False)  # these arguments must be optional
res2 = fuzzy_match2.fuzzy_matcher(first_col=new_df2.col1, second_col=new_df2.col2, match_track=5, matcher='fuzz.ratio')
