import pandas as pd
import plotly.graph_objects as go
from bs4 import BeautifulSoup
import quandl
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import plotly.express as px
import statsmodels.api as sm
import datetime
import config
from rq import Queue
from worker import conn
from utils import count_words_at_url

app = dash.Dash(__name__)
q = Queue(connection=conn)
result = q.enqueue(count_words_at_url, 'https://guarded-harbor-46773.herokuapp.com/')
quandl.ApiConfig.api_key = config.quandl_key


# Tokyo data
row_data = pd.read_csv('https://stopcovid19.metro.tokyo.lg.jp/data/130001_tokyo_covid19_patients.csv')
by_day = row_data.groupby('公表_年月日')
dates = []
counts = []
for bd in by_day:
    dates.append(bd[0])
    counts.append(len(bd[1]))
daily_cases = pd.DataFrame({'counts':counts} ,index=dates)
datetimes = []
for d in daily_cases.index:
    datetimes.append(datetime.datetime.strptime(d, '%Y-%m-%d'))
daily_cases.index = datetimes
seasonal = sm.tsa.seasonal_decompose(daily_cases.counts, period=7)
daily_cases['trend'] = seasonal.trend

# Kanagawaデータ
kan_row = pd.read_csv('https://www.pref.kanagawa.jp/osirase/1369/data/csv/patient.csv', encoding="shift-jis")
kan_by_day = kan_row.groupby('発表日')
kan_dates = []
kan_counts = []
for bd in kan_by_day:
    kan_dates.append(bd[0])
    kan_counts.append(len(bd[1]))
kan_daily_cases = pd.DataFrame({'counts':kan_counts} ,index=kan_dates)
kan_datetimes = []
for d in kan_daily_cases.index:
    kan_datetimes.append(datetime.datetime.strptime(d, '%Y-%m-%d'))
kan_daily_cases.index = kan_datetimes
kan_seasonal = sm.tsa.seasonal_decompose(kan_daily_cases.counts, period=7)
kan_daily_cases['trend'] = kan_seasonal.trend

# 大阪府データ
osk_row = pd.read_csv('https://covid19-osaka.info/data/summary.csv', encoding="shift-jis")
osk_dates = []
osk_daily_cases = pd.DataFrame({'counts': osk_row['陽性人数']}, index=osk_row['日付'])
osk_daily_cases['counts'] = osk_row['陽性人数'].values
osk_datetimes = []
for d in osk_daily_cases.index:
    osk_datetimes.append(datetime.datetime.strptime(d, '%Y-%m-%d'))
osk_daily_cases.index = osk_datetimes
osk_seasonal = sm.tsa.seasonal_decompose(osk_daily_cases.counts, period=7)
osk_daily_cases['trend'] = osk_seasonal.trend


# US Yield data

ust = quandl.get("USTREASURY/YIELD")
us_df = ust.drop(['1 MO', '2 MO', '3 MO', '6 MO'], axis=1).dropna().T

us_fig = go.Figure(data=[go.Surface(
    x=us_df.columns,
    y=us_df.index,
    z=us_df.values,
    opacity=0.05)])
us_fig.update_layout(
    title='US historical yield curve',
    scene=dict(
        xaxis_title='year',
        yaxis_title='term',
        zaxis_title='US yield[%]'
        ),
    height=750,
)


# # JP Yield Data

# jgb30 = quandl.get("MOFJ/INTEREST_RATE_JAPAN_30Y")
# jgb20 = quandl.get("MOFJ/INTEREST_RATE_JAPAN_20Y")
# jgb10 = quandl.get("MOFJ/INTEREST_RATE_JAPAN_10Y")
# jgb7 = quandl.get("MOFJ/INTEREST_RATE_JAPAN_7Y")
# jgb5 = quandl.get("MOFJ/INTEREST_RATE_JAPAN_5Y")
# jgb3 = quandl.get("MOFJ/INTEREST_RATE_JAPAN_3Y")
# jgb2 = quandl.get("MOFJ/INTEREST_RATE_JAPAN_2Y")
# jgb1 = quandl.get("MOFJ/INTEREST_RATE_JAPAN_1Y")
# jp_df = pd.concat([jgb1, jgb2, jgb3, jgb5, jgb7, jgb10, jgb20, jgb30], axis=1).dropna()
# jp_df.columns = us_df.index
# jp_df = jp_df.T

# jp_fig = go.Figure(data=[go.Surface(
#     x=jp_df.columns,
#     y=jp_df.index,
#     z=jp_df.values,
#     opacity=0.05)])
# jp_fig.update_layout(
#     title='JP historical yield curve',
#     scene=dict(
#         xaxis_title='year',
#         yaxis_title='term',
#         zaxis_title='US yield[%]'
#     ),
#     height=750,
# )

app.layout = html.Div(
    children=[
        html.H2(children='COVID-19 Daily Cases in Japan'),
        dcc.Graph(
            id='graph1',
            figure={
                'data':[
                    {'x': daily_cases.index,
                    'y': daily_cases['counts'],
                    'type': 'bar',
                    'name': '新規感染者数'},
                    {'x': daily_cases.index,
                    'y': daily_cases['trend'],
                    'type': 'line',
                    'name': '7日移動平均'}
                        ],
                'layout': {'title': '東京都内新規感染者数'}
                    }
                ),
        dcc.Graph(
            id='graph2',
            figure={
                'data':[
                    {'x': kan_daily_cases.index,
                    'y': kan_daily_cases['counts'],
                    'type': 'bar',
                    'name': '新規感染者数'},
                    {'x': kan_daily_cases.index,
                    'y': kan_daily_cases['trend'],
                    'type': 'line',
                    'name': '7日移動平均'}
                        ],
                'layout': {'title': '神奈川県内新規感染者数'}
                    }
                ),
        dcc.Graph(
            id='graph3',
            figure={
                'data':[
                    {'x': osk_daily_cases.index,
                    'y': osk_daily_cases['counts'],
                    'type': 'bar',
                    'name': '新規感染者数'},
                    {'x': osk_daily_cases.index,
                    'y': osk_daily_cases['trend'],
                    'type': 'line',
                    'name': '7日移動平均'}
                        ],
                'layout': {'title': '大阪府内新規感染者数'}
                    }
                ),
        html.H2(children='US Historical Yield Curve'),
        dcc.Graph(
            id='graph4',
            figure=us_fig),
        ]
    )

server = app.server

if __name__ == '__main__':
    app.run_server(debug=True)