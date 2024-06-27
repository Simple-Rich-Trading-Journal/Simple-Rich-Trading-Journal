from dash import html, dcc

import __env__

autocdropdown = dcc.Dropdown(
    id="autoCDropdown",
    style={
        "position": "absolute",
        "zIndex": -3,
        "width": 280,

    },
    optionHeight=20,
    maxHeight=__env__.gridRow3Height,
    className="autocdropdown"
)

autoctrigger = dcc.Input(id="autoCTrigger", style={"display": "none"})

COMPONENTS = html.Div([
    autocdropdown,
    autoctrigger
])
