from __future__ import annotations

from collections import OrderedDict
from typing import Literal, Callable, Any

from dash import html
from dash.dash_table import DataTable
from datetime import datetime, timedelta

from calc.log import LogCalc
from calc.utils import preventZeroDiv
from config import styles

_i = 0


def __sep():
    global _i
    _i += 1
    return {f"\u200b1{_i}": lambda x: None}


def __sep2():
    global _i
    _i += 1
    return {f"\u200b2{_i}": lambda x: None}


def __space():
    global _i
    _i += 1
    return {f"\u200b3{_i}": lambda x: None}


def __space1():
    global _i
    _i += 1
    return {f"\u200b4{_i}": lambda x: None}


def __gr2(i):
    if i is None:
        return "N/A"
    else:
        return f"{i:,.2f}"


def __p2(i):
    if i is None:
        return "N/A"
    else:
        return f"{i:,.2%}"


_records_def: OrderedDict[Any, Callable[[LogCalc], Any]] = OrderedDict()
_records_def |= __space1()
_records_def["DEPOSITS"] = lambda x: x.n_frame_deposits
_records_def["\u200b"] = lambda x: __gr2(x.sum_deposits)
_records_def |= __sep()
_records_def["PAYOUTS"] = lambda x: x.n_frame_payouts
_records_def["\u200b\u200b"] = lambda x: __gr2(x.sum_payouts)
_records_def |= __sep()
_records_def["MONEY"] = lambda x: __gr2(x.money)
_records_def |= __sep2()
_records_def |= __space()
_records_def["OPENINGS (O)"] = lambda x: x.n_openings
_records_def |= __sep()
_records_def["\u2007\u2007invest"] = lambda x: __gr2(x.openings_invest_amount)
_records_def["\u2007\u2007take"] = lambda x: __gr2(x.openings_take_amount)
_records_def["\u2007\u2007profit"] = lambda x: __gr2(x.sum_openings_profit)
_records_def["\u2007\u2007perf."] = lambda x: __p2(preventZeroDiv(x.sum_openings_profit, x.money, None))
_records_def |= __sep()
_records_def |= __space()
_records_def["CLOSURES (C)"] = lambda x: x.n_closures
_records_def |= __sep()
_records_def["\u2007\u2007invest\u200b"] = lambda x: __gr2(x.closures_invest_amount)
_records_def["\u2007\u2007take\u200b"] = lambda x: __gr2(x.closures_take_amount)
_records_def["\u2007\u2007profit\u200b"] = lambda x: __gr2(x.sum_closures_profit)
_records_def["\u2007\u2007perf.\u200b"] = lambda x: __p2(preventZeroDiv(x.sum_closures_profit, x.money, None))
_records_def |= __sep()
_records_def |= __space()
_records_def["C/O"] = lambda x: __gr2(preventZeroDiv(x.n_closures, x.n_openings, None))
_records_def |= __sep()
_records_def["\u2007\u2007invest\u200b\u200b"] = lambda x: __gr2(preventZeroDiv(x.closures_invest_amount, x.openings_invest_amount, None))
_records_def["\u2007\u2007take\u200b\u200b"] = lambda x: __gr2(preventZeroDiv(x.closures_take_amount, x.openings_take_amount, None))
_records_def["\u2007\u2007profit\u200b\u200b"] = lambda x: __gr2(preventZeroDiv(x.sum_closures_profit, x.sum_openings_profit, None))
_records_def["\u2007\u2007perf.\u200b\u200b"] = lambda x: __gr2(preventZeroDiv(preventZeroDiv(x.sum_openings_profit, x.money, 0), preventZeroDiv(x.sum_closures_profit, x.money, 0), None))
_records_def |= __sep()
_records_def |= __space()
_records_def["C&O"] = lambda x: "\u200b"
_records_def |= __sep()
_records_def["\u2007\u2007Ø profit/trade"] = lambda x: __gr2(x.profit_trade_avg)
_records_def["\u2007\u2007Ø perf./trade"] = lambda x: __gr2(x.performance_trade_avg)
_records_def["\u2007\u2007Ø profit/day"] = lambda x: __gr2(x.avg_profit_per_day)
_records_def["\u2007\u2007Ø perf/day"] = lambda x: __gr2(x.avg_performance_per_day)
_records_def["\u2007\u2007Ø profit/year"] = lambda x: __gr2(x.avg_profit_per_year)
_records_def["\u2007\u2007Ø perf/year"] = lambda x: __gr2(x.avg_performance_per_year)
_records_def["\u2007\u2007Ø holddays"] = lambda x: __gr2(x.holdtime_of_all_avg / 86400)
_records_def |= __sep2()
_records_def |= __space()
_records_def["DIVIDENDS"] = lambda x: x.n_dividends
_records_def |= __sep()
_records_def["\u200b\u200b\u200b"] = lambda x: __gr2(x.sum_dividends)
_records_def["\u2007\u2007dripping rate"] = lambda x: __p2(x.dripping_dividend_rate)
_records_def["\u2007\u2007current rate"] = lambda x: __p2(x.current_dividend_rate)
_records_def |= __sep()
_records_def |= __space()
_records_def["ITCs"] = lambda x: x.n_itcs
_records_def |= __sep()
_records_def["\u200b\u200b\u200b\u200b"] = lambda x: __gr2(x.sum_itcs)
_records_def["\u200b\u200b\u200b\u200b\u200b"] = lambda x: __p2(x.current_itcs_rate)
_records_def |= __sep2()
_records_def |= __space()
_records_def["PROFIT"] = lambda x: __gr2(x.sum_profits)
_records_def |= __sep()
_records_def["\u2007\u2007dripping perf."] = lambda x: __p2(x.dripping_performance_avg)
_records_def["\u2007\u2007current perf."] = lambda x: __p2(x.current_performance_on_portfolio)
_records_def |= __sep()
_records_def |= __space()
_records_def["SUMMARY"] = lambda x: __gr2(x.summary_value)
_records_def |= __sep()
_records_def["\u2007\u2007current rate\u200b\u200b"] = lambda x: __p2(x.current_summary_rate)
_records_def |= __sep2()
_records_def |= __space()
_records_def |= __sep2()

