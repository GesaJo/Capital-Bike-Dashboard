"""tests for helper functions of bike-dashboard"""

import pandas as pd
import numpy as np

from helper_functions import df_customer, get_date, get_weekday
from helper_functions import months_stacked, months_single
from helper_functions import day_single, day_stacked, graph_weather
from helper_functions import get_station


df = pd.read_csv('data/df_main.csv')[::1000]

def test_df_customer():
    df1, _ = df_customer(df, "members")
    assert df1["Member type"].unique() == "Member"


def test_get_date():
    date = get_date(5, 6, 2020)
    assert isinstance(date, str)
    assert len(date) == 10


def test_get_weekday():
    dfmonday = get_weekday("Monday", df)
    assert dfmonday["weekday"].unique() == "Monday"


def test_months_stacked():
    v, _, x, _, col1, col2 = months_stacked(6, df)
    assert col1.startswith("#")
    assert col2.startswith("#")
    assert isinstance(v, np.ndarray)
    assert len(x) > 0


def test_months_single():
    v, w, x, _ = months_single(9, df)
    assert v == w == 0
    assert len(x) == 24


def test_day_single():
    v, w, x, y = day_single(4, 7, 2018, df)
    assert v == w == 0
    assert len(x) > 0
    assert len(y) > 0


def test_day_stacked():
    _, w, x, _, col1, col2 = day_stacked(4, 7, 2019, df)
    assert col1.startswith("#")
    assert col2.startswith("#")
    assert len(x) == 24
    assert isinstance(w, pd.Series)

def test_graph_weather():
    result = graph_weather("TAVG", df)
    assert result[0].name == "Duration_bins"
    assert result[1].dtype == "int64"
    assert result[5] == '0 to 5'

def test_get_station():
    station_no, no_bikes = get_station(22, 5, 2018, df)
    assert station_no in range(31000, 32609)
    assert no_bikes.dtype == "int64"
