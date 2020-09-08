import dash_bootstrap_components as dbc
import dash_html_components as  html
import dash_core_components as dcc
from .side_navbar import _navbar
from .jupyter_dash import JupyterDash
from .style_sheet import *
from dash.dependencies import Input, Output, State
from .homepage import homepage
from collections import OrderedDict
from .plots_layout import plot_layout,plot_graph, add_parameters, _params, add_layer
from .data_exploration import dataexploration, plot_distributions, association





def run_app(df,mode='inline',host='127.0.0.1',port = 8050):
    """ Returns the User Interface for Data Analysis
    ----------------------------------------------------------------------------------


    Args:
    -----------------------------------------------------------------------------------
        df (Pandas Dataframe): Pandas dataframe on which the analyis is to be performed
        mode (str, optional):  Mode defines whether you want to run analysis 
                               inside the jupyter or outside the jupyter.
                               Possible Values ('inline','external'). 
                               Defaults to 'inline'.
        host (str, optional):  Base URL to run autoplotter. 
                               Defaults to '127.0.0.1'.
        port (int, optional):  Port to run autoplotter. 
                               Defaults to 8050.
    
    -------------------------------------------------------------

    Returns:
    -------------------------------------------------------------
        When mode = 'inline':
            Dash App: Dash app with leverages to do data analysis. 
        When mode = 'external':
            URL on which dash app is hosted.
    
    ----------------------------------
    
    Use:
    -----------------------------------

        import pandas as pd
        from autoplotter import run_app
        df=pd.read_csv(path_to_file)
        run_app(df)

    """
    global N_CLICKS, N_CLICKS2,CHART,CHART2
    app=JupyterDash(external_stylesheets=external_stylesheets,update_title='Loading...',serve_locally=False,
                        meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],)
    app.config.assets_external_path='https://github.com/ersaurabhverma/autoplotter/raw/master/assets/'
    app.scripts.config.serve_locally = False
    sidebar=_navbar(plot_icons,side_bar_buttons,side_nav_style,app)
    app.title='AutoPlotter'
    app.index_string="""
    <!DOCTYPE html>
        <html>
            <head>
                {%metas%}
                <title>{%title%}</title>
                <link rel="icon" href="https://github.com/ersaurabhverma/autoplotter/raw/master/assets/favicon.ico" type="image/x-icon" sizes="16x16">
                {%css%}
            </head>
            <body style= "background-color:#dedede;">
                {%app_entry%}
                <footer>
                    {%config%}
                    {%scripts%}
                    {%renderer%}
                </footer>
            </body>
        </html>
    """
    # getting homepage layout
    table=homepage(df,side_bar_buttons,data_type_style_h,data_type_style_p)
    # getting plot area layout
    plots=plot_layout(plot_icons,plot_buttons,margin_12,inline,dropdown_style,label_style,radio_style,value_style,app,df)
    # getting data analysis layout
    exploration_layout=dataexploration(df,margin_12,margin_10,dropdown_style,side_bar_buttons,radio_style,data_type_style_p)
    # setting up the app layout
    app.layout=html.Div([dcc.Location(id = 'url', refresh = False,),
    html.Div(children=[sidebar,html.Div([table],id='page-content',style=main_window)],style=body),],style=all_)
    N_CLICKS = OrderedDict([('box',0), ('bar',0),('scatter',0),('line',0),('area',0),\
                            ('violin',0),('histogram',0),('treemap',0),('waterfall',0),('heatmap',0),\
                            ('pie',0),('sunburst',0)])
    N_CLICKS2=OrderedDict([('box',0), ('bar',0),('scatter',0),('line',0),('area',0),('violin',0),('histogram',0)])
    CHART  = {'chart_type':'scatter'}
    CHART2 = {'chart_type':'box'}
    @app.callback([Output('page-content', 'children'),Output('datatable','style'),Output('plots','style'),
                                                    Output('analysis','style')],[Input('url', 'pathname')])
    def display_page(pathname):
        table_button=side_bar_buttons
        plot_button=side_bar_buttons
        analysis_button=side_bar_buttons
        if ( pathname == '/analysis' ):
            analysis_button=selected_button
            return exploration_layout, table_button, plot_button, analysis_button
        elif ( pathname == '/plots' ):
            plot_button=selected_button
            return plots, table_button, plot_button, analysis_button
        elif ( pathname == '/home' ) or ( pathname == '/' ):
            table_button=selected_button
            return table, table_button, plot_button, analysis_button
        
        return dbc.Jumbotron(
        [html.H1("404: Not found", className="text-danger"),
        html.Hr(),
        html.P(f"The pathname {pathname} was not recognised..."),],style=main_window),table_button, plot_button, analysis_button

        
    @app.callback(
    Output("collapse_", "is_open"),
    [Input("collapse-button", "n_clicks")],
    [State("collapse_", "is_open")])
    def toggle_collapse(n, is_open):
        if n:
            return not is_open
        return is_open


    @app.callback([Output('plot-area','children'),Output('add-parameter-drop','options'),Output('color_div','style'),

        Output('facet_col_div','style'),Output('margin_x_div','style'),Output('margin_y_div','style'),Output('trendline_div','style'),

        Output('size_div','style'),Output('animation_div','style'),Output('opacity_div','style'),Output('barmode_div','style'),

        Output('boxmode_div','style'),Output('q_div','style'),Output('points_div','style'),Output('add_layer_div','style'),

        Output('box','style'),Output('bar','style'),Output('scatter','style'),Output('area','style'),Output('line','style'),

        Output('violin','style'),

        Output('histogram','style'),Output('heatmap','style'),Output('treemap','style'),Output('waterfall','style'),

        Output('pie','style'), Output('sunburst','style'),

        Output('x-axis-label','children'),Output('y-axis-label','children'),Output('x-axis','placeholder'),Output('y-axis','placeholder'),

        Output('agg_funcs_div','style'),Output('z-axis-label','children'),Output('add-parameter-drop','placeholder'),

        Output('add-parameter-drop','multi'), Output('y-axis','multi'), Output('x-axis','options'), Output('y-axis','options')],

        [Input('box', 'n_clicks'),Input('bar', 'n_clicks'),Input('scatter', 'n_clicks'),Input('line', 'n_clicks'),Input('area', 'n_clicks'),

        Input('violin', 'n_clicks'),Input('histogram', 'n_clicks'),Input('treemap', 'n_clicks'),

        Input('waterfall','n_clicks'),Input('heatmap','n_clicks'),

        Input('pie','n_clicks'),Input('sunburst','n_clicks'),

        Input('box2', 'n_clicks'),Input('bar2', 'n_clicks'),Input('scatter2', 'n_clicks'),

        Input('line2', 'n_clicks'),Input('area2', 'n_clicks'),

        Input('violin2', 'n_clicks'),

        Input('x-axis','value'), Input('y-axis','value'), Input('theme_dropdown','value'), 

        Input('add-parameter-drop','value'),Input('color','value'),Input('facet_col','value'),Input('margin-x','value'),

        Input('margin-y','value'),Input('trendline','value'),Input('size','value'),Input('animation','value'),Input('opacity','value'),

        Input('barmode','value'), Input('boxmode','value'),Input('q','value'),Input('points','value'),Input('y-axis2','value'),

        Input('agg_funcs','value')])

    def update_plots(box,bar,scatter,line,area,violin,histogram,treemap,waterfall,heatmap,\
        pie,sunburst,\
        box2,bar2,scatter2,line2,area2,violin2,x,y,theme,added_params,color,facet_col,\
        margin_x,margin_y,trendline,size,animation,opacity,barmode,boxmode,q,points,y2,agg_func):
        global N_CLICKS, N_CLICKS2,CHART,CHART2
        color_style =       {'display': 'none'}
        facet_col_style =   {'display': 'none'}
        margin_x_style =    {'display': 'none'}
        margin_y_style =    {'display': 'none'}
        trendline_style=    {'display': 'none'}
        size_style =        {'display': 'none'}
        animation_style =   {'display': 'none'}
        opacity_style=      {'display': 'none'}
        barmode_style =     {'display': 'none'}
        boxmode_style =     {'display': 'none'}
        q_style=            {'display': 'none'}
        points_style=       {'display': 'none'}
        add_layer_div_style={'display': 'none'}
        agg_funcs_style =   {'display': 'none'}
        box_button_style = plot_buttons
        bar_button_style = plot_buttons
        scatter_button_style = plot_buttons
        area_button_style = plot_buttons
        line_button_style = plot_buttons
        violin_button_style = plot_buttons
        histogram_button_style = plot_buttons
        heatmap_button_style = plot_buttons
        treemap_button_style = plot_buttons
        waterfall_button_style = plot_buttons
        sunburst_button_style = plot_buttons
        pie_button_style = plot_buttons
        x_axis_label = 'X-axis'
        y_axis_label = 'Y-axis'
        x_axis_placeholder = 'X-axis'
        y_axis_placeholder = 'Y-axis'
        z_axis_label = 'Choose a Parameter'
        z_axis_placeholder = 'Add Params...'
        z_drop_multi = True
        y_drop_multi = True
        categorical = df.select_dtypes(include = 'object').columns
        numerical = df.select_dtypes(exclude = 'object').columns
        categotical_opts =[{'label': f"{col} ( object )", 'value': col} for col in categorical]
        numerical_opts =[{'label': f"{col} ( {df[col].dtype} )", 'value': col} for col in numerical]
        all_opts = [{'label': f"{col} ( {df[col].dtype} )", 'value': col} for col in df.columns]
        x_opts = all_opts
        y_opts = all_opts

        for (button, n_click_old), n_click_new in zip(N_CLICKS.items(), (box,bar,scatter,line,area,violin,histogram,\
                                                                        treemap,waterfall,heatmap,pie,sunburst)):
            if n_click_new > n_click_old:
                CHART['chart_type'] = button
                N_CLICKS[button] = n_click_new
                break
        chart_type=CHART['chart_type']
        if chart_type == 'box':
            box_button_style=selected_button
            y_drop_multi = False
        elif chart_type == 'bar':
            bar_button_style=selected_button
        elif chart_type == 'scatter':
            scatter_button_style=selected_button
        elif chart_type == 'area':
            area_button_style=selected_button
        elif chart_type == 'line':
            line_button_style=selected_button
        elif chart_type == 'violin':
            y_drop_multi = False
            violin_button_style=selected_button
        elif chart_type == 'histogram':
            histogram_button_style=selected_button
        elif chart_type == 'heatmap':
            heatmap_button_style=selected_button
            x_opts = categotical_opts
            y_opts = categotical_opts
            z_axis_label = 'Value'
            z_axis_placeholder = 'Select Value Columns'
            z_drop_multi = False
            y_drop_multi = False
        elif chart_type == 'treemap':
            treemap_button_style=selected_button
            x_opts = numerical_opts
            y_opts = categotical_opts
            x_axis_label = 'Values'
            y_axis_label = 'Path'
            x_axis_placeholder = 'Values'
            y_axis_placeholder = 'Path'
        elif chart_type == 'waterfall':
            waterfall_button_style=selected_button
            x_opts = categotical_opts
            y_opts = numerical_opts
            y_drop_multi = False
        elif chart_type == 'sunburst':
            sunburst_button_style = selected_button
            x_opts = numerical_opts
            y_opts = categotical_opts
            x_axis_label = 'Values'
            y_axis_label = 'Path'
            x_axis_placeholder = 'Values'
            y_axis_placeholder = 'Path'
        elif chart_type == 'pie':
            pie_button_style = selected_button
            x_opts = categotical_opts
            y_opts = numerical_opts
            x_axis_label = 'Names'
            y_axis_label = 'Values'
            x_axis_placeholder = 'Names'
            y_axis_placeholder = 'Values'
            y_drop_multi = False
        else:
            pass

        facet_col_val,color_val, margin_x_val,margin_y_val,trendline_val,size_val,animation_val,opacity_val,\
        barmode_val,boxmode_val,q_val,points_val,notched_val=None,None,None,None,None,None,None,1,'relative','group',\
                'linear','outliers',False
        box_val=False
        log_x = False
        log_y = False
        show_label = False
        if isinstance(added_params,list):
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
                if param =='Add Layer':
                    add_layer_div_style =_params()
                if param == 'Aggregation Function':
                    agg_funcs_style = _params()
                if param == 'Show Label':
                    show_label = True
        for (button, n_click_old), n_click_new in zip(N_CLICKS2.items(), (box2,bar2,scatter2,line2,area2,violin2)):
            if n_click_new > n_click_old:
                CHART2['chart_type'] = button
                N_CLICKS2[button] = n_click_new
                break
        new_layer_type=CHART2['chart_type']
        options = add_parameters(chart_type,df)
        try:
            plot_children, existing_fig = plot_graph(plot_type=chart_type,df=df,x=x,y=y,theme=theme,value = added_params,color=color_val,facet_col=facet_col_val,
                                marginal_x=margin_x_val,marginal_y=margin_y_val,trendline=trendline_val,log_x=log_x,log_y=log_y,
                                size=size_val,
                                animation_frame =animation_val,opacity=opacity_val,barmode=barmode_val,boxmode=boxmode_val,
            
                                quartilemethod=q_val,points=points_val,notched=notched_val,box=box_val,agg_func=agg_func,show_label=show_label,)
            if isinstance(added_params,list) and 'Add Layer' in added_params:
                plot_children= add_layer(existing_fig,new_layer_type,df,x,y2,theme)
            return plot_children, options, color_style, facet_col_style , margin_x_style, margin_y_style, \
                trendline_style , size_style ,animation_style, opacity_style, \
                barmode_style, boxmode_style,q_style,points_style,add_layer_div_style,\
                box_button_style,bar_button_style,scatter_button_style,area_button_style,\
                line_button_style,violin_button_style,histogram_button_style,heatmap_button_style,\
                treemap_button_style,waterfall_button_style,pie_button_style,sunburst_button_style,\
                x_axis_label,y_axis_label,\
                x_axis_placeholder,y_axis_placeholder,agg_funcs_style,z_axis_label,z_axis_placeholder,\
                z_drop_multi, y_drop_multi, x_opts, y_opts
        
        except Exception as e:
            
            return [html.Div(str(e))],options, color_style, facet_col_style , margin_x_style, \
                margin_y_style, trendline_style , size_style ,animation_style, opacity_style, \
                barmode_style, boxmode_style,q_style,points_style,add_layer_div_style,box_button_style,\
                bar_button_style,scatter_button_style,area_button_style,line_button_style,\
                violin_button_style,histogram_button_style,heatmap_button_style,treemap_button_style,\
                waterfall_button_style,pie_button_style,sunburst_button_style,x_axis_label,\
                y_axis_label,x_axis_placeholder,y_axis_placeholder,\
                agg_funcs_style,z_axis_label,z_axis_placeholder,z_drop_multi, y_drop_multi, x_opts, y_opts
        
    

    @app.callback(Output('hist_plot','children'),[Input('hist_col_dropdown','value'),Input('theme_dropdown','value'),Input('dist_type','value')])
    def update_data_distribution(col_list,theme,dist_type):
        children = plot_distributions(df,col_list,theme,dist_type)
        return children

    @app.callback([Output('corr','children'),Output('heatmap_corr','style')],
                        [Input('col1','value'),Input('col2','value'),Input('show-more','n_clicks')])
    def update_association(col1,col2,n):
        heat_map_style={'display':'none'}
        try:
            corr_child=association(df,col1,col2)
        except (TypeError):
            corr_child=[html.P('Please select numeric columns', style={'color':'red'})]
        if n is not None:
            if n%2==1:
                heat_map_style=_params()

        return corr_child,heat_map_style

    @app.callback(Output("sidebar", "className"),[Input("sidebar-toggle", "n_clicks")],[State("sidebar", "className")])
    def toggle_classname(n, classname):
        if n and classname == "":
            return "collapsed"
        return ""


    @app.callback(Output("collapse", "is_open"),[Input("navbar-toggle", "n_clicks")],[State("collapse", "is_open")])
    def toggle_collapse(n, is_open):
        if n:
            return not is_open
        return is_open

          
    app.run_server(mode=mode,port=port,debug=True,host=host)