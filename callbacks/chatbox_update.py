import dash
from dash import Input, Output
import json


def callback_chatbox_update(app):
    @app.callback(
        Output('chatbox', 'value'),
        Input('hidden-chat-history', 'children')
    )
    def update_chatbox(chat_history_json):
        if not chat_history_json:
            raise dash.exceptions.PreventUpdate
        return json.loads(chat_history_json)
