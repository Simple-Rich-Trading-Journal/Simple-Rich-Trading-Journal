import __env__


undefined = {"color": __env__.color_theme.mark_gray}

name_row_mark = {"fontWeight": "bold", "backgroundColor": __env__.color_theme.row_mark}

name = {"backgroundColor": __env__.color_theme.col_name}
name_finalized_trade = name | {}
name_undefined = name | {"borderLeft": "8px solid " + __env__.color_theme.mark_undefined} | undefined
name_DEPOSIT_tag = name | {"color": __env__.color_theme.record_deposit, "borderLeft": "1px solid " + __env__.color_theme.record_deposit}
name_PAYOUT_tag = name | {"color": __env__.color_theme.record_payout, "borderLeft": "1px solid " + __env__.color_theme.record_payout}
name_ITC_tag = name | {"color": __env__.color_theme.record_itc, "borderLeft": "1px solid " + __env__.color_theme.record_itc}
name_dividend = name | {"color": __env__.color_theme.record_dividend, "borderLeft": "1px solid " + __env__.color_theme.record_dividend}
name_opentrade = name | {"color": __env__.color_theme.record_opentrade, "borderLeft": "1px solid " + __env__.color_theme.record_opentrade}
name_has_note = name | {"borderRight": "3px solid " + __env__.color_theme.mark_note}
name_has_dividend = name | {"borderLeft": "2px solid " + __env__.color_theme.record_dividend}

n = {"backgroundColor": __env__.color_theme.col_n}
n_default = n | {}
n_special = n | {"color": __env__.color_theme.mark_gray}
n_ignore = n | {"color": __env__.color_theme.mark_gray}

symbol = {"backgroundColor": __env__.color_theme.col_symbol}
isin = {"backgroundColor": __env__.color_theme.col_isin}
type = {"backgroundColor": __env__.color_theme.col_type}
short = {"backgroundColor": __env__.color_theme.col_short}
sector = {"backgroundColor": __env__.color_theme.col_sector}
category = {"backgroundColor": __env__.color_theme.col_sector}
rating = {"backgroundColor": __env__.color_theme.col_rating, "color": __env__.color_theme.table_bg_header}

invest_col = {"backgroundColor": __env__.color_theme.col_invest}
take_col = {"backgroundColor": __env__.color_theme.col_take}
course_take = {"backgroundColor": __env__.color_theme.col_take}
course_invest = {"backgroundColor": __env__.color_theme.col_invest}
itc_col = {"backgroundColor": __env__.color_theme.col_itc}
note = {"backgroundColor": __env__.color_theme.col_note}
result = {"backgroundColor": __env__.color_theme.col_result}
holdtime = {"backgroundColor": __env__.color_theme.col_holdtime}
statistics = {"backgroundColor": __env__.color_theme.col_hypotheses}
profit_pos = {"color": __env__.color_theme.cell_posvalue} | result
profit_neg = {"color": __env__.color_theme.cell_negvalue} | result
performance_pos = profit_pos | result
performance_neg = profit_neg | result
statistic_pos = {} | statistics
statistic_neg = {"color": __env__.color_theme.cell_negvalue} | statistics
deposit_row = {"borderTop": "1px solid " + __env__.color_theme.record_deposit}
payout_row = {"borderTop": "1px solid " + __env__.color_theme.record_payout}
dividend_row = {"borderTop": "1px solid " + __env__.color_theme.record_dividend}
itc_row = {"borderTop": "1px solid " + __env__.color_theme.record_itc}
invest_deposit = invest_col | deposit_row
invest_amount_deposit = invest_col | deposit_row | {"fontWeight": "bold"}
invest_deposit_null = invest_deposit | {"color": __env__.color_theme.mark_gray}
invest_payout = invest_col | payout_row
invest_dividend = invest_col | dividend_row
invest_itc = invest_col | itc_row
take_deposit_null = take_col | deposit_row | {"color": __env__.color_theme.mark_gray}
take_deposit = take_col | deposit_row
take_payout = take_col | payout_row
take_amount_payout = take_col | payout_row | {"fontWeight": "bold"}
take_dividend = take_col | dividend_row
take_amount_dividend = take_col | dividend_row | {"fontWeight": "bold"}
take_itc = take_col | itc_row
itc_itc = itc_col | itc_row | {"fontWeight": "bold"}
performance_itc = result | itc_row
performance_payout = result | payout_row
itc_dividend = itc_col | dividend_row
itc_deposit = itc_col | deposit_row
itc_payout = itc_col | payout_row
performance_pos_deposit = performance_pos | deposit_row | {"fontWeight": "bold"}
performance_neg_deposit = performance_neg | deposit_row | {"fontWeight": "bold"}
profit_pos_deposit = profit_pos | deposit_row
profit_neg_deposit = profit_neg | deposit_row
result_deposit = result | deposit_row
result_dividend = result | dividend_row | {"fontWeight": "bold"}
