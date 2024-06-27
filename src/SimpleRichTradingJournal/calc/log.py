from __future__ import annotations

from datetime import datetime
from functools import cached_property
from re import search, IGNORECASE
from typing import Literal, Callable, NamedTuple, Any

import __env__
from config.functional import record_tags
from .utils import datetime_from_tradetimeformat, tradetimeparser, preventZeroDiv


manual_take_amount = False


class _LogRecord:
    cat_id: str = ""
    
    valid_cells: tuple[str, ...] = ("id", "cat", "mark")
    
    row_dat: dict
    index_date: datetime
    amount: float | None

    default_date: datetime
    _idx_date: datetime | None

    def _do_flush(self) -> bool:
        comp_keys = ("Name", "n", "InvestTime", "InvestAmount", "TakeTime", "TakeAmount", "ITC", "Note")
        for k in comp_keys:
            if self.row_dat.get(k) not in (None, ""):
                return False
        else:
            return True

    @cached_property
    def _dates(self) -> tuple | tuple[datetime] | tuple[datetime, datetime]:
        return tuple(d for k in ("InvestTime", "TakeTime") if (d := datetime_from_tradetimeformat(self.row_dat.get(k))))

    @cached_property
    def _min_date(self) -> datetime | None:
        if self._dates:
            return min(self._dates)

    @cached_property
    def _max_date(self) -> datetime | None:
        if self._dates:
            return max(self._dates)

    def get_min_date(self, default: datetime) -> datetime:
        return self._min_date or default

    def get_max_date(self, default: datetime) -> datetime:
        return self._max_date or default

    def get_idx_date(self, default: datetime) -> datetime:
        return self._idx_date or default

    def __init__(
            self,
            row_dat: dict,
            index_date: datetime | None,
            amount: float | None,
            default_date: datetime,
    ):
        row_dat["Name"] = (row_dat.get("Name", "") or "").strip()
        row_dat["cat"] = self.cat_id
        self.row_dat = row_dat
        self._idx_date = index_date
        self.index_date = index_date or default_date
        self.amount = amount
        self.default_date = default_date

    def reset(self):
        for prop in ("data", "_dates", "_min_date", "_max_date"):
            try:
                delattr(self, prop)
            except AttributeError:
                pass

    def reset_data(self):
        try:
            delattr(self, "data")
        except AttributeError:
            pass

    def make_data(self):
        self.reset_data()
        return self.data

    def copy(self):
        return self.__class__(self.row_dat.copy(), self._idx_date, self.amount, self.default_date)

    def __getitem__(self, key):
        return self.row_dat.__getitem__(key)

    def __setitem__(self, key, value):
        self.row_dat.__setitem__(key, value)

    @cached_property
    def data(self) -> dict:
        self.row_dat["Profit"] = self.row_dat["Performance"] = None
        self.row_dat["Profit/Day"] = self.row_dat["Performance/Day"] = None
        self.row_dat["Profit/Year"] = self.row_dat["Performance/Year"] = None
        self.row_dat["HoldTime"] = self.row_dat["RoundedHoldDays"] = None
        return self.row_dat

    def __repr__(self):
        return f"{self.__class__.__name__}({self.row_dat.get('id')})"

    def __hash__(self):
        return self["id"].__hash__()

    def __eq__(self, other: _LogRecord):
        return self["id"] == other["id"]

    def __lt__(self, other: _LogRecord):
        return self.index_date < other.index_date


class Deposit(_LogRecord):
    cat_id: str = "d"
    
    valid_cells: tuple[str, ...] = _LogRecord.valid_cells + ("n", "InvestTime", "InvestAmount", "ITC", "Note")

    payouts: list[Payout]
    payout: float
    profit: float
    dividend: float
    factor: float

    def __init__(self, row_dat: dict, index_date: datetime, amount: float | None, default_date: datetime):
        _LogRecord.__init__(self, row_dat, index_date, amount, default_date)
        self.reset()

    def reset(self):
        self.payouts = list()
        self.payout = 0
        self.profit = 0
        self.dividend = 0
        self.factor = 0
        self["TakeTime"] = None

    @property
    def amount_ai(self):
        return self.amount + (self.row_dat.get("ITC", 0) or 0)

    @property
    def value(self):
        return self.amount_ai - self.payout

    def set_factor(self, sum_deposits: float):
        self.factor = self.value / sum_deposits

    def add_profit(self, profit: float):
        self.profit += profit * self.factor

    def add_dividend(self, dividend: float):
        self.dividend += dividend * self.factor

    def add_payout(self, payout: Payout, remain_payout_value: float):
        self.payouts.append(payout)
        if remain_payout_value > self.value:
            remain_payout_value -= self.value
            self.payout = self.amount_ai
        else:
            self.payout += remain_payout_value
            remain_payout_value = 0
        return remain_payout_value

    def close(self):
        self["TakeTime"] = self.payouts[-1]["TakeTime"]

    @cached_property
    def data(self) -> dict:
        self.row_dat = {k: self.row_dat.get(k) for k in self.valid_cells}
        self["Name"] = record_tags.tag_DEPOSIT
        self["TakeAmount"] = self.payout or None
        self["Profit"] = self.profit
        self["Performance"] = self.profit / self.amount
        self["Dividend"] = self.dividend or None
        self["DividendRate"] = (self.dividend / self.amount) or None
        take_t = datetime_from_tradetimeformat(self.row_dat.get("TakeTime")) or self.default_date
        invest_t = datetime_from_tradetimeformat(self.row_dat.get("InvestTime"))
        hold_t = (take_t - invest_t).total_seconds()
        self["HoldTime"] = hold_t
        self["RoundedHoldDays"] = int(hold_t / 86400 + .5) or 1
        self["Profit/Day"] = self["Profit"] / self["RoundedHoldDays"]
        self["Performance/Day"] = self["Performance"] / self["RoundedHoldDays"]
        self["Profit/Year"] = self["Profit/Day"] * 365.25
        self["Performance/Year"] = self["Performance/Day"] * 365.25
        self["Profit"] = self["Profit"] or None
        self["Performance"] = self["Performance"] or None
        return self.row_dat


class Payout(_LogRecord):
    cat_id: str = "p"
    
    valid_cells: tuple[str, ...] = _LogRecord.valid_cells + ("n", "TakeTime", "TakeAmount", "ITC", "Note")

    base_value: int

    def __init__(self, row_dat: dict, index_date: datetime | None, amount: float | None, default_date: datetime):
        _LogRecord.__init__(self, row_dat, index_date, amount, default_date)
        self.reset()

    @property
    def real_amount(self):
        return self.amount + (self.row_dat.get("ITC", 0) or 0)

    def reset(self):
        super().reset()
        self.base_value = 0

    @cached_property
    def data(self) -> dict:
        self.row_dat = {k: self.row_dat.get(k) for k in self.valid_cells}
        self["Name"] = record_tags.tag_PAYOUT
        self["Performance"] = -preventZeroDiv(self.real_amount, self.base_value, 0) or None
        return self.row_dat

    def add_deposits(self, deposits: list[Deposit]):
        self.base_value += sum(d.value for d in deposits)


