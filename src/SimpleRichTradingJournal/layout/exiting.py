from dash import html

import __env__
from config import imgs, styles

MODAL = html.Div(
    [
        html.Div(
            [
                html.H1("Terminate Server"),
            ],
            id="exit_modal_head_",
        ),
        html.Hr(),
        exit_modal_body := html.Div(
            id="exit_modal_body_",
        ),
        html.Hr(),
        html.Div(
            exit_modal_button := html.Button(
                "Ok",
                id="exit_modal_button_",
                style={

                } | styles.misc.term_button
            )
        )
    ],
    id="exit_modal_",
    style={
        "position": "absolute",
        "zIndex": -2,
        "width": 500,
        "top": 50,
        "left": "calc(50% - 250px)",
        "backgroundColor": __env__.color_theme.table_bg_2,
        "color": __env__.color_theme.table_fg_main,
        "padding": 10,
        "borderRadius": 10,
        "overflow": "scroll"
    }
)

exit_button = html.Button(
    imgs.cross,
    id="exit_button_",
    style={
        "display": "inline-block",
        "margin": "7px",
        "fontSize": "13px",
        "paddingLeft": "10px",
        "paddingRight": "10px",
        "borderRadius": "15px",
        "backgroundColor": __env__.color_theme.cell_negvalue,
        "border": "1px solid " + __env__.color_theme.table_sep,
        "opacity": 0.7,
    },
)

COMPONENTS = html.Div([
    MODAL
])
