import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State, MATCH, ALL
import dash_bootstrap_components as dbc
from .plots import App, plot_graph, add_parameters, _params
from .homepage import Homepage
from jupyter_dash import JupyterDash
import pandas as pd
import logging
import plotly.graph_objects as go
from .data_exploration import dataexploration, plot_distributions ,association,get_pps_array,get_corr_array
from win32api import GetSystemMetrics
WIDTH = GetSystemMetrics(0)-400
added_params_value=[]
external_stylesheets = [dbc.themes.BOOTSTRAP,{
    'href': 'https://use.fontawesome.com/releases/v5.8.1/css/all.css',
    'rel': 'stylesheet',
    'integrity': 'sha384-50oBUHEmvpQ+1lW4y57PTFmhCaXp0ML5d60M1M7uH2+nqUivzIebhndOJK28anvf',
    'crossorigin': 'anonymous'
}]



def run_app(df):
    app = JupyterDash(__name__, external_stylesheets=external_stylesheets,suppress_callback_exceptions=True)
    app.config.suppress_callback_exceptions = True
    app.layout = html.Div([
    dcc.Location(id = 'url', refresh = False),
    html.Div(id = 'page-content')])
    try:
        @app.callback(Output('page-content', 'children'),[Input('url', 'pathname')])
        def display_page(pathname):
            if pathname == '/plot':
                return App(df)
            elif pathname == '/data-exploration':
                return dataexploration(df)
            else:
                return Homepage(df)

        @app.callback(Output('hist_plot','children'),[Input('hist_col_dropdown','value'),Input('theme_dropdown','value')])
        def update_data_distribution(col_list,theme):
            children = plot_distributions(df,col_list,theme)
            return children
        
        @app.callback([Output('corr','children'),Output('heatmap','style'),Output('heatmap-figure','children')],
                        [Input('col1','value'),Input('col2','value'),Input('asso_type','value'),Input('show-more','n_clicks')])
        def update_association(col1,col2,asso_type,n):
            heat_map_style={'display':'none'}
            heat_map_child=[]
            try:
                corr_child=association(df,asso_type,col1,col2)
            except (TypeError):
                corr_child=[html.P('Please select numeric columns', style={'color':'red'})]
            if n is not None:
                if n%2==1:
                    heat_map_style=_params()
            if asso_type=='Predictive Power Score':
                pps_fig = go.Figure(data=go.Heatmap(z=get_pps_array(df), x=df.columns,y=df.columns))
                pps_fig.update_layout(title='Heat Map for Predicted Power Score')
                heat_map_child=[dcc.Graph(figure=pps_fig)]
            if asso_type=='Correlation':
                corr_arr=get_corr_array(df)
                corr_fig=go.Figure(data=go.Heatmap(z=corr_arr, x=corr_arr.index,y=corr_arr.columns))
                corr_fig.update_layout(title='Heat Map for Correlation')
                heat_map_child=[dcc.Graph(figure=corr_fig)]

            return corr_child,heat_map_style,heat_map_child

        @app.callback([Output('output_plots','children'),Output('add-parameter-drop','options'),Output('color_div','style'),
        Output('facet_col_div','style'),Output('margin_x_div','style'),Output('margin_y_div','style'),Output('trendline_div','style'),
        Output('size_div','style'),Output('animation_div','style'),Output('opacity_div','style'),Output('barmode_div','style'),
        Output('boxmode_div','style'),Output('q_div','style'),Output('points_div','style')],
        [Input('charttype','value'), Input('xaxis','value'), Input('yaxis','value'), Input('theme_dropdown','value'), 
        Input('add-parameter-drop','value'),Input('color','value'),Input('facet_col','value'),Input('margin-x','value'),
        Input('margin-y','value'),Input('trendline','value'),Input('size','value'),Input('animation','value'),Input('opacity','value'),
        Input('barmode','value'), Input('boxmode','value'),Input('q','value'),Input('points','value')])
        def update_plots(chart_type,x,y,theme,added_params,color,facet_col,margin_x,margin_y,trendline,size,animation,opacity,barmode,boxmode,q,points):
            color_style = {'display': 'none'}
            facet_col_style = {'display': 'none'}
            margin_x_style = {'display': 'none'}
            margin_y_style = {'display': 'none'}
            trendline_style={'display':'none'}
            size_style = {'display':'none'}
            animation_style = {'display':'none'}
            opacity_style={'display': 'none'}
            barmode_style = {'display': 'none'}
            boxmode_style = {'display': 'none'}
            q_style={'display': 'none'}
            points_style={'display': 'none'}

            facet_col_val,color_val, margin_x_val,margin_y_val,trendline_val,size_val,animation_val,opacity_val,barmode_val,boxmode_val,q_val,points_val,notched_val=None,None,None,None,None,None,None,1,'relative','group','linear','outliers',False
            box_val=False
            log_x = False
            log_y = False
            for param in added_params:
                if param == 'log_x':
                    log_x=True
                if param=='log_y':
                    log_y=True
                if param=='color':
                    color_style = _params()
                    color_val=color
                if param=='facet_col':
                    facet_col_style = _params()
                    facet_col_val=facet_col
                if param == 'marginal_x':
                    margin_x_style= _params()
                    margin_x_val = margin_x
                if param == 'marginal_y':
                    margin_y_style=_params()
                    margin_y_val=margin_y
                if param=='trendline':
                    trendline_style=_params()
                    trendline_val=trendline
                if param=='size':
                    size_style = _params()
                    size_val=size
                if param == 'animation_frame':
                    animation_style=_params()
                    animation_val = animation
                if param == 'opacity':
                    opacity_style=_params()
                    opacity_val=opacity

                if param ==  'barmode':
                    barmode_style=_params()
                    barmode_val=barmode

                if param == 'mode':
                    boxmode_style=_params()
                    boxmode_val=boxmode
                if param == 'quartilemethod':
                    q_style=_params()
                    q_val=q
                if param == 'points':
                    points_style=_params()
                    points_val=points
                if param == 'notched':
                    notched_val=True
                if param == 'box':
                    box_val=True
            options = add_parameters(chart_type)
            plot_children = plot_graph(plot_type=chart_type,df=df,x=x,y=y,theme=theme,color=color_val,facet_col=facet_col_val,
                                    marginal_x=margin_x_val,marginal_y=margin_y_val,trendline=trendline_val,log_x=log_x,log_y=log_y,size=size_val,
                                    animation_frame =animation_val,opacity=opacity_val,barmode=barmode_val,boxmode=boxmode_val,
                                    quartilemethod=q_val,points=points_val,notched=notched_val,box=box_val)
           
            return plot_children, options, color_style, facet_col_style , margin_x_style, margin_y_style, trendline_style , size_style ,animation_style, opacity_style, barmode_style, boxmode_style,q_style,points_style    

        app.run_server(mode='inline',width=WIDTH,port=12345)
    except:
        app.run_server(mode='inline',width=WIDTH,port=12345)


