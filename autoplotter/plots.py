### Graphing
import plotly.graph_objects as go
import plotly.express as px
### Dash
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input

## Navbar
from .navbar import Navbar
from .data_exploration import plotly_templates
import logging

#px.scatter.__code__.co_varnames
added_param_label_style={'padding':'0 0 0 10px','font-weight': 'bold'}

def add_parameters(plot_type):
    scatter=['color','size','facet_col','animation_frame','opacity',
             'marginal_x','marginal_y','trendline','log_x','log_y']
    parallel_categories=['dimensions','color']
    parallel_coordinates=['dimensions','color']
    line=['color','facet_col','animation_frame','log_x','log_y']
    area=['color','facet_col','animation_frame','log_x','log_y']
    density_contour=['z','color','facet_col','animation_frame','marginal_x','marginal_y','log_x','log_y']
    density_heatmap=['z','facet_col','animation_frame','marginal_x','marginal_y','log_x','log_y']
    bar=['color','facet_col','animation_frame','opacity','barmode','log_x','log_y']
    histogram=['color','facet_col','animation_frame','opacity','barmode','log_x','log_y']
    box=['color','facet_col','quartilemethod','points','animation_frame','mode','log_x','log_y','notched']
    violin=['color','facet_col','animation_frame','mode','points','log_x','log_y','box']
    if plot_type=='line':
        return [{'label': i,'value' : i} for i in line]
    elif plot_type=='scatter':
        return [{'label': i,'value' : i} for i in scatter]
    elif plot_type=='parallel_categories':
        return [{'label': i,'value' : i} for i in parallel_categories]
    elif plot_type=='parallel_coordinates':
        return [{'label': i,'value' : i} for i in parallel_coordinates]
    elif plot_type=='area':
        return [{'label': i,'value' : i} for i in area]
    elif plot_type=='density_contour':
        return [{'label': i,'value' : i} for i in density_contour]
    elif plot_type=='density_heatmap':
        return [{'label': i,'value' : i} for i in density_heatmap]
    elif plot_type=='bar':
        return [{'label': i,'value' : i} for i in bar]
    elif plot_type=='histogram':
        return [{'label': i,'value' : i} for i in histogram]
    elif plot_type=='box':
        return [{'label': i,'value' : i} for i in box]
    elif plot_type=='violin':
        return [{'label': i,'value' : i} for i in violin]
    else:
        return []



def x_dropdown(df):
    dropdown=html.Div(children=[html.Label('X Axis'),dcc.Dropdown(id='xaxis', placeholder='Select X axis',
    options=[
        {'label': f"{col} ( {df[col].dtype} )", 'value': col} for col in df.columns
       
    ],value=None,multi=False)]) 
    return dropdown

def y_dropdown(df):
    dropdown=html.Div(children=[html.Label('Y Axis'),dcc.Dropdown(id='yaxis', placeholder='Select Y axis',
    options=[
        {'label': f"{col} ( {df[col].dtype} )", 'value': col} for col in df.columns
       
    ],value=None,multi=True)]) 
    return dropdown

nav = Navbar()
header = html.H3(
    'Select the name of an Illinois city to see its population!'
)


def all_plots():
    plots=['scatter','line','area','bar','histogram','box','violin']
    all_plots_dropdown = html.Div(
    children=[html.Label('Choose Plot Type '),
    dcc.Dropdown(id='charttype',options=[{'label':chart,'value':chart} for chart in plots], value='scatter',placeholder='Select a chart type')])
    return all_plots_dropdown

def axes(df):
    axis=html.Div(children=[html.Div(children=[x_dropdown(df)],style={'width': '50%', 'display': 'inline-block'}),
                             html.Div(children=[y_dropdown(df)],style={'width': '50%', 'float': 'right', 'display': 'inline-block'})])
    return axis                        

