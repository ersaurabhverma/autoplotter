import dash_bootstrap_components as dbc
import dash_html_components as html 
import dash_core_components as dcc
import plotly.express as px
import plotly.graph_objects as go
import logging
from plotly.subplots import make_subplots




def _waterfall_df(df,x,y,theme,agg_func='sum',orientation='v',show_label=False):
    dff= df.groupby(x,as_index=True,sort=False).agg({y:agg_func})[y].reset_index()
    initial = dff[y].iloc[0]
    value_sum = dff[y].sum()
    dff[y] = dff[y].diff(periods=1)
    dff[y].iloc[0] = initial
    dff = dff.append({x:'Total',y:value_sum},ignore_index=True)
    text = dff[y].astype(str).tolist()[:-1]+['Total'] if show_label == True else None
    fig = go.Figure(go.Waterfall(orientation = orientation,
                                 measure = sum([['relative'] for _ in range(df[x].unique().shape[0])],[])+['total'],
                                 x = dff[x],
                                 textposition = "outside",
                                 text = text,
                                 y = dff[y],
                                 connector = {"line":{"color":"rgb(63, 63, 63)"}}))

    fig.update_layout(title = None,showlegend = False,template=theme,waterfallgap = 0.3)
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)
    return fig


def _bar_df(df,x,y,template,log_x,log_y,opacity,barmode,agg_func='sum',orientation='v',show_label= False):
    dff= df.groupby(x,as_index=True,sort=False).agg({i:agg_func for i in y})
    dff = dff[y].reset_index()
    fig=px.bar(data_frame=dff,x=x,y=y,template=template,log_x=log_x,log_y=log_y,opacity=opacity,barmode=barmode)
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)
    return fig



