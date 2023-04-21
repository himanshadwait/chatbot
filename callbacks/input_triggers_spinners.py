from dash import Input, Output
import time


def callback_triggers_spinner(app):
    @app.callback(Output("loading-output-1", "children"), Input('send-btn', 'n_clicks'))
    def input_triggers_spinner(value):
        time.sleep(1)
        return value