class _Trade(_LogRecord):
    
    valid_cells: tuple[str, ...] = _LogRecord.valid_cells + ("Name", "Symbol", "ISIN", "Type", "Short", "Sector", "Category", "Rating", "n", "InvestTime", "InvestAmount", "InvestCourse", "TakeTime", "TakeAmount", "TakeCourse", "ITC", "Note")

    dividends: list[Dividend]

    def __init__(self, row_dat: dict, index_date: datetime, amount: float | None, default_date: datetime):
        _LogRecord.__init__(self, row_dat, index_date, amount, default_date)
        self.reset()

    def reset(self):
        self["Dividend"] = None
        self.dividends = list()

    @cached_property
    def data(self) -> dict:
        self.row_dat = {k: self.row_dat.get(k) for k in self.valid_cells}
        if self.row_dat.get("InvestCourse") is not None:
            self["InvestAmount"] = (self["InvestCourse"] * self["n"]) or None
        else:
            self["InvestCourse"] = (self["InvestAmount"] / self["n"]) or None
        if (c := self.row_dat.get("TakeCourse")) is not None:
            self["TakeAmount"] = c * (self["n"] or 0)
        elif (a := self.row_dat.get("TakeAmount")) is not None and self["n"]:
            self["TakeCourse"] = a / self["n"]
        else:
            self["TakeAmount"] = self["TakeCourse"] = None
        rel_dividend = 0
        for dividend in self.dividends:
            factor = self.amount / sum(t.amount for t in dividend.trades)
            rel_dividend += dividend.amount * factor
        self["Dividend"] = rel_dividend or None
        take_t = datetime_from_tradetimeformat(self.row_dat.get("TakeTime")) or self.default_date
        invest_t = datetime_from_tradetimeformat(self.row_dat.get("InvestTime"))
        hold_t = (take_t - invest_t).total_seconds()
        self["HoldTime"] = hold_t
        self["RoundedHoldDays"] = int(hold_t / 86400 + .5) or 1
        self["Short"] = bool(self.row_dat.get("Short"))
        return self.row_dat


class TradeFinalized(_Trade):
    cat_id: str = "tf"

    has_take: bool = True

    @property
    def profit(self) -> float:
        return ((self["TakeAmount"] or 0) - self["InvestAmount"]) + (self.row_dat.get("ITC") or 0)

    @cached_property
    def data(self) -> dict:
        _ = super().data
        self["Profit"] = self.profit
        self["Performance"] = (self["TakeAmount"] or 0) / self["InvestAmount"] - 1
        self["Profit/Day"] = self["Profit"] / self["RoundedHoldDays"]
        self["Performance/Day"] = self["Performance"] / self["RoundedHoldDays"]
        self["Profit/Year"] = self["Profit/Day"] * 365.25
        self["Performance/Year"] = self["Performance/Day"] * 365.25
        return self.row_dat


class TradeOpen(_Trade):
    cat_id: str = "to"

    @property
    def profit(self) -> float:
        return self["Profit"]

    has_take: bool

    def __init__(self, row_dat: dict, index_date: datetime, amount: float | None, default_date: datetime, has_take: bool):
        _Trade.__init__(self, row_dat, index_date, amount, default_date)
        self.has_take = has_take
        if __env__.plugin.course_call(self.row_dat, manual_take_amount):
            self.has_take = self.row_dat.get("TakeAmount") is not None
        if self.has_take:
            self.make_data()

    def copy(self):
        return self.__class__(self.row_dat.copy(), self._idx_date, self.amount, self.default_date, self.has_take)

    def update_course(self) -> TradeOpen:
        if __env__.plugin.course_call(self.row_dat, False):
            self.has_take = self.row_dat.get("TakeCourse") is not None
            self.make_data()
        return self

    @cached_property
    def data(self) -> dict:
        _ = super().data
        if self.has_take:
            self["Profit"] = ((self["TakeAmount"] or 0) - self["InvestAmount"]) + (self.row_dat.get("ITC", 0) or 0)
            self["Performance"] = (self["TakeAmount"] or 0) / self["InvestAmount"] - 1
            self["Profit/Day"] = self["Profit"] / self["RoundedHoldDays"]
            self["Performance/Day"] = self["Performance"] / self["RoundedHoldDays"]
            self["Profit/Year"] = self["Profit/Day"] * 365.25
            self["Performance/Year"] = self["Performance/Day"] * 365.25
        return self.row_dat


class _CmdTradeClose(_LogRecord):
    ...


class Dividend(_LogRecord):
    cat_id: str = "v"
    
    valid_cells: tuple[str, ...] = _LogRecord.valid_cells + ("Name", "n", "TakeTime", "Note")

    name: str
    trades: list[_Trade]
    itc: float
    by_course: bool
    _amount: float

    @cached_property
    def n_shares(self) -> float:
        return sum(trade["n"] for trade in self.trades)

    @cached_property
    def amount(self) -> float:
        if self.by_course:
            return self._amount * self.n_shares
        else:
            return self._amount

    def __init__(self, row_dat: dict, index_date: datetime, amount: float | None, default_date: datetime, by_course: bool):
        _LogRecord.__init__(self, row_dat, index_date, amount, default_date)
        self.name = self["Name"]
        self.by_course = by_course
        self._amount = amount
        self.reset()

    def copy(self):
        return self.__class__(self.row_dat.copy(), self._idx_date, self.amount, self.default_date, self.by_course)

    def reset(self):
        self.trades = list()
        self.itc = 0

    def add_trade(self, trade: _Trade):
        self.itc += trade.amount
        self.trades.append(trade)
        trade.dividends.append(self)

    @cached_property
    def data(self) -> dict:
        self.row_dat = {k: self.row_dat.get(k) for k in self.valid_cells}
        if self.itc:
            self["ITC"] = self.itc
            self["Performance"] = self.amount / self.itc
        else:
            self["ITC"] = self["Performance"] = None
        self["TakeCourse"] = preventZeroDiv(self.amount, self.n_shares, None)
        self["TakeAmount"] = self.amount
        return self.row_dat


class Itc(_LogRecord):
    cat_id: str = "i"
    
    valid_cells: tuple[str, ...] = _LogRecord.valid_cells + ("n", "ITC", "Note")

    base_value: int
    at_invest: bool

    def __init__(self, row_dat: dict, index_date: datetime, amount: float | None, default_date: datetime, at_invest: bool = None):
        _LogRecord.__init__(self, row_dat, index_date, amount, default_date)
        self.at_invest = at_invest
        self.reset()
        self.valid_cells = Itc.valid_cells + (("InvestTime",) if self.at_invest else ("TakeTime",))

    def reset(self):
        super().reset()
        self.base_value = 0

    def copy(self):
        return self.__class__(self.row_dat.copy(), self._idx_date, self.amount, self.default_date, self.at_invest)

    @cached_property
    def data(self) -> dict:
        self.row_dat = {k: self.row_dat.get(k) for k in self.valid_cells}
        self["Name"] = record_tags.tag_ITC
        self["Performance"] = preventZeroDiv(self.amount, self.base_value, None)
        return self.row_dat

    def add_deposits(self, deposits: list[Deposit]):
        self.base_value += sum(d.value for d in deposits)


