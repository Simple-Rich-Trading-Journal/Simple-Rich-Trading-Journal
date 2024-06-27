from dash import callback, Output, Input, callback_context, no_update, State

import layout
from config import styles


@callback(
    Output(layout.c2Hide_trigger, "n_clicks", allow_duplicate=True),
    Output(layout.header.statistics_button, "n_clicks"),
    Output(layout.header.balance_button, "n_clicks"),
    Output(layout.statistics.STATISTICS, "style"),
    Output(layout.balance.BALANCE, "style"),
    Output(layout.split_handle, "style"),
    Input(layout.header.statistics_button, "n_clicks"),
    Input(layout.header.balance_button, "n_clicks"),
    State(layout.statistics.STATISTICS, "style"),
    State(layout.balance.BALANCE, "style"),
    State(layout.split_handle, "style"),
    config_prevent_initial_callbacks=True
)
def c2(
        i_statistics_button_n_clicks,
        i_balance_button_n_clicks,
        i_style_statistics,
        i_style_balance,
        i_style_split_handle,
):
    if callback_context.triggered_id == layout.header.statistics_button.id:
        if i_statistics_button_n_clicks % 2:
            i_style_statistics["display"] = ""
            i_style_balance["display"] = "none"
            i_style_split_handle |= styles.misc.statistics_split_handle
            return 2, no_update, 0, i_style_statistics, i_style_balance, i_style_split_handle
        else:
            i_style_statistics["display"] = "none"
            i_style_balance["display"] = "none"
            i_style_split_handle = no_update
            return 1, 0, 0, i_style_statistics, i_style_balance, i_style_split_handle
    elif callback_context.triggered_id == layout.header.balance_button.id:
        if i_balance_button_n_clicks % 2:
            i_style_statistics["display"] = "none"
            i_style_balance["display"] = ""
            i_style_split_handle |= styles.misc.balance_split_handle
            return 2, 0, no_update, i_style_statistics, i_style_balance, i_style_split_handle
        else:
            i_style_statistics["display"] = "none"
            i_style_balance["display"] = "none"
            i_style_split_handle = no_update
            return 1, 0, 0, i_style_statistics, i_style_balance, i_style_split_handle
    else:
        return no_update
