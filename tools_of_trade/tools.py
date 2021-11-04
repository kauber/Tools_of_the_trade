from datetime import date, timedelta
import pandas as pd
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


def get_closest_monday(df: pd.DataFrame, date_field: str) -> str:
    """
    Computes the closest monday to a given date and returns it as a string
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
