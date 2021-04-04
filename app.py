import pandas as pd
import plotly.graph_objects as go
from bs4 import BeautifulSoup
import quandl
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import plotly.express as px
import datetime
import config

app = dash.Dash(__name__)
quandl.ApiConfig.api_key = config.quandl_key

# US Yield data
ust = quandl.get("USTREASURY/YIELD", start_date="2011-01-01")
us_df = ust.drop(['1 MO', '2 MO', '3 MO', '6 MO', '2 YR'], axis=1).dropna().T

# JP Yield Data
jgb30 = quandl.get("MOFJ/INTEREST_RATE_JAPAN_30Y", start_date="2011-01-01")
jgb20 = quandl.get("MOFJ/INTEREST_RATE_JAPAN_20Y", start_date="2011-01-01")
jgb10 = quandl.get("MOFJ/INTEREST_RATE_JAPAN_10Y", start_date="2011-01-01")
jgb7 = quandl.get("MOFJ/INTEREST_RATE_JAPAN_7Y", start_date="2011-01-01")
jgb5 = quandl.get("MOFJ/INTEREST_RATE_JAPAN_5Y", start_date="2011-01-01")
jgb3 = quandl.get("MOFJ/INTEREST_RATE_JAPAN_3Y", start_date="2011-01-01")
jgb1 = quandl.get("MOFJ/INTEREST_RATE_JAPAN_1Y", start_date="2011-01-01")
jp_df = pd.concat([jgb1,  jgb3, jgb5, jgb7, jgb10, jgb20, jgb30], axis=1).dropna().T
jp_df.index = us_df.index


# layout
us_fig = go.Figure(data=[go.Surface(
    x=us_df.columns,
    y=us_df.index,
    z=us_df.values,
    opacity=0.1)])
us_fig.update_layout(
    title='US historical yield curve',
    scene=dict(
        xaxis_title='year',
        yaxis_title='term',
        zaxis_title='US yield[%]'
        ),
    height=750,
)

trace0 = go.Scatter(
    y = us_df.iloc[0].values,
    x = us_df.columns,
    name = '1YR')
trace1 = go.Scatter(
    y = us_df.iloc[1].values,
    x = us_df.columns,
    name = '3YR')
trace2 = go.Scatter(
    y = us_df.iloc[2].values,
    x = us_df.columns,
    name = '5YR')
trace3 = go.Scatter(
    y = us_df.iloc[3].values,
    x = us_df.columns,
    name = '7YR')
trace4 = go.Scatter(
    y = us_df.iloc[4].values,
    x = us_df.columns,
    name ='10YR')
trace5 = go.Scatter(
    y = us_df.iloc[5].values,
    x = us_df.columns,
    name ='20YR')
trace6 = go.Scatter(
    y = us_df.iloc[6].values,
    x = us_df.columns,
    name ='30YR')
usr_fig = go.Figure(data=[trace0, trace1, trace2, trace3, trace4, trace5, trace6])

jp_fig = go.Figure(data=[go.Surface(
    x=jp_df.columns,
    y=jp_df.index,
    z=jp_df.values,
    opacity=0.1)])
jp_fig.update_layout(
    title='JP historical yield curve',
    scene=dict(
        xaxis_title='year',
        yaxis_title='term',
        zaxis_title='JP yield[%]'
        ),
    height=750,
)

jptrace0 = go.Scatter(
    y = jp_df.iloc[0].values,
    x = jp_df.columns,
    name = '1YR')
jptrace1 = go.Scatter(
    y = jp_df.iloc[1].values,
    x = jp_df.columns,
    name = '3YR')
jptrace2 = go.Scatter(
    y = jp_df.iloc[2].values,
    x = jp_df.columns,
    name = '5YR')
jptrace3 = go.Scatter(
    y = jp_df.iloc[3].values,
    x = jp_df.columns,
    name = '7YR')
jptrace4 = go.Scatter(
    y = jp_df.iloc[4].values,
    x = jp_df.columns,
    name ='10YR')
jptrace5 = go.Scatter(
    y = jp_df.iloc[5].values,
    x = jp_df.columns,
    name ='20YR')
jptrace6 = go.Scatter(
    y = jp_df.iloc[6].values,
    x = jp_df.columns,
    name ='30YR')
jpy_fig = go.Figure(data=[jptrace0, jptrace1, jptrace2, jptrace3, jptrace4, jptrace5, jptrace6])


app.layout = html.Div(
    children=[
        html.H2(children='US Historical Yield Curve'),
        html.Div(
            children=[
                dcc.Graph(
                    id='graph1',
                    figure=us_fig),
                dcc.Graph(
                    id='graph2',
                    figure=usr_fig),
            ],
            style = {'display': 'flex'}
        ),
        html.H2(children='JP Historical Yield Curve'),
        html.Div(
            children=[
                dcc.Graph(
                    id='graph3',
                    figure=jp_fig),
                dcc.Graph(
                    id='graph4',
                    figure=jpy_fig),
            ],
            style = {'display': 'flex'}
        )
    ]
)

server = app.server

if __name__ == '__main__':
    app.run_server(debug=True)