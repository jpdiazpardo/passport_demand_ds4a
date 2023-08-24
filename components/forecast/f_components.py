# Import libraries
from dash import html , dcc
import dash_bootstrap_components as dbc

from prophet.plot import plot_plotly, plot_components_plotly

from codebase.prophet_predictions import predict_prophet
from codebase.preprocessing import pre_process_paquete

f_paquete, paquete, entrega = pre_process_paquete("data/ps_paquete.csv", "data/ps_entregapasaporte.csv")
pm_forecast, only_forecast, f_table, pm = predict_prophet(f_paquete, start_date="2021-10-01", forecast_end="2022-12")

class forecast_components:
    
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
        
        ploty_comp = plot_components_plotly(pm, pm_forecast, plot_cap=False)
        ploty_comp.update_layout(title={'text': "<b>Series components</b>",'y':0.9,'x':0.5,'xanchor': 'center','yanchor': 'top'})
        
        return ploty_comp

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