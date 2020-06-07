import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go

from helper_functions import df_customer, get_date, get_weekday
from helper_functions import months_stacked, months_single, graph_week
from helper_functions import day_single, day_stacked
from helper_data import options_days, options_customers, options_months_year
from helper_data import options_days31, colors_weather, months_dict
from helper_data import  options_months
from sankey import gen_sankey


df = pd.read_csv('data/df_main.csv')
df_loc = pd.read_csv("data/df_loc.csv")

mapbox_access_token = "pk.eyJ1Ijoia2VzaSIsImEiOiJja2IxemUwdzkwNnZnMnhtYXZ5dnE2NHBtIn0.d5Xf1lZV009l1ubMrOAieQ"


app = dash.Dash()

app.layout = html.Div([

    html.H1(children='Dashboard Capital Bikeshare 2019',
            style={"textAlign": "center",
            }),


    ### basic-container1
    html.Div([

    ####### pretty container
        html.Div([
                html.P(
                    "Filter by month and (optional) by day, \
                     default shows values for the whole year/month.",
                    className="control_label",),

                dcc.Dropdown(id='choose-month',
                    className="input-line",
                    style={"flex-grow":"2",},
                    options=options_months_year,
                     value= 0.0),

                html.P("Filter by customer status:", className="control_label"),
                dcc.RadioItems(
                    id="customer-status-selector",
                    options=options_customers,
                    value="all",
                    labelStyle={"display": "inline-block"},
                    className="radio-select",),
                html.P("Filter by weekday:", className="control_label"),
                dcc.Dropdown(id='choose-weekday',
                    className="input-line",
                    style={"flex-grow":"2",},
                    options=options_days,
                    value= "all"),
                html.P("Display single day:", className="control_label"),
                dcc.RadioItems(
                    id="check_single_day",
                    options=[{"label": "Yes", 'value':'yes'},
                            {"label": "No", 'value':'no'}],
                    value='no'
                ),

                ##### Side by side
                html.Div([
                    dcc.Dropdown(id='choose-day1',
                        className="input-line",
                        # style={"flex-grow":"2",},
                        options=options_days31,
                         value= 1),
                    dcc.Dropdown(id='choose-month1',
                        className="input-line",
                        # style={"flex-grow":"2",},
                        options=options_months,
                        value=1)
                ], className="sidebyside"),
                #### END Side by side
            ],
            className="pretty-container three columns",
            ),
    ##### END pretty container

    ### basic graph
        html.Div([
            dcc.Graph(id='basic-graph'),
            ],
            className="pretty-container nine columns"),
    ### END basic graph
    ], className="basic-container"),
    ### END basic container1



    ### basic container2
    html.Div([
        ### map
        html.Div([
            dcc.Graph(
                id='map-graph'),
            dcc.Slider(
                id='month-slider',
                min=df['month'].min(),
                max=df['month'].max(),
                value=df['month'].min(),
                marks=months_dict,
                step=None),
            dcc.RadioItems(
                id="customer-status-selector-map",
                options=options_customers,
                value="all",
                labelStyle={"display": "inline-block"},
                className="radio-select")
                ],
                className="pretty-container nine columns",
            ),

        ### END map

        #### most-used-box
        html.Div([

            html.Div([
                html.P("Station number:"),
                html.H6(id="most_used_stations"),
                ], className="mini_container",
            ),
            html.Div([
                html.P("Adress:"),
                html.H6(id="most_used_address"),
                ], className="mini_container",
            ),
            html.Div([
                html.P("Number of bikes rented per day/month:"),
                html.H6(id="number_bikes"),
                ], className="mini_container",
            ),

            ##### Side by side
            html.Div([
                dcc.Dropdown(id='choose-month2',
                    className="input-line",
                    style={"flex-grow":"2",},
                    options=options_months_year,
                    value=1.0),
                dcc.Input(id='choose-day2',
                    className="input-line",
                    style={"flex-grow":"1",},
                    value=0, type='number',
                    min=0, max=31, step=1,)
            ], className="sidebyside"),
            #### END Side by side

            ### Customer Selection
            html.P("Filter by customer status:", className="control_label"),
            dcc.RadioItems(
                id="customer-status-selector2",
                options=[
                    {"label": "All ", "value": "all"},
                    {"label": "Members ", "value": "members"},
                    {"label": "Casual riders ", "value": "casual"},
                ],
                value="all",
                labelStyle={"display": "inline-block"},
                className="radio-select",),
            ### END customer selecttion

        ], className="pretty-container three columns")
        ### END most-used-box

        ], className="basic-container"),
        ### END basic container 2


        ### basic container 3
        html.Div([
            html.Div([
                dcc.Graph(
                    id='sankey'),
                            ], className = "pretty-container seven columns"),

            html.Div([
                dcc.Graph(
                    id="weekday-graph")
                    ],className="pretty-container five columns")
            ],className="basic-container"),

        ### END basic container 3




        #### basic container 4
        html.Div([

        ### weather graph
            html.Div([
                dcc.Graph(id='weather-graph')
                ],
                className="pretty-container"),
        ### END weather graph

        ####### pretty container
            html.Div([
                    html.Div([
                        html.P(
                            "Filter by month and see the impact of the weather",
                            className="control_label"),
                        dcc.Dropdown(id='choose-weather',
                            className="input-line",
                            style={"flex-grow":"2",},
                            options=[{"label": "Temperature", "value": "TAVG"},
                                    {"label":"Precipitation", "value":"PRCP"},
                                    {"label":"Snow", "value":"SNOW"},
                                    {"label":"Wind", "value":"AWND"},
                                    {"label":"thunder, hail, fog", "value":"bad_weather"}],
                             value= "TAVG"),
                         dcc.Dropdown(id='choose-month-w',
                             className="input-line",
                             style={"flex-grow":"2",},
                             options=options_months_year,
                             value=0)])
                    ],className="pretty-container five columns")

        ##### END pretty container
        ], className="basic-container")
        ##### END basic container 4

    ])