def plot_layout(plot_icons,plot_buttons,margin_12,inline,dropdown_style,label_style,radio_style,value_style,app,df):
    """[summary]

    Args:
        plot_icons (dict): css for plot icons
        plot_buttons (dict): css for plot buttons
        margin_12 (dict): css
        inline (dict): css
        dropdown_style (dict): css
        app (JupyterDash Instance): 
        df (Pandas Dataframe): [description]

    Returns:
        Dash Layout: dash.Dash layout
    """

    color_div=html.Div(style={'display': 'none'},id='color_div',children=[html.Div(html.Label('Color',style=label_style),
            ),html.Div(dcc.Dropdown(id='color', placeholder='Color Column',
    options=[{'label': f"{col} ( {df[col].dtype} )", 'value': col} for col in df.columns],
                value=None,multi=False,style=dropdown_style) ,style={})])


    size_div=html.Div(style={'display': 'none'},id='size_div',children=[html.Div(html.Label('Size',style=label_style),
            ),html.Div(dcc.Dropdown(id='size', placeholder='Size',
    options=[{'label': f"{col} ( {df[col].dtype} )", 'value': col} for col in df.columns],
                value=None,multi=False,style=dropdown_style) ,style={})])
    
    
    facet_col_div = html.Div(style={'display': 'none'},id='facet_col_div',children=[html.Div(html.Label('Facet Column',style=label_style),
            ),html.Div(dcc.Dropdown(id='facet_col', placeholder='Facet Column',
    options=[{'label': f"{col} ( {df[col].dtype} )", 'value': col} for col in df.columns],
                value=None,multi=False,style=dropdown_style),style={})])
    
    
    margin_x_div = html.Div(style={'display': 'None'},id='margin_x_div',children=[html.Div(html.Label('Margin X',style=label_style),
            ),html.Div(dcc.RadioItems(id='margin-x',
    options=[{'label': i, 'value': i} for i in ('rug', 'box', 'violin', 'histogram')],
                value=None,labelStyle=inline,inputStyle=margin_12,style=value_style) ,style={})])

    
    margin_y_div  = html.Div(style={'display': 'none'},id='margin_y_div',children=[html.Div(html.Label('Margin Y',style=label_style),
            ),html.Div(dcc.RadioItems(id='margin-y',
    options=[{'label': i, 'value': i} for i in ('rug', 'box', 'violin', 'histogram')],
                value=None,labelStyle=inline,inputStyle=margin_12,style=value_style) ,style={})])
    

    trendline_div = html.Div(style={'display': 'None'},id='trendline_div',children=[html.Div(html.Label('Trendline',style=label_style),
            ),html.Div(dcc.RadioItems(id='trendline',
    options=[{'label': 'Ordinary Least Square', 'value': 'ols'},
            {'label': 'Locally Weighted Scatterplot Smoothing line ', 'value': 'lowess'}],value=None,
    labelStyle=inline,inputStyle=margin_12,style=value_style))])


    animation_div=html.Div(style={'display': 'none'},id='animation_div',children=[html.Div(html.Label('Animated Frame',style=label_style),
            ),html.Div(dcc.Dropdown(id='animation', placeholder='Animated Frame Column',
    options=[{'label': f"{col} ( {df[col].dtype} )", 'value': col} for col in df.columns],
                value=None,multi=False,style=dropdown_style) ,style={})])

    opacity_div=html.Div(style={'display': 'none'},id='opacity_div',children=[html.Div(html.Label('Opacity',style=label_style),
            ),html.Div(dcc.Slider(id='opacity',min=0,max=1,step=0.1,value=1,)) ])

    
    barmode_div = html.Div(style={'display': 'None'},id='barmode_div',children=[html.Div(html.Label('Bar Mode',style=label_style),
            ),html.Div(dcc.RadioItems(id='barmode',
    options=[{'label': i, 'value': i} for i in ('group', 'overlay', 'relative' )],
                value='relative',labelStyle=inline,inputStyle=margin_12,style=value_style) ,style={})])
    
    boxmode_div = html.Div(style={'display': 'None'},id='boxmode_div',children=[html.Div(html.Label('Mode',style=label_style),
            ),html.Div(dcc.RadioItems(id='boxmode',
    options=[{'label': i, 'value': i} for i in ('group', 'overlay' )],
                value='group',labelStyle=inline,inputStyle=margin_12,style=value_style) ,style={})])
    
    q_div = html.Div(style={'display': 'None'},id='q_div',children=[html.Div(html.Label('Quartile Method',style=label_style)),
            html.Div(dcc.RadioItems(id='q',
    options=[{'label': i, 'value': i} for i in ('linear', 'inclusive','exclusive' )],
                value='linear',labelStyle=inline,inputStyle=margin_12,style=value_style) ,style={})])

    points_div = html.Div(style={'display': 'None'},id='points_div',children=[html.Label('Points',style=label_style),
            html.Div(dcc.RadioItems(id='points',
    options=[{'label': i, 'value': i} for i in ('outliers', 'suspectedoutliers', 'all' )],
                value='outliers',labelStyle=inline,inputStyle=margin_12,style=value_style) ,style={})])


    layer_chart_type=html.Div([dbc.DropdownMenu([
        dbc.DropdownMenuItem(html.Img(src=f'{app.config.assets_external_path}/box.png',style=plot_icons),id='box2',n_clicks=0),
        dbc.DropdownMenuItem(html.Img(src=f'{app.config.assets_external_path}/bar.png',style=plot_icons),id='bar2',n_clicks=0),
        dbc.DropdownMenuItem(html.Img(src=f'{app.config.assets_external_path}/scatter.png',style=plot_icons),id='scatter2',n_clicks=0),
        dbc.DropdownMenuItem(html.Img(src=f'{app.config.assets_external_path}/line.png',style=plot_icons),id='line2',n_clicks=0),
        dbc.DropdownMenuItem(html.Img(src=f'{app.config.assets_external_path}/area.png',style=plot_icons),id='area2',n_clicks=0),
        dbc.DropdownMenuItem(html.Img(src=f'{app.config.assets_external_path}/violin.png',style=plot_icons),id='violin2',n_clicks=0),
       
    ],direction="right",label="Chart Type ")])
    
    layer_y_axis= html.Div([dcc.Dropdown(
    options=[
        {'label': f"{col} ( {df[col].dtype} )", 'value': col} for col in df.columns
    ],
    placeholder='Y-axis 2',
    value=None,
    multi=False,id ='y-axis2',
    style=dropdown_style
    )]) 
    
    themes=['ggplot2', 'seaborn', 'plotly', 'plotly_dark', 'presentation']
    theme_radios = dbc.FormGroup(
    [dbc.RadioItems(
            options=[{"label": i, "value": i} for i in themes],
            id="theme_dropdown",inline=True,value='presentation',style=radio_style)],style=margin_12)


    agg_funcs = ('count','sum','mean','median','std','min','max','var','size','first','last')
    agg_funcs_options = html.Div(style={'display': 'None'},id='agg_funcs_div',children=[html.Div(html.Label('Aggregation Function',style=label_style)),
            html.Div(dcc.RadioItems(id='agg_funcs',
    options=[{'label': i, 'value': i} for i in agg_funcs],
                value='sum',labelStyle=inline,inputStyle=margin_12,style=value_style) ,style={})])

    x_axis, y_axis = axis_dropdown(df,dropdown_style,label_style)


    add_layer_div =html.Div(style={'display':'None'},id='add_layer_div',children=[html.Div([html.Div(layer_chart_type,
    style={'width': '10%','margin':'10px'}),
    html.Div(layer_y_axis,style={'width': '26%','margin':'10px'}),])])

    add_parameters_dropdown=html.Div(children=[html.Label('Choose a Parameter',style=label_style,id='z-axis-label'),
                    dcc.Dropdown(id='add-parameter-drop',options=[],placeholder='Add Params..',value=[],multi=True,
                    style=dropdown_style)])
    
   
    axis=html.Div(children=[html.Div(children=[x_axis],style={'width': '26%', 'display': 'inline-block','margin':'10px'}),
                             html.Div(children=[y_axis],style={'width': '26%', 'display': 'inline-block','margin':'10px'}),
                             html.Div(children=[add_parameters_dropdown],style={'width': '40%', 'display': 'inline-block','margin':'10px','float':'right'})])
    plot_area=dbc.Card(children=[dbc.CardBody([dcc.Graph()],id='plot-area')],style={'margin':'10px',
                                                                'box-shadow': 'inset 0 4px 8px 0 rgba(0, 0, 0, 0.3)','border-radius':'20px'}) 
    nav = html.Div([dbc.Nav(
    [
        dbc.Button(html.Img(src=f'{app.config.assets_external_path}/box.png',style=plot_icons),style=plot_buttons,id='box',n_clicks=0),
        dbc.Button(html.Img(src=f'{app.config.assets_external_path}/bar.png',style=plot_icons),style=plot_buttons,id='bar',n_clicks=0),
        dbc.Button(html.Img(src=f'{app.config.assets_external_path}/scatter.png',style=plot_icons),style=plot_buttons,id='scatter',n_clicks=0),
        dbc.Button(html.Img(src=f'{app.config.assets_external_path}/area.png',style=plot_icons),style=plot_buttons,id='area',n_clicks=0),
        dbc.Button(html.Img(src=f'{app.config.assets_external_path}/line.png',style=plot_icons),style=plot_buttons,id='line',n_clicks=0),
        dbc.Button(html.Img(src=f'{app.config.assets_external_path}/violin.png',style=plot_icons),style=plot_buttons,id='violin',n_clicks=0),
        dbc.Button(html.Img(src=f'{app.config.assets_external_path}/histogram.png',style=plot_icons),style=plot_buttons,id='histogram',n_clicks=0),
        dbc.Button(html.Img(src=f'{app.config.assets_external_path}/heatmap.png',style=plot_icons),style=plot_buttons,id='heatmap',n_clicks=0),
        dbc.Button(html.Img(src=f'{app.config.assets_external_path}/treemap.png',style=plot_icons),style=plot_buttons,id='treemap',n_clicks=0),
        dbc.Button(html.Img(src=f'{app.config.assets_external_path}/waterfall.png',style=plot_icons),style=plot_buttons,id='waterfall',n_clicks=0),
        dbc.Button(html.Img(src=f'{app.config.assets_external_path}/pie.png',style=plot_icons),style=plot_buttons,id='pie',n_clicks=0),
        dbc.Button(html.Img(src=f'{app.config.assets_external_path}/sunburst.png',style=plot_icons),style=plot_buttons,id='sunburst',n_clicks=0),        
    ]
    ),tooltips(),theme_radios, axis,color_div,size_div,facet_col_div,margin_x_div,\
        margin_y_div,trendline_div,animation_div,opacity_div,barmode_div,\
        boxmode_div,q_div,points_div,add_layer_div,agg_funcs_options,plot_area])

    return nav



