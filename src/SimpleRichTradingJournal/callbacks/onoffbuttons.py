from __future__ import annotations

from dash import callback, Output, Input, State, no_update
from dash import html

import layout
from config import styles


def _make_callback(
    button_obj: html.Button,
    trigger_obj: html.Div,
    button_on_style: dict,
    button_on_children,
    button_off_style: dict,
    button_off_children,
):
    @callback(
        Output(trigger_obj, "n_clicks"),
        Output(button_obj, "style"),
        Output(button_obj, "children"),
        Input(button_obj, "n_clicks"),
        State(button_obj, "style"),
    )
    def call(n, style, bons=button_on_style, bonc=button_on_children, boffs=button_off_style, boffc=button_off_children):
        if n % 2:
            return n, style | bons, bonc
        else:
            return n, style | boffs, boffc


_make_callback(layout.balance.T_button_, layout.balance.T_trigger_, styles.balance.t52w_button_on, no_update, styles.balance.t52w_button_off, no_update)
_make_callback(layout.balance.C_button_, layout.balance.C_trigger_, styles.balance.current_button_on, no_update, styles.balance.current_button_off, no_update)
_make_callback(layout.balance.Y_button_, layout.balance.Y_trigger_, styles.balance.year_button_on, no_update, styles.balance.year_button_off, no_update)
_make_callback(layout.balance.Q_button_, layout.balance.Q_trigger_, styles.balance.quarter_button_on, no_update, styles.balance.quarter_button_off, no_update)
_make_callback(layout.header.with_open_button, layout.header.with_open_trigger, styles.misc.with_open_on, no_update, styles.misc.with_open_off, no_update)
