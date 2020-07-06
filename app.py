import pandas as pd
import plotly.graph_objs as go
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from helper_functions import df_customer, get_date, get_weekday
from helper_functions import months_stacked, months_single, graph_week
from helper_functions import day_single, day_stacked, graph_weather
from helper_functions import get_station
from helper_data import options_days, options_customers, options_months_year
from helper_data import options_days31, colors_weather, months_dict
from helper_data import  options_months, options_days_w, options_years, options_years_only
from sankey import gen_sankey

# load data
df = pd.read_csv('data/df_main.csv')
df_loc = pd.read_csv("data/df_loc.csv")
mapbox_access_token = pd.read_csv("ignore/pw.txt", header=None)

df_2018 = df[df["year"]==2018]
df_2019 = df[df["year"]==2019]
df_2020 = df[df["year"]==2020]

# main app
app = dash.Dash()
app.layout = html.Div([

    # First Row
    html.Div([

        # Image and Input container left
        html.Div([
                html.Img(id="bike image",
                    height="180px",
                    src="assets/bike_flipped.jpg",
                    style={"border-radius": "20px"}),

                html.H3("Filter by:",
                    className="filter"),

                html.H4("Year:",
                    className="control_label"),

                dcc.Dropdown(id='choose-year',
                    className="input-line",
                    style={"flex-grow":"2"},
                    options=options_years,
                    value= 0.0),

                html.H4("Month:",
                    className="control_label"),

                dcc.Dropdown(id='choose-month',
                    className="input-line",
                    style={"flex-grow":"2"},
                    options=options_months_year,
                    value= 0.0),

                html.H4("Customer status:",
                    className="control_label"),

                dcc.RadioItems(id="customer-status-selector",
                    options=options_customers,
                    value="all",
                    labelStyle={"display": "inline-block"},
                    className="radio-select"),

                html.H4("Weekday:",
                    className="control_label"),

                dcc.Dropdown(id='choose-weekday',
                    className="input-line",
                    style={"flex-grow":"2",},
                    options=options_days,
                    value= "all"),

                html.H4("Display single day:",
                    className="control_label"),

                dcc.RadioItems(id="check_single_day",
                    options=[{"label": "Yes", 'value':'yes'},
                            {"label": "No", 'value':'no'}],
                    value='no'),

                html.Div([
                    dcc.Dropdown(id='choose-year1',
                        className="input-line",
                        style={"flex-grow":"2"},
                        options=options_years_only,
                        value= 2018),
                    dcc.Dropdown(id='choose-month1',
                        className="input-line",
                        style={"flex-grow":"3",},
                        options=options_months,
                        value=1),
                    dcc.Dropdown(id='choose-day1',
                        className="input-line",
                        style={"flex-grow":"1",},
                        options=options_days31,
                        value= 1)
                ], className="sidebyside"),


        ],className="pretty-container three columns"),


        # Title and main-graph container right
        html.Div([
            html.Div([
                html.H1('Dashboard Capital Bikeshare',
                    style={"textAlign": "center",
                            "display":"flex",
                            "alignItems":"center",
                            "justifyContent": "center"})
                    ], className = "pretty-container"),

            html.Div([
                dcc.Graph(id='basic-graph', style={'padding-top': '20px',
                                                'padding-bottom': '20px'})],
                    className="pretty-container")

        ], className="basic-container-column twelve columns"),

    ],className="basic-container"),


# Second Row
    html.Div([

        # Map
        html.Div([
            dcc.Graph(id='map-graph'),
            dcc.Slider(id='month-slider',
                min=df['month'].min(),
                max=df['month'].max(),
                value=df['month'].min(),
                marks=months_dict),

            html.Div([
                dcc.RadioItems(id="choose_year_map",
                    options=options_years,
                    value=2018,
                    labelStyle={"display": "inline-block"},
                    className="radio-select-map"),

                dcc.RadioItems(id="customer-status-selector-map",
                    options=options_customers,
                    value="all",
                    labelStyle={"display": "inline-block"},
                    className="radio-select-map2"),
            ],className="sidebyside"),


            html.H5("Search for station by station-number \
                (numbers range from 31000 to 32609):"),

            dcc.Input(id="map_single_station",
                type="text",
                placeholder = "Station-number",
                value="")

        ], className="pretty-container nine columns"),


        # Most used stations
        html.Div([
            html.H2("Most used station per day/month/year",
                style={"textAlign": "center"}),

            html.Div([
                html.H3(id="most_used_stations"),

            ], className="mini_container"),

            html.Div([
                html.H5("Number of bikes rented:"),
                html.H3(id="number_bikes"),

            ], className="mini_container"),

            html.Div([
                dcc.Dropdown(id='choose-year2',
                    className="input-line",
                    style={"flex-grow":"2"},
                    options=options_years,
                    value= 0.0),
                dcc.Dropdown(id='choose-month2',
                    className="input-line",
                    style={"flex-grow":"2"},
                    options=options_months_year,
                    value=0),

                dcc.Dropdown(id='choose-day2',
                    className="input-line",
                    style={"flex-grow":"2",},
                    options=options_days_w,
                    value= 0),
            ], className="sidebyside"),

            html.P("Filter by customer status:",
                className="control_label"),

            dcc.RadioItems(id="customer-status-selector2",
                options=[{"label": "All ", "value": "all"},
                    {"label": "Members ", "value": "members"},
                    {"label": "Casual riders ", "value": "casual"}],
                value="all",
                labelStyle={"display": "inline-block"},
                className="radio-select")

        ], className="pretty-container three columns")

    ], className="basic-container"),


# Third row
    html.Div([
        html.Div([
            dcc.Graph(id='sankey'),

        ], className = "container-sankey"),

        html.Div([
            html.P("Number of rentals per weekday and time of the day",
                style={"textAlign":"center",
                    "fontSize": "20px",
                    "color": "#ff7f0e"}),
            dcc.Graph(id="weekday-graph"),

        ],className="pretty-container six columns"),

    ],className="basic-container"),

# Fourth Row
    html.Div([
        html.H3("Influence of weather-conditions",
            style={"textAlign": "center",
                "fontSize": "20px",
                "fontWeight": "normal"})

    ], className="pretty-container"),

# Fifth row
    html.Div([

    # Weather-graph left
        html.Div([
            dcc.Graph(id='weather-graph'),

            html.P("Filter by month and see the impact of different \
                weather-conditions for the whole dataset. The size of the \
                dots represents the average duration of the rides.",
                className="control_label"),

            dcc.Dropdown(id='choose-weather',
                className="input-line",
                style={"flex-grow":"2",},
                options=[{"label": "Temperature in C°", "value": "TAVG"},
                    {"label":"Precipitation", "value":"PRCP"},
                    {"label":"Windspeed", "value":"AWND"}],
                value= "TAVG"),

             dcc.Dropdown(id='choose-month-w',
                 className="input-line",
                 style={"flex-grow":"2",},
                 options=options_months_year,
                 value=0)
        ], className="pretty-container six columns"),


    # Weather-graph right
        html.Div([
            html.Div([
                dcc.Graph(id='weather2-graph'),

                html.P("See the impact of different weather-conditions on \
                    average duration of rides for a datasample-set that has \
                    the same number of rentals for each condition.",
                    className="control_label"),

                dcc.Dropdown(id='choose-weather2',
                    className="input-line",
                    style={"flex-grow":"2",},
                    options=[{"label": "Temperature in C°", "value": "TAVG"},
                        {"label":"Precipitation", "value":"PRCP"},
                        {"label":"Windspeed", "value":"AWND"}],
                     value= "TAVG"),
            ])
        ],className="pretty-container six columns")

    ], className="basic-container")

],className= "general")


