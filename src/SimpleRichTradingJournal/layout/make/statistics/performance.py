from datetime import datetime
from datetime import timedelta
from typing import Literal

import plotly.graph_objects as go
from numpy import array, ndarray
from plotly.subplots import make_subplots

import __env__
from calc.log import LogCalc, TradeFrameCalc
from config import styles


class _Performance:
    new_calc: bool
    new_vis: bool
    lc: LogCalc | TradeFrameCalc
    by_attr: Literal["idx", "min", "max", "or"] | str
    
    step_time: timedelta
    trailing_frame: timedelta
    trailing_interval: timedelta
    range_: timedelta
    hypothesis_per_day: bool
    
    order: tuple[int, int, int, int, int, int, int]

    profits: list | ndarray
    summary: list | ndarray
    current_performances: list | ndarray
    dripping_performances: list | ndarray
    summary_rate: list | ndarray
    deposits: list | ndarray
    trade_invests: list | ndarray
    trade_takes: list | ndarray
    trades_sum_profits: list | ndarray
    performance_per_day_avg: list | ndarray
    profit_per_day_avg: list | ndarray
    performance_per_year_avg: list | ndarray
    profit_per_year_avg: list | ndarray
    dates: list | ndarray
    trade_invests_2: list | ndarray
    trade_takes_2: list | ndarray
    trades_performance_2: list | ndarray
    performance_per_day_avg_2: list | ndarray
    profit_per_day_avg_2: list | ndarray
    performance_per_year_avg_2: list | ndarray
    profit_per_year_avg_2: list | ndarray
    activity_2: list | ndarray
    holdtime_avg_2: list | ndarray
    dates_2: list | ndarray
    deposits_index_date: list | ndarray
    deposits_amount: list | ndarray
    payouts_index_date: list | ndarray
    payouts_amount: list | ndarray
    
    figure: go.Figure
    
    def __init__(
            self,
            lc: LogCalc,
            by_attr: Literal["idx", "min", "max", "or"] | str,
            step_time: timedelta,
            trailing_frame: timedelta,
            trailing_interval: timedelta,
            range_: timedelta,
            order,
            hypothesis_per_day: bool
    ):
        self.lc = lc
        self.opt__by_attr(by_attr)
        self.opt__trailing(step_time, trailing_frame, trailing_interval, range_, hypothesis_per_day)
        self.opt__order(order)

    def opt__by_attr(self, by_attr: Literal["idx", "min", "max", "or"] | str = "or"):
        self.by_attr = by_attr
        self.new_calc = True
        
    def opt__trailing(
            self,
            step_time: timedelta = timedelta(weeks=1),
            trailing_frame: timedelta = timedelta(weeks=12),
            trailing_interval: timedelta = timedelta(weeks=1),
            range_: timedelta = timedelta(0),
            hypothesis_per_day: bool = False
    ):
        self.step_time = step_time
        self.trailing_frame = trailing_frame
        self.trailing_interval = trailing_interval
        self.range_ = range_
        self.hypothesis_per_day = hypothesis_per_day
        self.new_calc = True
        
    def opt__order(self, order):
        self.order = order
        self.new_vis = True
    
    def get(self):
        update_figure = False
        if self.lc.first_record:
            datetime_now = datetime.now()
            if self.new_calc:
                self.new_calc = False
                self.new_vis = True

                self.profits = list()
                self.summary = list()
                self.current_performances = list()
                self.dripping_performances = list()
                self.summary_rate = list()
                self.deposits = list()
                self.trade_invests = list()
                self.trade_takes = list()
                self.trades_sum_profits = list()
                self.performance_per_day_avg = list()
                self.profit_per_day_avg = list()
                self.performance_per_year_avg = list()
                self.profit_per_year_avg = list()
                self.dates = list()

                if self.hypothesis_per_day:

                    def hypothesis_per_append(__frame):
                        self.performance_per_day_avg.append(__frame.avg_performance_per_day)
                        self.profit_per_day_avg.append(__frame.avg_profit_per_day)

                    def hypothesis_per_append_2(__frame):
                        self.performance_per_day_avg_2.append(__frame.avg_performance_per_day)
                        self.profit_per_day_avg_2.append(__frame.avg_profit_per_day)

                else:
                    def hypothesis_per_append(__frame):
                        self.performance_per_year_avg.append(__frame.avg_performance_per_year)
                        self.profit_per_year_avg.append(__frame.avg_profit_per_year)

                    def hypothesis_per_append_2(__frame):
                        self.performance_per_year_avg_2.append(__frame.avg_performance_per_year)
                        self.profit_per_year_avg_2.append(__frame.avg_profit_per_year)

                first = last = self.lc.first_record.index_date
                while (last := last + self.step_time) <= self.lc.last_record.index_date:
                    frame = self.lc.getTradeFrame(first, last)
                    self.profits.append(frame.sum_profits)
                    self.summary.append(frame.summary_value)
                    self.current_performances.append(frame.current_performance_on_portfolio)
                    self.dripping_performances.append(frame.dripping_performance_avg)
                    self.summary_rate.append(frame.current_summary_rate)
                    self.deposits.append(frame.money)
                    self.trade_invests.append(frame.sum_fin_invest)
                    self.trade_takes.append(frame.sum_fin_take)
                    self.trades_sum_profits.append(frame.sum_fin_take - frame.sum_fin_invest)
                    hypothesis_per_append(frame)
                    self.dates.append(last)

                if self.range_:
                    begin = datetime_now - self.range_
                    i = 0
                    for i in range(len(self.dates)):
                        if self.dates[i] >= begin:
                            break

                    self.profits = self.profits[i:]
                    self.summary = self.summary[i:]
                    self.current_performances = self.current_performances[i:]
                    self.dripping_performances = self.dripping_performances[i:]
                    self.summary_rate = self.summary_rate[i:]
                    self.deposits = self.deposits[i:]
                    self.trade_invests = self.trade_invests[i:]
                    self.trade_takes = self.trade_takes[i:]
                    self.trades_sum_profits = self.trades_sum_profits[i:]
                    self.performance_per_day_avg = self.performance_per_day_avg[i:]
                    self.profit_per_day_avg = self.profit_per_day_avg[i:]
                    self.performance_per_year_avg = self.performance_per_year_avg[i:]
                    self.profit_per_year_avg = self.profit_per_year_avg[i:]
                    self.dates = self.dates[i:]

                self.profits.append(self.lc.sum_profits)
                self.summary.append(self.lc.summary_value)
                self.current_performances.append(self.lc.current_performance_on_portfolio)
                self.dripping_performances.append(self.lc.dripping_performance_avg)
                self.summary_rate.append(self.lc.current_summary_rate)
                self.deposits.append(self.lc.money)
                self.trade_invests.append(self.lc.sum_fin_invest)
                self.trade_takes.append(self.lc.sum_fin_take)
                self.trades_sum_profits.append(self.lc.sum_fin_take - self.lc.sum_fin_invest)
                hypothesis_per_append(self.lc)
                self.dates.append(datetime_now)

                self.trade_invests_2 = list()
                self.trade_takes_2 = list()
                self.trades_performance_2 = list()
                self.performance_per_day_avg_2 = list()
                self.profit_per_day_avg_2 = list()
                self.performance_per_year_avg_2 = list()
                self.profit_per_year_avg_2 = list()
                self.activity_2 = list()
                self.holdtime_avg_2 = list()
                self.dates_2 = list()

                first = self.lc.first_record.index_date
                while first <= self.lc.last_record.index_date:
                    last = first + self.trailing_frame
                    frame = self.lc.getTradeFrame(first, last)
                    first += self.trailing_interval
                    self.trade_invests_2.append(frame.sum_fin_invest)
                    self.trade_takes_2.append(frame.sum_fin_take)
                    try:
                        self.trades_performance_2.append(frame.sum_fin_take / frame.sum_fin_invest - 1)
                    except ZeroDivisionError:
                        self.trades_performance_2.append(None)
                    hypothesis_per_append_2(frame)
                    self.activity_2.append(frame.n_trades_open + frame.n_trades_fin)
                    self.holdtime_avg_2.append(frame.holdtime_of_all_avg / 86400)
                    self.dates_2.append(last)

                self.deposits_index_date = [i.index_date for i in self.lc.frame_deposits]
                self.deposits_amount = [i.amount for i in self.lc.frame_deposits]
                self.payouts_amount = [-i.amount for i in self.lc.frame_payouts]
                self.payouts_index_date = [i.index_date for i in self.lc.frame_payouts]

                if self.range_:
                    begin = datetime_now - self.range_
                    i = 0
                    for i in range(len(self.dates_2)):
                        if self.dates_2[i] >= begin:
                            break

                    self.trade_invests_2 = self.trade_invests_2[i:]
                    self.trade_takes_2 = self.trade_takes_2[i:]
                    self.trades_performance_2 = self.trades_performance_2[i:]
                    self.performance_per_day_avg_2 = self.performance_per_day_avg_2[i:]
                    self.profit_per_day_avg_2 = self.profit_per_day_avg_2[i:]
                    self.performance_per_year_avg_2 = self.performance_per_year_avg_2[i:]
                    self.profit_per_year_avg_2 = self.profit_per_year_avg_2[i:]
                    self.dates_2 = self.dates_2[i:]

                    i = 0
                    for i in range(len(self.deposits_index_date)):
                        if self.deposits_index_date[i] >= begin:
                            break
                    self.deposits_index_date = array(self.deposits_index_date[i:])
                    self.deposits_amount = array(self.deposits_amount[i:])

                    i = 0
                    for i in range(len(self.payouts_index_date)):
                        if self.payouts_index_date[i] >= begin:
                            break
                    self.payouts_index_date = array(self.payouts_index_date[i:])
                    self.payouts_amount = array(self.payouts_amount[i:])

                self.profits = array(self.profits)
                self.summary = array(self.summary)
                self.current_performances = array(self.current_performances)
                self.dripping_performances = array(self.dripping_performances)
                self.summary_rate = array(self.summary_rate)
                self.deposits = array(self.deposits)
                self.trade_invests = array(self.trade_invests)
                self.trade_takes = array(self.trade_takes)
                self.trades_sum_profits = array(self.trades_sum_profits)
                self.performance_per_day_avg = array(self.performance_per_day_avg)
                self.profit_per_day_avg = array(self.profit_per_day_avg)
                self.performance_per_year_avg = array(self.performance_per_year_avg)
                self.profit_per_year_avg = array(self.profit_per_year_avg)
                self.dates = array(self.dates)
                self.trade_invests_2 = array(self.trade_invests_2)
                self.trade_takes_2 = array(self.trade_takes_2)
                self.trades_performance_2 = array(self.trades_performance_2)
                self.performance_per_year_avg_2 = array(self.performance_per_year_avg_2)
                self.profit_per_year_avg_2 = array(self.profit_per_year_avg_2)
                self.activity_2 = array(self.activity_2)
                self.holdtime_avg_2 = array(self.holdtime_avg_2)
                self.dates_2 = array(self.dates_2)

        else:
            self.new_vis = False
            update_figure = True

            self.figure = go.Figure()

        if self.new_vis:
            self.new_vis = False
            update_figure = True

            self.figure = make_subplots(
                rows=__env__.nStatisticsDrag, cols=1,
                specs=[[{"secondary_y": True}],] * __env__.nStatisticsDrag,
                shared_xaxes=True,
                horizontal_spacing=0.01,
                vertical_spacing=0.01,
            )

            if self.lc.calc_trades:
                date = self.lc.calc_trades[-1].index_date
                date_label = date.strftime(__env__.timeFormatLastCalc)
                date += timedelta(1)
                date = date.strftime("%Y-%m-%d")
                self.figure.add_shape(
                    type="line",
                    xref=f"x{__env__.nStatisticsDrag}",
                    yref="paper",
                    x0=date,
                    x1=date,
                    y0=0,
                    y1=1,
                    line=dict(
                        color=__env__.color_theme.shape_last_calc,
                        width=1,
                        dash="dot"
                    ),
                )
                self.figure.add_shape(
                    type="rect",
                    xref=f"x{__env__.nStatisticsDrag}",
                    yref="paper",
                    y0=0.003,
                    y1=0.003,
                    x0=date,
                    x1=date,
                    label=dict(text=date_label, textposition="middle right"),
                )

            self.figure.add_trace(
                go.Scatter(
                    name="Profits",
                    y=self.profits,
                    x=self.dates,
                    line=dict(color=__env__.color_theme.trace_profit),
                    marker=dict(color=__env__.color_theme.trace_profit),
                    showlegend=False
                ),
                row=self.order[0], col=1, secondary_y=False
            )

            self.figure.add_trace(
                go.Scatter(
                    name="Current Performance",
                    y=self.current_performances,
                    x=self.dates,
                    line=dict(color=__env__.color_theme.trace_current_performance),
                    marker=dict(color=__env__.color_theme.trace_current_performance),
                    showlegend=False
                ),
                row=self.order[0], col=1, secondary_y=True
            )

            self.figure.add_trace(
                go.Scatter(
                    name="Dripping Perf. Ø",
                    y=self.dripping_performances,
                    x=self.dates,
                    line=dict(color=__env__.color_theme.trace_dripping_performance),
                    marker=dict(color=__env__.color_theme.trace_dripping_performance),
                    showlegend=False
                ),
                row=self.order[0], col=1, secondary_y=True
            )

            self.figure.add_trace(
                go.Scatter(
                    name="Summary",
                    y=self.summary,
                    x=self.dates,
                    line=dict(color=__env__.color_theme.trace_summary),
                    marker=dict(color=__env__.color_theme.trace_summary),
                    showlegend=False
                ),
                row=self.order[1], col=1, secondary_y=False
            )

            self.figure.add_trace(
                go.Scatter(
                    name="Summary Rate",
                    y=self.summary_rate,
                    x=self.dates,
                    line=dict(color=__env__.color_theme.trace_summary_rate),
                    marker=dict(color=__env__.color_theme.trace_summary_rate),
                    showlegend=False
                ),
                row=self.order[1], col=1, secondary_y=True
            )

            self.figure.add_trace(
                go.Bar(
                    name="Deposits",
                    y=self.deposits_amount,
                    x=self.deposits_index_date,
                    marker=dict(color=__env__.color_theme.trace_deposit, line=dict(width=0)),
                    showlegend=False,
                    hovertemplate="%{y}"
                ),
                row=self.order[2], col=1, secondary_y=False
            )

            self.figure.add_trace(
                go.Bar(
                    name="Payouts",
                    y=self.payouts_amount,
                    x=self.payouts_index_date,
                    marker=dict(color=__env__.color_theme.trace_payout, line=dict(width=0)),
                    showlegend=False,
                    hovertemplate="%{y}"
                ),
                row=self.order[2], col=1, secondary_y=False
            )

            self.figure.add_trace(
                go.Scatter(
                    name="Money",
                    y=self.deposits,
                    x=self.dates,
                    line=dict(color=__env__.color_theme.trace_money),
                    marker=dict(color=__env__.color_theme.trace_money),
                    showlegend=False
                ),
                row=self.order[2], col=1, secondary_y=True
            )

            self.figure.add_trace(
                go.Scatter(
                    name="Investments",
                    y=self.trade_invests,
                    x=self.dates,
                    line=dict(color=__env__.color_theme.trace_trade_sum_invest),
                    marker=dict(color=__env__.color_theme.trace_trade_sum_invest),
                    showlegend=False
                ),
                row=self.order[3], col=1, secondary_y=False
            )

            self.figure.add_trace(
                go.Scatter(
                    name="Takes",
                    y=self.trade_takes,
                    x=self.dates,
                    line=dict(color=__env__.color_theme.trace_trade_sum_take),
                    marker=dict(color=__env__.color_theme.trace_trade_sum_take),
                    showlegend=False
                ),
                row=self.order[3], col=1, secondary_y=False
            )

            self.figure.add_trace(
                go.Scatter(
                    name="Takes - Invest",
                    y=self.trades_sum_profits,
                    x=self.dates,
                    line=dict(color=__env__.color_theme.trace_trade_performance),
                    marker=dict(color=__env__.color_theme.trace_trade_performance),
                    showlegend=False
                ),
                row=self.order[3], col=1, secondary_y=True
            )

            if self.hypothesis_per_day:

                self.figure.add_trace(
                    go.Scatter(
                        name="Ø Profit/Day",
                        y=self.profit_per_day_avg,
                        x=self.dates,
                        line=dict(color=__env__.color_theme.trace_profit_per_day_avg),
                        marker=dict(color=__env__.color_theme.trace_profit_per_day_avg),
                        showlegend=False
                    ),
                    row=self.order[4], col=1, secondary_y=False
                )

                self.figure.add_trace(
                    go.Scatter(
                        name="Ø Perf./Day",
                        y=self.performance_per_day_avg,
                        x=self.dates,
                        line=dict(color=__env__.color_theme.trace_performance_per_day_avg),
                        marker=dict(color=__env__.color_theme.trace_performance_per_day_avg),
                        showlegend=False
                    ),
                    row=self.order[4], col=1, secondary_y=True
                )

            else:
                self.figure.add_trace(
                    go.Scatter(
                        name="Ø Profit/Year",
                        y=self.profit_per_year_avg,
                        x=self.dates,
                        line=dict(color=__env__.color_theme.trace_profit_per_day_avg),
                        marker=dict(color=__env__.color_theme.trace_profit_per_day_avg),
                        showlegend=False
                    ),
                    row=self.order[4], col=1, secondary_y=False
                )

                self.figure.add_trace(
                    go.Scatter(
                        name="Ø Perf./Year",
                        y=self.performance_per_year_avg,
                        x=self.dates,
                        line=dict(color=__env__.color_theme.trace_performance_per_day_avg),
                        marker=dict(color=__env__.color_theme.trace_performance_per_day_avg),
                        showlegend=False
                    ),
                    row=self.order[4], col=1, secondary_y=True
                )

            self.figure.add_trace(
                go.Scatter(
                    name="~Investments",
                    y=self.trade_invests_2,
                    x=self.dates_2,
                    line=dict(color=__env__.color_theme.trace_trade_sum_invest_trailing),
                    marker=dict(color=__env__.color_theme.trace_trade_sum_invest_trailing),
                    showlegend=False
                ),
                row=self.order[5], col=1, secondary_y=False
            )

            self.figure.add_trace(
                go.Scatter(
                    name="~Takes",
                    y=self.trade_takes_2,
                    x=self.dates_2,
                    line=dict(color=__env__.color_theme.trace_trade_sum_take_trailing),
                    marker=dict(color=__env__.color_theme.trace_trade_sum_take_trailing),
                    showlegend=False
                ),
                row=self.order[5], col=1, secondary_y=False
            )

            self.figure.add_trace(
                go.Scatter(
                    name="~Performance",
                    y=self.trades_performance_2,
                    x=self.dates_2,
                    line=dict(color=__env__.color_theme.trace_trade_performance_trailing),
                    marker=dict(color=__env__.color_theme.trace_trade_performance_trailing),
                    showlegend=False
                ),
                row=self.order[5], col=1, secondary_y=True
            )

            if self.hypothesis_per_day:

                self.figure.add_trace(
                    go.Scatter(
                        name="~Ø Profit/Day",
                        y=self.profit_per_day_avg_2,
                        x=self.dates_2,
                        line=dict(color=__env__.color_theme.trace_profit_per_day_avg_trailing),
                        marker=dict(color=__env__.color_theme.trace_profit_per_day_avg_trailing),
                        showlegend=False
                    ),
                    row=self.order[6], col=1, secondary_y=False
                )

                self.figure.add_trace(
                    go.Scatter(
                        name="~Ø Perf./Day",
                        y=self.performance_per_day_avg_2,
                        x=self.dates_2,
                        line=dict(color=__env__.color_theme.trace_performance_per_day_avg_trailing),
                        marker=dict(color=__env__.color_theme.trace_performance_per_day_avg_trailing),
                        showlegend=False
                    ),
                    row=self.order[6], col=1, secondary_y=True
                )

            else:

                self.figure.add_trace(
                    go.Scatter(
                        name="~Ø Profit/Year",
                        y=self.profit_per_year_avg_2,
                        x=self.dates_2,
                        line=dict(color=__env__.color_theme.trace_profit_per_day_avg_trailing),
                        marker=dict(color=__env__.color_theme.trace_profit_per_day_avg_trailing),
                        showlegend=False
                    ),
                    row=self.order[6], col=1, secondary_y=False
                )

                self.figure.add_trace(
                    go.Scatter(
                        name="~Ø Perf./Year",
                        y=self.performance_per_year_avg_2,
                        x=self.dates_2,
                        line=dict(color=__env__.color_theme.trace_performance_per_day_avg_trailing),
                        marker=dict(color=__env__.color_theme.trace_performance_per_day_avg_trailing),
                        showlegend=False
                    ),
                    row=self.order[6], col=1, secondary_y=True
                )

            self.figure.add_trace(
                go.Scatter(
                    name="~Activity",
                    y=self.activity_2,
                    x=self.dates_2,
                    line=dict(color=__env__.color_theme.trace_activity),
                    marker=dict(color=__env__.color_theme.trace_activity),
                    showlegend=False,
                ),
                row=self.order[7], col=1, secondary_y=False
            )

            self.figure.add_trace(
                go.Scatter(
                    name="~Ø Hold Days",
                    y=self.holdtime_avg_2,
                    x=self.dates_2,
                    line=dict(color=__env__.color_theme.trace_holdtime_avg),
                    marker=dict(color=__env__.color_theme.trace_holdtime_avg),
                    showlegend=False
                ),
                row=self.order[7], col=1, secondary_y=True
            )

        if update_figure:

            self.figure.update_yaxes(
                title=dict(
                    text="Profit"
                ),
                showline=True,
                row=self.order[0], col=1
            )
            self.figure.update_yaxes(
                title=dict(
                    text="Performance"
                ),
                tickformat=",.2%",
                row=self.order[0], col=1,
                secondary_y=True
            )
            self.figure.update_yaxes(
                title=dict(
                    text="Summary"
                ),
                showline=True,
                row=self.order[1], col=1
            )
            self.figure.update_yaxes(
                title=dict(
                    text="Rate"
                ),
                tickformat=",.2%",
                row=self.order[1], col=1,
                secondary_y=True
            )
            self.figure.update_yaxes(
                title=dict(
                    text="Payouts | Deposits"
                ),
                showline=True,
                row=self.order[2], col=1
            )
            self.figure.update_yaxes(
                title=dict(
                    text="Money"
                ),
                row=self.order[2], col=1,
                secondary_y=True
            )
            self.figure.update_yaxes(
                title=dict(
                    text="Invest & Take<br>Alltime"
                ),
                showline=True,
                row=self.order[3], col=1
            )
            self.figure.update_yaxes(
                title=dict(
                    text="Take - Invest"
                ),
                row=self.order[3], col=1,
                secondary_y=True
            )
            self.figure.update_yaxes(
                title=dict(
                    text="Ø Profit / t"
                ),
                showline=True,
                row=self.order[4], col=1
            )
            self.figure.update_yaxes(
                title=dict(
                    text="Ø Perf. / t"
                ),
                tickformat=",.2%",
                row=self.order[4], col=1,
                secondary_y=True
            )
            self.figure.update_yaxes(
                title=dict(
                    text="~ Invest & Take"
                ),
                showline=True,
                row=self.order[5], col=1
            )
            self.figure.update_yaxes(
                title=dict(
                    text="~Ø Performance"
                ),
                tickformat=",.2%",
                row=self.order[5], col=1,
                secondary_y=True
            )
            self.figure.update_yaxes(
                title=dict(
                    text="~Ø Profit / t"
                ),
                showline=True,
                row=self.order[6], col=1
            )
            self.figure.update_yaxes(
                title=dict(
                    text="~Ø Perf. / t"
                ),
                tickformat=",.2%",
                row=self.order[6], col=1,
                secondary_y=True
            )
            self.figure.update_yaxes(
                title=dict(
                    text="~ Activity"
                ),
                showline=True,
                row=self.order[7], col=1
            )
            self.figure.update_yaxes(
                title=dict(
                    text="~Ø Hold Days"
                ),
                row=self.order[7], col=1,
                secondary_y=True
            )

            self.figure.update_yaxes(
                gridcolor=styles.figures.color_grid_y,
                zeroline=False,
                showticklabels=True,
                showspikes=True,
                spikemode='across',
                spikesnap='cursor',
                spikethickness=styles.figures.spike_thickness_y,
                spikecolor=styles.figures.color_spike_y,
                spikedash="solid",
                showline=True,
            )
            self.figure.update_xaxes(
                gridcolor=styles.figures.color_grid_x,
                griddash="dot",
                zeroline=False,
                showticklabels=True,
                showspikes=True,
                spikemode='across',
                spikesnap='cursor',
                spikethickness=styles.figures.spike_thickness_x,
                spikecolor=styles.figures.color_spike_x,
                spikedash="solid",
                showline=False,
            )

            self.figure.update_traces(xaxis=f"x{__env__.nStatisticsDrag}")

            self.figure.update_layout(
                dict(plot_bgcolor=styles.figures.color_bg_plot, paper_bgcolor=styles.figures.color_bg_paper),
                font=dict(color=styles.figures.color_fg_plot),
                hovermode='x unified',
                modebar=dict(orientation="v"),
                margin=dict(t=0, l=0, r=0, b=0),
            )

        return self.figure

    @staticmethod
    def new(
            lc: LogCalc,
            by_attr: Literal["idx", "min", "max", "or"] | str,
            step_time: timedelta,
            trailing_frame: timedelta,
            trailing_interval: timedelta,
            range_: timedelta,
            order,
            hypothesis_per_day: bool
    ):
        global OBJ
        OBJ = _Performance(lc, by_attr, step_time, trailing_frame, trailing_interval, range_, order, hypothesis_per_day)
        return OBJ


OBJ: _Performance = _Performance


