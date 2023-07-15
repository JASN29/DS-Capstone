# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                 dcc.Dropdown(
        id='site-dropdown',
        options=[{'label': 'All Sites', 'value': 'ALL'}] + [{'label': site, 'value': site} for site in spacex_df['Launch Site'].unique()],
        value='ALL',
        placeholder='Select a Launch Site',
        style={'width': '50%', 'margin': '0 auto', 'display': 'block'}
    ),                                
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(
        id='payload-slider',
        min=min_payload,
        max=max_payload,
        step=1000,
        value=[min_payload, max_payload],
        marks={str(payload): str(payload) for payload in range(int(min_payload), int(max_payload) + 1, 2000)},
        tooltip={'always_visible': True}
    ),


                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def update_pie_chart(site):
        if site == 'ALL':
            title = 'Total Success Launches By Site'
            df = spacex_df[spacex_df['Launch Site'].isin(['CCAFS LC-40', 'VAFB SLC-4E', 'KSC LC-39A', 'CCAFS SLC-40'])]
            df_counts = df['Launch Site'].value_counts()
            labels = df_counts.index.tolist()
            values = df_counts.values.tolist()
        
        else:
            title = f'Success vs. Failed Launches for {site}'
            df = spacex_df[spacex_df['Launch Site'] == site]
            df_counts = df['class'].value_counts()
            labels = df_counts.index.tolist()
            values = df_counts.values.tolist()

        fig = px.pie(names=labels, values=values, title=title)
        return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value'),
    Input(component_id='payload-slider', component_property='value')
)
def update_scatter_chart(site, payload_range):
    if site == 'ALL':
        title = 'Payload vs. Launch Success for All Sites'
        df = spacex_df.copy()
    else:
        title = f'Payload vs. Launch Success for {site}'
        df = spacex_df[spacex_df['Launch Site'] == site]
    
    filtered_df = df[(df['Payload Mass (kg)'] >= payload_range[0]) & (df['Payload Mass (kg)'] <= payload_range[1])]
    fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', color='Booster Version Category', title=title)
    fig.update_layout(
        xaxis_title='Payload Mass (kg)',
        yaxis_title='Launch Outcome',
        legend_title='Booster Version Category'
    )
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