###############################################################################

###############################################################################


@app.callback(
    Output('basic-graph', 'figure'),
    [Input('choose-year', 'value'),
    Input('choose-month', 'value'),
    Input('choose-weekday', 'value'),
    Input('customer-status-selector', 'value'),
    Input('check_single_day', 'value'),
    Input('choose-year1', 'value'),
    Input('choose-month1', 'value'),
    Input('choose-day1', 'value'),])
def update_basic_graph(year, month, weekday, customer, check, year1, month1, day1, df=df):
    df, color1 = df_customer(df, customer)
    color2 = color1

    if check == "yes":
        if year1 == 2018:
            df = df_2018
        elif year1 == 2019:
            df = df_2019
        else:
            df = df_2020

        if customer == "all":
            v, w, x, y, color1, color2 = day_stacked(day1, month1, year1, customer, df)
        else:
            v, w, x, y = day_single(day1, month1, year1, df)
    else:
        if year == 2018:
            df = df_2018
        elif year == 2019:
            df = df_2019
        elif year == 2020:
            df = df_2020
        else:
            year = "Average"

        if customer == "all":
            df_w = get_weekday(weekday, df)
            v, w, x, y, color1, color2 = months_stacked(month, customer, df_w)
        else:
            df_w = get_weekday(weekday, df)
            v, w, x, y = months_single(month, df_w)

    return {
        "data":[{"type": "bar",
            "x" : x,
            "y" : y,
            "marker":{"color": color1},
            "name": "Members"},
            {"type":"bar",
            "x": v,
            "y": w,
            "marker": {"color": color2},
            "name":"Casual riders"}],
        "layout": dict(
            barmode="stack",
            autosize=True,
            height=600,
            font=dict(color="#485C6E"),
            titlefont=dict(color="#485C6E", size='14'),
            margin=dict(l=35,r=35,b=35,t=45),
            hovermode="closest",
            title=f"Number of rides per hour of the day: {year}",
            plot_bgcolor='#fffcfc',
            paper_bgcolor='#fffcfc',
            legend=dict(font=dict(size=10), orientation='h'))
    }


