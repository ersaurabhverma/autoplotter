import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import numpy as np


def get_radios(): 
        button=html.Div(dcc.RadioItems(id='asso_type',options=[
                {'label': 'Predictive Power Score', 'value': 'Predictive Power Score'},
                {'label': 'Correlation', 'value': 'Correlation'}],value='Predictive Power Score',labelStyle={'display': 'inline-block','margin':'0 10px 0 10px'},inputStyle={'margin':'10px 10px 10px 10px'}))
        return button
  


def distribution_type(margin_10,radio_style):
    dist_radio=dbc.FormGroup(
    [dbc.RadioItems(
            options=[{"label": i, "value": i} for i in ['Histogram','Distribution']],
            id="dist_type",inline=True,value='Histogram',style=radio_style)],style=margin_10)
    return dist_radio




def plotly_templates(margin_12,radio_style):
    themes=['ggplot2', 'seaborn', 'plotly', 'plotly_dark', 'presentation']
    template=dbc.FormGroup(
    [dbc.RadioItems(
            options=[{"label": i, "value": i} for i in themes],
            id="theme_dropdown",inline=True,style=radio_style,value='presentation')],style=margin_12)
    return template

def get_missing_valaues(df,col):
    n=df[col].notna().sum()
    values=(n/df.shape[0])*100
    return values,n


tabs_styles = {
    'height': '44px',
    'position': 'static', 
    'top': '0px',
    'margin': '10px',
    'border' : '0px'
   
  
   
}
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold',
    'box-shadow': '-3px -3px 7px #fff, 3px 3px 5px rgba(94,104,121,0.712)',
    'border-radius':'10px'
   
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': 'rgb(200, 150, 150)',
    'color': 'white',
    'padding': '6px',
    'box-shadow': 'inset -3px -3px 7px #fff, inset 3px 3px 5px rgba(200, 150, 150,0.7)',
    'border-radius':'10px',
    'fontWeight': 'bold',
}

def columns_dropdown(df,dropdown_style):
    dropdown=html.Div(children=[html.Label('Select the columns'),dcc.Dropdown(id='hist_col_dropdown', placeholder='Select Columns',
    options=[
        {'label': f"{col} ( {df[col].dtype} )", 'value': col} for col in df.columns
       
    ],value=[df.columns[0]],multi=True,style=dropdown_style)]) 

    return dropdown

def plot_distributions(df,cols,theme,dist_type):
    out_plots=[]
    for col in cols:
        if df[col].dtype=='object':
            figure=px.histogram(df, x=col, color_discrete_sequence=['#C89696'],template=theme,hover_data=df.columns)
            figure.update_xaxes(showgrid=False)
            figure.update_yaxes(showgrid=False)
            figure.update_layout(title_text=f'Histogram of {col}')
            value,n=get_missing_valaues(df,col)
            progress=dbc.Progress(style={"height": "20px","margin":"10px 10px 10px 10px"},children=[dbc.Progress(f"{df.shape[0]-n} missing values",
            value=value, color="success", bar=True), 
            dbc.Progress(style={"height": "20px"},value=100-value,color="danger", bar=True)],multi=True,)
            out_plots.append(html.Div(children=[progress,dcc.Graph(figure=figure)]))
        else:
            if dist_type=='Distribution':
                hist_data = [df[col].fillna(method='bfill')]
                group_labels = [col]
                figure = ff.create_distplot(hist_data, group_labels,show_hist=False,show_rug=False,colors=['#C89696'],)
                figure.update_xaxes(showgrid=False)
                figure.update_yaxes(showgrid=False,showticklabels=False)
                figure.update_layout(title_text=f'Distribution of {col}',template=theme)
            else:
                figure=px.histogram(df, x=col, color_discrete_sequence=['#C89696'],template=theme,marginal="box",hover_data=df.columns)
                figure.update_xaxes(showgrid=False)
                figure.update_yaxes(showgrid=False)
                figure.update_layout(title_text=f'Histogram of {col}')
            value,n=get_missing_valaues(df,col)
            progress=dbc.Progress(style={"height": "20px","margin":"10px 10px 10px 10px"},children=[dbc.Progress(f"{df.shape[0]-n} missing values",
            value=value, color="success",  bar=True), 
            dbc.Progress(value=100-value,
            color="danger", bar=True)],multi=True)
            out_plots.append(html.Div(children=[progress,dcc.Graph(figure=figure)]))
    return out_plots


