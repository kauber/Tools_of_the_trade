# we want a function to prepare the column (replace strings with '', remove alphanumeric, lower case)
# we then want to wrap the fuzzy matching in a function
# we also want some quick way to rejoin the fuzzy matching dataset to the master df, or use to filter it
from datetime import datetime
import pandas as pd
from fuzzywuzzy import fuzz


class FuzzyMatcher(object):
    """
    Initializer: it creates a fuzzymatcher instance
    :param column1: column we want to match against column2
    :param column2: column we want to match against column1
    :param matcher: type of matcher algorithm
    :param first_chars: parameter that determines whether we want to perform matching only on strings with n equal
    first characters (useful if we have too many strings to match)
    :return none
    """

    def __init__(self, column1: pd.Series, column2: pd.Series, matcher: fuzz.ratio,
                 first_chars: 0, similarity_threshold: 0) -> None:
        self.matcher = matcher
        self.column1 = column1
        self.column2 = column2
        self.first_chars = first_chars
        self.similarity_threshold = similarity_threshold

    def string_normalizer(self, do_replace: bool, colname1: str, colname2: str, *args, **kwargs) -> pd.DataFrame:
        """
        This is a method that implements string normalization. We can pass a list of strings to be removed from
        the strings we're matching. Non alphanumeric values will be removed by default
        :param do_replace: boolean: if true we can pass a list of strings we want removed from the names we're matching
        :param colname1: name of the first column
        :param colname2: name of the second column
        :param args:
        :param kwargs:
        :return: A new df with colnames specified above, and strings normalized
        """
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
        return pd.DataFrame(zipped_list, columns=[colname1, colname2])  # pass colnames

    def fuzzy_matcher(self, first_col: pd.Series, second_col: pd.Series, match_track: int, matcher='fuzz.ratio',
                      *args,
                      **kwargs) -> pd.DataFrame:
        """

        :param first_col: The first string column we want to match
        :param second_col: The string column we want to match the first column against
        :param match_track: How many matches have to occur before a print statement gives an update on the number of
        matches performed
        :param matcher: one of the functions available in the fuzzy wuzzy package, default is fuzz.ratio, can also be
        fuzz.token_ratio or fuzz.partial_ratio
        :param args:
        :param kwargs:
        :return: df with first_col, second_col and a similarity score
        """
        fuzzy = []
        count = 0
        print('Matching started at: ' + str(datetime.now().strftime('%H:%M:%S')))
        # matcher = kwargs.get('matcher', None)
        for i in first_col:
            count += 1
            if (count % match_track) == 0:
                print(str(count) + ' records matched at ' + str(datetime.now().strftime('%H:%M:%S')))
            for j in second_col:
                if self.first_chars > 0:
                    if i[:self.first_chars] == j[:self.first_chars]:
                        fuzzy.append([i, j, self.matcher(i, j)])
                else:
                    fuzzy.append([i, j, self.matcher(i, j)])
            # we want pass the self.matcher
        print('Matching completed at: ' + str(datetime.now().strftime('%H:%M:%S')))
        name_matching = pd.DataFrame(fuzzy, columns=[first_col.name, second_col.name, 'similarity_score'])
        return name_matching

    def post_processor(self, df: pd.DataFrame, highest_matches: bool):
        """
        This method implements some post-processing on the data. Namely, it keeps only rows with similarity score
        above a certain threshold (defined when the class is initialized) and optionally keeps matches with highest
        similarity score among all matches
        :param df: dataframe we want to process
        :param highest_matches: keep match with highest similarity score among all possible matches
        :return: processed df
        """
        df = df.loc[df['similarity_score'] >= self.similarity_threshold]
        if highest_matches:
            indices = df.groupby(df.iloc[:, 0])['similarity_score'].transform(max) == df['similarity_score']
            df_out = df[indices]
            df_out.reset_index(drop=True, inplace=True)
            return df_out
        return df
