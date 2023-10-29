import dash
from dash import dcc, html
from dash.dependencies import Input, Output

import pandas as pd

import plotly.express as px

import os

# get train and test data set
DATA_PATH = './data'
TRAIN_DATA = pd.read_csv(os.path.join(DATA_PATH,'train.csv'), index_col='Id')

MIN_YEAR_BUILT = TRAIN_DATA['YearBuilt'].min()
MAX_YEAR_BUILT = TRAIN_DATA['YearBuilt'].max()

NEIGHBORHOOD_OPTIONS = TRAIN_DATA['Neighborhood'].unique()


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
        dcc.Graph(id="graph_box"),
        
        # left half
        html.Div(children=[
            
            # year range
            html.Div(children=[
                html.H3(id='title_slider_year_built'),
                dcc.RangeSlider(MIN_YEAR_BUILT, MAX_YEAR_BUILT, id='slider_year_built')  
            ], style={'border-style': 'dashed', 'padding':'10px'})  
            
        ], style={'width':'650px', 'display':'inline-block', 'vertical-align':'middle'}),
        
        # right half
        html.Div(children=[
            html.Div(children=[
               
            ], style={'display': 'inline-block'}),
            
            # neighborhood
            html.Div(children=[
                html.H3('Neighborhood: '),
                dcc.Checklist(NEIGHBORHOOD_OPTIONS, id='checklist_neighborhood')
            ], style={'text-align': 'left', 'display': 'inline-block', 'border-style': 'dashed', 'padding':'10px'})
            
        ], style={'width':'700px', 'display':'inline-block', 'vertical-align':'middle'})
        
    ], style={'width': '1400px', 'margin': 'auto', 'background-color':'white'}),
    
    # footnote
    html.Div(children=[
        html.P('Created by RaffaelK', style={'margin':'10px'})
    ])

], style={'text-align':'center', 'background-color':'lightgrey'})

# callbacks
@app.callback(
    Output(component_id='graph_box', component_property='figure'),
    Output(component_id='title_slider_year_built', component_property='children'),
    Input(component_id='slider_year_built', component_property='value'),
    Input(component_id='checklist_neighborhood', component_property='value')
)
def update_box_fig(year_range, hood_list):
    
    # copy unfiltered data
    box_data = TRAIN_DATA.copy()

    # year range filter
    year_range_title = 'Built between: '    
    if year_range:
        year_range_title += f'{year_range[0]} and {year_range[1]}'
        box_data = box_data[box_data['YearBuilt'] >= year_range[0]]
        box_data = box_data[box_data['YearBuilt'] <= year_range[1]]
        
    # neighborhood filter
    if hood_list:
        box_data = box_data[box_data['Neighborhood'].isin(hood_list)]
    
    # create figure with filtered data
    box_fig = px.box(box_data, x='OverallQual', y='SalePrice', title='Sales Price')
    
    return box_fig, year_range_title
    

if __name__ == '__main__':
    app.run_server(debug=True)