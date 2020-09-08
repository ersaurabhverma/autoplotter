import dash_table as dt
import dash_html_components as html
import dash_bootstrap_components as dbc



def column_classification(df,side_bar_buttons,data_type_style_h,data_type_style_p):
    """[summary]

    Args:
        df ([type]): [description]

    Returns:
        [type]: [description]
    """
    classifier = df.dtypes.reset_index().rename(columns={'index':'col',0:'type'})
    classifier.type=classifier.type.apply(str)
    types={i:[html.H5(f'⇛{i}',style=data_type_style_h)]+list(map(lambda x : html.P(f'→{x}',style=data_type_style_p),classifier.loc[classifier['type']==i,'col'].tolist())) for i in classifier['type'].unique()}
    data_types = html.Div(sum([types[i] for i in types.keys()],[]),)
    collapse = html.Div(
    [dbc.Button([html.P("Data Types",style={'margin':'0px','color':'grey','fontWeight': 'bold'}),html.P('show/hide',style={'margin':'0px'})],\
                            id="collapse-button",className="mb-3",color="primary",style=side_bar_buttons),
        dbc.Collapse(
            dbc.Card(dbc.CardBody([data_types],style = {'backgroundColor':'#dedede'})),
            id="collapse_",
        ),
    ])   
    return collapse 


def homepage(df,side_bar_buttons,data_type_style_h,data_type_style_p):
    """[summary]

    Args:
        df ([type]): [description]

    Returns:
        [type]: [description]
    """
    data_body=html.Div([column_classification(df,side_bar_buttons,data_type_style_h,data_type_style_p),dt.DataTable(data=df.to_dict('records'),columns=[{'id': c, 'name': c} for c in df.columns],
    filter_action="native",sort_action="native",sort_mode="multi",page_size= 15,
    style_cell={'textAlign': 'center','padding': '3px', 'fontWeight': 'italic','backgroundColor': 'rgb(200, 150, 150)',
        'color': 'white'},
    style_header={
        'backgroundColor': '#444',
        'fontWeight': 'bold'
    },
   
    )],
    )
    return data_body