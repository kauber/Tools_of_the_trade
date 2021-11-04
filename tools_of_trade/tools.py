from datetime import date, timedelta


def get_latest_monday() -> str:
    """
    Calculates the latest Monday and returns it as a string
    :return latest monday as a string:
    """
    today = date.today()
    day_diff = today.weekday()
    my_date = date.today() - timedelta(days=day_diff)
    return my_date.strftime("%d-%m-%Y")


def get_latest_date() -> str:
    return "no"
