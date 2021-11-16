import pandas as pd
from fuzzy_matcher.fuzzy_tools import FuzzyMatcher

list1 = ['dunno how', 'cantsee if', 'Wontwork maybe', 'willwork surely']
list2 = ['dunnowhy99&', 'cantsee If', 'wontwork maybe', 'stuck']
zip_list = zip(list1, list2)

df = pd.DataFrame(zip_list, columns=['column1', 'column2'])

fuzzy_match = FuzzyMatcher(normalization=True, column1=df.column1, column2=df.column2, matcher='fuzz.ratio',
                           first_chars=False)

new_df = fuzzy_match.name_normalizer(column1=df.column1, column2=df.column2)
