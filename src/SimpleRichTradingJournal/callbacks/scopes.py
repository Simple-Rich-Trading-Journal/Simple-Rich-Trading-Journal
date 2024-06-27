from time import perf_counter

from dash import State, Output, Input, callback, no_update

import layout

_pre_scopes = set()
_pre_scopes_t = 0
_pre_scopes_d = ""
_pre_scopes_l = 0

_doubleClickTime = 0.3


@callback(
    Output(layout.tradinglog, "dashGridOptions", allow_duplicate=True),
    Output(layout.header.scopes_check, "value", allow_duplicate=True),
    Input(layout.header.scopes_check, "value"),
    config_prevent_initial_callbacks=True
)
def scopes_check(scopes):
    global _pre_scopes, _pre_scopes_t, _pre_scopes_d, _pre_scopes_l
    t = perf_counter()
    scopes = set(scopes)
    len_scopes = len(scopes)
    try:
        if t - _pre_scopes_t <= _doubleClickTime:
            if diff := (scopes.difference(_pre_scopes) or _pre_scopes.difference(scopes)):
                diff = diff.pop()
                _pre_scopes_d = diff
                if diff == _pre_scopes_d:
                    if _pre_scopes_l == 1:
                        scopes = list(layout.header.scopes_x_func)
                        scopes.remove(diff)
                        scopes = set(scopes)
                    else:
                        scopes = {diff}
                elif len(_pre_scopes) >= 1:
                    scopes = {diff}
                else:
                    scopes = list(layout.header.scopes_x_func)
                    scopes.remove(diff)
                    scopes = set(scopes)

                _pre_scopes_l = len(scopes)

        elif len_scopes in (0, 7):
            opts = layout.log._dashGridOptions | {
                "isExternalFilterPresent": {"function": "false"},
                "doesExternalFilterPass": {"function": "true"}
            }
            return opts, no_update

        opts = layout.log._dashGridOptions | {
            "isExternalFilterPresent": {"function": "true"},
            "doesExternalFilterPass": {"function": str(" || ").join(func for k, func in layout.header.scopes_x_func.items() if k in scopes)}
        }
        return opts, list(scopes)

    finally:
        _pre_scopes = scopes
        _pre_scopes_t = t


@callback(
    Output(layout.tradinglog, "dashGridOptions", allow_duplicate=True),
    Input(layout.header.search_input, "value"),
    State(layout.tradinglog, "dashGridOptions"),
    State(layout.quick_search_receiver, "value"),
    config_prevent_initial_callbacks=True
)
def quick_search(val, opt, ctrl_qick_search):
    if ctrl_qick_search:
        return opt | {"quickFilterText": None}
    else:
        return opt | {"quickFilterText": val}
