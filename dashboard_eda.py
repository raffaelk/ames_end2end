import dash
from dash import dcc, html
from dash.dependencies import Input, Output

import pandas as pd

import plotly.express as px

import os

# get train and test data set
DATA_PATH = './data'
TRAIN_DATA = pd.read_csv(os.path.join(DATA_PATH,'train.csv'), index_col='Id')

FEATURES = list(TRAIN_DATA.drop('SalePrice', axis=1).columns)


# create app
app = dash.Dash()

# define the layout
app.layout = html.Div(children=[
    # title line
    html.Div(children=[
        html.H1('House Prices', style={'display':'inline-block', 'vertical-align':'middle'})
    ]),
    
    # body
    html.Div(children=[
        dcc.Graph(id="graph_main"),
        
        # left half
        html.Div(children=[
            html.H3('Feature:'),
            dcc.Dropdown(FEATURES, 'OverallQual', id='dropdown_features')
        ], style={'width':'650px', 'display':'inline-block', 'vertical-align':'middle'}),
        
        # right half
        html.Div(children=[
            html.H3('Plot Type:'),
            dcc.RadioItems(['Boxplot', 'Scatterplot'], 'Boxplot', id='radio_plottype', inline=True)
        ], style={'width':'700px', 'display':'inline-block', 'vertical-align':'middle'})

        
    ], style={'width': '1400px', 'margin': 'auto', 'background-color':'white'}),
    
    # footnote
    html.Div(children=[
        html.P('Created by RaffaelK', style={'margin':'10px'})
    ])

], style={'text-align':'center', 'background-color':'lightgrey'})

# callbacks
@app.callback(
    Output(component_id='graph_main', component_property='figure'),
    Input(component_id='dropdown_features', component_property='value'),
    Input(component_id='radio_plottype', component_property='value')
)
def update_box_fig(feature, plottype):
    
    # copy unfiltered data
    graph_data = TRAIN_DATA.copy()
   
    # create figure with data
    if plottype == 'Boxplot':
        fig_main = px.box(graph_data, x=feature, y='SalePrice', title='Sales Price')

    elif plottype == 'Scatterplot':
        fig_main = px.scatter(graph_data, x=feature, y='SalePrice', title='Sales Price')
    
    return fig_main
    

if __name__ == '__main__':
    app.run_server(port=5001, debug=True)