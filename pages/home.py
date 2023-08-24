import dash
from dash import html, dcc
from dash_labs.plugins import register_page
import dash_bootstrap_components as dbc

register_page(__name__,path="/")

layout = html.Div(
            className="content",
            children=[


    html.Div(
        className="right_content",
        children=[
            html.Div(
                className="top_metrics",
                children=[
                html.H3('Forecasts & Trends'),
                html.H6('This view displays a weekly forecast of passport requests for the next three months along with year-on-year view to compare current year volume with the last year. Both views come a slider object to zoom in/out certain periods. Below there are two panes: an NLG based engine (left) that summarizes the main highlights for the forecasted values vs. previous periods and an anomaly detection plot that flags abnormal behaviors that occurred outside a confidence interval.'),
                html.H3('Status'),
                html.H6('This view displays the number of unclaimed passports within the past 12-months (left) and the number of passports that were issued by the entity and that will expire within the next 12-month window (right).')
                ]
            ),
        ]
    ),
    
    dbc.Carousel(
        className="right_menu",
    items=[
        {"key": "1", "src": "https://www.boyaca.gov.co/wp-content/uploads/2021/03/Logos-Gobernacion-Avanza-300x64.png"},
        {"key": "2", "src": "https://correlation1-public.s3-us-west-2.amazonaws.com/assets/c1-logo.png", "height":"80%" }
    ],
    controls=False,
    indicators=False,
    interval=2000,
    ride="carousel"
    )

])