def tooltips():
    return html.Div([dbc.Tooltip("Box Plot",target="box",placement="bottom"),dbc.Tooltip("Bar Chart",target="bar",placement="bottom"),
    dbc.Tooltip("Scatter Plot",target="scatter",placement="bottom"),dbc.Tooltip("Line Plot",target="line",placement="bottom"),
    dbc.Tooltip("Area Plot",target="area",placement="bottom"),dbc.Tooltip("Violin Plot",target="violin",placement="bottom"),
    dbc.Tooltip("Histogram",target="histogram",placement="bottom"),dbc.Tooltip("Heat Map",target="heatmap",placement="bottom"),
    dbc.Tooltip("Tree Map",target="treemap",placement="bottom"), dbc.Tooltip("Waterfall Chart",target="waterfall",placement="bottom"),
    dbc.Tooltip('Pie Chart',target="pie",placement="bottom"),dbc.Tooltip('Sunburst Chart',target="sunburst",placement="bottom"),
    dbc.Tooltip("Box Plot",target="box2",placement="right"),dbc.Tooltip("Bar Chart",target="bar2",placement="right"),
    dbc.Tooltip("Scatter Plot",target="scatter2",placement="right"),dbc.Tooltip("Line Plot",target="line2",placement="right"),
    dbc.Tooltip("Area Plot",target="area2",placement="right"),dbc.Tooltip("Violin Plot",target="violin2",placement="right"),])

