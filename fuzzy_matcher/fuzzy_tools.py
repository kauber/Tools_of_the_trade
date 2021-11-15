# we want a function to prepare the column (replace strings with '', remove alphanumeric, lower case)
# we then want to wrap the fuzzy matching in a function
# we also want some quick way to rejoin the fuzzy matching dataset to the master df, or use to filter it
import pandas as pd


class FuzzyMatcher(object):
    def __init__(self, column1: pd.Series, column2: pd.Series, matcher: str, first_char: bool) -> None:
        self.matcher = matcher
        self.column1 = column1
        self.column2 = column2
        self.first_chars = first_char










