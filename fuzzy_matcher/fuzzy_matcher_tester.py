import pandas as pd
from fuzzy_matcher.fuzzy_tools import FuzzyMatcher

list1 = ['dunno how', 'cantsee if', 'Wontwork maybe', 'willwork surely', 'stucklimited']
list2 = ['dunnowhy99&', 'cantsee If', 'wontwork maybe', 'see', 'stuckltd']
zip_list = zip(list1, list2)

df = pd.DataFrame(zip_list, columns=['column1', 'column2'])

fuzzy_match = FuzzyMatcher(column1=df.column1,
                           column2=df.column2,
                           matcher='fuzz.ratio',
                           first_chars=0)

substrings = ['ltd', 'limited']

new_df = fuzzy_match.name_normalizer(doreplace=False) # these arguments must be optional

new_df2 = fuzzy_match.name_normalizer(doreplace=True, replace_list=substrings)

res = fuzzy_match.fuzzy_matcher(threshold=3)

res
