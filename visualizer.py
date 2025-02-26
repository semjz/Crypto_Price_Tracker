import plotly.express as px
import pandas as pd
from dash import dash
from dash import dcc, html
from dash.dependencies import Output, Input
from constants import *
app = dash.Dash(__name__)

# App layout
app.layout = html.Div(
    children=[
        html.H1("📈 Live Crypto Price History"),
        dcc.Graph(id='live-price-chart'),
        dcc.Interval(
            id='interval-component',
            interval=TIME_INTERVAL,  # Update every 5 minutes
            n_intervals=0  # Initial trigger
        )
    ]
)

class Visualizer:
    def __init__(self):
        self.file_loc = 'data/price_history.csv'
        self.df = pd.DataFrame(data=self.retrieve_data())


    def visualize(self):
        fig = px.line(self.df, x="datetime", y="price_hour_ago", title="Price history")
        fig.show()

    def retrieve_data(self):
        """Retrieves price history data safely."""
        try:
            return pd.read_csv(self.file_loc)
        except (FileNotFoundError, pd.errors.EmptyDataError):
            return pd.DataFrame(columns=["datetime", "price_hour_ago"])

    # Update the graph dynamically
    @app.callback(
        Output('live-price-chart', 'figure'),
        Input('interval-component', 'n_intervals')
    )
    def update_graph(self, n):
        df = self.retrieve_data()
        if df.empty:
            return px.line(title="⚠️ No Data Available")

        fig = px.line(df, x="datetime", y="price_hour_ago", title="📊 Price History (Updated Every 5 Minutes)")
        return fig
