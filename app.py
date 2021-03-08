import pandas as pd
from plotly.graph_objs as go
from bs4 import BeautifulSoup
import dash
import dash_core_components as dcc
import dash_core_components as html
import datetime


app = dash.Dash(__name__)


server = app.server

if __name__ == '__main__':
    app.run_server(debug=True)