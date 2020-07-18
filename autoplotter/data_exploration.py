import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from .navbar import Navbar
import plotly.express as px
import plotly.graph_objects as go
import ppscore as pps
import numpy as np

nav=Navbar()

def get_radios(): 
        button=html.Div(dcc.RadioItems(id='asso_type',options=[
                {'label': 'Predictive Power Score', 'value': 'Predictive Power Score'},
                {'label': 'Correlation', 'value': 'Correlation'}],value='Predictive Power Score',labelStyle={'display': 'inline-block','margin':'0 10px 0 10px'},inputStyle={'margin':'10px 10px 10px 10px'}))
        return button
  

def plotly_templates():
    themes=['ggplot2', 'seaborn', 'simple_white', 'plotly',
         'plotly_white', 'plotly_dark', 'presentation', 'xgridoff',
         'ygridoff', 'gridon', 'none']
    template_dropdown=html.Div(children=[html.Label('Select a theme'),dcc.Dropdown(id='theme_dropdown',placeholder='Select Theme',options=[
        {'label': i, 'value': i} for i in themes],value='plotly_dark')])
    return template_dropdown

def get_missing_valaues(df,col):
    n=df[col].notna().sum()
    values=(n/df.shape[0])*100
    return values,n


tabs_styles = {
    'height': '44px',
    'position': 'static', 
    'top': '0px'
  
   
}
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold',
   
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#FF6347',
    'color': 'white',
    'padding': '6px'
}

def columns_dropdown(df):
    dropdown=html.Div(children=[html.Label('Select the columns'),dcc.Dropdown(id='hist_col_dropdown', placeholder='Select Columns',
    options=[
        {'label': f"{col} ( {df[col].dtype} )", 'value': col} for col in df.columns
       
    ],value=[df.columns[0]],multi=True)]) 

    return dropdown

def plot_distributions(df,cols,theme):
    out_plots=[]
    for col in cols:
        if df[col].dtype=='object':
            figure=px.histogram(df, x=col, color_discrete_sequence=['tomato'],template=theme,hover_data=df.columns)
            figure.update_xaxes(showgrid=False)
            figure.update_yaxes(showgrid=False)
            figure.update_layout(title_text=f'Histogram of {col}')
            value,n=get_missing_valaues(df,col)
            progress=dbc.Progress(style={"height": "20px","margin":"10px 20px 10px 20px"},children=[dbc.Progress(f"{df.shape[0]-n} missing values",
            value=value, color="success", bar=True), 
            dbc.Progress(style={"height": "20px"},value=100-value,color="danger", bar=True)],multi=True,)
            out_plots.append(html.Div(children=[progress,dcc.Graph(figure=figure)]))
        else:
            figure=px.histogram(df, x=col, color_discrete_sequence=['tomato'],template=theme,marginal="box",hover_data=df.columns)
            figure.update_xaxes(showgrid=False)
            figure.update_yaxes(showgrid=False)
            figure.update_layout(title_text=f'Histogram of {col}')
            value,n=get_missing_valaues(df,col)
            progress=dbc.Progress(style={"height": "20px","margin":"10px 20px 10px 20px"},children=[dbc.Progress(f"{df.shape[0]-n} missing values",
            value=value, color="success",  bar=True), 
            dbc.Progress(value=100-value,
            color="danger", bar=True)],multi=True)
            out_plots.append(html.Div(children=[progress,dcc.Graph(figure=figure)]))
    return out_plots


def association(df,type,col1,col2):
    if col1 is not None and col2  is not None:

        if type== 'Predictive Power Score':
            return [html.Label(f' PPS between {col1} and {col2} = {pps.score(df,col1,col2)["ppscore"]}',style={'margin':'10px 0 0 10px'})]
        else:
            return [html.Label(f' Correlation between {col1} and {col2} = {df[col1].corr(df[col2])}',style={'margin':'10px 0 0 10px'})]



def get_corr_array(df):
    return df.corr()

def get_pps_array(df):
    ps=[]
    for i,col1 in enumerate(df.columns):
        ps.append([])
        for col2 in df.columns:
            ps[i].append(pps.score(df,col1,col2)['ppscore'])
    return np.array(ps)

def dataexploration(df):
    # Graphs
    distributions_plots=html.Div(id='hist_plot',children=[])
    pps_fig = go.Figure(data=go.Heatmap(z=get_pps_array(df), x=df.columns,y=df.columns))
    pps_fig.update_layout(title='Heat Map for Predicted Power Score')
    association_structure=html.Div(children=[get_radios(),


    html.Div([dcc.Dropdown(id='col1',options=[{ 'label': f"{col} ( {df[col].dtype} )", 'value': col} for col in df.columns 
       
    ])], style={'width': '48%', 'display': 'inline-block','margin': '10px 0 10px 10px'} ),

    html.Div([dcc.Dropdown(id='col2',options=[{ 'label': f"{col} ( {df[col].dtype} )", 'value': col} for col in df.columns 
       
    ])], style={'width': '48%', 'float': 'right', 'display': 'inline-block','margin': '10px 10px 10px 0'} ),

      html.Div(id='corr',children=[],style={'dislay':'block'}),
      dbc.Button("Show/Hide", outline=True, color="success", className="mr-1",id='show-more',style={'margin': '10px 10px 10px 10px'}),
      html.Div(style={'display':'none'},id='heatmap',children=[html.Div([dcc.Graph(figure=pps_fig)],id='heatmap-figure')])
    
    
    ])



    stats_analysis=html.Div([html.P(f'  DataFrame shape = {df.shape}'),dbc.Table.from_dataframe(df.describe().reset_index(), striped=True, bordered=True, hover=True,dark=True)])
    
    # Tab layout
    data_exploration_structure=html.Div(children=[html.Div(children=[columns_dropdown(df)],style={'width': '65%', 'display': 'inline-block','margin': '0 0 10px 10px'}),
                             html.Div(children=[plotly_templates()],style={'width': '30%', 'float': 'right', 'display': 'inline-block','margin': '0 10px 10px 0'})])
    tabs=html.Div(children=[nav,dcc.Tabs(id='tabs', value='tab-1', children=[
        dcc.Tab(style=tab_style, selected_style=tab_selected_style,label='Data Distributions', value='tab-1',
                                                        children=[data_exploration_structure,distributions_plots]),
        dcc.Tab(style=tab_style, selected_style=tab_selected_style,label='Statistical Analysis', value='tab-2',
                                                children=[stats_analysis]),
        dcc.Tab(style=tab_style, selected_style=tab_selected_style,label='Association', value='tab-3',
                                                children=[association_structure])
    ], style=tabs_styles)])
    return tabs