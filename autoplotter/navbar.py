import dash_bootstrap_components as dbc
import dash_html_components as html
def Navbar():
    navbar = dbc.NavbarSimple(color ='dark',dark=True,className="ml-auto flex-nowrap mt-3 mt-md-0",
                                children=[dbc.NavItem(dbc.NavLink("Data Exploration", href="/data-exploration",className="fas fa-chart-line")),
                                        dbc.NavItem(dbc.NavLink("Plots", href="/plot",className="fas fa-chart-area")),
                                         ],brand="Data",brand_href="/home",sticky="top"
        )
    return navbar

def homepage_heading():
    heading=html.H4('Data Preview',style={'text-align':'center'})
    return heading