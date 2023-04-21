from dash import Input, Output

from layouts.home_layout import build_home_layout


def callback_content_update(app):
    @app.callback(
        Output("page-content", "children"),
        [Input("url", "pathname")]
    )
    def render_page_content(pathname):
        if pathname == "/":
            return [
                build_home_layout(app)
            ]
