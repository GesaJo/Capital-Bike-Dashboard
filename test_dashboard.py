"""tests for bike-dashboard"""

import pandas as pd

from helper_functions import df_customer, get_date, get_weekday
from helper_functions import months_stacked, months_single, graph_week
from helper_functions import day_single, day_stacked, graph_weather
from helper_functions import get_station

from helper_data import list_days


#################### test helper functions ####################
df = pd.read_csv('data/df_main.csv')[::10000]

def test_df_customer():
    df1, color = df_customer(df, "members")
    assert df1["Member type"].unique() == "Member"

def test_get_date():
    date = get_date(5, 6, 2020, df)
    assert type(date) == str
    assert len(date) == 10


# get_weekday
