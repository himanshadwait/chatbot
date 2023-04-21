# I want the format of chatbot to be something like this


import dash
from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc

from layouts.home_layout import build_home_layout
from callbacks import callbacks

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

sidebar = html.Div(
    [
        html.A(
            # Use row and col to control vertical alignment of logo / brand
            dbc.Row(
                [
                    dbc.Col(html.Img(src=app.get_asset_url("LAMA-logo_Final-01.png"), height="30px")),
                    dbc.Col(dbc.NavbarBrand("Askllama", className="ms-5")),
                ],
                align="center",
                className="g-0",
            ),
            href="https://plotly.com",
            style={"textDecoration": "none"},
        ),
        html.Hr(),
        html.P("Here is some content for the sidebar."),
        dbc.Button("+ New Chat", id="sidebar-button", className="mt-3"),
    ],
    style={
        "position": "fixed",
        "top": 0,
        "left": 0,
        "bottom": 0,
        "width": "250px",
        "padding": "20px",
        "background-color": "#f8f9fa",
    }
)

chatbot = html.Div(
    [
        dcc.Input(id='input', type='text', value=''),
        html.Div(id='output')
    ],
    style={
        "margin-left": "250px",
        "padding": "20px",
    }
)

app.layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(sidebar, width=3),
                dbc.Col(chatbot, width=15),
            ]
        )
    ],
    fluid=True,
)


@app.callback(Output('output', 'children'),
              Input('input', 'value'))
def update_output_div(input_value):
    return [
        build_home_layout(app),
        callbacks(app)

    ]


# Clicking here refreshes everything on the chatbot screen
@app.callback(Output('sidebar-button', 'n_clicks'),
              Input('sidebar-button', 'n_clicks'))
def handle_sidebar_button_click(n_clicks):
    if n_clicks is None:
        return 0
    else:
        return n_clicks


if __name__ == '__main__':
    app.run_server(debug=True)
