# Import libraries
import plotly.graph_objects as go
from dash import html , dcc

from codebase.prophet_predictions import predict_prophet
from codebase.preprocessing import pre_process_paquete

f_paquete, paquete, entrega = pre_process_paquete("data/ps_paquete.csv", "data/ps_entregapasaporte.csv")
pm_forecast, only_forecast, _, _ = predict_prophet(f_paquete, start_date="2021-10-01", forecast_end="2022-12")

class forecast_plot:
    
    """A class to represent a samplemap of Montreal Elections"""        
    def __init__(self,plot_title:str,ID:str):
        """__init__
        Construct all the attributes for the sample map
     
        Args:
            map_title (str): _Title for the map_
            ID (str): _div id to specify unique #id with callbacks and css_
        
        Methods:

        display()
            Function to display a sample map with no arguments, uses plotly express data.
            
            Arguments:
                None

            Returns:
                html.Div : A Div container with a dash core component dcc.Graph() inside
        """
        
        self.plot_title = plot_title
        self.id = ID

    
    
    @staticmethod
    def figura():
        
        fig = go.Figure([
            go.Scatter(#Actual values
                name='Actual Values',
                x = pm_forecast['ds'],
                y = pm_forecast['y'],
                mode='lines',
                line=dict(color='royalblue'),
                text = pm_forecast['time_lab']
            ),

            go.Scatter(#Forecasted values
                name='Forecast',
                x=only_forecast["ds"],
                y=only_forecast["yhat"],
                mode='lines',
                line=dict(color='purple',dash="dot"),
                text = only_forecast['time_lab'] + "<br>"
                       "Upper bound: " + only_forecast["yhat_upper"].astype(str) + "<br>"
                       "Lower bound: " + only_forecast["yhat_lower"].astype(str)

            ),

          go.Scatter(#Upper Confidence Interval
                name='Upper Bound',
                x=pm_forecast["ds"],
                y=pm_forecast["yhat_upper"],
                mode='lines',
                marker=dict(color="lightseagreen"),
                line=dict(width=0),
                hoverinfo='skip',
                showlegend=False
            ),

            go.Scatter(#Lower Confidence Interval
                name='Lower Bound',
                x=pm_forecast["ds"],
                y=pm_forecast["yhat_lower"],
                marker=dict(color="lightseagreen"),
                line=dict(width=0),
                mode='lines',
                fillcolor='rgba(32, 178, 170, 0.3)',
                fill='tonexty',
                hoverinfo='skip',
                showlegend=False
            )

        ])

        for lab in pm_forecast["label"].unique():
          legend = False
          hover = 'skip'
          if lab == "Anomaly":
            legend=True
            hover='name+y+text'

          fig.add_trace(go.Scatter(#Normal / Outliers
                  name=lab,
                  x = pm_forecast[pm_forecast["label"]==lab]['ds'],
                  y = pm_forecast[pm_forecast["label"]==lab]['y'],
                  mode='markers',
                  marker = {'color': pm_forecast[pm_forecast["label"]==lab]["color"], 'size': pm_forecast[pm_forecast["label"]==lab]["size"]},
                  text = pm_forecast[pm_forecast["label"]==lab]['time_lab'],
                  hoverinfo=hover,
                  showlegend=legend
                  ))

        fig.update_layout(
            yaxis_title='Solictudes',
            title={'text': "<b>Número de solicitudes</b>",'y':0.9,'x':0.5,'xanchor': 'center','yanchor': 'top'},
            hovermode= 'x unified'
        )


        fig.update_xaxes(
            rangeslider_visible=True,
            rangeselector=dict(
                buttons=list([
                    dict(count=1, label="1m", step="month", stepmode="backward"),
                    dict(count=6, label="6m", step="month", stepmode="backward"),
                    dict(count=1, label="1y", step="year", stepmode="backward"),
                    dict(count=1, label="YTD", step="year", stepmode="todate"),
                    dict(step="all")
                ])
            )
        )
        return fig

    def display(self):
       
        layout = html.Div(
            [
                html.H4([self.plot_title]),
                html.Div([
                    dcc.Graph(figure=self.figura())
                ])
                
            ],id=self.id
        )
        return layout