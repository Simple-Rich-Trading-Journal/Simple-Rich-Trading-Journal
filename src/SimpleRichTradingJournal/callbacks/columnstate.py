from dash import callback, Output, Input, State, no_update

import __env__
import layout

if __env__.columnStateCache:

    @callback(
        Output(layout.tradinglog, "columnState", allow_duplicate=True),
        Output(layout.tradinglog, "columnDefs", allow_duplicate=True),
        Output(layout.colstate_done_trigger, "n_clicks", allow_duplicate=True),
        Input(layout.init_done_trigger2, "n_clicks"),
        State(layout.tradinglog, "columnDefs"),
        config_prevent_initial_callbacks=True
    )
    def init(n, col_defs):
        if __env__.iniColumnState and __env__.COLUMN_CACHE_DATA:
            widths = {c["colId"]: c["width"] for c in __env__.COLUMN_CACHE_DATA}
            for _col_def in col_defs:
                try:
                    _col_def["width"] = widths[_col_def["field"]]
                except KeyError:
                    try:
                        for child in _col_def["children"]:
                            child["width"] = widths[child["field"]]
                    except KeyError:
                        pass
            return __env__.COLUMN_CACHE_DATA, col_defs, 1
        else:
            return no_update, no_update, 1

    @callback(
        Output(layout.colstate_done_trigger, "id"),
        State(layout.colstate_done_trigger, "n_clicks"),
        Input(layout.tradinglog, "dashGridOptions"),
        Input(layout.tradinglog, "columnState"),
        config_prevent_initial_callbacks=True
    )
    def call(n, grid_opts, _state):
        if n:
            __env__.dump_column_state(_state)
        return no_update


@callback(
    Output(layout.tradinglog, "columnDefs", allow_duplicate=True),
    Output(layout.tradinglog, "resetColumnState"),
    Input(layout.header.reset_columns_button, "n_clicks"),
    config_prevent_initial_callbacks=True
)
def reset(_):
    __env__.dump_column_state(None)
    return layout.log.columnDefs, True
