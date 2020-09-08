import dash_bootstrap_components as dbc
import dash_html_components as  html
import dash_core_components as dcc

def _navbar(plot_icons,side_bar_buttons,side_nav_style,app):
    """[summary]

    Args:
        plot_icons ([type]): [description]
        side_nav_style ([type]): [description]
        app ([type]): [description]

    Returns:
        [type]: [description]
    """
    BADGES=html.Div(
        [
        dbc.Card(
            [
                dbc.CardBody([
                html.P(dbc.Button(html.Img(src=f'{app.config.assets_external_path}/cols.png',style=plot_icons),id='datatable',href='/home',style=side_bar_buttons)),
                html.P(dbc.Button(html.Img(src=f'{app.config.assets_external_path}/plots.png',style=plot_icons),id='plots',href='/plots',style=side_bar_buttons)),
                html.P(dbc.Button(html.Img(src=f'{app.config.assets_external_path}/analysis.png',style=plot_icons),id='analysis',href='/analysis',style=side_bar_buttons)),         
            ]
        ) 
    ], style={"width": "0rem"}),tooltips()],style=side_nav_style
    ) 
    return BADGES




def tooltips():
    return html.Div([dbc.Tooltip("Plots",target="plots",placement="right"),
    dbc.Tooltip("Data Preview",target="datatable",placement="right"), dbc.Tooltip("Analysis",target="analysis",placement="right"),])

