# Imports
import dash
from dash import Input, Output, State, html, dcc
import dash_bootstrap_components as dbc
import logging
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from layouts.chatbot_response import fetch_chatbot_response
from layouts.characters import characters
import time

# Set up logging

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP], title="Askllama")

navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=app.get_asset_url("LAMA-logo_Final-01.png"), height="30px")),
                        dbc.Col(dbc.NavbarBrand("Askllama", className="ms-2")),
                    ],
                    align="center",
                    className="g-0",
                ),
                href="https://plotly.com",
                style={"textDecoration": "none"},
            ),
            dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
            dbc.Collapse(
                id="navbar-collapse",
                is_open=False,
                navbar=True,
            ),
        ]
    ),
    color="dark",
    dark=True,
)
app.layout = dbc.Container([
    navbar,
    html.H1('Please select the Masters you want to talk to:'),
    dcc.Checklist(
        id='character-checklist',
        options=[{'label': character['name'], 'value': character['name']} for character in characters],
        value=[]
    ),
    html.Br(),
    dbc.Textarea(id='chatbox', readOnly=True, rows=15, style={'width': '100%', 'white-space': 'pre-wrap'}),
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
    Output('chatbox', 'value'),
    Input('hidden-chat-history', 'children')
)
def update_chatbox(chat_history_json):
    if not chat_history_json:
        raise dash.exceptions.PreventUpdate
    return json.loads(chat_history_json)


@app.callback(Output("loading-output-1", "children"), Input('send-btn', 'n_clicks'))
def input_triggers_spinner(value):
    time.sleep(1)
    return value


if __name__ == '__main__':
    app.run_server(debug=False)

    dbc.Row([
        dbc.Col([
            dbc.Nav([
                dbc.NavItem(dbc.NavLink("Home", href="/")),
                dbc.NavItem(dbc.NavLink("Privacy Policy", href="/privacy-policy"))
                dbc.NavItem(dbc.NavLink("Disclaimer", href="/disclaimer")),
