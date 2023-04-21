from dash import Dash, html, Input, Output, State
import dash_bootstrap_components as dbc

@app.callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

app.layout= navbar
if __name__ == "__main__":
    app.run_server()
