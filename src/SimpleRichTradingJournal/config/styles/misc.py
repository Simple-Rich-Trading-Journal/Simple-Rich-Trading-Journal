import __env__

modal_close = {"border": "1px solid " + __env__.color_theme.table_sep, "backgroundColor": __env__.color_theme.top_onoff_bg, "borderRadius": 25, "height": 50}

term_button = {"border": "1px solid " + __env__.color_theme.table_sep, "backgroundColor": __env__.color_theme.top_onoff_bg, "borderRadius": 25}

by_taketime_on = {"color": __env__.color_theme.table_fg_header, "border": "1px solid " + __env__.color_theme.table_sep, "backgroundColor": __env__.color_theme.col_take, "backgroundImage": ""}
by_taketime_off = by_taketime_on | {"backgroundColor": __env__.color_theme.col_invest}

by_index_off = by_taketime_on | {"backgroundColor": __env__.color_theme.table_bg_main, "backgroundImage": __env__.color_theme.top_by_index_off}

with_open_on = {"color": __env__.color_theme.table_fg_main, "border": "1px solid " + __env__.color_theme.table_sep, "backgroundColor": __env__.color_theme.record_opentrade}
with_open_off = by_taketime_on | {"color": __env__.color_theme.table_fg_header, "backgroundColor": __env__.color_theme.table_bg_main}

autosave_on = {"color": __env__.color_theme.top_onoff_fg, "border": "1px solid " + __env__.color_theme.table_sep, "backgroundColor": __env__.color_theme.top_onoff_bg}
autosave_off = {"color": __env__.color_theme.table_fg_header, "border": "1px solid " + __env__.color_theme.table_sep, "backgroundColor": ""}

group_by_options_off = {"color": __env__.color_theme.table_fg_main, "border": "1px solid " + __env__.color_theme.table_sep, "backgroundColor": __env__.color_theme.table_bg_main}
group_by_options_on = group_by_options_off | {"backgroundColor": __env__.color_theme.top_onoff_bg}
framing_options_off = {"color": __env__.color_theme.table_fg_main, "border": "1px solid " + __env__.color_theme.table_sep, "backgroundColor": __env__.color_theme.table_bg_main}
framing_options_on = framing_options_off | {"backgroundColor": __env__.color_theme.top_onoff_bg}
performance_size = {}

interval_on = {"color": __env__.color_theme.top_onoff_fg, "border": "1px solid " + __env__.color_theme.table_sep, "backgroundColor": __env__.color_theme.top_onoff_bg}
interval_off = {"color": __env__.color_theme.table_fg_header, "border": "1px solid " + __env__.color_theme.table_sep, "backgroundColor": ""}

summary_footer = {"color": __env__.color_theme.table_fg_main, "backgroundColor": __env__.color_theme.table_bg_header}
summary_error = {"borderTop": "5px solid " + __env__.color_theme.mark_error}
summary_error_reset = {"borderTop": ""}

statistics_button = {
    "color": __env__.color_theme.table_fg_main,
    "backgroundColor": __env__.color_theme.table_bg_main,
    "border": "1px solid " + __env__.color_theme.statistics_button_border,
    "boxShadow": __env__.color_theme.statistics_button_shadow + " 0px 3px 10px",
}
balance_button = {
    "color": __env__.color_theme.table_fg_main,
    "backgroundColor": __env__.color_theme.table_bg_main,
    "border": "1px solid " + __env__.color_theme.balance_button_border,
    "boxShadow": __env__.color_theme.balance_button_shadow + " 0px 3px 10px",
}
statistics_split_handle = {
    "border": "1px solid " + __env__.color_theme.statistics_button_border,
    "boxShadow": __env__.color_theme.statistics_button_shadow + " 0px 3px 10px",
    "width": "4px",
}
balance_split_handle = {
    "border": "1px solid " + __env__.color_theme.balance_button_border,
    "boxShadow": __env__.color_theme.balance_button_shadow + " 0px 3px 10px",
    "width": "4px",
}

header = {"borderBottom": "1px solid " + __env__.color_theme.table_sep}
