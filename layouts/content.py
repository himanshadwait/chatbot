from dash import html

CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}


def update_content(app):
    content = html.Div(id="page-content", children=[], style=CONTENT_STYLE)
    return content