###############################################################################
#-----------------------------------------------------------------------------#
###############################################################################



@app.callback(
    Output('basic-graph', 'figure'),
    [Input('choose-month', 'value'),
    Input('choose-weekday', 'value'),
    Input('customer-status-selector', 'value'),
    Input('check_single_day', 'value'),
    Input('choose-day1', 'value'),
    Input('choose-month1', 'value'),])
def update_basic_graph(month, weekday, customer, check, day1, month1, df=df):
    df, color1 = df_customer(df, customer)
    color2 = color1
    df = get_weekday(weekday, df)
    if check == "yes":
        if customer == "all":
            v, w, x, y, color1, color2 = day_stacked(day1, month1, customer, df)
        else:
            v, w, x, y = day_single(day1, month1, df)
    elif customer == "all":
        v, w, x, y, color1, color2 = months_stacked(month, weekday, customer, df)
    else:
        v, w, x, y = months_single(month, weekday, df)

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
        height=500,
        font=dict(color="#191A1A"),
        titlefont=dict(color="#191A1A", size='14'),
        margin=dict(l=35,r=35,b=35,t=45),
        hovermode="closest",
        title="Number of rides per hour of the day",
        plot_bgcolor='#fffcfc',
        paper_bgcolor='#fffcfc',
        legend=dict(font=dict(size=10), orientation='h'))
    }



@app.callback(
    Output('map-graph', 'figure'),
    [Input('month-slider', 'value'),
    Input('customer-status-selector-map', 'value')])
