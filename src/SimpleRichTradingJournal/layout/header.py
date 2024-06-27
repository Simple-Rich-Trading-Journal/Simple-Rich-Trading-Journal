from dash import html, dcc

from config import styles, imgs
import __env__

_Deposits = "\u2007Deposits \u2007\u2007"
_Payouts = "\u2007Payouts \u2007\u2007"
_Fin = "\u2007Fin Trades \u2007\u2007"
_Open = "\u2007Open Trades \u2007\u2007"
_Dividends = "\u2007Dividends \u2007\u2007"
_ITCs = "\u2007ITCs \u2007\u2007"
_Undefined = "\u2007Undef. \u2007\u2007"
_marked = "\u2007marked \u2007\u2007"

scopes_x_func = {
    _Deposits: "params.data.cat == 'd'",
    _Payouts: "params.data.cat == 'p'",
    _Fin: "params.data.cat == 'tf'",
    _Open: "params.data.cat == 'to'",
    _Dividends: "(params.data.cat == 'v') || (params.data.cat == 'tf' && params.data.Dividend) || (params.data.cat == 'to' && params.data.Dividend)",
    _ITCs: "params.data.cat == 'i'",
    _Undefined: "params.data.cat == ''",
    _marked: "params.data.mark == 1"
}

_layout = [
    {"value": _Deposits, "label": html.Span(_Deposits, style=styles.log.name_DEPOSIT_tag)},
    {"value": _Payouts, "label": html.Span(_Payouts, style=styles.log.name_PAYOUT_tag)},
    {"value": _Fin, "label": html.Span(_Fin, style={"color": __env__.color_theme.table_fg_main})},
    {"value": _Open, "label": html.Span(_Open, style=styles.log.name_opentrade)},
    {"value": _Dividends, "label": html.Span(_Dividends, style=styles.log.name_dividend)},
    {"value": _ITCs, "label": html.Span(_ITCs, style=styles.log.name_ITC_tag)},
    {"value": _Undefined, "label": html.Span(_Undefined, style=styles.log.name_undefined)},
    {"value": _marked, "label": html.Span(_marked, style=styles.log.name_row_mark)},
]

