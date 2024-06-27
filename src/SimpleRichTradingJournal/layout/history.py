from dash import html, dcc

import __env__

MODAL = html.Div([
    html.H1("History"),
    html.Hr(),
    html.Div(
        [
            html.P(
                "Slots are created at startup if the current data differs from the first slot in the history. "
                "Therefore, the time stamps correspond to this startup and not the modification time."
            ),
            html.P(
                "When an slot is selected, `Auto. Save` is automatically deactivated. "
                "If the loaded slot is to be saved as new main data, `Auto. Save` must be activated manually. "
                "Otherwise the page can be reloaded to return to the current main data."
            ),
            html.Hr(),
            history_list := dcc.RadioItems(
                [],
                id="history_list_",
                style={
                    "fontFamily": "monospace",
                    "fontSize": "13px",
                }
            )
        ],
        style={
            "overflow": "scroll"
        }
    )
],
    id="history_modal_",
    style={
        "position": "absolute",
        "zIndex": -2,
        "width": 500,
        "top": 50,
        "bottom": 10,
        "left": "calc(50% - 250px)",
        "backgroundColor": __env__.color_theme.table_bg_2,
        "color": __env__.color_theme.table_fg_main,
        "padding": 10,
        "borderRadius": 10,
        "overflow": "scroll"
    }
)
