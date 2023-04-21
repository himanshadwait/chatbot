from dash import html, register_page, page_container

from .side_bar import build_sidebar
from .home_layout import build_home_layout
from .content import update_content


def layout(app):
    return html.Div(id="main_div", children=[
        build_sidebar(app),
        update_content(app),
        html.Div(id='second_div', children=[
            page_container
        ]),
    ])


def register_app_pages():
    page_values = [
        # id , name, path, layout
        ["page1", "Home", '/', build_home_layout()],
        # ["page2", "Privacy Policy", '/pri_pol', build_pri_pol_layout()],
    ]

    for order, (module , name, path, layout) in enumerate(page_values):
        register_page(module, name=name, path=path, layout=layout, order=order)