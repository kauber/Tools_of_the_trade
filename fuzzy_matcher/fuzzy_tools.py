# we want a function to prepare the column (replace strings with '', remove alphanumeric, lower case)
# we then want to wrap the fuzzy matching in a function
# we also want some quick way to rejoin the fuzzy matching dataset to the master df, or use to filter it
from datetime import datetime
import pandas as pd
from fuzzywuzzy import fuzz


# what do we want initialized?
class FuzzyMatcher(object):
    """
    Initializer: it creates a fuzzymatcher instance
    @:param column1: column we want to match against column2
    @:param column2: column we want to match against column1
    @:param matcher: type of matcher algorithm
    @:param first_chars: parameter that determines whether we want to perform matching only on strings with n equal
    first characters (useful if we have too many strings to match)
    @:return none
    """
    def __init__(self, column1: pd.Series, column2: pd.Series, matcher: str,
                 first_chars: 0) -> None:
        self.matcher = matcher
        self.column1 = column1
        self.column2 = column2
        self.first_chars = first_chars

    def name_normalizer(self, do_replace: bool, *args, **kwargs) -> pd.DataFrame:
        self.column1 = self.column1.str.replace('[^a-zA-Z0-9]', '', regex=True).str.strip()
        self.column1 = self.column1.str.lower()
        self.column2 = self.column2.str.replace('[^a-zA-Z0-9]', '', regex=True).str.strip()
        self.column2 = self.column2.str.lower()
        if do_replace:
            replace_list = kwargs.get('replace_list', None)
            remove_strings = '|'.join(replace_list)
            self.column1 = self.column1.str.replace(remove_strings, '', regex=True)
            self.column2 = self.column2.str.replace(remove_strings, '', regex=True)
        col1 = list(self.column1.unique())
        col2 = list(self.column2.unique())
        zipped_list = zip(col1, col2)
        return pd.DataFrame(zipped_list, columns=['col1', 'col2'])  # pass colnames

    def fuzzy_matcher(self, first_col: pd.Series, second_col: pd.Series, match_track: int, matcher='fuzz.ratio', *args,
                      **kwargs) -> pd.DataFrame:  # leave threshold optional
        fuzzy = []
        count = 0
        print('Matching started at: ' + str(datetime.now().strftime('%H:%M:%S')))
        for i in first_col:
            count += 1
            if (count % match_track) == 0:
                print(str(count) + ' records matched at ' + str(datetime.now().strftime('%H:%M:%S')))
            for j in second_col:
                if self.first_chars > 0:
                    if i[:self.first_chars] == j[:self.first_chars]:  # pass to param
                        fuzzy.append([i, j, fuzz.ratio(i, j)])
                else:
                    fuzzy.append([i, j, fuzz.ratio(i, j)])
            # we want pass the self.matcher
        print('Matching completed at: ' + str(datetime.now().strftime('%H:%M:%S')))
        name_matching = pd.DataFrame(fuzzy, columns=['col1', 'col2', 'similarity_score'])
        return name_matching

    def post_processor(self):  # threshold, keep highest score by match
        pass
