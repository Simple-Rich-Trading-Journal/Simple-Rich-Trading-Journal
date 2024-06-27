from dash import html

from calc.log import LogCalc
from calc.utils import durationformat

_style_footer_col = {
    "display": "inline-block",
    "width": "25%"
}
_style_col_table = {
    "width": "100%",
}


def make_footer(lc: LogCalc):
    return html.Div([
        html.Div([
            html.Table([
                html.Tbody([
                    html.Tr([
                        html.Th("Portfolio age"),
                        html.Td(durationformat(lc.portfolio_age_sec), style={"textAlign": "end"}),
                    ], style={"borderBottom": "3px double"}),
                    html.Tr([
                        html.Th("Deposits"),
                        html.Td(f"{lc.sum_deposits:,.2f}", style={"textAlign": "end"}),
                    ]),
                    html.Tr([
                        html.Th("Payouts"),
                        html.Td(f"{lc.sum_payouts:,.2f}", style={"textAlign": "end"}),
                    ]),
                    html.Tr([
                        html.Th("Money"),
                        html.Td(f"{lc.sum_deposits - lc.sum_payouts:,.2f}", style={"textAlign": "end"}),
                    ], style={"borderTop": "1px solid"}),
                ])
            ], style=_style_col_table),
        ], style=_style_footer_col | {"verticalAlign": "top", "paddingRight": "5rem"}),
        html.Div([
            html.Table([
                html.Tbody([
                    html.Tr([
                        html.Th(), html.Th("open"), html.Th("total")
                    ], style={"borderBottom": "3px double"}),
                    html.Tr([
                        html.Th("Positions"),
                        html.Td(f"{lc.n_trades_open}"),
                        html.Td(f"{lc.n_trades_open + lc.n_trades_fin}"),
                    ]),
                    html.Tr([
                        html.Th("Amount"),
                        html.Td(f"{lc.sum_open_invest:,.2f}"),
                        html.Td(f"{lc.sum_open_invest + lc.sum_fin_invest:,.2f}"),
                    ]),
                ])
            ], style=_style_col_table),
        ], style=_style_footer_col | {"verticalAlign": "top", "paddingRight": "5rem"}),
        html.Div([
            html.Table([
                html.Tbody([
                    html.Tr([
                        html.Th("-avg"), html.Th("performance", style={"textAlign": "end"}), html.Th("profit", style={"textAlign": "end"})
                    ], style={"borderBottom": "3px double"}),
                    html.Tr([
                        html.Th("Trade"),
                        html.Td(f"{lc.performance_trade_avg:,.2%}", style={"textAlign": "end"}),
                        html.Td(f"{lc.profit_trade_avg:,.2f}", style={"textAlign": "end"}),
                    ]),
                    html.Tr([
                        html.Th("Day"),
                        html.Td(f"{lc.avg_performance_per_day:,.2%}", style={"textAlign": "end"}),
                        html.Td(f"{lc.avg_profit_per_day:,.2f}", style={"textAlign": "end"}),
                    ]),
                    html.Tr([
                        html.Th("Hold Time"),
                        html.Td(durationformat(lc.holdtime_of_fin_trades_avg), style={"textAlign": "left"}, colSpan=2),
                    ]),
                ])
            ], style=_style_col_table),
        ], style=_style_footer_col | {"verticalAlign": "top", "paddingRight": "5rem"}),
        html.Div([
            html.Table([
                html.Tbody([
                    html.Tr([
                        html.Th(), html.Th("$"), html.Th("Current %"), html.Th("Dripping %")
                    ]),
                    html.Tr([
                        html.Th("Profits"),
                        html.Td(f"{lc.sum_profits:,.2f}"),
                        html.Td(f"{lc.current_performance_on_portfolio:,.2%}"),
                        html.Td(f"{lc.dripping_performance_avg:,.2%}"),
                    ]),
                    html.Tr([
                        html.Th("Dividends"),
                        html.Td(f"{lc.sum_dividends:,.2f}"),
                        html.Td(f"{lc.current_dividend_rate:,.2%}"),
                        html.Td(f"{lc.dripping_dividend_rate:,.2%}"),
                    ]),
                    html.Tr([
                        html.Th("ITCs"),
                        html.Td(f"{lc.sum_itcs:,.2f}"),
                        html.Td(f"{lc.current_itcs_rate:,.2%}"),
                        html.Td(),
                    ]),
                    html.Tr([
                        html.Th(),
                        html.Td(f"{lc.summary_value:,.2f}", style={"borderTop": "1px solid"}),
                        html.Td(f"{lc.current_summary_rate:,.2%}", style={"borderTop": "1px solid"}),
                        html.Td(style={"borderTop": "1px solid"}),
                    ]),
                ])
            ], style=_style_col_table | {"textAlign": "end"}),
        ], style=_style_footer_col | {"textAlign": "end", "verticalAlign": "bottom"}),
    ],
        style={
            "fontSize": "12px",
            "padding": "10px",
        })
