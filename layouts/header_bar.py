from dash import dcc, html
import dash_bootstrap_components as dbc


def build_header_bar(app):
    return dbc.Navbar(className="banner", sticky="top", children=[
        build_banner(app),
        build_intervals_div()
    ])


def build_banner(app):
    return dbc.Container(children=[
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
            href="https://www.myllama.co/",
            style={"textDecoration": "none"},
        ),
        dbc.Row(id="header_tabs_1",
                children=dbc.Col(
                    children=[
                        build_tabs()
                        # dbc.NavbarToggler(id="navbar-toggler", className="pull-right", n_clicks=0),
                        # dbc.Collapse(
                        #     dbc.Nav(build_tabs(),
                        #             navbar=True),
                        #     id="navbar-collapse",
                        #     navbar=True,
                        #     is_open = False
                        # ),
                    ]
                ),
                )

    ]
    )


def build_tabs():
    # The keys of this dictionary should be same as module defined in
    # layouts/__init__.py while registering pages

    header_tabs = ["Home", "Privacy Policy", "Disclaimer"]


    tabs = [
        dbc.Col(html.H6([i, " ", html.I(className="fa fa-chevron-down fa-2xs fa-beat")]), id=i, class_name="tab_name",
                width="auto")
        for i in header_tabs]

    return html.Div(children=[
        dbc.Row(tabs)
    ])


def build_intervals_div():
    return html.Div(id='interval_div', children=[
        dcc.Interval(id="i1", interval=1 * 1000, n_intervals=0),
        dcc.Interval(id="i2", interval=2 * 1000, n_intervals=0),
        dcc.Interval(id="i5", interval=5 * 1000, n_intervals=0),
        dcc.Interval(id="i60", interval=60 * 1000, n_intervals=0),
    ])
