from dash import html
import dash_bootstrap_components as dbc

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}


def build_sidebar(app):
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
    return sidebar
