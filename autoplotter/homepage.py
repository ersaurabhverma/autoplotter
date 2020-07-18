import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from .navbar import Navbar, homepage_heading
import dash_table as dt
import pandas as pd

nav = Navbar()
headline=homepage_heading()


def  data_preview(df):
    data_body=html.Div(dt.DataTable(data=df.to_dict('records'),columns=[{'id': c, 'name': c} for c in df.columns],
    filter_action="native",sort_action="native",sort_mode="multi",page_size= 20,
    style_cell={'textAlign': 'center','padding': '5px', 'fontWeight': 'italic','backgroundColor': 'rgb(100, 100, 100)',
        'color': 'white'},
    style_header={
        'backgroundColor': '#FF6347',
        'fontWeight': 'bold'
    },
   
    ),style={'margin':'20px 20px 20px 30px'},
    )
    return data_body

def Homepage(df):
 
    layout = html.Div([
       
    nav,
    headline,
    data_preview(df)
    ])
    return layout