_rows = [{"_": r} for r in _records_def]

_style_data_conditional = [
    {"if": {"filter_query": "{_} contains '\u200b1'"}} | styles.balance.sep,
    {"if": {"filter_query": "{_} contains '\u200b2'"}} | styles.balance.sep2,
    {"if": {"filter_query": "{_} contains '\u200b3'"}} | styles.balance.space,
    {"if": {"filter_query": "{_} contains '\u200b4'"}} | styles.balance.space1,
    {"if": {"state": "active"}} | styles.balance.active,
    {"if": {"state": "selected"}} | styles.balance.selected,
]

_dt1 = DataTable(
    _rows,
    [{"name": "\u2007", "id": "_"}],
    style_cell=styles.balance.col1_cell_default,
    style_header=styles.balance.col1_header_default,
    style_data_conditional=_style_data_conditional,
)


class _Balance:
    new_calc: bool
    new_vis: bool
    lc: LogCalc
    by_attr: Literal["idx", "min", "max", "or"] | str

    vis_years: bool
    vis_quarters: bool
    vis_t52w: bool
    vis_current_: bool

    records: list
    columns: list
    years: list
    quarters: list
    style_data_conditional: list
    style_header_conditional: list
    current_: tuple[str, str]
    t52w: str

    dt: DataTable

    def __init__(
            self,
            lc: LogCalc,
            by_attr: Literal["idx", "min", "max", "or"] | str = "or",
            years: bool = True,
            quarters: bool = True,
            t52w: bool = True,
            current_: bool = True,
    ):
        self.lc = lc
        self.opt__by_attr(by_attr)
        self.opt__visible(years, quarters, t52w, current_)
        self.records = list()
        self.columns = list()
        self.years = list()
        self.quarters = list()
        self.style_data_conditional = list()
        self.style_header_conditional = list()
        self.current_ = ("", "")
        self.t52w = ""
        self.dt = DataTable()

    def opt__by_attr(self, by_attr: Literal["idx", "min", "max", "or"] | str = "or"):
        self.by_attr = by_attr
        self.new_calc = True

    def opt__visible(
            self,
            years: bool = True,
            quarters: bool = True,
            t52w: bool = True,
            current_: bool = True,
    ):
        self.vis_years = years
        self.vis_quarters = quarters
        self.vis_t52w = t52w
        self.vis_current_ = current_
        self.new_vis = True

    def get(self):
        if first_record := self.lc.first_record:
            if self.new_calc:
                self.new_calc = False
                self.new_vis = True

                this_date = datetime.now()

                data = dict()
                columns = list()
                self.years = list()
                self.quarters = list()

                def add_frame(col, frame: LogCalc):

                    for rec, func in _records_def.items():
                        data.setdefault(rec, dict())[col] = func(frame)

                    columns.append(col)

                first_date = first_record._min_date
                first_year = first_date.year
                this_year = this_date.year
                first_quarter = (first_date.month - (first_date.month % 3)) + 1
                this_quarter = (this_date.month - (this_date.month % 3)) + 1

                if first_year == this_year:
                    for mo in range(first_quarter, this_quarter, 3):
                        q = f"Q{(mo - 1) // 3 + 1} {first_year}"
                        self.quarters.append(q)
                        add_frame(
                            q,
                            self.lc.getTradeFrame(datetime(first_year, mo, 1), datetime(first_year, mo + 3, 1), by_attr=self.by_attr)
                        )
                    current_quarter = f"~Q{(this_quarter - 1) // 3 + 1} {first_year}"
                    add_frame(
                        current_quarter,
                        self.lc.getTradeFrame(datetime(first_year, 10, 1), datetime(first_year + 1, 1, 1), by_attr=self.by_attr)
                    )
                    current_year = f"~Y{first_year}"
                    add_frame(
                        current_year,
                        self.lc.getTradeFrame(first_date, datetime(first_year + 1, 1, 1), by_attr=self.by_attr)
                    )
                else:
                    for mo in range(first_quarter, 10, 3):
                        q = f"Q{(mo - 1) // 3 + 1} {first_year}"
                        self.quarters.append(q)
                        add_frame(
                            q,
                            self.lc.getTradeFrame(datetime(first_year, mo, 1), datetime(first_year, mo + 3, 1), by_attr=self.by_attr)
                        )
                    q = f"Q4 {first_year}"
                    self.quarters.append(q)
                    add_frame(
                        q,
                        self.lc.getTradeFrame(datetime(first_year, 10, 1), datetime(first_year + 1, 1, 1), by_attr=self.by_attr)
                    )
                    y = f"Y{first_year}"
                    self.years.append(y)
                    add_frame(
                        y,
                        self.lc.getTradeFrame(first_date, datetime(first_year + 1, 1, 1), by_attr=self.by_attr)
                    )
                    for year in range(first_year + 1, this_year):
                        for q, mo in enumerate(range(1, 10, 3), 1):
                            q = f"Q{q} {year}"
                            self.quarters.append(q)
                            add_frame(
                                q,
                                self.lc.getTradeFrame(datetime(year, mo, 1), datetime(year, mo + 3, 1), by_attr=self.by_attr)
                            )
                        q = f"Q4 {year}"
                        self.quarters.append(q)
                        add_frame(
                            q,
                            self.lc.getTradeFrame(datetime(year, 10, 1), datetime(year + 1, 1, 1), by_attr=self.by_attr)
                        )
                        y = f"Y{year}"
                        self.years.append(y)
                        add_frame(
                            y,
                            self.lc.getTradeFrame(datetime(year, 1, 1), datetime(year + 1, 1, 1), by_attr=self.by_attr)
                        )
                    if this_quarter == 10:
                        for q, mo in enumerate(range(1, 10, 3), 1):
                            q = f"Q{q} {this_year}"
                            self.quarters.append(q)
                            add_frame(
                                q,
                                self.lc.getTradeFrame(datetime(this_year, mo, 1), datetime(this_year, mo + 3, 1), by_attr=self.by_attr)
                            )
                        current_quarter = f"~Q4 {this_year}"
                        add_frame(
                            current_quarter,
                            self.lc.getTradeFrame(datetime(this_year, 10, 1), datetime(this_year + 1, 1, 1), by_attr=self.by_attr)
                        )
                    else:
                        q = 0
                        for q, mo in enumerate(range(1, this_quarter, 3), 1):
                            _q = f"Q{q} {this_year}"
                            self.quarters.append(_q)
                            add_frame(
                                _q,
                                self.lc.getTradeFrame(datetime(this_year, mo, 1), datetime(this_year, mo + 3, 1), by_attr=self.by_attr)
                            )
                        current_quarter = f"~Q{q + 1} {this_year}"
                        add_frame(
                            current_quarter,
                            self.lc.getTradeFrame(datetime(this_year, this_quarter, 1), datetime(this_year, this_quarter + 3, 1), by_attr=self.by_attr)
                        )
                    current_year = f"~Y{this_year}"
                    add_frame(
                        current_year,
                        self.lc.getTradeFrame(datetime(this_year, 1, 1), datetime(this_year + 1, 1, 1), by_attr=self.by_attr)
                    )

                this_m52W = this_date - timedelta(weeks=52)
                this_p1D = this_date + timedelta(days=1)
                if (scopeW := (this_p1D - this_m52W).days // 7) < 52:
                    self.t52w = f"T52W (~{scopeW})"
                else:
                    self.t52w = "T52W"
                add_frame(
                    self.t52w,
                    self.lc.getTradeFrame(this_m52W, this_p1D, by_attr=self.by_attr)
                )

                self.records = [{"_": row} | data[row] for row in _records_def.keys()]
                self.columns = [{"name": "\u200b", "id": "_", "hideable": True}] + [{"name": c, "id": c} for c in reversed(columns)]

                self.style_data_conditional = _style_data_conditional + [
                    {"if": {"column_id": y}} | styles.balance.year_cell for y in self.years
                ] + [
                    {"if": {"column_id": q4}} | styles.balance.q4_cell for q4 in self.quarters if q4.startswith("Q4")
                ] + [
                    {"if": {"column_id": q1}} | styles.balance.q1_cell for q1 in self.quarters if q1.startswith("Q1")
                ] + [
                    {"if": {"column_id": self.t52w}} | styles.balance.t52w_cell,
                    {"if": {"column_id": current_year}} | styles.balance.current_cell,
                    {"if": {"column_id": current_quarter}} | styles.balance.current_cell,
                ]
                self.style_header_conditional = [
                    {"if": {"column_id": y}} | styles.balance.year_header for y in self.years
                ] + [
                    {"if": {"column_id": q4}} | styles.balance.q4_header for q4 in self.quarters if q4.startswith("Q4")
                ] + [
                    {"if": {"column_id": q1}} | styles.balance.q1_header for q1 in self.quarters if q1.startswith("Q1")
                ] + [
                    {"if": {"column_id": self.t52w}} | styles.balance.t52w_header,
                    {"if": {"column_id": current_year}} | styles.balance.current_header,
                    {"if": {"column_id": current_quarter}} | styles.balance.current_header,
                ]
                self.current_ = (current_year, current_quarter)

            if self.new_vis:
                self.new_vis = False
                hidden_columns = ["_"]

                if not self.vis_years:
                    hidden_columns += self.years
                if not self.vis_quarters:
                    hidden_columns += self.quarters
                if not self.vis_current_:
                    hidden_columns += self.current_
                if not self.vis_t52w:
                    hidden_columns.append(self.t52w)

                self.dt = DataTable(
                    self.records,
                    self.columns,
                    hidden_columns=hidden_columns,
                    style_cell=styles.balance.cell_default,
                    style_header=styles.balance.header_default,
                    style_data_conditional=self.style_data_conditional,
                    style_header_conditional=self.style_header_conditional,
                    css=[{"selector": ".show-hide", "rule": "display: none"}]
                )

            return html.Div([
                html.Div(
                    _dt1,
                    style={"display": "inline-block"}
                ),
                html.Div(
                    self.dt,
                    style={"display": "inline-block", "overflowX": "scroll", "width": "100%"}
                ),
            ],
                style={
                    "display": "flex"
                })

    @staticmethod
    def new(
            lc: LogCalc,
            by_attr: Literal["idx", "min", "max", "or"] | str = "or",
            years: bool = True,
            quarters: bool = True,
            t52w: bool = True,
            current_: bool = True,
    ):
        global OBJ
        OBJ = _Balance(lc, by_attr, years, quarters, t52w, current_)
        return OBJ


OBJ: _Balance = _Balance
