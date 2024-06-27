from dash import html

from config import imgs, styles

modal_layer = html.Div(
    style={
        "position": "absolute",
        "top": 0,
        "bottom": 0,
        "left": 0,
        "right": 0,
        "zIndex": -3,
    }
)

close_button = html.Button(
    imgs.cross,
    style={
        "position": "absolute",
        "left": 20,
        "top": 20,
        "border": 0,
        "zIndex": -3,
    } | styles.misc.modal_close
)


COMPONENTS = html.Div([
    modal_layer,
    close_button,
])
