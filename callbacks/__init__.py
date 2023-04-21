
from .chatbox_update import callback_chatbox_update
from .input_triggers_spinners import callback_triggers_spinner
from .get_chatbot_response import callback_chatbot_response
from .content_update import callback_content_update


def callbacks(app):
    callback_chatbot_response(app)
    callback_chatbox_update(app)
    callback_triggers_spinner(app)
    callback_content_update(app)