@app.callback(
    Output('map-graph', 'figure'),
    [Input('month-slider', 'value'),
    Input('choose_year_map', 'value'),
    Input('map_single_station', 'value'),
    Input('customer-status-selector-map', 'value')])
def update_map(month, year, single_station, customer, df=df):

    if year == 2018:
        df = df_2018
    elif year == 2019:
        df = df_2019
    elif year == 2020:
        df = df_2020
    else:
        year = "Average"

    map_data = df[df['month']==month]
    df_c, color = df_customer(map_data, customer)
    if single_station == "":
        lat = df_loc['LATITUDE']
        lon = df_loc['LONGITUDE']
        m_size= df_c.groupby("Start station number").count()["Duration"]/50
    else:
        single_station = int(single_station)
        lat = df_loc[df_loc['TERMINAL_NUMBER'] == single_station]['LATITUDE']
        lon = df_loc[df_loc['TERMINAL_NUMBER'] == single_station]['LONGITUDE']
        m_size= df_c[df_c["Start station number"]==single_station].groupby("Start station number").count()["Duration"]/50

    return {
        "data":[
            {"type" : "scattermapbox",
            "lat" : lat,
            "lon" : lon,
            "mode" : "markers",
            "marker": {"size": m_size,
                "sizemin": 2,
                "color": color,
                "opacity": 0.5},
            "text": df_c.groupby('Start station number').count()['Duration']}],
        "layout": dict(
            autosize=True,
            height=500,
            font=dict(color="#485C6E"),
            titlefont=dict(color="#485C6E", size='14'),
            margin=dict(l=35,r=35,b=35,t=45),
            hovermode="closest",
            plot_bgcolor='#fffcfc',
            paper_bgcolor='#fffcfc',
            title=f"Number of bikes rented from each station: {year}",
            legend=dict(font=dict(size=10), orientation='h'),
            mapbox=dict(
                accesstoken=mapbox_access_token[0][0],
                style="light",
                center=dict(lon=-77.03722,lat=38.90805),
                zoom=11))
    }


@app.callback(
    [Output('most_used_stations', 'children'),
    Output('number_bikes', 'children')],
    [Input('choose-year2', 'value'),
    Input('choose-month2', 'value'),
    Input('choose-day2', 'value'),
    Input('customer-status-selector2', 'value')])
def most_used_stations(year, month, day, customer, df=df, df_loc=df_loc):

    if year == 2018:
        df = df_2018
    elif year == 2019:
        df = df_2019
    elif year == 2020:
        df = df_2020
    df, _ = df_customer(df, customer)
    station_no, no_bikes = get_station(day, month, df)
    station_address = df_loc[df_loc["TERMINAL_NUMBER"] == station_no]["ADDRESS"].iloc[0]

    return (f"Station {station_no}, at {station_address}"), no_bikes