def App(df):  
    output = html.Div(id = 'output_plots',children=[])  
    charts=html.Div(children=[html.Div(children=[all_plots()] ,
                            style={'width': '25%', 'display': 'inline-block','margin': '0 0 0 10px'}),
                             html.Div(children=[plotly_templates()],
                            style={'width': '20%', 'display': 'inline-block','margin': '0 10px 0 0'}),
                             html.Div(children=[axes(df)],
                            style={'width': '50%', 'float': 'right', 'display': 'inline-block','margin': '0 10px 10px 0'})])
    add_parameters_dropdown=html.Div(children=[html.Label('Choose a Parameter'),
                    dcc.Dropdown(id='add-parameter-drop',options=[],placeholder='Add Params..',value=[],multi=True)])
    
    
    color_div=html.Div(style={'display': 'none'},id='color_div',children=[html.Div(html.Label('Color '),
            style=added_param_label_style),html.Div(dcc.Dropdown(id='color', placeholder='Color Column',
    options=[{'label': f"{col} ( {df[col].dtype} )", 'value': col} for col in df.columns],
                value=None,multi=False) ,style={})])

    size_div=html.Div(style={'display': 'none'},id='size_div',children=[html.Div(html.Label('Size'),
            style=added_param_label_style),html.Div(dcc.Dropdown(id='size', placeholder='Size',
    options=[{'label': f"{col} ( {df[col].dtype} )", 'value': col} for col in df.columns],
                value=None,multi=False) ,style={})])
    
    
    facet_col_div = html.Div(style={'display': 'none'},id='facet_col_div',children=[html.Div(html.Label('Facet Column'),
            style=added_param_label_style),html.Div(dcc.Dropdown(id='facet_col', placeholder='Facet Column',
    options=[{'label': f"{col} ( {df[col].dtype} )", 'value': col} for col in df.columns],
                value=None,multi=False),style={})])
    
    
    margin_x_div = html.Div(style={'display': 'None'},id='margin_x_div',children=[html.Div(html.Label('Margin X'),
            style=added_param_label_style),html.Div(dcc.RadioItems(id='margin-x',
    options=[{'label': i, 'value': i} for i in ('rug', 'box', 'violin', 'histogram')],
                value=None,labelStyle={'display': 'inline-block'},inputStyle={'margin':'10px 10px 10px 10px'}) ,style={})])

    
    margin_y_div  = html.Div(style={'display': 'none'},id='margin_y_div',children=[html.Div(html.Label('Margin Y'),
            style=added_param_label_style),html.Div(dcc.RadioItems(id='margin-y',
    options=[{'label': i, 'value': i} for i in ('rug', 'box', 'violin', 'histogram')],
                value=None,labelStyle={'display': 'inline-block'},inputStyle={'margin':'10px 10px 10px 10px'}) ,style={})])
    

    trendline_div = html.Div(style={'display': 'None'},id='trendline_div',children=[html.Div(html.Label('Trendline'),
            style=added_param_label_style),html.Div(dcc.RadioItems(id='trendline',
    options=[{'label': 'Ordinary Least Square', 'value': 'ols'},
            {'label': 'Locally Weighted Scatterplot Smoothing line ', 'value': 'lowess'}],value=None,
    labelStyle={'display': 'inline-block'},inputStyle={'margin':'10px 10px 10px 10px'}))])


    animation_div=html.Div(style={'display': 'none'},id='animation_div',children=[html.Div(html.Label('Animated Frame '),
            style=added_param_label_style),html.Div(dcc.Dropdown(id='animation', placeholder='Animated Frame Column',
    options=[{'label': f"{col} ( {df[col].dtype} )", 'value': col} for col in df.columns],
                value=None,multi=False) ,style={})])

    opacity_div=html.Div(style={'display': 'none'},id='opacity_div',children=[html.Div(html.Label('Opacity Value'),
            style=added_param_label_style),html.Div(dcc.Slider(id='opacity',min=0,max=1,step=0.1,value=1,)) ])

    
    barmode_div = html.Div(style={'display': 'None'},id='barmode_div',children=[html.Div(html.Label('Bar Mode'),
            style=added_param_label_style),html.Div(dcc.RadioItems(id='barmode',
    options=[{'label': i, 'value': i} for i in ('group', 'overlay', 'relative' )],
                value='relative',labelStyle={'display': 'inline-block'},inputStyle={'margin':'10px 10px 10px 10px'}) ,style={})])
    
    boxmode_div = html.Div(style={'display': 'None'},id='boxmode_div',children=[html.Div(html.Label('Box Mode'),
            style=added_param_label_style),html.Div(dcc.RadioItems(id='boxmode',
    options=[{'label': i, 'value': i} for i in ('group', 'overlay' )],
                value='group',labelStyle={'display': 'inline-block'},inputStyle={'margin':'10px 10px 10px 10px'}) ,style={})])
    
    q_div = html.Div(style={'display': 'None'},id='q_div',children=[html.Div(html.Label('Quartile Method'),
            style=added_param_label_style),html.Div(dcc.RadioItems(id='q',
    options=[{'label': i, 'value': i} for i in ('linear', 'inclusive','exclusive' )],
                value='linear',labelStyle={'display': 'inline-block'},inputStyle={'margin':'10px 10px 10px 10px'}) ,style={})])

    points_div = html.Div(style={'display': 'None'},id='points_div',children=[html.Div(html.Label('Points'),
            style=added_param_label_style),html.Div(dcc.RadioItems(id='points',
    options=[{'label': i, 'value': i} for i in ('outliers', 'suspectedoutliers', 'all' )],
                value='outliers',labelStyle={'display': 'inline-block'},inputStyle={'margin':'10px 10px 10px 10px'}) ,style={})])

    
    layout = html.Div([nav,charts,add_parameters_dropdown,color_div,size_div,trendline_div,facet_col_div, 
                        margin_x_div ,margin_y_div,animation_div,opacity_div,barmode_div,q_div,boxmode_div,points_div,output])
    return layout