def axis_dropdown(df,dropdown_style,label_style):
    """[summary]

    Args:
        df ([type]): [description]
        dropdown_style ([type]): [description]

    Returns:
        [type]: [description]
    """
    columns=df.columns
    x_axis=html.Div([html.Label('X-axis',style=label_style,id='x-axis-label'),dcc.Dropdown(
    options=[
        {'label': f"{col} ( {df[col].dtype} )", 'value': col} for col in columns
    ],
    placeholder='X-axis',
    value=None,
    id ='x-axis',
    style=dropdown_style 
    )]) 

    
    y_axis= html.Div([html.Label('Y-axis',style=label_style,id='y-axis-label'),dcc.Dropdown(
    options=[
        {'label': f"{col} ( {df[col].dtype} )", 'value': col} for col in columns
    ],
    placeholder='Y-axis',
    value=None,
    multi=True,id ='y-axis',
    style=dropdown_style
    )]) 
  
    return x_axis,y_axis




def add_parameters(plot_type,df):
    """[summary]

    Args:
        plot_type (str): [description]

    Returns:
        list: [description]
    """
    scatter=             ('color','size','facet_col','animation_frame','opacity','marginal_x','marginal_y',\
                          'trendline','log_x','log_y','Add Layer')
    parallel_categories= ('dimensions','color','Add Layer')
    parallel_coordinates=('dimensions','color','Add Layer')
    line=                ('color','facet_col','animation_frame','log_x','log_y','Add Layer')
    area=                ('color','facet_col','animation_frame','log_x','log_y','Add Layer')
    density_contour=     ('z','color','facet_col','animation_frame','marginal_x','marginal_y','log_x','log_y','Add Layer')
    density_heatmap=     ('z','facet_col','animation_frame','marginal_x','marginal_y','log_x','log_y','Add Layer')
    bar=                 ('color','facet_col','animation_frame','opacity','barmode','log_x','log_y','Add Layer',)
    histogram=           ('opacity','barmode','log_x','log_y','Add Layer','Aggregation Function')
    box=                 ('color','facet_col','quartilemethod','points','animation_frame','mode','log_x','log_y','notched','Add Layer')
    violin=              ('color','facet_col','animation_frame','mode','points','log_x','log_y','box','Add Layer')
    treemap=             ('color',)
    waterfall=           ('Aggregation Function','Show Label')
    heatmap =            df.select_dtypes(exclude=['object']).columns
    pie =                ('color',)
    sunburst =           ('color',)

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
    elif plot_type == 'treemap':
        return [{'label': i,'value' : i} for i in treemap]
    elif plot_type == 'waterfall':
        return [{'label': i,'value' : i} for i in waterfall]
    elif plot_type == 'heatmap':
        return [{'label': f"{col} ( {df[col].dtype} )", 'value': col} for col in heatmap]
    elif plot_type == 'pie':
        return [{'label': i,'value' : i} for i in pie]
    elif plot_type == 'sunburst':
        return [{'label': i,'value' : i} for i in sunburst]
    
    else:
        return []