def association(df,col1,col2):
    if col1 is not None and col2  is not None:
        return [html.Label(f' Correlation between {col1} and {col2} = {df[col1].corr(df[col2])}',style={'margin':'10px 0 0 10px'})]



def get_corr_array(df):
    return df.corr()



def dataexploration(df,margin_12,margin_10,dropdown_style,side_bar_buttons,radio_style,data_type_style_p):
    distributions_plots=dbc.Card([dbc.CardBody([html.Div(id='hist_plot',children=[])])],style=side_bar_buttons)
    corr_arr=get_corr_array(df)
    corr_fig=go.Figure(data=go.Heatmap(z=corr_arr, x=corr_arr.index,y=corr_arr.columns,))
    corr_fig.update_layout(title='Heat Map for Correlation',template='presentation')

    association_structure=html.Div(children=[html.Div('Correlation'),


    html.Div([dcc.Dropdown(id='col1',options=[{ 'label': f"{col} ( {df[col].dtype} )", 'value': col} for col in df.columns 
       
     if df[col].dtype!='object'],style=dropdown_style)], style={'width': '48%', 'display': 'inline-block','margin': '10px 0 10px 10px'} ),

    html.Div([dcc.Dropdown(id='col2',options=[{ 'label': f"{col} ( {df[col].dtype} )", 'value': col} for col in df.columns 
       
    if df[col].dtype!='object'],style=dropdown_style)], style={'width': '48%', 'float': 'right', 'display': 'inline-block','margin': '10px 10px 10px 0'} ),

      html.Div(id='corr',children=[],style={'dislay':'block'}),
      dbc.Button("Show/Hide", outline=True, color="success", className="mr-1",id='show-more',style={'margin': '10px 10px 10px 10px'}),
      html.Div(style={'display':'none'},id='heatmap_corr',children=[dbc.Card(dbc.CardBody([html.Div([dcc.Graph(figure=corr_fig)],id='heatmap-figure')]),style=side_bar_buttons)])
    
    
    ])



    stats_analysis=html.Div([html.P(f'  DataFrame shape = {df.shape}',style=data_type_style_p),dbc.Table.from_dataframe(df.describe().reset_index().rename(columns={'index':'Measure'}), striped=True, bordered=True, hover=True,dark=True)])
    
    # Tab layout
    data_exploration_structure=html.Div(children=[html.Div(children=[plotly_templates(margin_12,radio_style)],),
                             html.Div(children=[columns_dropdown(df,dropdown_style)],style={'width': '60%', 'display': 'inline-block','margin': '0 0 12px 12px'}),
                             html.Div([distribution_type(margin_12,radio_style)],style={'width': '35%', 'float': 'right', 'display': 'inline-block','margin': '20px 12px 12px 0'})])
    tabs=html.Div(children=[dcc.Tabs(id='tabs', value='tab-1', children=[
        dcc.Tab(style=tab_style, selected_style=tab_selected_style,label='Data Distributions', value='tab-1',
                                                        children=[data_exploration_structure,distributions_plots]),
        dcc.Tab(style=tab_style, selected_style=tab_selected_style,label='Statistical Analysis', value='tab-2',
                                                children=[stats_analysis]),
        dcc.Tab(style=tab_style, selected_style=tab_selected_style,label='Association', value='tab-3',
                                                children=[association_structure])
    ], style=tabs_styles)])
    return tabs