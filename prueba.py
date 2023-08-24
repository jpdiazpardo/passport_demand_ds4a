#libraries
import dash
import dash_labs as dl
from dash import dcc
import dash_bootstrap_components as dbc
from dash import html
from dash.dependencies import Input, Output
import os

#from callbacks import register_callbacks


request_path_prefix = "/"

#request_path_prefix = '/http://20.213.116.142:8050/tree/'

    
# Dash instance declaration
app = dash.Dash(__name__, plugins=[dl.plugins.pages], requests_pathname_prefix=request_path_prefix, external_stylesheets=[dbc.themes.FLATLY],)


# styling the sidebar
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#E7E7E7",
}

# padding for the page content
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        dbc.Card(
            dbc.CardBody(
                [
                    html.H4("Team - 10", className="card-title"),
                    html.H6("Card subtitle", className="card-subtitle"),
                ]
            ),
            style={"width": "16rem"},
        ),
        
        html.Hr(),
        html.P(
            "Number of passports", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink(
                    [
                        html.Div(page["name"], className="ms-2"),
                    ],
                    href=page["path"],
                    active="exact",
                )
                for page in dash.page_registry.values()
                if page["path"].startswith("/")
            ],
            vertical=True,
            pills=True,
            className="bg-light",
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = dbc.Container(
    [
        sidebar,
        dl.plugins.page_container        
    ],
    className="dbc",
    fluid=True,
)

# Testing server, don't use in production, host
if __name__ == "__main__":
    app.run_server(host='0.0.0.0', port=8889, debug=True)