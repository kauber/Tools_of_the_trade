from datetime import date, timedelta
import pandas as pd
import numpy as np
from typing import Optional


def get_latest_monday() -> str:
    """
    :return latest monday as a string:
    """
    today = date.today()
    day_diff = today.weekday()
    my_date = date.today() - timedelta(days=day_diff)
    return my_date.strftime("%d-%m-%Y")


def get_latest_date() -> str:
    """
    :return today's date as a string:
    """
    today = date.today()
    return today.strftime("%d-%m-%Y")


def get_closest_monday(df: pd.DataFrame, date_field: str) -> pd.DataFrame:
    """
    Computes the closest monday to a given date and returns it as a dataframe column
    :param
    df: pandas df
    date_field: the field containing the dates we want to calculate the closest monday on
    @:return: column with calculated closest monday
        """
    df.loc[:, date_field] = pd.to_datetime(df.loc[:, date_field])
    df.loc[:, date_field] = pd.to_datetime(df.loc[:, date_field].dt.date)
    day_of_week = df.loc[:, date_field].dt.dayofweek
    monday_dist = (0 - day_of_week)
    monday_dist = monday_dist.fillna(0).astype(int)
    closest_monday = df.loc[:, date_field] + pd.to_timedelta(monday_dist, unit='D')
    assert (sum(closest_monday.dropna().dt.dayofweek) == 0)
    closest_monday_f = closest_monday.astype(str)
    return closest_monday_f


def mean_updater(mean1: float, mean2: float, n1: int, n2: int):
    """
    This function computes the combined mean of two separate groups
    :param mean1: mean of the first group
    :param mean2: mean of the second group
    :param n1: size of first group
    :param n2: size of second group
    :return: combined means of the two groups
    """
    return ((mean1 * n1) + (mean2 * n2)) / (n1 + n2)


def std_updater(mean1: float, mean2: float, std1: float, std2: float, n1: int, n2: int):
    """
    This function computes the combined std (or variance) for the separate groups
    :param mean1: mean of the first group
    :param mean2: mean of the second group
    :param std1: std of the first group
    :param std2: std of the second group
    :param n1: size of the first group
    :param n2: size of the second group
    :return:
    """
    d1 = mean_updater(mean1, mean2, n1, n2)
    return np.sqrt((n1 * (std1 ** 2 + (d1 - mean1) ** 2) + (n2 * (std2 ** 2 + (d1 - mean2) ** 2))) / (n1 + n2))
