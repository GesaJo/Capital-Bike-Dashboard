"""helper functions and data"""
import pandas as pd
from helper_data import list_days

df_weekday = pd.read_csv('data/df_weekday.csv')


def df_customer(df, customer):
    if customer == "members":
        df = df[df["Member type"]=="Member"]
        color= "#91BCCE"
    elif customer == "casual":
        df = df[df["Member type"]=="Casual"]
        color= "#ff7f0e"
    else:
        color= "#535E7A"
    return df, color


def months_stacked(month, weekday, customer, df):
    x=df["hour"].unique()
    v=x
    if month == 0:
        w = df[df["Member type"]=="Casual"].groupby("hour").count()["day"]
        y = df[df["Member type"]=="Member"].groupby("hour").count()["day"]
    else:
        w=df[(df["Member type"]=="Casual") & (df["month"]==month)].groupby("hour").count()["day"]
        y = df[(df["Member type"]=="Member") & (df["month"]==month)].groupby("hour").count()["day"]
    color1 = "#91BCCE"
    color2= "#ff7f0e"
    return v, w, x, y, color1, color2


def months_single(month, weekday, df):
    x=df["hour"].unique()
    v=0
    w=0
    if month == 0:
        x=df["hour"].unique()
        y=df.groupby("hour").count()["day"]
    else:
        x=df["hour"].unique()
        y=df[df["month"]== month].groupby("hour").count()["day"]
    return v, w, x, y


def day_stacked(day, month, customer, df):

    df = df[df["month"]==month]
    date = get_date(day, month, df)
    w = df[(df["Member type"]=="Casual") & (df["day"]==date)].groupby("hour").count()["day"]
    y = df[(df["Member type"]=="Member") & (df["day"]==date)].groupby("hour").count()["day"]
    x = df["hour"].unique()
    v = x
    color1 = "#91BCCE"
    color2= "#ff7f0e"
    return v, w, x, y, color1, color2


def day_single(day, month, df):

    df = df[df["month"]==month]
    date = get_date(day, month, df)
    y = df[df["day"]==date].groupby("hour").count()["day"]
    x = df["hour"].unique()
    v = 0
    w = 0
    return v, w, x, y


def get_date(day, month, df):
    if day < 10:
        day = "0"+ str(day)
    if month < 10:
        month = "0"+str(month)
    date =f"2019-{month}-{day}"
    return date


def get_weekday(weekday, df):
    """returns the dataframe filtered by given day"""

    if weekday == "Monday":
        df = df[df["weekday"]=="Monday"]
    elif weekday == "Tuesday":
        df = df[df["weekday"]=="Tuesday"]
    elif weekday == "Wednesday":
        df = df[df["weekday"]=="Wednesday"]
    elif weekday == "Thursday":
        df = df[df["weekday"]=="Thursday"]
    elif weekday == "Friday":
        df = df[df["weekday"]=="Friday"]
    elif weekday == "Saturday":
        df = df[df["weekday"]=="Saturday"]
    elif weekday == "Sunday":
        df = df[df["weekday"]=="Sunday"]
    else:
        df = df
    return df


def graph_week(df=df_weekday, list_days = list_days):
    """Graph to return a list with data for plotting for each weekday"""
    list_results = []
    for day in list_days:
        list_results.append(df[df["weekday"]==day]["hour"])
        list_results.append(df[df["weekday"]==day].groupby("hour").sum()["Duration"])
        list_results.append(day)
    return list_results


def graph_weather(weather, df):
    """Graph to return a list with data for plotting weather"""

    list_results = []
    if weather == "TAVG":
        list_results.append(df[df["TAVG"]<0][:80000].groupby("Duration_bins").count()["Duration"].index)
        list_results.append(df[df["TAVG"]<0][:80000].groupby("Duration_bins").count()["Duration"])
        list_results.append("0 or colder")
        list_results.append(df[df["TAVG"]>0][:80000].groupby("Duration_bins").count()["Duration"].index)
        list_results.append(df[(df["TAVG"]>0) & (df["TAVG"]<5)][:80000].groupby("Duration_bins").count()["Duration"])
        list_results.append("0 to 5")
        list_results.append(df[df["TAVG"]>5][:80000].groupby("Duration_bins").count()["Duration"].index)
        list_results.append(df[(df["TAVG"]>5) & (df["TAVG"]<10)][:80000].groupby("Duration_bins").count()["Duration"])
        list_results.append("05 to 10")
        list_results.append(df[df["TAVG"]>10][:80000].groupby("Duration_bins").count()["Duration"].index)
        list_results.append(df[(df["TAVG"]>10) & (df["TAVG"]<20)][:80000].groupby("Duration_bins").count()["Duration"])
        list_results.append("10 to 20")
        list_results.append(df[df["TAVG"]>20][:80000].groupby("Duration_bins").count()["Duration"].index)
        list_results.append(df[(df["TAVG"]>20)][:80000].groupby("Duration_bins").count()["Duration"])
        list_results.append("20 or warmer")
    elif weather == "PRCP":
        list_results.append(df[df["PRCP"]==0][:100000].groupby("Duration_bins").count()["Duration"].index)
        list_results.append(df[df["PRCP"]==0][:100000].groupby("Duration_bins").count()["Duration"])
        list_results.append("Dry")
        list_results.append(df[df["PRCP"]>0][:100000].groupby("Duration_bins").count()["Duration"].index)
        list_results.append(df[(df["PRCP"]>0) & (df["TAVG"]<5)][:100000].groupby("Duration_bins").count()["Duration"])
        list_results.append("Rain, snow or hail")
        list_results.extend([0,0,0,0,0,0,0,0,0])
    elif weather == "AWND":
        list_results.append(df[df["AWND"]<5][:100000].groupby("Duration_bins").count()["Duration"].index)
        list_results.append(df[df["AWND"]<5][:100000].groupby("Duration_bins").count()["Duration"])
        list_results.append("No wind to gentle breeze")
        list_results.append(df[df["AWND"]>5][:100000].groupby("Duration_bins").count()["Duration"].index)
        list_results.append(df[(df["AWND"]>5) & (df["TAVG"]<5)][:100000].groupby("Duration_bins").count()["Duration"])
        list_results.append("Stronger wind")
        list_results.extend([0,0,0,0,0,0,0,0,0])

    return list_results

def get_station(day, month, df):
    if month == 0:
        station_no = df.groupby("Start station number").count()["Start station"].sort_values()[-1:].index[0]
        no_bikes = df.groupby("Start station number").count()["Start station"].sort_values()[-1:].iloc[0]
    elif day == 0:
        station_no = df[df["month"]==month].groupby("Start station number").count()["Start station"].sort_values()[-1:].index[0]
        no_bikes = df[df["month"]==month].groupby("Start station number").count()["Start station"].sort_values()[-1:].iloc[0]
    else:
        date = get_date(day, month, df)
        station_no = df[df["day"]==date].groupby("Start station number").count()["Start station"].sort_values()[-1:].index[0]
        no_bikes = df[df["day"]==date].groupby("Start station number").count()["Start station"].sort_values()[-1:].iloc[0]
    return station_no, no_bikes
