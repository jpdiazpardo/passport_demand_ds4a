# Import libraries
import plotly.graph_objects as go
from dash import html , dcc
import plotly.express as px 

from codebase.status_unclaimed import status_unclaimed
from codebase.preprocessing import pre_process_paquete

f_paquete, paquete, entrega = pre_process_paquete("data/ps_paquete.csv", "data/ps_entregapasaporte.csv")
stat_paquete, unclaimed_f = status_unclaimed(paquete, entrega)

class status_plot_expiry:
    
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
        
        #Plot figure
        p_expiry = px.bar(stat_paquete, title="<b>Soon to expiry passports</b>")
        p_expiry.layout.update(showlegend=False, title_x=0.5, xaxis_title="Expiry date", yaxis_title="Number of passports")
        p_expiry.update_traces(marker_color='deeppink')
        
        return p_expiry

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