class LogCalc:
    __mainFrame__: LogCalc

    _deposits: list[Deposit]
    _payouts: list[Payout]
    _fin_trades: list[TradeFinalized]
    _open_trades: list[TradeOpen]
    _undefined: list[_LogRecord]
    _dividends: list[Dividend]
    _itcs: list[Itc]

    _log_data: list[dict]

    _index_by_take_date: bool
    _calc_with_open_positions: bool

    _cached_props: tuple[str, ...]

    _names: set[str]
    _symbols: set[str]
    _isins: set[str]
    _types: set[str]
    _sectors: set[str]
    _categories: set[str]

    def __init__(
            self,
            log_data: list[dict],
    ):
        self._log_data = log_data
        self._payouts = list()
        self._fin_trades = list()
        self._open_trades = list()
        self._undefined = list()
        self._dividends = list()
        self._itcs = list()
        self._cached_props = tuple(k for k, v in LogCalc.__dict__.items() if isinstance(v, cached_property))
        self.__mainFrame__ = self
        self._index_by_take_date = False
        self._calc_with_open_positions = False
        self._names = set()
        self._symbols = set()
        self._isins = set()
        self._types = set()
        self._sectors = set()
        self._categories = set()

    def __len__(self):
        return sum(map(len, (self._deposits, self._payouts, self._fin_trades, self._open_trades, self._undefined, self._dividends, self._itcs)))

    def set_parameter(
            self,
            index_by_take_date: bool | None = None,
            calc_with_open_positions: bool | None = None,
    ):
        if index_by_take_date is not None and index_by_take_date != self._index_by_take_date:
            self._index_by_take_date = index_by_take_date
            if calc_with_open_positions is not None:
                self._calc_with_open_positions = calc_with_open_positions
            self.__f_init_data__(self.__get_log_json__())
        elif calc_with_open_positions is not None and calc_with_open_positions != self._calc_with_open_positions:
            self._calc_with_open_positions = calc_with_open_positions
            self.__f_reset_calc__()

    def act(
            self,
            row: Payout | Dividend | Itc | _LogRecord | Deposit | TradeFinalized | TradeOpen,
            ea_deposits: Callable[[Deposit, LogCalc], Any] = lambda __o, __i: None,
            ea_payouts: Callable[[Payout, LogCalc], Any] = lambda __o, __i: None,
            ea_fin_trades: Callable[[TradeFinalized, LogCalc], Any] = lambda __o, __i: None,
            ea_open_trades: Callable[[TradeOpen, LogCalc], Any] = lambda __o, __i: None,
            ea_undefined: Callable[[_LogRecord, LogCalc], Any] = lambda __o, __i: None,
            ea_dividends: Callable[[Dividend, LogCalc], Any] = lambda __o, __i: None,
            ea_itcs: Callable[[Itc, LogCalc], Any] = lambda __o, __i: None,
    ):
        if type(row) in (_LogRecord, _CmdTradeClose):
            ea_undefined(row, self)
        elif isinstance(row, TradeOpen):
            ea_open_trades(row, self)
        elif isinstance(row, TradeFinalized):
            ea_fin_trades(row, self)
        else:
            for typ, func in (
                    (Deposit, ea_deposits),
                    (Payout, ea_payouts),
                    (TradeFinalized, ea_fin_trades),
                    (TradeOpen, ea_open_trades),
                    (Dividend, ea_dividends),
                    (Itc, ea_itcs),
            ):
                if isinstance(row, typ):
                    func(row, self)
                    break

    def cat(
            self,
            row: dict,
            ea_deposits: Callable[[Deposit, LogCalc], Any] = lambda __o, __i: None,
            ea_payouts: Callable[[Payout, LogCalc], Any] = lambda __o, __i: None,
            ea_fin_trades: Callable[[TradeFinalized, LogCalc], Any] = lambda __o, __i: None,
            ea_open_trades: Callable[[TradeOpen, LogCalc], Any] = lambda __o, __i: None,
            ea_undefined: Callable[[_LogRecord, LogCalc], Any] = lambda __o, __i: None,
            ea_dividends: Callable[[Dividend, LogCalc], Any] = lambda __o, __i: None,
            ea_itcs: Callable[[Itc, LogCalc], Any] = lambda __o, __i: None,
    ) -> Payout | Dividend | Itc | _LogRecord | Deposit | TradeFinalized | TradeOpen | _CmdTradeClose:
        invest_t = datetime_from_tradetimeformat(row.get("InvestTime"))
        take_t = datetime_from_tradetimeformat(row.get("TakeTime"))
        invest_a = row.get("InvestAmount")
        take_a = row.get("TakeAmount")
        itc = row.get("ITC")
        n = row.get("n")
        default_date = datetime.now()
        # deposit / payout / dividend / itc
        if n == 0:
            if invest_t:
                if invest_a:
                    # deposit
                    obj = Deposit(row_dat=row, index_date=invest_t, amount=invest_a, default_date=default_date)
                    ea_deposits(obj, self)
                elif itc is not None:
                    # itc
                    obj = Itc(row_dat=row, index_date=invest_t, amount=itc, default_date=default_date, at_invest=True)
                    ea_itcs(obj, self)
                else:
                    # undefined with time
                    obj = _LogRecord(row_dat=row, index_date=invest_t, amount=None, default_date=default_date)
                    ea_undefined(obj, self)
            # payout / dividend
            elif take_t:
                if take_a:
                    if row.get("Name") in (record_tags.tag_PAYOUT, None, ""):
                        # payout
                        obj = Payout(row_dat=row, index_date=take_t, amount=take_a, default_date=default_date)
                        ea_payouts(obj, self)
                    else:
                        # dividend
                        obj = Dividend(row_dat=row, index_date=take_t, amount=take_a, default_date=default_date, by_course=False)
                        ea_dividends(obj, self)
                elif itc is not None:
                    # itc
                    obj = Itc(row_dat=row, index_date=take_t, amount=itc, default_date=default_date, at_invest=False)
                    ea_itcs(obj, self)
                else:
                    # undefined with time
                    obj = _LogRecord(row_dat=row, index_date=take_t, amount=None, default_date=default_date)
                    ea_undefined(obj, self)
            else:
                obj = _LogRecord(row_dat=row, index_date=None, amount=None, default_date=default_date)
                ea_undefined(obj, self)
        # trade
        elif n is not None:
            if n > 0:
                # trade
                if invest_t:
                    if invest_a:
                        if take_a is not None:
                            if take_t:
                                obj = TradeFinalized(row_dat=row, index_date=(take_t if self._index_by_take_date else invest_t), amount=invest_a, default_date=default_date)
                                ea_fin_trades(obj, self)
                            else:
                                obj = TradeOpen(row_dat=row, index_date=invest_t, amount=invest_a, default_date=default_date, has_take=True)
                                ea_open_trades(obj, self)
                        else:
                            obj = TradeOpen(row_dat=row, index_date=invest_t, amount=invest_a, default_date=default_date, has_take=False)
                            ea_open_trades(obj, self)
                    else:
                        # invalid record with date
                        obj = _LogRecord(row_dat=row, index_date=invest_t, amount=None, default_date=default_date)
                        ea_undefined(obj, self)
                # invalid record with date
                elif take_t:
                    obj = _LogRecord(row_dat=row, index_date=take_t, amount=None, default_date=default_date)
                    ea_undefined(obj, self)
                # invalid record without date
                else:
                    obj = _LogRecord(row_dat=row, index_date=None, amount=None, default_date=default_date)
                    ea_undefined(obj, self)
            else:
                # trade close
                if take_t:
                    if take_a is not None:
                        obj = _CmdTradeClose(row_dat=row, index_date=take_t, amount=take_a, default_date=default_date)
                    else:
                        obj = _LogRecord(row_dat=row, index_date=take_t, amount=None, default_date=default_date)
                    ea_undefined(obj, self)
                # invalid record with date
                elif invest_t:
                    obj = _LogRecord(row_dat=row, index_date=take_t, amount=None, default_date=default_date)
                    ea_undefined(obj, self)
                # invalid record without date
                else:
                    obj = _LogRecord(row_dat=row, index_date=None, amount=None, default_date=default_date)
                    ea_undefined(obj, self)
        # n is undefined with date
        elif invest_t:
            obj = _LogRecord(row_dat=row, index_date=invest_t, amount=None, default_date=default_date)
            ea_undefined(obj, self)
        # n is undefined with date
        elif take_t:
            obj = _LogRecord(row_dat=row, index_date=take_t, amount=None, default_date=default_date)
            ea_undefined(obj, self)
        # n is undefined without date
        else:
            obj = _LogRecord(row_dat=row, index_date=None, amount=None, default_date=default_date)
            ea_undefined(obj, self)

        return obj

    def do(
            self,
            row: dict | _LogRecord,
            ea_deposits: Callable[[Deposit, LogCalc], Any],
            ea_payouts: Callable[[Payout, LogCalc], Any],
            ea_fin_trades: Callable[[TradeFinalized, LogCalc], Any],
            ea_open_trades: Callable[[TradeOpen, LogCalc], Any],
            ea_undefined: Callable[[_LogRecord, LogCalc], Any],
            ea_dividends: Callable[[Dividend, LogCalc], Any],
            ea_itcs: Callable[[Itc, LogCalc], Any],
    ) -> Payout | Dividend | Itc | _LogRecord | Deposit | TradeFinalized | TradeOpen:
        if isinstance(row, dict):
            return self.cat(row, ea_deposits, ea_payouts, ea_fin_trades, ea_open_trades, ea_undefined, ea_dividends, ea_itcs)
        else:
            self.act(row, ea_deposits, ea_payouts, ea_fin_trades, ea_open_trades, ea_undefined, ea_dividends, ea_itcs)
            return row

    def rm(self, row: dict | _LogRecord) -> Payout | Dividend | Itc | _LogRecord | Deposit | TradeFinalized | TradeOpen:
        def ea_deposits(__o, __i): __i._deposits.remove(__o)

        def ea_payouts(__o, __i): __i._payouts.remove(__o)

        def ea_fin_trades(__o, __i): __i._fin_trades.remove(__o)

        def ea_open_trades(__o, __i): __i._open_trades.remove(__o)

        def ea_undefined(__o, __i): __i._undefined.remove(__o)

        def ea_dividends(__o, __i): __i._dividends.remove(__o)

        def ea_itcs(__o, __i): __i._itcs.remove(__o)

        return self.do(row, ea_deposits, ea_payouts, ea_fin_trades, ea_open_trades, ea_undefined, ea_dividends, ea_itcs)

    def get(self, __id: int) -> Payout | Dividend | Itc | _LogRecord | Deposit | TradeFinalized | TradeOpen:
        _log = self._deposits + self._payouts + self._fin_trades + self._open_trades + self._dividends + self._itcs + self._undefined
        return _log[_log.index({"id": __id})]

    def add(self, row: dict | _LogRecord) -> Payout | Dividend | Itc | _LogRecord | Deposit | TradeFinalized | TradeOpen:
        def ea_deposits(__o, __i): (__i._deposits.append(__o), __i._deposits.sort())

        def ea_payouts(__o, __i): (__i._payouts.append(__o), __i._payouts.sort())

        def ea_fin_trades(__o, __i): (__i._fin_trades.append(__o), __i._fin_trades.sort())

        def ea_open_trades(__o, __i): (__i._open_trades.append(__o), __i._open_trades.sort())

        def ea_undefined(__o, __i): (__i._undefined.append(__o), __i._undefined.sort())

        def ea_dividends(__o, __i): (__i._dividends.append(__o), __i._dividends.sort())

        def ea_itcs(__o, __i): (__i._itcs.append(__o), __i._itcs.sort())

        return self.do(row, ea_deposits, ea_payouts, ea_fin_trades, ea_open_trades, ea_undefined, ea_dividends, ea_itcs)

    def replace(self, old_row: _LogRecord | dict | None, new_row: _LogRecord | dict) -> tuple[Payout | Dividend | Itc | _LogRecord | Deposit | TradeFinalized | TradeOpen, Payout | Dividend | Itc | _LogRecord | Deposit | TradeFinalized | TradeOpen | None]:
        if old_row:
            old_row = self.rm(old_row)
        new_row = self.add(new_row)
        return old_row, new_row

    def new_row(self) -> _LogRecord:
        new = {"id": len(self)}
        default_date = datetime.now()
        new = _LogRecord(row_dat=new, index_date=None, amount=None, default_date=default_date)
        self.add(new)
        return new

    def __f_init_data__(self, log_data: list[dict] = None):
        self.__x_init_data__ = lambda *_, **__: None

        if log_data is None:
            log_data = self._log_data
            del self._log_data

        self._deposits = list()
        self._payouts = list()
        self._fin_trades = list()
        self._open_trades = list()
        self._undefined = list()
        self._dividends = list()
        self._itcs = list()
        self._names = set()
        self._symbols = set()
        self._isins = set()
        self._types = set()
        self._sectors = set()
        self._categories = set()

        def add_ids(__o, __i):
            if i := __o.row_dat.get("Name"):
                __i._names.add(i)
            if i := __o.row_dat.get("Symbol"):
                __i._symbols.add(i)
            if i := __o.row_dat.get("ISIN"):
                __i._isins.add(i)
            if i := __o.row_dat.get("Type"):
                __i._types.add(i)
            if i := __o.row_dat.get("Sector"):
                __i._sectors.add(i)
            if i := __o.row_dat.get("Category"):
                __i._categories.add(i)

        def ea_undefined(__o, __i):
            if not __o._do_flush():
                __i._undefined.append(__o)

        def ea_deposits(__o, __i):
            __i._deposits.append(__o)

        def ea_payouts(__o, __i):
            __i._payouts.append(__o)

        def ea_fin_trades(__o, __i):
            __i._fin_trades.append(__o)
            add_ids(__o, __i)

        def ea_open_trades(__o, __i):
            __i._open_trades.append(__o)
            add_ids(__o, __i)

        def ea_dividends(__o, __i):
            __i._dividends.append(__o)
            add_ids(__o, __i)

        def ea_itcs(__o, __i):
            __i._itcs.append(__o)

        for row in log_data:
            self.cat(row, ea_deposits, ea_payouts, ea_fin_trades, ea_open_trades, ea_undefined, ea_dividends, ea_itcs)

        self._deposits.sort()
        self._payouts.sort()
        self._fin_trades.sort()
        self._open_trades.sort()
        self._undefined.sort()
        self._dividends.sort()
        self._itcs.sort()

        self.new_row()

        for n, o in enumerate(self.__get_sorted_log_objs__()):
            o["id"] = n

        self.__f_reset_calc__()
        self.__f_calc__()
        pass

    __x_init_data__ = __f_init_data__

    def __f_calc__(self) -> list[Itc]:
        self.__x_reset_calc__()
        self.__x_init_data__()
        self.__x_calc__ = lambda: None

        log = self._deposits + self._payouts + self._fin_trades + self._open_trades + self._dividends + self._itcs
        log.sort(key=lambda x: x._min_date)

        pre_deposits = list()
        pre_trades = list()
        added_rows = list()

        def update_factors():
            sum_deposits = sum(tuple(cp_io.amount for cp_io in pre_deposits))
            for pre_d in pre_deposits:
                pre_d.set_factor(sum_deposits)

        if self._calc_with_open_positions:
            def is_calc_trade():
                return row.has_take
        else:
            def is_calc_trade():
                return isinstance(row, TradeFinalized)

        for row in log:
            row.reset()
            if isinstance(row, Deposit):
                pre_deposits.append(row)
                update_factors()
            elif isinstance(row, Payout):
                row.add_deposits(pre_deposits)
                remain_payout_value = row.real_amount
                try:
                    while remain_payout_value:
                        remain_payout_value = pre_deposits[0].add_payout(row, remain_payout_value)
                        if not pre_deposits[0].value:
                            pre_deposits.pop(0).close()
                except IndexError:
                    row.amount -= remain_payout_value
                    row["TakeAmount"] = row.amount
                    _new = self.new_row()
                    new = _new.row_dat | {"n": 0, "TakeTime": row["TakeTime"], "ITC": remain_payout_value}
                    new = Itc(new, datetime_from_tradetimeformat(row["TakeTime"]), remain_payout_value, datetime.now())
                    self.replace(_new, new)
                    added_rows.append(new)
                    added_rows += self.__f_calc__()
                    break
                update_factors()
            elif isinstance(row, Dividend):
                for pre_d in pre_deposits:
                    pre_d.add_dividend(row.amount)
                for pre_t in pre_trades:
                    if pre_t.row_dat["Name"] == row.name:
                        if isinstance(pre_t, TradeFinalized):
                            if pre_t._min_date <= row.index_date < pre_t._max_date:
                                row.add_trade(pre_t)
                        else:
                            row.add_trade(pre_t)
            elif isinstance(row, Itc):
                row.add_deposits(pre_deposits)
            elif is_calc_trade():
                for pre_d in pre_deposits:
                    pre_d.add_profit(row.profit)
                pre_trades.append(row)
            else:
                pre_trades.append(row)

        self.__reset_props__()
        return added_rows

    __x_calc__ = __f_calc__

    def __f_reset_calc__(self):
        self.__x_reset_calc__ = lambda: None
        self.__reset_props__()
        self.__x_calc__ = self.__f_calc__

    __x_reset_calc__ = __f_reset_calc__

    def __reset_props__(self):
        for record in self.__get_log_objs__():
            record.reset_data()
        for prop in self._cached_props:
            try:
                delattr(self, prop)
            except AttributeError:
                pass

    class EditItem(NamedTuple):
        updates: list
        added: list
        summary_relevant: bool
        id_relevant: bool
        same_type: bool

    def edit(self, update: dict) -> EditItem:
        global manual_take_amount
        try:
            relevant_summary = True
            relevant_id = False

            upd_row = update["data"]
            triggered_col = update["colId"]
            old_row = upd_row | {triggered_col: update.get("oldValue")}

            if triggered_col in ("Note", "Rating", "mark"):
                relevant_summary = False
            elif triggered_col == "Name":
                __env__.plugin.symbol_call(update)
                upd_row = update["data"]
                relevant_summary = upd_row.get("n") == 0
                relevant_id = True
            elif triggered_col in ("Symbol", "ISIN", "Type", "Short", "Sector", "Category"):
                __env__.plugin.symbol_call(update)
                upd_row = update["data"]
                relevant_summary = False
                relevant_id = True
            elif update.get("value") is None:  # cell delete
                match triggered_col:
                    case "InvestAmount":
                        upd_row.pop("InvestCourse", None)
                    case "InvestCourse":
                        upd_row.pop("InvestAmount", None)
                    case "TakeAmount":
                        upd_row.pop("TakeCourse", None)
                        manual_take_amount = True
                    case "TakeCourse":
                        upd_row.pop("TakeAmount", None)
                        manual_take_amount = True
            else:
                if triggered_col in ("InvestTime", "TakeTime"):
                    upd_row[update["colId"]] = tradetimeparser(update["value"])
                if n := upd_row.get("n"):
                    match triggered_col:
                        case "InvestAmount":
                            upd_row["InvestCourse"] = upd_row[triggered_col] / n
                        case "InvestCourse":
                            upd_row["InvestAmount"] = upd_row[triggered_col] * n
                        case "TakeAmount":
                            upd_row["TakeCourse"] = upd_row[triggered_col] / n
                            manual_take_amount = True
                        case "TakeCourse":
                            upd_row["TakeAmount"] = upd_row[triggered_col] * n
                            manual_take_amount = True

            new_row = self.cat(upd_row)
            if isinstance(new_row, _CmdTradeClose):
                return self.close_trade(new_row)
            elif not relevant_summary:
                row = self.get(upd_row["id"])
                row.row_dat.update(upd_row)
                ei = self.EditItem(
                    updates=[row.row_dat],
                    added=[],
                    summary_relevant=False,
                    id_relevant=relevant_id,
                    same_type=False
                )
            else:
                old_row = self.cat(old_row)
                self.replace(old_row, new_row)
                t_new = type(new_row)
                t_old = type(old_row)
                if not ((new_nin_calc := t_new is _LogRecord) and t_old is _LogRecord):
                    added = list(i.data for i in self.__f_calc__())
                    self.__reset_props__()
                    updates = list(i.data for i in self.calc_deposits + self.calc_payouts + self.fin_trades + self.open_trades + self.dividends + self.itcs)
                    if new_nin_calc:
                        updates.append(new_row.data)
                    ei = self.EditItem(
                        updates=updates,
                        added=added,
                        summary_relevant=True,
                        id_relevant=relevant_id,
                        same_type=t_old is t_new
                    )
                else:
                    ei = self.EditItem(
                        updates=[new_row.data],
                        added=[],
                        summary_relevant=False,
                        id_relevant=relevant_id,
                        same_type=t_old is t_new
                    )

            return ei
        finally:
            manual_take_amount = False

    def close_trade(self, row: _CmdTradeClose) -> EditItem:
        open_trades = sorted(self.open_trades)
        close_name = row["Name"]
        close_t = row["TakeTime"]
        close_n = abs(row["n"])
        row["TakeAmount"] = abs(row["TakeAmount"])
        close_c = row["TakeAmount"] / close_n
        row["TakeCourse"] = close_c
        updates = list()
        for ot in open_trades:
            if ot["Name"] == close_name:
                _close_n = close_n - ot["n"]
                if _close_n < 0:
                    ot["n"] = abs(_close_n)
                    ot["InvestAmount"] = ot["InvestCourse"] * ot["n"]
                    if ot.row_dat.get("TakeCourse") is not None:
                        ot["TakeAmount"] = ot["TakeCourse"] * ot["n"]

                    row["n"] = close_n
                    row["InvestTime"] = ot["InvestTime"]
                    row["InvestAmount"] = ot["InvestCourse"] * close_n
                    row["TakeAmount"] = close_c * close_n
                    row["TakeCourse"] = close_c

                    self.replace(row, row.row_dat)
                    break
                else:
                    ot["TakeTime"] = close_t
                    ot["TakeCourse"] = close_c
                    ot["TakeAmount"] = close_c * ot["n"]
                    self.replace(ot, ot.row_dat)
                    if _close_n == 0:
                        row.row_dat = {"id": row["id"], "cat": row["cat"]}
                        self.replace(row, row.row_dat)
                        updates.append(row.row_dat)
                        break
                    close_n = _close_n
        else:
            row["n"] = None
            row["Name"] = f"# (-{close_n})? {row['Name']}"
            self.replace(row, row.row_dat)
            updates.append(row.row_dat)

        added = list(i.data for i in self.__f_calc__())
        self.__reset_props__()
        updates += list(i.data for i in self.calc_deposits + self.calc_payouts + self.fin_trades + self.open_trades + self.dividends + self.itcs)
        ei = self.EditItem(
            updates=updates,
            added=added,
            summary_relevant=True,
            id_relevant=False,
            same_type=False
        )

        return ei

    def update(self, new_row: dict, old_row: dict | None) -> EditItem:
        new_row = self.cat(new_row)
        if isinstance(new_row, _CmdTradeClose):
            return self.close_trade(new_row)
        if old_row:
            old_row = self.cat(old_row)
        self.replace(old_row, new_row)
        t_new = type(new_row)
        t_old = type(old_row)
        if not ((new_nin_calc := t_new is _LogRecord) and t_old is _LogRecord):
            added = list(i.data for i in self.__f_calc__())
            self.__reset_props__()
            updates = list(i.data for i in self.calc_deposits + self.calc_payouts + self.fin_trades + self.open_trades + self.dividends + self.itcs)
            if new_nin_calc:
                updates.append(new_row.data)
            ei = self.EditItem(
                updates=updates,
                added=added,
                summary_relevant=True,
                id_relevant=True,
                same_type=t_old is t_new
            )
        else:
            ei = self.EditItem(
                updates=[new_row.data],
                added=[],
                summary_relevant=False,
                id_relevant=True,
                same_type=t_old is t_new
            )

        return ei

    def update_course(self) -> list[dict]:
        return [self.replace(ot, ot.update_course())[1].data for ot in self.open_trades]

    def getTradeFrame(
            self,
            first: datetime,
            last: datetime,
            by_attr: Literal["idx", "min", "max", "or"] | str = "idx",
            name_filter: str | None = None,
            ui: bool = False
    ) -> TradeFrameCalc:
        return TradeFrameCalc(self, first, last, by_attr, name_filter, ui)

    ##########################################################################################################################################

    @cached_property
    def calc_deposits(self) -> tuple[Deposit, ...]:
        self.__x_init_data__()
        self.__x_calc__()
        return tuple(self._deposits)

    @cached_property
    def frame_deposits(self) -> tuple[Deposit, ...]: return self.calc_deposits
    
    @cached_property
    def calc_payouts(self) -> tuple[Payout, ...]:
        self.__x_init_data__()
        self.__x_calc__()
        return tuple(self._payouts)

    @cached_property
    def frame_payouts(self) -> tuple[Payout, ...]: return self.calc_payouts
    
    @cached_property
    def calc_trades(self) -> tuple[TradeFinalized | TradeOpen, ...]:
        self.__x_init_data__()
        self.__x_calc__()
        if self._calc_with_open_positions:
            return tuple(t for t in sorted(self._open_trades + self._fin_trades) if t.has_take)
        else:
            return self.fin_trades

    @cached_property
    def fin_trades(self) -> tuple[TradeFinalized, ...]:
        self.__x_init_data__()
        self.__x_calc__()
        return tuple(self._fin_trades)

    @cached_property
    def open_trades(self) -> tuple[TradeOpen, ...]:
        self.__x_init_data__()
        self.__x_calc__()
        return tuple(self._open_trades)

    @cached_property
    def undefined(self) -> tuple[_LogRecord, ...]:
        self.__x_init_data__()
        self.__x_calc__()
        return tuple(self._undefined)

    @cached_property
    def dividends(self) -> tuple[Dividend, ...]:
        self.__x_init_data__()
        self.__x_calc__()
        return tuple(self._dividends)

    @cached_property
    def itcs(self) -> tuple[Itc, ...]:
        self.__x_init_data__()
        self.__x_calc__()
        return tuple(self._itcs)

    def __get_log_objs__(self):
        self.__x_init_data__()
        self.__x_calc__()
        return self._deposits + self._payouts + self._fin_trades + self._open_trades + self._dividends + self._itcs + self._undefined

    def __get_sorted_log_objs__(self):
        return sorted(self.__get_log_objs__(), key=lambda o: o.index_date, reverse=True)

    def __get_log_json__(self):
        return [o.data for o in self.__get_log_objs__()]

    def __get_sorted_log_json__(self):
        return [o.data for o in self.__get_sorted_log_objs__()]

    ##########################################################################################################################################

    @cached_property
    def n_trades_fin(self) -> int:
        return len(self.fin_trades)

    @cached_property
    def n_trades_open(self) -> int:
        return len(self.open_trades)

    @cached_property
    def n_calc_deposits(self) -> int:
        return len(self.calc_deposits)

    @cached_property
    def n_calc_payouts(self) -> int:
        return len(self.calc_payouts)

    @cached_property
    def n_frame_deposits(self) -> int:
        return len(self.frame_deposits)

    @cached_property
    def n_frame_payouts(self) -> int:
        return len(self.frame_payouts)

    @cached_property
    def n_dividends(self) -> int:
        return len(self.dividends)

    @cached_property
    def n_itcs(self) -> int:
        return len(self.itcs)

    @cached_property
    def n_calc_trades(self) -> int:
        return len(self.calc_trades)

    @cached_property
    def first_record(self) -> TradeOpen | TradeFinalized | Deposit | Payout | None:
        firsts = self.frame_deposits[:1] + self.frame_payouts[:1] + self.fin_trades[:1] + self.open_trades[:1]
        if firsts:
            return min(firsts, key=lambda x: x.index_date)

    @cached_property
    def last_record(self) -> TradeOpen | TradeFinalized | Deposit | Payout | None:
        last = self.frame_deposits[-1:] + self.frame_payouts[-1:] + self.fin_trades[-1:] + self.open_trades[-1:]
        if last:
            return max(last, key=lambda x: x.index_date)

    @cached_property
    def portfolio_age_sec(self) -> int:
        first_record = self.first_record
        if first_record:
            return int((datetime.now() - first_record.index_date).total_seconds())
        else:
            return 0

    @cached_property
    def profit_trade_avg(self) -> float:
        return preventZeroDiv(sum(i.data["Profit"] for i in self.calc_trades), self.n_calc_trades, 0)

    @cached_property
    def performance_trade_avg(self) -> float:
        return preventZeroDiv(sum(i.data["Performance"] or 0 for i in self.calc_trades), self.n_calc_trades, 0)

    @cached_property
    def sum_profits(self) -> float:
        self.__x_calc__()
        return sum(i.data["Profit"] or 0 for i in self.calc_deposits)

    @cached_property
    def dripping_performance_avg(self) -> float:
        self.__x_calc__()
        return preventZeroDiv(sum(i.data["Performance"] or 0 for i in self.calc_deposits), self.n_calc_deposits, 0)

    @cached_property
    def current_performance_on_portfolio(self) -> float:
        return preventZeroDiv(self.sum_profits, self.money, 0)

    @cached_property
    def holdtime_of_fin_trades_avg(self) -> float:
        return preventZeroDiv(sum(i.data["HoldTime"] for i in self.fin_trades), self.n_trades_fin, 0)

    @cached_property
    def holdtime_of_all_avg(self) -> float:
        return preventZeroDiv(sum(i.data["HoldTime"] for i in self.fin_trades + self.open_trades), self.n_trades_fin + self.n_trades_open, 0)

    @cached_property
    def sum_payouts(self) -> float:
        return sum(i.amount for i in self.calc_payouts)

    @cached_property
    def sum_deposits(self) -> float:
        return sum(i.amount for i in self.calc_deposits)

    @cached_property
    def money(self) -> float:
        return self.sum_deposits - self.sum_payouts

    @cached_property
    def sum_dividends(self) -> float:
        return sum(i.amount for i in self.dividends)

    @cached_property
    def current_dividend_rate(self) -> float:
        return preventZeroDiv(self.sum_dividends, self.money, 0)

    @cached_property
    def dripping_dividend_rate(self):
        self.__x_calc__()
        return preventZeroDiv(sum(i.data["DividendRate"] or 0 for i in self.calc_deposits), self.n_calc_deposits, 0)

    @cached_property
    def sum_fin_invest(self) -> float:
        return sum(i.amount for i in self.fin_trades)

    @cached_property
    def sum_open_invest(self) -> float:
        return sum(i.amount for i in self.open_trades)

    @cached_property
    def sum_fin_take(self):
        return sum(i["TakeAmount"] or 0 for i in self.fin_trades)

    @cached_property
    def sum_itcs(self) -> float:
        return sum(i.amount for i in self.itcs)

    @cached_property
    def current_itcs_rate(self) -> float:
        return preventZeroDiv(self.sum_itcs, self.money, 0)

    @cached_property
    def summary_value(self) -> float:
        return self.sum_profits + self.sum_dividends + self.sum_itcs

    @cached_property
    def current_summary_rate(self) -> float:
        return preventZeroDiv(self.summary_value, self.money, 0)

    @cached_property
    def avg_profit_per_day(self):
        return preventZeroDiv(sum(i.data["Profit/Day"] for i in self.calc_trades), self.n_calc_trades, 0)

    @cached_property
    def avg_performance_per_day(self):
        return preventZeroDiv(sum(i.data["Performance/Day"] for i in self.calc_trades), self.n_calc_trades, 0)

    @cached_property
    def avg_profit_per_year(self):
        return preventZeroDiv(sum(i.data["Profit/Year"] for i in self.calc_trades), self.n_calc_trades, 0)

    @cached_property
    def avg_performance_per_year(self):
        return preventZeroDiv(sum(i.data["Performance/Year"] for i in self.calc_trades), self.n_calc_trades, 0)


