import pandas as pd
from fuzzy_matcher.fuzzy_tools import FuzzyMatcher
from fuzzywuzzy import fuzz

list1 = ['dunno how', 'cantsee if', 'Wontwork maybe', 'willwork surely', 'stucklimited']
list2 = ['dunnowhy99&', 'cantsee If', 'wontwork maybe', 'see', 'stuckltd']

zip_list = zip(list1, list2)

df = pd.DataFrame(zip_list, columns=['column1', 'column2'])

fuzzy_match = FuzzyMatcher(column1=df.column1,
                           column2=df.column2,
                           matcher=fuzz.partial_ratio,
                           first_chars=0,
                           similarity_threshold=60)

substrings = ['ltd', 'limited']

new_df = fuzzy_match.string_normalizer(do_replace=True, replace_list=substrings, colname1='test1',
                                       colname2='test2')
res = fuzzy_match.fuzzy_matcher(first_col=new_df.test1, second_col=new_df.test2, match_track=25)

fin_res = fuzzy_match.post_processor(res, highest_matches=False)

fuzzy_match2 = FuzzyMatcher(column1=df.column1,
                            column2=df.column2,
                            matcher=fuzz.ratio,
                            first_chars=1,
                            similarity_threshold=0)

new_df2 = fuzzy_match2.string_normalizer(do_replace=False, colname1='test1',
                                         colname2='test2')  # these arguments must be optional
res2 = fuzzy_match2.fuzzy_matcher(first_col=new_df2.test1, second_col=new_df2.test2, match_track=5)
