from dash import clientside_callback, Output, Input

import layout

clientside_callback(
    "c2Hide",
    Output(layout.c2Hide_trigger, "n_clicks"),
    Input(layout.c2Hide_trigger, "n_clicks"),
    prevent_initial_call=True
)


clientside_callback(
    "syncColumns",
    Output(layout.tradinglog, "id"),
    Input(layout.renderer_trigger, "n_clicks"),
    prevent_initial_call=True
)


clientside_callback(
    "autocomplete",
    Output(layout.autocomplet.autocdropdown, "value"),
    Input(layout.autocomplet.autocdropdown, "value"),
    prevent_initial_call=True
)


clientside_callback(
    "noteLinkPipe",
    Output(layout.note.noteLinkPipe, "value", allow_duplicate=True),
    Input(layout.note.noteLinkPipe, "value"),
    prevent_initial_call=True
)
