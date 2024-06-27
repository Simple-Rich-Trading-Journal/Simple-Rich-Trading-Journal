from __future__ import annotations

from functools import cached_property
from typing import Literal

import plotly.graph_objects as go

from calc.log import LogCalc, _Trade
from config import styles
import __env__


class _Positions:
    new_calc: bool
    new_vis: bool

    lc: LogCalc
    group_by: list[Literal["Name", "Symbol", "Type", "Short", "Sector", "Category"] | str]

    open_ids: list
    open_labels: list
    open_parents: list
    open_values: list
    open_colors: list

    all_ids: list
    all_labels: list
    all_parents: list
    all_values: list
    all_colors: list

    open_figure: go.Figure
    all_figure: go.Figure

    show_all: bool
    
    def __init__(
            self,
            lc: LogCalc,
            group_by: list[Literal["Name", "Symbol", "Type", "Short", "Sector", "Category"] | str],
            show_all: bool
    ):
        self.lc = lc
        self.opt__group_by(group_by)
        self.opt__show_all(show_all)

    def opt__group_by(
            self,
            group_by: list[Literal["Name", "Symbol", "Type", "Short", "Sector", "Category"] | str]
    ):
        self.group_by = group_by
        self.new_calc = True

    def opt__show_all(
            self,
            show_all: bool
    ):
        self.show_all = show_all
        self.new_vis = True

    def get(self):
        if self.new_calc:
            self.new_calc = False
            self.new_vis = True

            _id_ = 0
            
            class Fork:

                id: int
                forks: dict[str, Fork]
                trades: list[_Trade]
                parent: Fork
                group_attr: str
                group: str | Literal[1, -1] | None
                color: str | None

                def __init__(
                        self,
                        trade: _Trade | None,
                        parent: Fork | None,
                        group_attr: str | None,
                        group: str | Literal[1, -1] | None,
                        color: str | None,
                ):
                    nonlocal _id_
                    self.id = _id_
                    _id_ += 1
                    self.forks = dict()
                    self.trades = [trade]
                    self.parent = parent
                    self.group_attr = group_attr
                    self.group = group
                    self.color = color

                def add(self, trade: _Trade, group_by: list):
                    if group_by[0] == "Short":
                        if trade["Short"]:
                            gr = -1
                            color = __env__.color_theme.cell_negvalue
                        else:
                            gr = 1
                            color = __env__.color_theme.cell_posvalue
                    else:
                        gr = trade[group_by[0]]
                        color = __env__.get_position_color(gr)
                    if fork := self.forks.get(gr):
                        fork.trades.append(trade)
                    else:
                        fork = Fork(trade, self, group_by[0], gr, color)
                        self.forks[gr] = fork
                    if group_by := group_by[1:]:
                        fork.add(trade, group_by)

                @cached_property
                def value(self):
                    return sum(i.amount for i in self.trades)

                @property
                def label(self):
                    match self.group:
                        case -1:
                            gr = "Short"
                        case 1:
                            gr = "Long"
                        case _:
                            gr = self.group
                    return (f"{gr}<br>"
                            f"{self.value:,.2f} ( {self.value / self.parent.value:,.2%} )")

                def get(self):
                    nonlocal _id_
                    labels = [self.label]
                    values = [self.value]
                    parents = [self.parent.id]
                    ids = [self.id]
                    colors = [self.color]
                    if not self.forks:
                        for trade in self.trades:
                            labels.append(
                                (f"{trade[__env__.statisticsGroupId]}<br>"
                                 f"{trade.amount:,.2f} ( {trade.amount / self.value:,.2%} )")
                            )
                            values.append(trade.amount)
                            parents.append(self.id)
                            ids.append(_id_)
                            _id_ += 1
                            colors.append(self.color)
                    else:
                        for fork in self.forks.values():
                            _get = fork.get()
                            labels += _get[0]
                            values += _get[1]
                            parents += _get[2]
                            ids += _get[3]
                            colors += _get[4]
                    return labels, values, parents, ids, colors

            class Root(Fork):

                @cached_property
                def value(self):
                    return sum(i.value for i in self.forks.values())

                @property
                def label(self):
                    return f"{len(self.forks)}<br>{self.value:,.2f}"

                def __init__(self):
                    class Parent:
                        id = ""

                    Fork.__init__(self, None, Parent, "", "", "")
                    self.trades = list()

            data = Root()

            for _trade in self.lc.open_trades:
                data.add(_trade, self.group_by)

            self.open_labels, self.open_values, self.open_parents, self.open_ids, self.open_colors = data.get()

            data = Root()

            for _trade in self.lc.open_trades + self.lc.fin_trades:
                data.add(_trade, self.group_by)

            self.all_labels, self.all_values, self.all_parents, self.all_ids, self.all_colors = data.get()

        if self.new_vis:
            self.new_vis = False

            if self.show_all:
                maxdepth = None
            else:
                maxdepth = __env__.statisticsSunMaxDepth

            self.open_figure = go.Figure(
                go.Sunburst(
                    ids=self.open_ids,
                    labels=self.open_labels,
                    parents=self.open_parents,
                    values=self.open_values,
                    branchvalues="total",
                    maxdepth=maxdepth,
                    marker=dict(colors=self.open_colors),
                    hovertemplate="%{label}<extra></extra>"
                ),
            )

            self.all_figure = go.Figure(
                go.Sunburst(
                    ids=self.all_ids,
                    labels=self.all_labels,
                    parents=self.all_parents,
                    values=self.all_values,
                    branchvalues="total",
                    maxdepth=maxdepth,
                    marker=dict(colors=self.all_colors),
                    hovertemplate="%{label}<extra></extra>"
                ),
            )

            self.open_figure.update_layout(
                dict(plot_bgcolor=styles.figures.color_bg_plot, paper_bgcolor=styles.figures.color_bg_paper),
                font=dict(color=styles.figures.color_fg_plot),
                margin=dict(t=0, l=0, r=0, b=0),
            )

            self.all_figure.update_layout(
                dict(plot_bgcolor=styles.figures.color_bg_plot, paper_bgcolor=styles.figures.color_bg_paper),
                font=dict(color=styles.figures.color_fg_plot),
                margin=dict(t=0, l=0, r=0, b=0),
            )

        return self.open_figure, self.all_figure

    @staticmethod
    def new(
            lc: LogCalc,
            group_by: list[Literal["Name", "Symbol", "Type", "Short", "Sector", "Category"] | str],
            show_all: bool
    ):
        global OBJ
        OBJ = _Positions(lc, group_by, show_all)
        return OBJ


OBJ: _Positions = _Positions


