import dash
from dash import Input, Output, html, dcc, State
import dash_bootstrap_components as dbc

from layouts.characters import characters


def build_home_layout(app):
    layout = dbc.Container(
        [
            html.H1(
                'Please select the Masters you want to talk to:'
            ),
            dcc.Checklist(
                id='character-checklist',
                options=[
                    dict(
                        label=character['name'],
                        value=character['name']
                    )
                    for character in characters
                ],
                value=[]
            ),
            html.Br(),
            dbc.Textarea(
                id='chatbox',
                readOnly=True,
                rows=20,
                style={'width': '100%', 'white-space': 'pre-wrap'}
            ),
            html.Br(),
            dbc.Input(
                id='question',
                placeholder='Ask a question:',
                type='text'
            ),
            html.Br(),
            dbc.Button(
                'Send',
                id='send-btn',
                color='primary'
            ),
            html.Div(
                id='hidden-chat-history',
                style={'display': 'none'}
            ),
            html.Div(
                id='hidden-character-history',
                style={'display': 'none'}
            )
        ]
    )

    return layout
