import dash
from dash import Input, Output, State

import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from layouts.chatbot_response import fetch_chatbot_response
from layouts.characters import characters


def callback_chatbot_response(app):
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