def update_map(month, customer, df=df):
    df, color = df_customer(df, customer)
    map_data = df[df['month']==month]
    return {
    "data":[
        {"type" : "scattermapbox",
         "lat" : df_loc['LATITUDE'],
         "lon" : df_loc['LONGITUDE'],
         "mode" : "markers",
         "marker": {"size": map_data.groupby("Start station number").count()["Duration"]/50,
                    "color": color,
                    "opacity":0.5},
         "text": map_data.groupby('Start station number').count()['Duration']}],
    "layout": dict(
        autosize=True,
        height=500,
        font=dict(color="#191A1A"),
        titlefont=dict(color="#191A1A", size='14'),
        margin=dict(l=35,r=35,b=35,t=45),
        hovermode="closest",
        plot_bgcolor='#fffcfc',
        paper_bgcolor='#fffcfc',
        title="Number of bikes rented from each station",
        legend=dict(font=dict(size=10), orientation='h'),
        mapbox=dict(
            accesstoken=mapbox_access_token,
            style="light",
            center=dict(lon=-77.03722,lat=38.90805),
            zoom=11))
    }


@app.callback(
    [Output('most_used_stations', 'children'),
    Output('most_used_address', 'children'),
    Output('number_bikes', 'children')],
    [Input('choose-month2', 'value'),
    Input('choose-day2', 'value'),
    Input('customer-status-selector2', 'value')])
def most_used_stations(month, day, customer, df=df, df_loc=df_loc):
    df, _ = df_customer(df, customer)
    if day == 0:
        station_no = df[df["month"]==month].groupby("Start station number").count()["Start station"].sort_values()[-1:].index[0]
        no_bikes = df[df["month"]==month].groupby("Start station number").count()["Start station"].sort_values()[-1:].iloc[0]
    else:
        date = get_date(day, month, df)
        station_no = df[df["day"]==date].groupby("Start station number").count()["Start station"].sort_values()[-1:].index[0]
        no_bikes = df[df["day"]==date].groupby("Start station number").count()["Start station"].sort_values()[-1:].iloc[0]

    station_address = df_loc[df_loc["TERMINAL_NUMBER"] == station_no]["ADDRESS"].iloc[0]
    return station_no, station_address, no_bikes

@app.callback(
    Output('sankey', 'figure'),
    [Input('choose-day1', 'value')])
def draw_sankey(value):
    fig = gen_sankey()
    return fig


@app.callback(
    Output('weather-graph', 'figure'),
    [Input('choose-weather', 'value'),
    Input('choose-month-w', 'value')])
def weather_graph(weather, month, df=df):
    if month != 0:
        df = df[df["month"]==month]
    else:
        df=df
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
                showscale=True,
                size=10))
            ],
    "layout": dict(
        xaxis={'title': 'Date'},
        yaxis={'title': 'Number of rentals'},
        autosize=True,
        height=500,
        font=dict(color="#191A1A"),
        titlefont=dict(color="#191A1A", size='14'),
        margin=dict(l=35,r=35,b=35,t=45),
        hovermode="closest",
        title="Weather and number of rentals",
        plot_bgcolor='#fffcfc',
        paper_bgcolor='#fffcfc',
        legend=dict(font=dict(size=10), orientation='h'))
    }


@app.callback(
    Output('weekday-graph', 'figure'),
    [Input('choose-weather', 'value')])
def weekday_graph(dummy):
    res  = graph_week()
    return {
        "data":[{"x" : res[0],
                "y" : res[1],
                "name": res[2]},
                {"x": res[3],
                "y": res[4],
                "name": res[5] },
                {"x": res[6],
                "y": res[7],
                "name":  res[8]},
                {"x": res[9],
                "y": res[10],
                "name": res[11] },
                {"x": res[12],
                "y": res[13],
                "name": res[14] },
                {"x": res[15],
                "y": res[16],
                "name": res[17] },
                {"x": res[18],
                "y": res[19],
                "name": res[20]}
                ],

    "layout": dict(
        xaxis={'title': 'Hour of day'},
        yaxis={'title': 'Number of rentals'},
        autosize=True,
        height=500,
        font=dict(color="#191A1A"),
        titlefont=dict(color="#191A1A", size='14'),
        margin=dict(l=35,r=35,b=35,t=45),
        hovermode="closest",
        title="Weekdays, time and number of rentals",
        plot_bgcolor='#fffcfc',
        paper_bgcolor='#fffcfc',
        legend=dict(font=dict(size=10), orientation='h'))
    }



if __name__ == '__main__':
    app.run_server(debug=True)
