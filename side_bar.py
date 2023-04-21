import dash
from dash import Dash, Input, Output, html, dcc, State
import dash_bootstrap_components as dbc
import json
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from layouts.chatbot_response import fetch_chatbot_response
from layouts.characters import characters

app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    title="Askllama"
)

# styling the sidebar
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# padding for the page content
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.A(
            # Use row and col to control vertical alignment of logo / brand
            dbc.Row(
                [
                    dbc.Col(html.Img(src=app.get_asset_url("LAMA-logo_Final-01.png"), height="40px")),
                    dbc.Col(html.H3("Askllama", className="display-6 text-dark")),
                ],
                align="center",
                className="g-0",
            ),
            href="https://www.myllama.co/",
            style={"textDecoration": "none"},
        ),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact"),
                dbc.NavLink("Privacy Policy", href="/privacy-policy", active="exact"),
                dbc.NavLink("Disclaimer", href="/disclaimer", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", children=[], style=CONTENT_STYLE)

app.layout = html.Div([
    dcc.Location(id="url"),
    sidebar,
    content
])


@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")]
)
def render_page_content(pathname):
    if pathname == "/":
        return [
            dbc.Container([
                html.H1('Please select the Masters you want to talk to:'),
                dcc.Checklist(
                    id='character-checklist',
                    options=[{'label': character['name'], 'value': character['name']} for character in characters],
                    value=[]
                ),
                html.Br(),
                dbc.Textarea(id='chat-box', readOnly=True, rows=15, style={'width': '100%', 'white-space': 'pre-wrap'}),
                html.Br(),
                dcc.Loading(
                    id="loading-1",
                    type="default",
                    children=html.Div(id="loading-output-1")
                ),
                dbc.Input(id='question', placeholder='Ask a question:', type='text'),
                html.Br(),
                dbc.Button('Send', id='send-btn', color='primary'),
                html.Div(id='hidden-chat-history', style={'display': 'none'}),
                html.Div(id='hidden-character-history', style={'display': 'none'})
            ])

        ]
    elif pathname == "/privacy-policy":
        return [
            html.H1('This is our PP',
                    style={'textAlign': 'center'}),
        ]
    elif pathname == "/disclaimer":
        return [
            html.H1('Disclaimer',
                    style={'textAlign': 'center'}),
        ]
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )


@app.callback(
    Output('hidden-chat-history', 'children'),
    Output('hidden-character-history', 'children'),
    Input('send-btn', 'n_clicks'),
    State('character-checklist', 'value'),
    State('question', 'value'),
    State('hidden-chat-history', 'children'),
    State('hidden-character-history', 'children')
)
def get_chatbot_responses(n_clicks, selected_character_names, question, chat_history_json, character_history_json):
    if not n_clicks or not selected_character_names or not question:
        raise dash.exceptions.PreventUpdate
    selected_characters = [
        character for character in characters if character['name'] in selected_character_names
    ]
    if not chat_history_json:
        chat_history = ''
    else:
        chat_history = json.loads(chat_history_json)
    if not character_history_json:
        character_history = {character['name']: [] for character in characters}
    else:
        character_history = json.loads(character_history_json)
    user_avatar = "https://secure.gravatar.com/avatar/84e1cab23663f968345fafb812c73a85?s=50&d=mm&r=g"
    chat_history += f'\n\n![User]({user_avatar}) **You**: {question}'
    with ThreadPoolExecutor() as executor:
        future_responses = {
            executor.submit(fetch_chatbot_response, character, question,
                            character_history[character['name']]): character for character in selected_characters
        }
        for future in as_completed(future_responses):
            character, completion = future.result()
            completion_with_character = f"![{character['name']}]({character['image']}) : {completion}"
            chat_history += f'\n\n{completion_with_character}'
            character_history[character['name']].append({"role": "assistant", "content": completion})
    return json.dumps(chat_history), json.dumps(character_history)


@app.callback(
    Output('chat-box', 'value'),
    Input('hidden-chat-history', 'children')
)
def update_chat_box(chat_history_json):
    if not chat_history_json:
        raise dash.exceptions.PreventUpdate
    return json.loads(chat_history_json)


@app.callback(Output("loading-output-1", "children"), Input('send-btn', 'n_clicks'))
def input_triggers_spinner(value):
    time.sleep(1)
    return value


if __name__ == '__main__':
    app.run_server(debug=True, port=3000)