scopes_check = dcc.Checklist(
    options=_layout,
    value=list(),
    inline=True,
    id="scopes_",
    style={
        "fontSize": "13px",
        "padding": "10px",
        "display": "inline-block",
    },
    className="noselect"
)
search_input = dcc.Input(
    placeholder="Search ...",
    id="quickSearch",
    style={
        "margin": "7px",
        "fontSize": "13px",
        "display": "inline-block",
    }
)
auto_save_button = html.Button(
    "Auto. Save",
    n_clicks=1,
    id="auto_save_button_",
    style={
        "display": "inline-block",
        "margin": "7px",
        "fontSize": "13px",
        "borderRadius": "15px",
    }
)
history_button = html.Button(
    "History",
    id="history_button_",
    n_clicks=0,
    style={
        "display": "inline-block",
        "margin": "7px",
        "fontSize": "13px",
        "color": __env__.color_theme.table_fg_header,
        "backgroundColor": __env__.color_theme.table_bg_main,
        "border": "1px solid " + __env__.color_theme.table_sep,
        "paddingLeft": "10px",
        "paddingRight": "10px",
        "borderRadius": "15px",
    }
)
export_button = html.Button(
    "Export",
    id="export_button_",
    n_clicks=0,
    style={
        # todo "display": "inline-block",
        "display": "none",

        "margin": "7px",
        "fontSize": "13px",
        "color": __env__.color_theme.table_fg_header,
        "backgroundColor": __env__.color_theme.table_bg_main,
        "border": "1px solid " + __env__.color_theme.table_sep,
        "paddingLeft": "10px",
        "paddingRight": "10px",
        "borderRadius": "15px",
    }
)
import_button = html.Button(
    "Import",
    id="import_button_",
    n_clicks=0,
    style={
        # todo "display": "inline-block",
        "display": "none",

        "margin": "7px",
        "fontSize": "13px",
        "color": __env__.color_theme.table_fg_header,
        "backgroundColor": __env__.color_theme.table_bg_main,
        "border": "1px solid " + __env__.color_theme.table_sep,
        "paddingLeft": "10px",
        "paddingRight": "10px",
        "borderRadius": "15px",
    }
)
reset_columns_button = html.Button(
    "Reset Columns",
    id="reset_columns_button_",
    n_clicks=0,
    style={
        "display": "inline-block",
        "margin": "7px",
        "fontSize": "13px",
        "color": __env__.color_theme.table_fg_header,
        "backgroundColor": __env__.color_theme.table_bg_main,
        "border": "1px solid " + __env__.color_theme.table_sep,
        "paddingLeft": "10px",
        "paddingRight": "10px",
        "borderRadius": "15px",
    }
)
statistics_button = html.Button(
    "STATISTICS",
    id="statistics_button_",
    n_clicks=__env__.sideInitStatisticValue,
    style={
        "display": "inline-block",
        "margin": "7px",
        "fontSize": "13px",
        "paddingLeft": "10px",
        "paddingRight": "10px",
        "borderRadius": "15px",
    } | styles.misc.statistics_button
)
balance_button = html.Button(
    "BALANCE",
    id="balance_button_",
    n_clicks=__env__.sideInitBalanceValue,
    style={
        "display": "inline-block",
        "margin": "7px",
        "fontSize": "13px",
        "paddingLeft": "10px",
        "paddingRight": "10px",
        "borderRadius": "15px",
    } | styles.misc.balance_button
)
daterange = dcc.DatePickerRange(
    clearable=True,
    display_format=__env__.timeFormatDaterange,
    start_date_placeholder_text=__env__.timeFormatDaterange,
    end_date_placeholder_text=__env__.timeFormatDaterange,
    first_day_of_week=__env__.dateFormatFirstDayOfWeek,
    number_of_months_shown=6,
    day_size=20,
    id="daterange_",
    style={
        "margin": "7px",
        "fontSize": "13px",
    }
)
index_by_button = html.Button(
    "Index by ...",
    n_clicks=__env__.indexByTakeTime,
    id="index_by_button_",
    style={
        "display": "inline-block",
        "margin": "7px",
        "fontSize": "13px",
        "paddingLeft": "10px",
        "paddingRight": "10px",
        "borderRadius": "15px",
    }
)
scope_by_button = html.Button(
    "Scope by ...",
    n_clicks=__env__.scopeByIndex,
    id="scope_by_button_",
    style={
        "display": "inline-block",
        "margin": "7px",
        "fontSize": "13px",
        "paddingLeft": "10px",
        "paddingRight": "10px",
        "borderRadius": "15px",
    }
)
with_open_button = html.Button(
    "with open",
    n_clicks=__env__.calcWithOpens,
    id="with_open_button_",
    style={
        "display": "inline-block",
        "margin": "7px",
        "fontSize": "13px",
        "paddingLeft": "10px",
        "paddingRight": "10px",
        "borderRadius": "15px",
    }
)
with_open_trigger = html.Div(id="with_open_trigger_", n_clicks=__env__.calcWithOpens, style={"display": "none"})

if __env__.coursePluginUpdateInterval and __env__.coursePluginUpdateIntervalOn:
    _interval_n = 1
    style_state = styles.misc.interval_on
else:
    _interval_n = 0
    style_state = styles.misc.interval_off
update_interval_button = html.Button(
    imgs.stats,
    n_clicks=_interval_n,
    id="update_interval_button_",
    style={
        "display": "inline-block",
        "margin": "7px",
        "fontSize": "13px",
        "paddingLeft": "10px",
        "paddingRight": "10px",
        "borderRadius": "15px",
    } | style_state,
)
update_interval = dcc.Interval(id="update_interval_", interval=__env__.coursePluginUpdateIntervalMs, disabled=(not __env__.coursePluginUpdateInterval) or (not __env__.coursePluginUpdateIntervalOn))
update_interval_trigger = html.Div(id="update_interval_trigger_", n_clicks=_interval_n, style={"display": "none"})