def add_layer(existing_fig,new_layer_type,df,x,y,theme,title=None):
    """[summary]

    Args:
        existing_fig (Plotly Figure): [description]
        new_layer_type (str): [description]
        df (Pandas Dataframe): [description]
        x (str): [description]
        y (str): [description]
        theme (str): [description]
        title (str, optional): [description]. Defaults to None.

    Returns:
        Dash Component: [description]
    """
    opacity=0.5
    new_fig = make_subplots(specs=[[{"secondary_y": True}]])
    for i in range(len(existing_fig.data)):
        new_fig.add_trace(existing_fig.data[i])
    if new_layer_type=='bar':
        fig=px.bar(data_frame=df,x=x,y=y,opacity=opacity)
        for i in range(len(fig.data)):
            new_fig.add_trace(fig.data[0],secondary_y=True).update_layout(yaxis2=dict(side='right'))
        new_fig.update_xaxes(showgrid=False)
        new_fig.update_yaxes(showgrid=False)
        new_fig.update_layout(template=theme,title=title)
        return [html.Div(children=[dcc.Graph(figure=new_fig)])]
    if new_layer_type=='box':
        fig=px.box(data_frame=df,x=x,y=y,template=theme)
        for i in range(len(fig.data)):
            new_fig.add_trace(fig.data[0],secondary_y=True).update_layout(yaxis2=dict(side='right'))
        new_fig.update_xaxes(showgrid=False)
        new_fig.update_yaxes(showgrid=False)
        new_fig.update_layout(template=theme,title=title)
        return [html.Div(children=[dcc.Graph(figure=new_fig)])]
    if new_layer_type=='line':
        fig=px.line(data_frame=df,x=x,y=y,template=theme)
        for i in range(len(fig.data)):
            new_fig.add_trace(fig.data[0],secondary_y=True).update_layout(yaxis2=dict(side='right'))
        new_fig.update_xaxes(showgrid=False)
        new_fig.update_yaxes(showgrid=False)
        new_fig.update_layout(template=theme,title=title)
        return [html.Div(children=[dcc.Graph(figure=new_fig)])]
    if new_layer_type=='area':
        fig=px.area(data_frame=df,x=x,y=y,template=theme)
        for i in range(len(fig.data)):
            new_fig.add_trace(fig.data[0],secondary_y=True).update_layout(yaxis2=dict(side='right'))
        new_fig.update_xaxes(showgrid=False)
        new_fig.update_yaxes(showgrid=False)
        new_fig.update_layout(template=theme,title=title)
        return [html.Div(children=[dcc.Graph(figure=new_fig)])]
    if new_layer_type=='scatter':
        fig=px.scatter(data_frame=df,x=x,y=y,opacity=opacity,template=theme)
        for i in range(len(fig.data)):
            new_fig.add_trace(fig.data[0],secondary_y=True).update_layout(yaxis2=dict(side='right'))
        new_fig.update_xaxes(showgrid=False)
        new_fig.update_yaxes(showgrid=False)
        new_fig.update_layout(template=theme,title=title)
        return [html.Div(children=[dcc.Graph(figure=new_fig)])]
    if new_layer_type=='violin':
        fig=px.violin(data_frame=df,x=x,y=y,template=theme)
        for i in range(len(fig.data)):
            new_fig.add_trace(fig.data[0],secondary_y=True).update_layout(yaxis2=dict(side='right'))
        new_fig.update_xaxes(showgrid=False)
        new_fig.update_yaxes(showgrid=False)
        new_fig.update_layout(template=theme,title=title)
        return [html.Div(children=[dcc.Graph(figure=new_fig)])]