@app.callback(
    Output('sankey', 'figure'),
    [Input('choose-day1', 'value')])
def draw_sankey(value):
    fig = gen_sankey()

    return fig


@app.callback(
    Output('weekday-graph', 'figure'),
    [Input('choose-weather', 'value')])
def weekday_graph(dummy):
    res  = graph_week()

    return {
        "data":[{"x" : res[0],
            "y" : res[1],
            "name": res[2],
            "line": {"color": "#2D6F76"}},
            {"x": res[3],
            "y": res[4],
            "name": res[5],
            "line": {"color": "#A1E1E9"}},
            {"x": res[6],
            "y": res[7],
            "name":  res[8],
            "line": {"color": "#63A3AA"}},
            {"x": res[9],
            "y": res[10],
            "name": res[11],
            "line": {"color": "#5176A1"}},
            {"x": res[12],
            "y": res[13],
            "name": res[14],
            "line": {"color": "#7B74A8"}},
            {"x": res[15],
            "y": res[16],
            "name": res[17],
            "line": {"color": "#A371A0"}},
            {"x": res[18],
            "y": res[19],
            "name": res[20],
            "line": {"color": "#C2708D"}}],

        "layout": dict(
            autosize=True,
            height=500,
            font=dict(color="#485C6E"),
            titlefont=dict(color="#485C6E", size='14'),
            margin=dict(l=35,r=35,b=35,t=45),
            hovermode="closest",
            plot_bgcolor='#fffcfc',
            paper_bgcolor='#fffcfc',
            legend=dict(font=dict(size=12), orientation='h'))
    }


@app.callback(
    Output('weather-graph', 'figure'),
    [Input('choose-weather', 'value'),
    Input('choose-month-w', 'value')])
def weather_graph(weather, month, df=df):
    if month != 0:
        df = df[df["month"]==month]

    return {
    "data":[
        go.Scatter(
            x = df.groupby("day").mean().index,
            y = df.groupby("day").count()["Duration"],
            text = df["day"],
            mode="markers",
            opacity=0.7,
            marker = dict(
                color= df.groupby("day").mean()[weather],
                colorscale= colors_weather[weather],
                size=df.groupby("day").mean()["Duration"]/5,
                sizemin=2,
                sizeref= (max(df.groupby("day").mean()["Duration"]))/(10**2),
                showscale=True))],
    "layout": dict(
        xaxis={'title': 'Date'},
        yaxis={'title': 'Number of rentals'},
        autosize=True,
        height=500,
        font=dict(color="#485C6E"),
        titlefont=dict(color="#485C6E", size='14'),
        margin=dict(l=35,r=35,b=35,t=45),
        hovermode="closest",
        title="Weather, average duration and number of rentals per day",
        plot_bgcolor='#fffcfc',
        paper_bgcolor='#fffcfc',
        legend=dict(font=dict(size=10), orientation='h'))
    }


@app.callback(
    Output('weather2-graph', 'figure'),
    [Input('choose-weather2', 'value')])
def weekday_graph(weather, df=df):
    res  = graph_weather(weather, df)

    return {
        "data":[{"x" : res[0],
            "y" : res[1],
            "name": res[2],
            "line": {"color":"#DD8097"}},
            {"x": res[3],
            "y": res[4],
            "name": res[5],
            "line": {"color":"#A17199"}},
            {"x": res[6],
            "y": res[7],
            "name":  res[8],
            "line": {"color":"#A39CFF"}},
            {"x": res[9],
            "y": res[10],
            "name": res[11],
            "line": {"color":"#C1BAE0"}},
            {"x": res[12],
            "y": res[13],
            "name": res[14],
            "line": {"color":"#E1DAFF"}}],
        "layout": dict(
            autosize=True,
            height=500,
            font=dict(color="#485C6E"),
            titlefont=dict(color="#485C6E", size='14'),
            margin=dict(l=35,r=35,b=35,t=45),
            hovermode="closest",
            title="Number of rentals and average duration of rides under weather-conditions",
            plot_bgcolor='#fffcfc',
            paper_bgcolor='#fffcfc',
            legend=dict(font=dict(size=10), orientation='h'))
    }


if __name__ == '__main__':
    app.run_server(debug=True)
