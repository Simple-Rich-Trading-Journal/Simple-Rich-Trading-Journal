#####################################################
# https://dash.plotly.com/dash-ag-grid/styling-themes
table_theme = "ag-theme-alpine"
######################################################

# main
table_bg_main = "white"
table_bg_2 = "white"
table_bg_header = "white"
table_fg_main = "black"
table_fg_header = "black"
table_sep = "silver"

# /log/row mark
row_mark = ""

# /log/alt colors
alt_neg = ""
alt_pos = ""

# /log/columns
col_name = None
col_symbol = None
col_isin = None
col_type = None
col_short = None
col_sector = None
col_category = None
col_rating = None
col_n = None
col_invest = None
col_take = None
col_itc = None
col_result = None
col_holdtime = None
col_note = None
col_hypotheses = None

# /log/record/special labels and separators
record_deposit = ""
record_payout = ""
record_itc = ""
record_dividend = ""
record_opentrade = ""

# /log/record/result highlight
cell_posvalue = None
cell_negvalue = None

# /log/record/other markings
mark_note = ""
mark_gray = ""
mark_error = ""
mark_undefined = ""

# /log/record/rating
rating_scale = [
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
]
alt_rating_scale = [
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
]

# /statistics/figure/main
figure_plot = None
figure_paper = None
figure_font = None
figure_grid = None
figure_spike = None

# /statistics/figure/traces
trace_profit = None
trace_summary = None
trace_current_performance = None
trace_dripping_performance = None
trace_summary_rate = None
trace_deposit = None
trace_payout = None
trace_money = None
trace_trade_sum_invest = None
trace_trade_sum_take = None
trace_trade_performance = None
trace_profit_per_day_avg = None
trace_performance_per_day_avg = None
trace_trade_sum_invest_trailing = None
trace_trade_sum_take_trailing = None
trace_trade_performance_trailing = None
trace_profit_per_day_avg_trailing = None
trace_performance_per_day_avg_trailing = None
trace_activity = None
trace_holdtime_avg = None


class color_palette_positions:

    @staticmethod
    def copy():
        return color_palette_positions

    @staticmethod
    def pop(_):
        return None


# /statistics/figure/shape
shape_last_calc = None

# /footer/open sidebar
statistics_button_border = ""
statistics_button_shadow = ""
balance_button_border = ""
balance_button_shadow = ""

# /footer/life signal
footer_sig1 = ""
footer_sig2 = ""

# /top bar
top_onoff_bg = ""
top_onoff_fg = ""
top_by_index_off = ""

# /balance
sheet_col1_sep = ""
sheet_col_year = ""
sheet_header_year = ""
sheet_quarter_sep = ""
sheet_current_sep = ""
sheet_col_t52 = ""
sheet_header_t52 = ""
sheet_col_current = ""
sheet_header_current = ""
sheet_cell_active_bg = ""
sheet_cell_selected_bg = ""
sheet_hover_bg = ""

# /notepaper
notepaper_bg = "white"
notepaper_def_transparency = ""
notepaper_fg = "black"
notepaper_border = ""
notepaper_link = "blue"

# /noteeditor
notebook_bg = ""
notebook_def_transparency = ""
notebook_gutter_bg = ""
notebook_def_gutter_transparency = ""

# /noteeditor/dialog
noteeditor_dialog_fg = ""
noteeditor_dialog_bg = ""
noteeditor_dialog_border = ""
noteeditor_dialog_ignore = ""
noteeditor_dialog_rename = ""
noteeditor_dialog_overwrite = ""
