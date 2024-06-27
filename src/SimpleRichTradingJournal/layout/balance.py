from dash import html

import __env__

BALANCE = html.Div(
    [
        html.Div(
            html.Div(
                [
                    T_button_ := html.Button("\u2007\u2007T\u2007\u2007", style={"display": "inline-block", "margin": "1px"}, n_clicks=__env__.balanceT52W, id="T_button_"),
                    C_button_ := html.Button("\u2007\u2007~\u2007\u2007", style={"display": "inline-block", "margin": "1px"}, n_clicks=__env__.balanceCurrent, id="C_button_"),
                    Y_button_ := html.Button("\u2007\u2007Y\u2007\u2007", style={"display": "inline-block", "margin": "1px"}, n_clicks=__env__.balanceYears, id="Y_button_"),
                    Q_button_ := html.Button("\u2007\u2007Q\u2007\u2007", style={"display": "inline-block", "margin": "1px"}, n_clicks=__env__.balanceQuarters, id="Q_button_"),
                    T_trigger_ := html.Div("", style={"display": "none"}, n_clicks=__env__.balanceT52W, id="T_trigger_"),
                    C_trigger_ := html.Div("", style={"display": "none"}, n_clicks=__env__.balanceCurrent, id="C_trigger_"),
                    Y_trigger_ := html.Div("", style={"display": "none"}, n_clicks=__env__.balanceYears, id="Y_trigger_"),
                    Q_trigger_ := html.Div("", style={"display": "none"}, n_clicks=__env__.balanceQuarters, id="Q_trigger_"),
                ],
                style={
                    "position": "absolute",
                    "zIndex": 1,
                    "fontSize": "8px"
                }
            ),
        ),
        balance_content := html.Div(
            id="balance_content_",
            style={
                "height": "100%",
                "overflowY": "scroll"
            }
        ),
    ],
    id="balance_",
    style={
        "height": "100%",
        "display": ("" if __env__.sideInitBalanceValue else "none")
    }
)

