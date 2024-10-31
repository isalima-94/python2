# Import necessary libraries
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

# Dashboard financiero
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])


server=app.server

app.title = 'Dashboard financiero'

# Load data
df = pd.read_csv('/Users/isabellima/Desktop/Octavo semestre/empresas.csv')

# List of sales metrics
sales_list = ['Total revenues', 'Cost of Revenues', 'Gross profit', 'Total Operating Expenses', 'Operating Income',
              'Net Income', 'Shares Outstanding', 'Close Stock Price', 'Market Cap', 'Multiple of Revenue']

# App layout
app.layout = html.Div([

    # Row for dropdowns
    html.Div([
        html.Div([

            # Dropdown for selecting companies
            dcc.Dropdown(
                id='stockdropdown',
                value=['Amazon', 'Tesla', 'Microsoft', 'Apple', 'Google'],
                clearable=False,
                multi=True,
                options=[{'label': x, 'value': x} for x in sorted(df['Company'].unique())]
            )
        ], className='six columns', style={'width': '50%'}),

        # Dropdown for selecting numeric metric
        html.Div([
            dcc.Dropdown(
                id='numericdropdown',
                value='Total revenues',
                clearable=False,
                options=[{'label': x, 'value': x} for x in sales_list]
            )
        ], className='six columns', style={'width': '50%'})
        
    ], className='row custom-dropdown'),

    # Graphs
    html.Div([dcc.Graph(id='bar', figure={})]),
    html.Div([dcc.Graph(id='boxplot', figure={})]),

    # Data table
    html.Div(id='table-container_1', style={'marginBottom': '15px', 'marginTop': '0px'})
])

# Callback to update graphs and table
@app.callback(
    [Output('bar', 'figure'), Output('boxplot', 'figure'), Output('table-container_1', 'children')],
    [Input('stockdropdown', 'value'), Input('numericdropdown', 'value')]
)
def display_value(selected_stock, selected_numeric):
    if len(selected_stock) == 0:
        df_filtered = df[df['Company'].isin(['Amazon', 'Tesla', 'Microsoft', 'Apple', 'Google'])]
    else:
        df_filtered = df[df['Company'].isin(selected_stock)]

    # Line chart
    fig = px.line(
        df_filtered, x='Quarter', y=selected_numeric, color='Company', markers=True,
        width=1000, height=500, title=f'{selected_numeric} de {selected_stock}'
    )
    fig.update_layout(xaxis_title='Quarters',)
    fig.update_traces(line=dict(width=2))

    # Box plot
    fig2 = px.box(
        df_filtered, x='Company', y=selected_numeric, color='Company',
        width=1000, height=500, title=f'{selected_numeric} de {selected_stock}'
    )

    # Data table
    df_reshaped = df_filtered.pivot(index="Company", columns="Quarter", values=selected_numeric)
    df_reshaped2 = df_reshaped.reset_index()

    # Display table
    table = dash_table.DataTable(
        columns=[{"name": i, "id": i} for i in df_reshaped2.columns],
        data=df_reshaped2.to_dict("records"),
        export_format="csv",
        fill_width=True,
        style_cell={"font-size": "12px"},
        style_table={"maxWidth": 1000},
        style_header={"backgroundColor": "blue", "color": "white"},
        style_data_conditional=[{"backgroundColor": "white", "color": "black"}]
    )

    return fig, fig2, table

# Set server and run the app
if __name__ == "__main__":
    app.run_server(port=10000)
