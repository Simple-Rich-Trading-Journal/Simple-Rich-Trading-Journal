from __future__ import annotations

from dash import callback, Output, Input, State, callback_context

import layout
from config import styles


layer_open = layout.modal.modal_layer.style | {"zIndex": 99}
layer_close = layout.modal.modal_layer.style | {"zIndex": -3}
button_open = layout.modal.close_button.style | {"zIndex": 101}
button_close = layout.modal.close_button.style | {"zIndex": -3}
history_open = layout.history.MODAL.style | {"zIndex": 100}
history_close = layout.history.MODAL.style | {"zIndex": -3}
about_open = layout.about.MODAL.style | {"zIndex": 100}
about_close = layout.about.MODAL.style | {"zIndex": -3}
statistics_pop_open = layout.statistics.POP.style | {"zIndex": 100}
statistics_pop_close = layout.statistics.POP.style | {"zIndex": -3}
exiting_open = layout.exiting.MODAL.style | {"zIndex": 100}
exiting_close = layout.exiting.MODAL.style | {"zIndex": -3}


@callback(
    Output(layout.about.MODAL, "style", allow_duplicate=True),
    Output(layout.modal.modal_layer, "style", allow_duplicate=True),
    Output(layout.modal.close_button, "style", allow_duplicate=True),
    Input(layout.about.about_button, "n_clicks"),
    config_prevent_initial_callbacks=True
)
def open_about_modal(_):
    return about_open, layer_open, button_open


@callback(
    Output(layout.history.MODAL, "style", allow_duplicate=True),
    Output(layout.modal.modal_layer, "style", allow_duplicate=True),
    Output(layout.modal.close_button, "style", allow_duplicate=True),
    Input(layout.header.history_button, "n_clicks"),
    config_prevent_initial_callbacks=True
)
def open_backup_modal(_):
    return history_open, layer_open, button_open


@callback(
    Output(layout.statistics.POP, "style", allow_duplicate=True),
    Output(layout.modal.modal_layer, "style", allow_duplicate=True),
    Output(layout.modal.close_button, "style", allow_duplicate=True),
    Input(layout.statistics_pop_trigger, "n_clicks"),
    config_prevent_initial_callbacks=True
)
def statistics_pop_modal(_):
    return statistics_pop_open, layer_open, button_open


@callback(
    Output(layout.exiting.MODAL, "style", allow_duplicate=True),
    Output(layout.modal.modal_layer, "style", allow_duplicate=True),
    Output(layout.modal.close_button, "style", allow_duplicate=True),
    Input(layout.exiting_modal_trigger, "n_clicks"),
    config_prevent_initial_callbacks=True
)
def exiting_modal(_):
    return exiting_open, layer_open, button_open


@callback(
    Output(layout.history.MODAL, "style", allow_duplicate=True),
    Output(layout.about.MODAL, "style", allow_duplicate=True),
    Output(layout.statistics.POP, "style", allow_duplicate=True),
    Output(layout.exiting.MODAL, "style", allow_duplicate=True),
    Output(layout.modal.modal_layer, "style", allow_duplicate=True),
    Output(layout.modal.close_button, "style", allow_duplicate=True),
    Input(layout.modal.modal_layer, "n_clicks"),
    Input(layout.modal.close_button, "n_clicks"),
    Input(layout.esc_trigger, "value"),
    config_prevent_initial_callbacks=True
)
def close(*_):
    return history_close, about_close, statistics_pop_close, exiting_close, layer_close, button_close


@callback(
    Output(layout.statistics.group_by_settings, "style"),
    Output(layout.statistics.framing_settings, "style"),
    Output(layout.statistics.group_by_button, "style"),
    Output(layout.statistics.framing_button, "style"),
    Input(layout.statistics.group_by_button, "n_clicks"),
    Input(layout.statistics.framing_button, "n_clicks"),
    State(layout.statistics.group_by_settings, "style"),
    State(layout.statistics.framing_settings, "style"),
    State(layout.statistics.group_by_button, "style"),
    State(layout.statistics.framing_button, "style"),
    config_prevent_initial_callbacks=True
)
def open_group_by(g_n, f_n, g_style, f_style, g_b_style, f_b_style):
    if callback_context.triggered_id == layout.statistics.framing_button.id:
        g_style |= {"zIndex": -3}
        g_b_style |= styles.misc.group_by_options_off
        if f_style["zIndex"] == -3:
            f_style |= {"zIndex": 15}
            f_b_style |= styles.misc.framing_options_on
        else:
            f_style |= {"zIndex": -3}
            f_b_style |= styles.misc.framing_options_off
    else:
        f_style |= {"zIndex": -3}
        f_b_style |= styles.misc.framing_options_off
        if g_style["zIndex"] == -3:
            g_style |= {"zIndex": 15}
            g_b_style |= styles.misc.group_by_options_on
        else:
            g_style |= {"zIndex": -3}
            g_b_style |= styles.misc.group_by_options_off
    return g_style, f_style, g_b_style, f_b_style
