#libraries
import dash
from dash import Dash, html , dcc
import dash_bootstrap_components as dbc
from dash_labs.plugins import register_page

from components.status.s_plot_expiry import status_plot_expiry
from components.status.s_plot_unclaimed import status_plot_unclaimed

# dash-labs plugin call, menu name and route
register_page(__name__,path="/status")

p_status_expiry = status_plot_expiry('Expiry', 'id_mapa_ejemplo')
p_status_unclaimed = status_plot_unclaimed('Unclaimed', 'id_mapa_ejemplo')

# specific layout for this page
layout = dbc.Container(
    className="right_content",
    children=[
        dbc.Row([
            dbc.Col([
                p_status_expiry.display()
            ], xs=12, className='card')]),
        dbc.Row([
            dbc.Col([
                p_status_unclaimed.display()
            ], xs=12, className='card')])
        
       ], style={'backgroundColor': '#FAFAFA', 'width': 'auto', 'display': 'block', 'margin' : 'auto'})