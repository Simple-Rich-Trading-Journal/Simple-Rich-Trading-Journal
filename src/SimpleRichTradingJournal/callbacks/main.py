from __future__ import annotations

import json
from datetime import datetime, timedelta
from json import loads
from sys import stderr
from traceback import print_exception

import plotly.graph_objects as go
from dash import callback, Output, Input, State, no_update
from dash import callback_context

import __env__
import __ini__.logtags
import layout
from calc.log import LogCalc, TradeFrameCalc
from calc.utils import do_add_row
from config import styles

__lc__: LogCalc | TradeFrameCalc


_group_by_trigger_ids = tuple(i.id for i in layout.statistics._group_by_checks) + (layout.drag_event_receiver2.id,)


def _group_by(
        i_drag_event_receiver2_value,
        i_group_by_type,
        i_group_by_short,
        i_group_by_sector,
        i_group_by_category,
        i_group_by_id,
):
    if i_drag_event_receiver2_value:
        drag_event_receiver_ = loads(i_drag_event_receiver2_value)
        order = list(i.split("-")[1] for i in drag_event_receiver_["target_children"])
        order.reverse()
    else:
        order = layout.statistics._group_by_default_order.copy()
    for attr, val in (
            ("Short", i_group_by_short),
            ("Type", i_group_by_type),
            ("Sector", i_group_by_sector),
            ("Category", i_group_by_category),
    ):
        if not val:
            try:
                order.remove(attr)
            except ValueError:
                pass
    if not i_group_by_id:
        try:
            order.remove("Name")
        except ValueError:
            order.remove("Symbol")
    return order


def new_side(
        group_by,
        i_group_by_type,
        i_group_by_short,
        i_group_by_sector,
        i_group_by_category,
        i_group_by_id,
        i_group_by_show_all,
        scope_by_attr,
        i_performance_steps_value,
        i_performance_trailing_frame_value,
        i_performance_trailing_interval_value,
        i_performance_range_value,
        i_hypothesis_per_day_value,
        i_drag_event_receiver_value,
        i_performance_size_slider_value,
        i_Y_trigger_,
        i_Q_trigger_,
        i_T_trigger_,
        i_C_trigger_,
        i_STATISTICS_style,
        i_BALANCE_style,
):
    o_open_positions_graph_figure = o_all_positions_graph_figure = o_performance_graph_figure = o_BALANCE_children = o_drag_container_style = no_update
    layout.make.positions.OBJ.new(__lc__, _group_by(group_by, i_group_by_type, i_group_by_short, i_group_by_sector, i_group_by_category, i_group_by_id), bool(i_group_by_show_all))
    layout.make.performance.OBJ.new(
        __lc__,
        scope_by_attr,
        timedelta(weeks=i_performance_steps_value),
        timedelta(weeks=i_performance_trailing_frame_value),
        timedelta(weeks=i_performance_trailing_interval_value),
        timedelta(weeks=i_performance_range_value),
        __env__.statisticsPerformanceOrder,
        i_hypothesis_per_day_value,
    )
    if i_drag_event_receiver_value:
        drag_event_receiver_ = loads(i_drag_event_receiver_value)
        order = tuple(int(i.split("-")[1]) for i in drag_event_receiver_["target_children"])
        order = tuple(order.index(i) + 1 for i in range(1, __env__.nStatisticsDrag + 1))
        layout.make.performance.OBJ.opt__order(order)
    o_drag_container_style = layout.statistics.drag_container.style | {"height": "%dpx" % i_performance_size_slider_value}
    layout.make.balance.OBJ.new(__lc__, scope_by_attr, i_Y_trigger_, i_Q_trigger_, i_T_trigger_, i_C_trigger_)
    if i_STATISTICS_style:
        o_open_positions_graph_figure, o_all_positions_graph_figure = layout.make.positions.OBJ.get()
        o_performance_graph_figure = layout.make.performance.OBJ.get().update_layout(height=i_performance_size_slider_value)
    elif i_BALANCE_style:
        o_BALANCE_children = layout.make.balance.OBJ.get()
    return o_open_positions_graph_figure, o_all_positions_graph_figure, o_performance_graph_figure, o_BALANCE_children, o_drag_container_style