def plot_graph(plot_type,df,x,y,theme,value,color=None,facet_col=None,marginal_x=None,marginal_y=None,\
    trendline=None,log_x=None,log_y=None,size=None,animation_frame=None,opacity=1,\
    barmode='relative',boxmode=None,quartilemethod=None,points='outliers',\
    notched=False,box=False,agg_func='sum',show_label = False,):
    """[summary]

    Args:
        plot_type ([type]): [description]
        df ([type]): [description]
        x ([type]): [description]
        y ([type]): [description]
        theme ([type]): [description]
        color ([type], optional): [description]. Defaults to None.
        facet_col ([type], optional): [description]. Defaults to None.
        marginal_x ([type], optional): [description]. Defaults to None.
        marginal_y ([type], optional): [description]. Defaults to None.
        trendline ([type], optional): [description]. Defaults to None.
        log_x ([type], optional): [description]. Defaults to None.
        log_y ([type], optional): [description]. Defaults to None.
        size ([type], optional): [description]. Defaults to None.
        animation_frame ([type], optional): [description]. Defaults to None.
        opacity (int, optional): [description]. Defaults to 1.
        barmode (str, optional): [description]. Defaults to 'relative'.
        boxmode ([type], optional): [description]. Defaults to None.
        quartilemethod ([type], optional): [description]. Defaults to None.
        points (str, optional): [description]. Defaults to 'outliers'.
        notched (bool, optional): [description]. Defaults to False.
        box (bool, optional): [description]. Defaults to False.

    Returns:
        [type]: [description]
    """
    try:
        out=[]
        fig=[]
        if plot_type == 'bar':
            fig=px.bar(data_frame=df,x=x,y=y,template=theme,color=color,facet_col=facet_col,log_x=log_x,log_y=log_y,opacity=opacity,animation_frame=animation_frame,barmode=barmode)
            fig.update_xaxes(showgrid=False)
            fig.update_yaxes(showgrid=False)
            out.append(html.Div(children=[dcc.Graph(figure=fig)]))        
            return out,fig
        elif plot_type == 'line':
            fig=px.line(data_frame=df,x=x,y=y,template=theme,color=color,facet_col=facet_col,log_x=log_x,log_y=log_y,animation_frame=animation_frame)
            fig.update_xaxes(showgrid=False)
            fig.update_yaxes(showgrid=False)
            out.append(html.Div(children=[dcc.Graph(figure=fig)]))
            return out,fig
        elif plot_type=='area':
            fig=px.area(data_frame=df,x=x,y=y,template=theme,color=color,facet_col=facet_col,log_x=log_x,log_y=log_y,animation_frame=animation_frame)
            fig.update_xaxes(showgrid=False)
            fig.update_yaxes(showgrid=False)
            out.append(html.Div(children=[dcc.Graph(figure=fig)]))
            return out,fig
        elif plot_type=='box':
            fig=px.box(data_frame=df,x=x,y=y,template=theme,color=color,facet_col=facet_col,log_x=log_x,log_y=log_y,animation_frame=animation_frame,boxmode=boxmode,points=points,notched=notched)
            fig.update_xaxes(showgrid=False)
            fig.update_yaxes(showgrid=False)
            fig.update_traces(quartilemethod=quartilemethod,boxmean='sd')
            out.append(html.Div(children=[dcc.Graph(figure=fig)]))
            return out,fig
        elif plot_type=='violin':
            fig=px.violin(data_frame=df,x=x,y=y,template=theme,color=color,facet_col=facet_col,log_x=log_x,log_y=log_y,animation_frame=animation_frame,violinmode=boxmode,points=points,box=box)
            fig.update_xaxes(showgrid=False)
            fig.update_yaxes(showgrid=False)
            fig.update_traces(meanline_visible=True)
            out.append(html.Div(children=[dcc.Graph(figure=fig)]))
            return out,fig
        elif plot_type=='histogram':
            fig = _bar_df(df=df,x=x,y=y,template=theme,\
                        log_x=log_x,log_y=log_y,opacity=opacity,\
                        barmode=barmode,agg_func=agg_func,\
                        orientation='v',show_label= False,)
            out.append(html.Div(children=[dcc.Graph(figure=fig)]))
            return out,fig
        elif plot_type=='parallel_categories':
            fig=px.parallel_categories(data_frame=df,template=theme,color=color,)
            fig.update_xaxes(showgrid=False)
            fig.update_yaxes(showgrid=False)
            out.append(html.Div(children=[dcc.Graph(figure=fig)]))
            return out,fig
        
        elif plot_type == 'treemap':
            fig=px.treemap(data_frame=df,path = y,values = x,template=theme,color=color,)
            fig.update_xaxes(showgrid=False)
            fig.update_yaxes(showgrid=False)
            out.append(html.Div(children=[dcc.Graph(figure=fig)]))
            return out,fig
        

        elif plot_type == 'waterfall':
            fig = _waterfall_df(df,x,y,theme,agg_func=agg_func,show_label=show_label)
            out.append(html.Div(children=[dcc.Graph(figure=fig)]))
            return out,fig


        elif plot_type == 'heatmap':
            fig = go.Figure(data=go.Heatmap(z=df[value],x=df[x],y=df[y],hoverongaps = False))
            out.append(html.Div(children=[dcc.Graph(figure=fig)]))
            return out, fig
        

        elif plot_type == 'pie':
            fig = px.pie(df, values=y, names=x,template=theme,color=color)
            fig.update_traces(textposition='inside', textinfo='percent+label')
            out.append(html.Div(children=[dcc.Graph(figure=fig)]))
            return out, fig
        
        elif plot_type == 'sunburst':
            fig = px.sunburst(df, path=y, values=x,template=theme,color=color)
            out.append(html.Div(children=[dcc.Graph(figure=fig)]))
            return out, fig

        elif plot_type=='parallel_coordinates':
            try:
                fig=px.parallel_coordinates(data_frame=df,template=theme,color=color)
                fig.update_xaxes(showgrid=False)
                fig.update_yaxes(showgrid=False)
                out.append(html.Div(children=[dcc.Graph(figure=fig)]))
                return out,fig
            except (ValueError,TypeError) as e:
                pass
        else:
            fig=px.scatter(data_frame=df,x=x,y=y,template=theme,color=color,facet_col=facet_col,marginal_x=marginal_x,marginal_y=marginal_y,trendline=trendline,log_x=log_x,log_y=log_y,size=size,opacity=opacity,animation_frame=animation_frame)
            fig.update_xaxes(showgrid=False)
            fig.update_yaxes(showgrid=False)
            out.append(html.Div(children=[dcc.Graph(figure=fig)]))
            return out,fig
    except (TypeError,ValueError,KeyError) as e:
        pass


def _params():
    return {'display':'block','margin':'12px'}
    