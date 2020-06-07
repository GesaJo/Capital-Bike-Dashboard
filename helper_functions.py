"""helper functions and data"""
import pandas as pd

df_weekday = pd.read_csv('data/df_weekday.csv')


options_months = [
    {'label': 'January', 'value': 1},
    {'label': 'February', 'value': 2},
    {'label': 'March', 'value': 3},
    {'label': 'April', 'value': 4},
    {'label': 'May', 'value': 5},
    {'label': 'June', 'value': 6},
    {'label': 'July', 'value': 7},
    {'label': 'August', 'value': 8},
    {'label': 'September', 'value': 9},
    {'label': 'October', 'value': 10},
    {'label': 'November', 'value': 11},
    {'label': 'December', 'value': 12},
    {'label': 'Whole year', 'value': 0}]

options_days = [
    {'label': 'Monday', 'value': 'Monday'},
    {'label': 'Tuesday', 'value': 'Tuesday'},
    {'label': 'Wednesday', 'value': 'Wednesday'},
    {'label': 'Thursday', 'value': 'Thursday'},
    {'label': 'Friday', 'value': 'Friday'},
    {'label': 'Saturday', 'value': 'Saturday'},
    {'label': 'Sunday', 'value': 'Sunday'}]

list_days = ["Monday", "Tuesday", "Wednesday", "Thursday",
            "Friday", "Saturday", "Sunday"]

options_customers = [
    {"label": "All ", "value": "all"},
    {"label": "Members ", "value": "members"},
    {"label": "Casual riders ", "value": "casual"}]


colors = {"PRCP":"Darkmint",
        "TAVG": "BlueRed",
        "SNOW": "Magenta",
        "AWND": "Blugrn",
        "bad_weather": "matter"}


def df_customer(df, customer):
    if customer == "members":
        df = df[df["Member type"]=="Member"]
        color= "#0088D5"
    elif customer == "casual":
        df = df[df["Member type"]=="Casual"]
        color= "#6CFBCE"
    else:
        color= "#0E44A4"
    return df, color


def customer_stacked(month, day, weekday, customer, df):
    x=df["hour"].unique()
    v=x
    if month == 0:
        w = df[df["Member type"]=="Casual"].groupby("hour").count()["day"]
        y = df[df["Member type"]=="Member"].groupby("hour").count()["day"]
    elif day == 0:
        w = df[(df["Member type"]=="Casual") & (df["month"]==month)].groupby("hour").count()["day"]
        y = df[(df["Member type"]=="Member") & (df["month"]==month)].groupby("hour").count()["day"]
    else:
        date= get_date(day, month, df)
        w=df[(df["Member type"]=="Casual") & (df["day"]==date)].groupby("hour").count()["day"]
        y = df[(df["Member type"]=="Member") & (df["day"]==date)].groupby("hour").count()["day"]
    return v, w, x, y



def customer_single(month, day, weekday, df):
    x=df["hour"].unique()
    v=0
    w=0
    if month == 0:
        x=df["hour"].unique()
        y=df.groupby("hour").count()["day"]
    elif day == 0:
        x=df["hour"].unique()
        y=df[df["month"]==month].groupby("hour").count()["day"]
    else:
        date= get_date(day, month, df)
        x=df["hour"].unique()
        y=df[df["day"]== date].groupby("hour").count()["day"]
    return v, w, x, y


def get_date(day, month, df):
    if day < 10:
        day = "0"+ str(day)
    if month < 10:
        month = "0"+str(month)
    date =f"2019-{month}-{day}"
    return date


def get_weekday(weekday, df):
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

    list_results = []
    for day in list_days:
        list_results.append(df[df["weekday"]==day]["hour"])
        list_results.append(df[df["weekday"]==day].groupby("hour").sum()["Duration"])
        list_results.append(day)
    return list_results