s_auto_save_on = layout.header.auto_save_button.style | styles.misc.autosave_on
s_auto_save_off = layout.header.auto_save_button.style | styles.misc.autosave_off
Output(layout.summary_footer, "style", allow_duplicate=True),
s_summary_error = layout.summary_footer.style | styles.misc.summary_error
s_summary_error_reset = layout.summary_footer.style | styles.misc.summary_error_reset


@callback(
    Output(layout.history.history_list, "options"),
    Output(layout.header.daterange, "min_date_allowed"),
    Output(layout.header.daterange, "max_date_allowed"),
    Output(layout.header.daterange, "initial_visible_month"),
    Output(layout.tradinglog, "rowData"),
    Output(layout.tradinglog, "rowTransaction", allow_duplicate=True),
    Output(layout.tradinglog, "dashGridOptions", allow_duplicate=True),
    Output(layout.summary_footer, "children", allow_duplicate=True),
    Output(layout.summary_footer, "style", allow_duplicate=True),
    Output(layout.renderer_trigger, "n_clicks", allow_duplicate=True),
    Output(layout.statistics.open_positions_graph, "figure", allow_duplicate=True),
    Output(layout.statistics.all_positions_graph, "figure", allow_duplicate=True),
    Output(layout.statistics.performance_graph, "figure", allow_duplicate=True),
    Output(layout.statistics.drag_container, "style", allow_duplicate=True),
    Output(layout.statistics_pop_trigger, "n_clicks"),
    Output(layout.statistics.pop_graph, "figure"),
    Output(layout.statistics.pop_title, "children"),
    Output(layout.balance.balance_content, "children", allow_duplicate=True),
    Output(layout.header.auto_save_button, "n_clicks"),
    Output(layout.header.auto_save_button, "style"),
    Output(layout.header.index_by_button, "style"),
    Output(layout.header.index_by_button, "children"),
    Output(layout.header.scope_by_button, "style"),
    Output(layout.header.scope_by_button, "children"),
    Output(layout.init_done_trigger, "n_clicks"),
    Output(layout.init_done_trigger2, "n_clicks", allow_duplicate=True),
    ##############################################################################################
    Input(layout.init_trigger, "n_clicks"),
    Input(layout.history.history_list, "value"),
    State(layout.tradinglog, "rowData"),
    Input(layout.tradinglog, "cellValueChanged"),
    State(layout.tradinglog, "dashGridOptions"),
    Input(layout.header.daterange, "start_date"),
    Input(layout.header.daterange, "end_date"),
    Input(layout.header.with_open_trigger, "n_clicks"),
    State(layout.renderer_trigger, "n_clicks"),
    Input(layout.header.auto_save_button, "n_clicks"),
    State(layout.statistics.open_positions_graph, "figure"),
    State(layout.statistics.all_positions_graph, "figure"),
    State(layout.statistics.performance_graph, "figure"),
    Input(layout.statistics.pop_open_positions, "n_clicks"),
    Input(layout.statistics.pop_all_positions, "n_clicks"),
    Input(layout.statistics.pop_performance, "n_clicks"),
    Input(layout.statistics.performance_size_slider, "value"),
    Input(layout.statistics.performance_steps, "value"),
    Input(layout.statistics.performance_trailing_frame, "value"),
    Input(layout.statistics.performance_trailing_interval, "value"),
    Input(layout.statistics.performance_range, "value"),
    Input(layout.statistics.performance_hypothesis_per, "value"),
    Input(layout.drag_event_receiver, "value"),
    State(layout.statistics.pop_graph, "figure"),
    Input(layout.statistics.pop_size_slider, "value"),
    Input(layout.statistics.STATISTICS, "style"),
    Input(layout.balance.BALANCE, "style"),
    Input(layout.balance.T_trigger_, "n_clicks"),
    Input(layout.balance.C_trigger_, "n_clicks"),
    Input(layout.balance.Y_trigger_, "n_clicks"),
    Input(layout.balance.Q_trigger_, "n_clicks"),
    Input(layout.header.index_by_button, "n_clicks"),
    State(layout.header.index_by_button, "style"),
    Input(layout.header.scope_by_button, "n_clicks"),
    State(layout.header.scope_by_button, "style"),
    Input(layout.drag_event_receiver2, "value"),
    Input(layout.edit_event_receiver, "value"),
    State(layout.statistics_pop_trigger, "n_clicks"),
    [Input(i, "value") for i in layout.statistics._group_by_checks],
    Input(layout.statistics.show_all, "value"),
    Input(layout.quick_search_receiver, "value"),
    config_prevent_initial_callbacks=True
)
def call(
        _,
        i_backup_list_value,
        i_tradinglog_rowData,
        i_tradinglog_cellValueChanged,
        i_tradinglog_dashGridOptions,
        i_daterange_start_date,
        i_daterange_end_date,
        i_with_open_value,
        i_renderer_trigger_n_clicks,
        i_auto_save_n_clicks,
        i_open_positions_graph_figure,
        i_all_positions_graph_figure,
        i_performance_graph_figure,
        i_pop_open_positions_n_clicks,
        i_pop_all_positions_n_clicks,
        i_pop_performance_n_clicks,
        i_performance_size_slider_value,
        i_performance_steps_value,
        i_performance_trailing_frame_value,
        i_performance_trailing_interval_value,
        i_performance_range_value,
        i_performance_hypothesis_per_value,
        i_drag_event_receiver_value,
        i_pop_graph_figure,
        i_pop_size_slider_value,
        i_STATISTICS_style,
        i_BALANCE_style,
        i_T_trigger_,
        i_C_trigger_,
        i_Y_trigger_,
        i_Q_trigger_,
        i_index_by_button_n_clicks,
        i_index_by_button_style,
        i_scope_by_button_n_clicks,
        i_scope_by_button_style,
        i_drag_event_receiver2_value,
        i_edit_event_receiver_value,
        i_statistics_pop_trigger_n_clicks,
        i_group_by_short,
        i_group_by_type,
        i_group_by_sector,
        i_group_by_category,
        i_group_by_id,
        i_group_by_show_all,
        i_quick_search_receiver_value,
):
    global __lc__

    i_with_open_value %= 2
    i_index_by_button_n_clicks %= 2
    i_scope_by_button_n_clicks %= 2

    i_auto_save_n_clicks %= 2

    i_Y_trigger_ %= 2
    i_Q_trigger_ %= 2
    i_T_trigger_ %= 2
    i_C_trigger_ %= 2

    o_backup_list_options = no_update
    o_daterange_min_date_allowed = no_update
    o_daterange_max_date_allowed = no_update
    o_daterange_initial_visible_month = no_update
    o_tradinglog_rowData = no_update
    o_tradinglog_rowTransaction = no_update
    o_tradinglog_dashGridOptions = no_update
    o_summary_footer_children = no_update
    o_summary_footer_style = no_update
    o_renderer_trigger_n_clicks = no_update
    o_open_positions_graph_figure = no_update
    o_all_positions_graph_figure = no_update
    o_performance_graph_figure = no_update
    o_drag_container_style = no_update
    o_statistics_pop_trigger_n_clicks = no_update
    o_pop_graph_figure = no_update
    o_pop_title_children = no_update
    o_BALANCE_children = no_update
    o_auto_save_n_clicks = no_update
    o_auto_save_style = no_update
    o_index_by_button_style = no_update
    o_index_by_button_children = no_update
    o_scope_by_button_style = no_update
    o_scope_by_button_children = no_update
    o_init_done_trigger_n_clicks = no_update
    o_init_done_trigger2_n_clicks = no_update

    i_STATISTICS_style = not i_STATISTICS_style.get("display")
    i_BALANCE_style = not i_BALANCE_style.get("display")

    if i_scope_by_button_n_clicks:
        scope_by_attr = "idx"
    else:
        scope_by_attr = __env__.scope_by_both

    __trigger__ = callback_context.triggered_id

    def _return():
        return (
            o_backup_list_options,
            o_daterange_min_date_allowed,
            o_daterange_max_date_allowed,
            o_daterange_initial_visible_month,
            o_tradinglog_rowData,
            o_tradinglog_rowTransaction,
            o_tradinglog_dashGridOptions,
            o_summary_footer_children,
            o_summary_footer_style,
            o_renderer_trigger_n_clicks,
            o_open_positions_graph_figure,
            o_all_positions_graph_figure,
            o_performance_graph_figure,
            o_drag_container_style,
            o_statistics_pop_trigger_n_clicks,
            o_pop_graph_figure,
            o_pop_title_children,
            o_BALANCE_children,
            o_auto_save_n_clicks,
            o_auto_save_style,
            o_index_by_button_style,
            o_index_by_button_children,
            o_scope_by_button_style,
            o_scope_by_button_children,
            o_init_done_trigger_n_clicks,
            o_init_done_trigger2_n_clicks,
        )

    def set_auto_save(on: int):
        nonlocal o_auto_save_n_clicks, o_auto_save_style, i_auto_save_n_clicks
        if on:
            i_auto_save_n_clicks = o_auto_save_n_clicks = 1
            o_auto_save_style = s_auto_save_on
        else:
            i_auto_save_n_clicks = o_auto_save_n_clicks = 0
            o_auto_save_style = s_auto_save_off

    def timeframe():
        global __lc__
        nonlocal i_daterange_end_date, o_tradinglog_rowData, o_summary_footer_children, o_renderer_trigger_n_clicks
        if not i_daterange_start_date:
            start = datetime(1, 1, 1)
        else:
            start = datetime.strptime(i_daterange_start_date, "%Y-%m-%d")
        if not i_daterange_end_date:
            end = datetime.now()
        else:
            end = datetime.strptime(i_daterange_end_date, "%Y-%m-%d") + timedelta(1)
        __lc__ = __lc__.getTradeFrame(start, end, by_attr=scope_by_attr, name_filter=i_quick_search_receiver_value, ui=True)
        o_tradinglog_rowData = __lc__.__get_sorted_log_json__()
        o_summary_footer_children = layout.make.make_footer(__lc__)
        o_renderer_trigger_n_clicks = i_renderer_trigger_n_clicks + 1

    def new_table(row_data: list):
        global __lc__
        nonlocal o_tradinglog_rowData, o_daterange_min_date_allowed, o_daterange_max_date_allowed, o_daterange_initial_visible_month, o_summary_footer_children, o_summary_footer_style, o_renderer_trigger_n_clicks

        __lc__ = LogCalc(row_data)
        __lc__.set_parameter(i_index_by_button_n_clicks, i_with_open_value)

        o_daterange_min_date_allowed = __lc__.__mainFrame__.first_record._min_date
        o_daterange_max_date_allowed = __lc__.__mainFrame__.last_record._max_date
        o_daterange_initial_visible_month = o_daterange_max_date_allowed - timedelta(days=150)
        o_daterange_min_date_allowed = o_daterange_min_date_allowed.strftime("%Y-%m-%d")
        o_daterange_max_date_allowed = o_daterange_max_date_allowed.strftime("%Y-%m-%d")
        o_daterange_initial_visible_month = o_daterange_initial_visible_month.strftime("%Y-%m-%d")

        if i_daterange_start_date or i_daterange_end_date or i_quick_search_receiver_value:
            timeframe()
        else:
            o_tradinglog_rowData = __lc__.__get_sorted_log_json__()
            o_summary_footer_children = layout.make.make_footer(__lc__)
            o_renderer_trigger_n_clicks = i_renderer_trigger_n_clicks + 1

    def save():
        if i_auto_save_n_clicks:
            __env__.dump_journal(__lc__.__mainFrame__.__get_log_json__())

    def set_index_by():
        nonlocal o_index_by_button_style, o_index_by_button_children, o_scope_by_button_style
        if i_index_by_button_n_clicks:
            o_index_by_button_style = i_index_by_button_style | styles.misc.by_taketime_on
            o_index_by_button_children = "Index\u2007by\u2007TakeTime\u2007"
        else:
            o_index_by_button_style = i_index_by_button_style | styles.misc.by_taketime_off
            o_index_by_button_children = "Index\u2007by\u2007InvestTime"
        if i_scope_by_button_n_clicks:
            o_scope_by_button_style = o_index_by_button_style

    def set_scope_by():
        nonlocal o_scope_by_button_style, o_scope_by_button_children
        if i_scope_by_button_n_clicks:
            o_scope_by_button_style = i_scope_by_button_style | i_index_by_button_style
            o_scope_by_button_children = "Scope\u2007by\u2007Index"
        else:
            o_scope_by_button_style = i_scope_by_button_style | styles.misc.by_index_off
            o_scope_by_button_children = "Scope\u2007by\u2007Both\u2007"

    def newside():
        nonlocal o_open_positions_graph_figure, o_all_positions_graph_figure, o_performance_graph_figure, o_BALANCE_children, o_drag_container_style
        (o_open_positions_graph_figure,
         o_all_positions_graph_figure,
         o_performance_graph_figure,
         o_BALANCE_children,
         o_drag_container_style) = new_side(
            i_drag_event_receiver2_value,
            i_group_by_type,
            i_group_by_short,
            i_group_by_sector,
            i_group_by_category,
            i_group_by_id,
            i_group_by_show_all,
            scope_by_attr,
            i_performance_steps_value,
            i_performance_trailing_frame_value,
            i_performance_trailing_interval_value,
            i_performance_range_value,
            "Day" in i_performance_hypothesis_per_value,
            i_drag_event_receiver_value,
            i_performance_size_slider_value,
            i_Y_trigger_,
            i_Q_trigger_,
            i_T_trigger_,
            i_C_trigger_,
            i_STATISTICS_style,
            i_BALANCE_style
        )

    try:
        # init
        if None in (__trigger__, i_tradinglog_rowData):
            set_auto_save(True)
            set_index_by()
            if i_scope_by_button_n_clicks:
                o_scope_by_button_style = i_scope_by_button_style | o_index_by_button_style
                o_scope_by_button_children = "Scope\u2007by\u2007Index"
            else:
                o_scope_by_button_style = i_scope_by_button_style | styles.misc.by_index_off
                o_scope_by_button_children = "Scope\u2007by\u2007Both\u2007"

            if __env__.startupFlushOpenTakeAmount:
                _course_call = __env__.plugin.course_call

                def course_call(row, _):
                    row.pop("TakeAmount", None)
                    row.pop("TakeCourse", None)
                    return True

                __env__.plugin.course_call = course_call
                new_table(__env__.JOURNAL_DATA)
                __env__.plugin.course_call = _course_call

            new_table(__env__.JOURNAL_DATA)

            o_backup_list_options = layout.make.make_history_list(__env__.HISTORY_KEYS_X_TIME_REVSORT)
            newside()
            o_init_done_trigger_n_clicks = o_init_done_trigger2_n_clicks = 1

        # index by
        elif __trigger__ == layout.header.index_by_button.id:
            set_index_by()
            __lc__.set_parameter(i_index_by_button_n_clicks, None)
            o_tradinglog_rowData = __lc__.__get_sorted_log_json__()
            newside()

        # main range
        elif __trigger__ in (layout.header.daterange.id, layout.quick_search_receiver.id):
            if i_daterange_start_date or i_daterange_end_date or i_quick_search_receiver_value:
                timeframe()
                newside()
                if __trigger__ == layout.quick_search_receiver.id:
                    o_tradinglog_dashGridOptions = i_tradinglog_dashGridOptions | {"quickFilterText": None}
            elif not i_daterange_end_date:
                __lc__ = __lc__.getMainFrame()
                o_tradinglog_rowData = __lc__.__get_sorted_log_json__()
                o_summary_footer_children = layout.make.make_footer(__lc__)
                o_renderer_trigger_n_clicks = i_renderer_trigger_n_clicks + 1
                newside()

        # scope by
        elif __trigger__ == layout.header.scope_by_button.id:
            set_scope_by()
            if i_daterange_start_date or i_daterange_end_date or i_quick_search_receiver_value:
                timeframe()
                newside()
            else:
                layout.make.balance.OBJ.opt__by_attr(scope_by_attr)
                layout.make.performance.OBJ.opt__by_attr(scope_by_attr)
                if i_BALANCE_style:
                    o_BALANCE_children = layout.make.balance.OBJ.get()
                elif i_STATISTICS_style:
                    o_performance_graph_figure = layout.make.performance.OBJ.get().update_layout(height=i_performance_size_slider_value)

        # calc with
        elif __trigger__ == layout.header.with_open_trigger.id:

            __lc__.set_parameter(None, i_with_open_value)
            o_tradinglog_rowTransaction = {"update": [d.data for d in __lc__.frame_deposits]}

            newside()
            o_summary_footer_children = layout.make.make_footer(__lc__)

        # auto save
        elif __trigger__ == layout.header.auto_save_button.id:
            set_auto_save(i_auto_save_n_clicks)
            save()

        # load backup
        elif __trigger__ == layout.history.history_list.id:
            save()
            new_table(__env__.HISTORY_DATA[i_backup_list_value]["data"])
            set_auto_save(False)
            newside()

        # table edit
        elif __trigger__ == layout.tradinglog.id:
            if i_tradinglog_cellValueChanged:
                o_tradinglog_rowTransaction = dict()
                added = list()
                edit_item = __lc__.edit(i_tradinglog_cellValueChanged[0])
                if edit_item.added:
                    added = edit_item.added
                if do_add_row(i_tradinglog_rowData):
                    added.append(__lc__.new_row().row_dat)
                if added:
                    o_tradinglog_rowTransaction = {"add": added, "addIndex": 0}
                save()
                o_tradinglog_rowTransaction |= {"update": edit_item.updates}
                if not edit_item.same_type:
                    o_renderer_trigger_n_clicks = i_renderer_trigger_n_clicks + 1
                if edit_item.summary_relevant:
                    o_summary_footer_children = layout.make.make_footer(__lc__)
                    newside()
                elif edit_item.id_relevant:
                    newside()

        # table edit from javascript
        elif __trigger__ == layout.edit_event_receiver.id:
            update = json.loads(i_edit_event_receiver_value)
            update["new_row"] = json.loads(update["new_row"])
            update["old_row"] = json.loads(update["old_row"])
            colid = update.get("colId")
            o_tradinglog_rowTransaction = dict()
            added = list()
            if colid:
                edit_item = __lc__.edit({"colId": colid, "data": update["new_row"], "oldValue": update["old_row"].get(colid)})
            else:
                edit_item = __lc__.update(update["new_row"], update["old_row"])
            if edit_item.added:
                added = edit_item.added
            if ((not colid) and (update["new_row"]["id"] in (0, len(__lc__.__mainFrame__) - 1))) or do_add_row(i_tradinglog_rowData):
                added.append(__lc__.new_row().row_dat)
            if added:
                o_tradinglog_rowTransaction = {"add": added, "addIndex": 0}
            o_tradinglog_rowTransaction |= {"update": edit_item.updates}
            if not edit_item.same_type:
                o_renderer_trigger_n_clicks = i_renderer_trigger_n_clicks + 1
            if edit_item.summary_relevant:
                o_summary_footer_children = layout.make.make_footer(__lc__)
                newside()
            elif edit_item.id_relevant:
                newside()
            save()

        # show balance / show statistics
        elif __trigger__ in (layout.balance.BALANCE.id, layout.statistics.STATISTICS.id):
            if i_STATISTICS_style:
                o_open_positions_graph_figure, o_all_positions_graph_figure = layout.make.positions.OBJ.get()
                o_performance_graph_figure = layout.make.performance.OBJ.get().update_layout(height=i_performance_size_slider_value)
            elif i_BALANCE_style:
                o_BALANCE_children = layout.make.balance.OBJ.get()

        # group by
        elif __trigger__ in _group_by_trigger_ids:
            layout.make.positions.OBJ.opt__group_by(_group_by(i_drag_event_receiver2_value, i_group_by_type, i_group_by_short, i_group_by_sector, i_group_by_category, i_group_by_id))
            o_open_positions_graph_figure, o_all_positions_graph_figure = layout.make.positions.OBJ.get()

        elif __trigger__ in layout.statistics.show_all.id:
            layout.make.positions.OBJ.opt__show_all(bool(i_group_by_show_all))
            o_open_positions_graph_figure, o_all_positions_graph_figure = layout.make.positions.OBJ.get()

        # performance trailing
        elif __trigger__ in (layout.statistics.performance_hypothesis_per.id, layout.statistics.performance_steps.id, layout.statistics.performance_trailing_frame.id, layout.statistics.performance_trailing_interval.id, layout.statistics.performance_range.id):
            layout.make.performance.OBJ.opt__trailing(
                timedelta(weeks=i_performance_steps_value),
                timedelta(weeks=i_performance_trailing_frame_value),
                timedelta(weeks=i_performance_trailing_interval_value),
                timedelta(weeks=i_performance_range_value),
                "Day" in i_performance_hypothesis_per_value,
            )
            if i_STATISTICS_style:
                o_performance_graph_figure = layout.make.performance.OBJ.get().update_layout(height=i_performance_size_slider_value)

        # performance graph drag
        elif __trigger__ == layout.drag_event_receiver.id:
            if i_drag_event_receiver_value:
                drag_event_receiver_ = loads(i_drag_event_receiver_value)
                order = tuple(int(i.split("-")[1]) for i in drag_event_receiver_["target_children"])
                order = tuple(order.index(i) + 1 for i in range(1, __env__.nStatisticsDrag + 1))
                layout.make.performance.OBJ.opt__order(order)
                o_performance_graph_figure = layout.make.performance.OBJ.get().update_layout(height=i_performance_size_slider_value)

        # performance graph size
        elif __trigger__ == layout.statistics.performance_size_slider.id:
            o_performance_graph_figure = go.Figure(i_performance_graph_figure).update_layout(height=i_performance_size_slider_value)
            o_drag_container_style = layout.statistics.drag_container.style | {"height": "%dpx" % i_performance_size_slider_value}

        # pop graph size
        elif __trigger__ == layout.statistics.pop_size_slider.id:
            o_pop_graph_figure = go.Figure(i_pop_graph_figure)
            o_pop_graph_figure.update_layout(height=i_pop_size_slider_value)

        # pop open positions graph
        elif __trigger__ == layout.statistics.pop_open_positions.id:
            o_pop_graph_figure = go.Figure(i_open_positions_graph_figure)
            o_pop_graph_figure.update_layout(height=i_pop_size_slider_value)
            o_statistics_pop_trigger_n_clicks = i_statistics_pop_trigger_n_clicks + 1
            o_pop_title_children = "Open Positions"

        # pop all positions graph
        elif __trigger__ == layout.statistics.pop_all_positions.id:
            o_pop_graph_figure = go.Figure(i_all_positions_graph_figure)
            o_pop_graph_figure.update_layout(height=i_pop_size_slider_value)
            o_statistics_pop_trigger_n_clicks = i_statistics_pop_trigger_n_clicks + 1
            o_pop_title_children = "Positions of Alltime"

        # pop performance graph
        elif __trigger__ == layout.statistics.pop_performance.id:
            o_pop_graph_figure = go.Figure(i_performance_graph_figure)
            o_pop_graph_figure.update_layout(height=i_pop_size_slider_value)
            o_statistics_pop_trigger_n_clicks = i_statistics_pop_trigger_n_clicks + 1
            o_pop_title_children = "Performance"

        # balance scopes
        elif __trigger__ in (layout.balance.Y_trigger_.id, layout.balance.Q_trigger_.id, layout.balance.T_trigger_.id, layout.balance.C_trigger_.id):
            layout.make.balance.OBJ.opt__visible(i_Y_trigger_, i_Q_trigger_, i_T_trigger_, i_C_trigger_)
            o_BALANCE_children = layout.make.balance.OBJ.get()

    except Exception as e:
        print_exception(e)
        print(__ini__.logtags.error, e, flush=True, file=stderr)
        o_summary_footer_style = s_summary_error
        o_tradinglog_rowTransaction = no_update
    else:
        o_summary_footer_style = s_summary_error_reset | __env__.get_footer_live_signal()

    return _return()