def plot_graph(plot_type,df,x,y,theme,color=None,facet_col=None,marginal_x=None,marginal_y=None,trendline=None,log_x=None,log_y=None,size=None,animation_frame=None,opacity=1,barmode='relative',boxmode=None,quartilemethod=None,points='outliers',notched=False,box=False):
    try:
        out=[]
        if plot_type == 'bar':
            fig=px.bar(data_frame=df,x=x,y=y,template=theme,color=color,facet_col=facet_col,log_x=log_x,log_y=log_y,opacity=opacity,animation_frame=animation_frame,barmode=barmode)
            fig.update_xaxes(showgrid=False)
            fig.update_yaxes(showgrid=False)
            out.append(html.Div(children=[dcc.Graph(figure=fig)]))        
            return out
        elif plot_type == 'line':
            fig=px.line(data_frame=df,x=x,y=y,template=theme,color=color,facet_col=facet_col,log_x=log_x,log_y=log_y,animation_frame=animation_frame)
            fig.update_xaxes(showgrid=False)
            fig.update_yaxes(showgrid=False)
            out.append(html.Div(children=[dcc.Graph(figure=fig)]))
            return out
        elif plot_type=='area':
            fig=px.area(data_frame=df,x=x,y=y,template=theme,color=color,facet_col=facet_col,log_x=log_x,log_y=log_y,animation_frame=animation_frame)
            fig.update_xaxes(showgrid=False)
            fig.update_yaxes(showgrid=False)
            out.append(html.Div(children=[dcc.Graph(figure=fig)]))
            return out
        elif plot_type=='box':
            fig=px.box(data_frame=df,x=x,y=y,template=theme,color=color,facet_col=facet_col,log_x=log_x,log_y=log_y,animation_frame=animation_frame,boxmode=boxmode,points=points,notched=notched)
            fig.update_xaxes(showgrid=False)
            fig.update_yaxes(showgrid=False)
            fig.update_traces(quartilemethod=quartilemethod,boxmean='sd')
            out.append(html.Div(children=[dcc.Graph(figure=fig)]))
            return out
        elif plot_type=='violin':
            fig=px.violin(data_frame=df,x=x,y=y,template=theme,color=color,facet_col=facet_col,log_x=log_x,log_y=log_y,animation_frame=animation_frame,violinmode=boxmode,points=points,box=box)
            fig.update_xaxes(showgrid=False)
            fig.update_yaxes(showgrid=False)
            fig.update_traces(meanline_visible=True)
            out.append(html.Div(children=[dcc.Graph(figure=fig)]))
            return out
        elif plot_type=='histogram':
            fig=px.histogram(data_frame=df,x=x,y=y,template=theme,color=color,facet_col=facet_col,log_x=log_x,log_y=log_y,opacity=opacity,animation_frame=animation_frame)
            fig.update_xaxes(showgrid=False)
            fig.update_yaxes(showgrid=False)
            out.append(html.Div(children=[dcc.Graph(figure=fig)]))
            return out
        elif plot_type=='parallel_categories':
            fig=px.parallel_categories(data_frame=df,template=theme,color=color,)
            fig.update_xaxes(showgrid=False)
            fig.update_yaxes(showgrid=False)
            out.append(html.Div(children=[dcc.Graph(figure=fig)]))
            return out
        elif plot_type=='parallel_coordinates':
            try:
                fig=px.parallel_coordinates(data_frame=df,template=theme,color=color)
                fig.update_xaxes(showgrid=False)
                fig.update_yaxes(showgrid=False)
                out.append(html.Div(children=[dcc.Graph(figure=fig)]))
                return out
            except (ValueError) as e:
                logging.warning(e)
        else:
            fig=px.scatter(data_frame=df,x=x,y=y,template=theme,color=color,facet_col=facet_col,marginal_x=marginal_x,marginal_y=marginal_y,trendline=trendline,log_x=log_x,log_y=log_y,size=size,opacity=opacity,animation_frame=animation_frame)
            fig.update_xaxes(showgrid=False)
            fig.update_yaxes(showgrid=False)
            out.append(html.Div(children=[dcc.Graph(figure=fig)]))
            return out
    except (TypeError,ValueError) as e:
        logging.warning(e)



def _params():
    return {'display':'block'}
    
