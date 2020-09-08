

import dash_bootstrap_components as dbc

side_nav_style={

    'width': '10%', 
    'float' : 'left',
        }

main_window=  {

    'width': '90%', 
    'display': 'inline-block',
    'float' : 'right',
 
  
    }

external_stylesheets = [dbc.themes.BOOTSTRAP]


body={

    'margin' : '5px'
}

all_ = {'background-color':'#efefef'}
plot_icons={'height':'30px', 'width':'30px'}
plot_buttons = {'margin':'0 0 0 2%','box-shadow': '-3px -3px 7px #fff, 3px 3px 5px rgba(94,104,121,0.8)','border-radius':'20px',
                'background-color':'white','border':'0px'}
side_bar_buttons = {'box-shadow': '-3px -3px 7px #fff, 3px 3px 5px rgba(94,104,121,0.712)',
                        'border-radius':'20px',
                        'background-color':'white','border':'0px','color':'black'}

margin_12= {'margin':'12px'}
margin_10={'margin':'10px'}

inline={'display': 'inline-block'}

dropdown_style={'color': '#333','background-color': '#fff','box-shadow': 'inset -3px -3px 7px #fff, inset 3px 3px 5px rgba(94,104,121,0.712)',
                    'border-radius':'15px'}

label_style = {'text-shadow':'-3px -3px 7px #fff, 3px 3px 5px rgba(94,104,121,0.8)', 'color':'white', 'fontWeight': 'bold',}

radio_style={'text-shadow':'-3px -3px 7px #fff, 3px 3px 5px rgba(94,104,121,0.8)',
            'color':'white', 'fontWeight': 'bold',}

selected_button = {'margin':'0 0 0 2%','box-shadow': 'inset -3px -3px 7px #fff, inset 3px 3px 5px rgba(94,104,121,0.3)','border-radius':'20px',
                'background-color':'white','border':'0px'}

value_style = {'text-shadow':'-3px -3px 7px #fff,3px 3px 5px rgba(94,104,121,0.8)','color':'white','fontWeight': 'bold'}

data_type_style_h={'margin':'5px 0 0 0','text-shadow':'-3px -3px 7px #fff,3px 3px 5px rgba(94,104,121,0.8)','color':'grey','fontWeight': 'bold',}
data_type_style_p={'margin':'0 0 0 12px','text-shadow':'-3px -3px 7px #fff,3px 3px 5px rgba(94,104,121,0.8)','color':'white','fontWeight': 'bold'}