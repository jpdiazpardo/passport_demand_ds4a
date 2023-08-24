# Import libraries
from dash import html , dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

from codebase.year_on_year import year_on_year
from codebase.preprocessing import pre_process_paquete

f_paquete, paquete, entrega = pre_process_paquete("data/ps_paquete.csv", "data/ps_entregapasaporte.csv")
YoY, cyear, lyear = year_on_year(f_paquete)

class forecast_yoy:
    
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
        
        yoy_plot = go.Figure([
            go.Scatter(#Current Year
                name= str(cyear),
                x = YoY.index,
                y = YoY['Current Year'],
                mode='lines',
                hoverinfo='name+y+text',
                line= dict(color='royalblue'),
                text = "% Change: " + YoY['% Change']),

              go.Scatter(#Last Year
                name= str(lyear),
                x = YoY.index,
                y = YoY['Last Year'],
                mode='lines',
                hoverinfo='name+y',
                line= dict(color='green'))

        ])

        yoy_plot.update_layout(
            yaxis_title='Solictiudes',
            title={'text': "<b>YoY - Número de solicitudes</b>",'y':0.9,'x':0.5,'xanchor': 'center','yanchor': 'top'},
            hovermode= 'x unified',
            legend={'title':"Year"}
        )


        yoy_plot.add_annotation(text='<b>'+ str(cyear) +':</b> ' + str(YoY['Current Year'].sum()) + "<br>" +
                                  '<b>'+ str(lyear) +':</b> ' + str(YoY['Last Year'].sum()) + "<br>" +
                                  '<b>% Change:</b> ' + str(round((YoY['Current Year'].sum()/YoY['Last Year'].sum())-1,1)*100) + "%<br>",

                            align='left',
                            showarrow=False,
                            xref='paper',
                            yref='paper',
                            x=0.77,
                            y=1.29,
                            bordercolor='black',
                            borderwidth=1)

        yoy_plot.update_xaxes(rangeslider_visible=True)
        return yoy_plot

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