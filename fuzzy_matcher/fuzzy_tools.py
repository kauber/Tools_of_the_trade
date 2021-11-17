# we want a function to prepare the column (replace strings with '', remove alphanumeric, lower case)
# we then want to wrap the fuzzy matching in a function
# we also want some quick way to rejoin the fuzzy matching dataset to the master df, or use to filter it
from datetime import datetime
from typing import Optional
import pandas as pd
from fuzzywuzzy import fuzz


# what do we want initialized?
class FuzzyMatcher(object):
    def __init__(self, normalization: bool, column1: pd.Series, column2: pd.Series, matcher: str,
                 first_chars: Optional[int, None]) -> None:
        self.normalization: normalization
        self.matcher = matcher
        self.column1 = column1
        self.column2 = column2
        self.first_chars = first_chars

    def name_normalizer(self, doreplace: bool, replace_list: list) -> pd.DataFrame:
        self.column1 = self.column1.str.replace('[^a-zA-Z0-9]', '', regex=True).str.strip()
        self.column1 = self.column1.str.lower()
        self.column2 = self.column2.str.replace('[^a-zA-Z0-9]', '', regex=True).str.strip()
        self.column2 = self.column2.str.lower()
        # what about replacing substrings?
        if doreplace:
            remove_strings = '|'.join(replace_list)
            self.column1 = self.column1.str.replace(remove_strings, '')
            self.column2 = self.column2.str.replace(remove_strings, '')
        self.column1 = list(self.column1.unique())
        self.column2 = list(self.column2.unique())
        zipped_list = zip(self.column1, self.column2)
        return pd.DataFrame(zipped_list, columns=['col1', 'col2'])

    def fuzzy_matcher(self, threshold: int) -> pd.DataFrame:  # leave threshold optional
        fuzzy = []
        count = 0
        print('Matching started at: ' + str(datetime.now().strftime('%H:%M:%S')))
        for i in self.column1:
            count += 1
            if (count % 1000) == 0:  # pass to param
                print(str(count) + ' records matched at ' + str(datetime.now().strftime('%H:%M:%S')))
            for j in self.column2:
                if self.first_chars is not None:
                    if i[:self.first_chars] == j[:self.first_chars]:  # pass to param
                        fuzzy.append([i, j, fuzz.ratio(i, j)])
                else:
                    fuzzy.append([i, j, fuzz.ratio(i, j)])
            # we want pass the self.matcher
        print('Matching completed at: ' + str(datetime.now().strftime('%H:%M:%S')))
        name_matching = pd.DataFrame(fuzzy, columns=['col1', 'col2', 'similarity_score'])
        return name_matching

    def post_processor(self):
        pass