class TradeFrameCalc(LogCalc):
    __mainFrame__: LogCalc
    frame_begin: datetime
    frame_end: datetime
    by_attr: Literal["idx", "min", "max", "or"] | str
    name_filter: str | None
    ui: bool
    
    def getMainFrame(self) -> LogCalc:
        self.__mainFrame__.__f_init_data__(self.__mainFrame__.__get_log_json__())
        return self.__mainFrame__

    def getTradeFrame(self, first: datetime, last: datetime, by_attr: Literal["idx", "min", "max", "or"] | str = "idx", name_filter: str | None = None, ui: bool = False) -> TradeFrameCalc:
        return LogCalc.getTradeFrame(self.__mainFrame__, first, last, by_attr, name_filter or self.name_filter, ui)

    def cat(self, row: dict, ea_deposits: Callable[[Deposit, LogCalc], Any] = lambda __o, __i: None, ea_payouts: Callable[[Payout, LogCalc], Any] = lambda __o, __i: None, ea_fin_trades: Callable[[TradeFinalized, LogCalc], Any] = lambda __o, __i: None, ea_open_trades: Callable[[TradeOpen, LogCalc], Any] = lambda __o, __i: None, ea_undefined: Callable[[_LogRecord, LogCalc], Any] = lambda __o, __i: None, ea_dividends: Callable[[Dividend, LogCalc], Any] = lambda __o, __i: None,
            ea_itcs: Callable[[Itc, LogCalc], Any] = lambda __o, __i: None) -> Payout | Dividend | Itc | _LogRecord | Deposit | TradeFinalized | TradeOpen:
        self.__mainFrame__.cat(row, ea_deposits, ea_payouts, ea_fin_trades, ea_open_trades, ea_undefined, ea_dividends, ea_itcs)
        return LogCalc.cat(self, row, ea_deposits, ea_payouts, ea_fin_trades, ea_open_trades, ea_undefined, ea_dividends, ea_itcs)

    def act(self, row: Payout | Dividend | Itc | _LogRecord | Deposit | TradeFinalized | TradeOpen, ea_deposits: Callable[[Deposit, LogCalc], Any] = lambda __o, __i: None, ea_payouts: Callable[[Payout, LogCalc], Any] = lambda __o, __i: None, ea_fin_trades: Callable[[TradeFinalized, LogCalc], Any] = lambda __o, __i: None, ea_open_trades: Callable[[TradeOpen, LogCalc], Any] = lambda __o, __i: None, ea_undefined: Callable[[_LogRecord, LogCalc], Any] = lambda __o, __i: None,
            ea_dividends: Callable[[Dividend, LogCalc], Any] = lambda __o, __i: None, ea_itcs: Callable[[Itc, LogCalc], Any] = lambda __o, __i: None):
        self.__mainFrame__.act(row, ea_deposits, ea_payouts, ea_fin_trades, ea_open_trades, ea_undefined, ea_dividends, ea_itcs)
        LogCalc.act(self, row, ea_deposits, ea_payouts, ea_fin_trades, ea_open_trades, ea_undefined, ea_dividends, ea_itcs)

    def new_row(self) -> _LogRecord:
        new_row = self.__mainFrame__.new_row()
        LogCalc.act(self, new_row, ea_undefined=lambda __o, __i: self._undefined.append(__o))
        return new_row

    def __f_init_data__(self, log_data: list[dict] = None):
        _cat = self.cat
        self.cat = lambda *args, **kwargs: LogCalc.cat(self, *args, **kwargs)
        super().__f_init_data__(log_data)
        self.cat = _cat

    def _init(self):

        by_attr = self.by_attr

        if self.by_attr.endswith("+"):
            by_attr = "or"

            if self.name_filter:
                def ismatch(rec: _LogRecord):
                    return (search(self.name_filter, rec["Name"], IGNORECASE)
                            and
                            (self.frame_begin <= rec.get_min_date(self.frame_begin) <= self.frame_end
                             or
                             self.frame_begin <= rec.get_max_date(self.frame_begin) <= self.frame_end))

            else:
                def ismatch(rec: _LogRecord):
                    return (self.frame_begin <= rec.get_min_date(self.frame_begin) <= self.frame_end
                            or
                            self.frame_begin <= rec.get_max_date(self.frame_begin) <= self.frame_end)

        elif self.name_filter:
            def ismatch(rec: _LogRecord):
                return search(self.name_filter, rec["Name"], IGNORECASE)

        else:
            def ismatch(rec: _LogRecord):
                return True

        match by_attr:
            case "or":
                # first=3, last=7 (data indexed by invest date)
                #              {                                                              }
                # [ (a=1;b=2), (a=2;b=7), (a=3;b=4), (a=4;b=6), (a=5;b=9), (a=6;b=7), (a=7;b=8), (a=8;b=9) ]
                #
                # first=3, last=7 (data indexed by take date)
                #              {                                        }
                # [ (a=1;b=2), (a=3;b=4), (a=4;b=6), (a=2;b=7), (a=6;b=7), (a=7;b=8), (a=5;b=9), (a=8;b=9) ]
                def start(rec: _LogRecord):
                    return self.frame_begin <= rec.get_max_date(self.frame_begin)

                def continue_(rec: _LogRecord):
                    return rec.get_min_date(self.frame_end) <= self.frame_end

                def stop(rec: _LogRecord):
                    return rec.get_min_date(self.frame_end) > self.frame_end
            case "min":
                def start(rec: _LogRecord):
                    return self.frame_begin <= rec.get_min_date(self.frame_begin)

                def continue_(rec: _LogRecord):
                    return rec.get_min_date(self.frame_end) <= self.frame_end

                def stop(rec: _LogRecord):
                    return rec.get_min_date(self.frame_end) > self.frame_end
            case "max":
                def start(rec: _LogRecord):
                    return self.frame_begin <= rec.get_max_date(self.frame_begin)

                def continue_(rec: _LogRecord):
                    return rec.get_max_date(self.frame_end) <= self.frame_end

                def stop(rec: _LogRecord):
                    return rec.get_max_date(self.frame_end) > self.frame_end
            case _:  # "idx"
                def start(rec: _LogRecord):
                    return self.frame_begin <= rec.get_idx_date(self.frame_begin)

                def continue_(rec: _LogRecord):
                    return rec.get_idx_date(self.frame_end) <= self.frame_end

                def stop(rec: _LogRecord):
                    return rec.get_idx_date(self.frame_end) > self.frame_end

        def _filter_trades(records):
            filtered = list()
            try:
                for i in range(len(records)):
                    if start(record := records[i]):
                        if ismatch(record):
                            filtered.append(record.copy())
                        i += 1
                        while continue_(record := records[i]):
                            if ismatch(record):
                                filtered.append(record.copy())
                            i += 1
                        break
            except IndexError:
                pass
            return filtered

        def _filter_undefined(records):
            filtered = list()
            try:
                for i in range(len(records)):
                    if start(record := records[i]):
                        if not record._do_flush():
                            filtered.append(record.copy())
                        i += 1
                        while continue_(record := records[i]):
                            if not record._do_flush():
                                filtered.append(record.copy())
                            i += 1
                        break
            except IndexError:
                pass
            return filtered

        def _filter_ios(records):
            filtered = records
            for i in range(len(records)):
                if stop(records[i]):
                    filtered = records[:i]
                    break
            return [i.copy() for i in filtered]

        self._deposits = _filter_ios(self.__mainFrame__.calc_deposits)
        self._payouts = _filter_ios(self.__mainFrame__.calc_payouts)
        self._fin_trades = _filter_trades(self.__mainFrame__.fin_trades)
        self._open_trades = _filter_trades(self.__mainFrame__.open_trades)
        self._dividends = _filter_trades(self.__mainFrame__.dividends)
        self._itcs = _filter_trades(self.__mainFrame__.itcs)

        if self.ui:
            self._undefined = _filter_undefined(self.__mainFrame__.undefined)
            self.new_row()
        else:
            self._undefined = _filter_trades(self.__mainFrame__.undefined)

        self.__f_reset_calc__()
        self.__f_calc__()

    def __init__(
            self,
            main: LogCalc,
            first: datetime,
            last: datetime,
            by_attr: Literal["idx", "min", "max", "or"] | str = "idx",
            name_filter: str | None = None,
            ui: bool = False
    ):
        LogCalc.__init__(self, [], )
        self._index_by_take_date = main._index_by_take_date
        self._calc_with_open_positions = main._calc_with_open_positions
        self.__mainFrame__ = main
        self.__x_init_data__ = lambda: None
        self.frame_begin = first
        self.frame_end = last
        self.by_attr = by_attr
        self.name_filter = name_filter
        self.ui = ui
        self._init()

    def set_parameter(self, index_by_take_date: bool | None = None, calc_with_open_positions: bool | None = None):
        self.__mainFrame__.set_parameter(index_by_take_date, calc_with_open_positions)
        LogCalc.set_parameter(self, index_by_take_date, calc_with_open_positions)
        self._init()

    @cached_property
    def openings(self) -> tuple[TradeOpen | TradeFinalized, ...] | tuple:
        openings = list()
        trades = list(self.fin_trades + self.open_trades)
        trades.sort(key=lambda x: x._min_date)
        try:
            for i in range(len(trades)):
                trade = trades[i]
                if self.frame_begin <= trade._min_date:
                    openings.append(trade)
                    i += 1
                    trade = trades[i]
                    while trade._min_date <= self.frame_end:
                        openings.append(trade)
                        i += 1
                        trade = trades[i]
                    break
        except IndexError:
            pass
        return tuple(openings)

    @cached_property
    def closures(self) -> tuple[TradeOpen | TradeFinalized, ...] | tuple:
        closures = list()
        trades = list(self.fin_trades)
        trades.sort(key=lambda x: x._max_date)
        try:
            for i in range(len(trades)):
                trade = trades[i]
                if self.frame_begin <= trade._max_date:
                    closures.append(trade)
                    i += 1
                    trade = trades[i]
                    while trade._max_date <= self.frame_end:
                        closures.append(trade)
                        i += 1
                        trade = trades[i]
                    break
        except IndexError:
            pass
        return tuple(closures)

    @cached_property
    def frame_deposits(self) -> tuple[Deposit, ...] | tuple:
        for i in range(len(self.__mainFrame__.calc_deposits)):
            if self.frame_begin <= self.__mainFrame__.calc_deposits[i].index_date:
                return self.__mainFrame__.calc_deposits[i:]
        else:
            return tuple()

    @cached_property
    def frame_payouts(self) -> tuple[Payout, ...] | tuple:
        for i in range(len(self.__mainFrame__.calc_payouts)):
            if self.frame_begin <= self.__mainFrame__.calc_payouts[i].index_date:
                return self.__mainFrame__.calc_payouts[i:]
        else:
            return tuple()

    @cached_property
    def n_openings(self) -> int:
        return len(self.openings)

    @cached_property
    def n_closures(self) -> int:
        return len(self.closures)

    @cached_property
    def openings_invest_amount(self) -> float:
        return sum((i.row_dat.get("InvestAmount") or 0) for i in self.openings)

    @cached_property
    def closures_invest_amount(self) -> float:
        return sum((i.row_dat.get("InvestAmount") or 0) for i in self.closures)

    @cached_property
    def openings_take_amount(self) -> float:
        return sum((i.row_dat.get("TakeAmount") or 0) for i in self.openings)

    @cached_property
    def closures_take_amount(self) -> float:
        return sum((i.row_dat.get("TakeAmount") or 0) for i in self.closures)

    @cached_property
    def sum_openings_profit(self):
        return sum((i.row_dat.get("Profit") or 0) for i in self.openings)

    @cached_property
    def sum_closures_profit(self):
        return sum((i.row_dat.get("Profit") or 0) for i in self.closures)

    @cached_property
    def avg_openings_profit(self):
        return preventZeroDiv(self.sum_openings_profit, self.n_openings, 0)

    @cached_property
    def avg_closures_profit(self):
        return preventZeroDiv(self.sum_closures_profit, self.n_closures, 0)

    @cached_property
    def current_openings_performance(self):
        return preventZeroDiv(self.sum_openings_profit, self.money, 0)

    @cached_property
    def current_closures_performance(self):
        return preventZeroDiv(self.sum_closures_profit, self.money, 0)
