from __future__ import annotations

from os import kill
from signal import SIGTERM

from dash import callback, Output, Input, State
from dash import html

import __env__
import __ini__.logtags
import layout


@callback(
    Output(layout.exiting.exit_modal_body, "children"),
    Output(layout.exiting_modal_trigger, "n_clicks"),
    Input(layout.exiting.exit_button, "n_clicks"),
    State(layout.exiting_modal_trigger, "n_clicks"),
    config_prevent_initial_callbacks=True
)
def exiting_req(_, n):
    msg = html.Div(
        html.Table(
            html.Tbody(
                [
                    html.Tr([html.Td("Address\u2007\u2007"), html.Th(f"{__env__.appHost}:{__env__.appPort}")]),
                    html.Tr([html.Td("PID\u2007\u2007"), html.Th(f"{__env__.SERVER_PROC.pid}")]),
                ]
            )
        )
    )
    return msg, n + 1


@callback(
    Output(layout.exiting.exit_modal_button, "children"),
    Input(layout.exiting.exit_modal_button, "n_clicks"),
    config_prevent_initial_callbacks=True
)
def confirm(_):
    return "Terminated"


@callback(
    Output(layout.exiting.exit_button, "id"),
    Input(layout.exiting.exit_modal_button, "children"),
    config_prevent_initial_callbacks=True
)
def exiting(_):
    print(__ini__.logtags.term, __env__.SERVER_PROC.pid, flush=True)
    kill(__env__.SERVER_PROC.pid, SIGTERM)
