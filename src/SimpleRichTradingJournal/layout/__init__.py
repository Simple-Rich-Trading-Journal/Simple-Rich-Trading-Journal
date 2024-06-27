from dash import html, dcc

import __env__
from config import styles
from . import header, history, statistics, balance, autocomplet, note, about, exiting, modal
from . import make
from .log import tradinglog

LAYOUT = html.Div(
    [
        html.Header(
            [
                html.Meta(name="viewport", content="width=device-width, initial-scale=1.0"),
            ]
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.Div(
                                            html.Div(
                                                [
                                                    header.scopes_check,
                                                    html.Div(header.index_by_button),
                                                    header.search_input,
                                                    html.Div([
                                                        header.daterange,
                                                        header.scope_by_button,
                                                    ], style={"border": "1px solid " + __env__.color_theme.table_sep, "borderRadius": "20px", "paddingLeft": "10px"}),
                                                    html.Div(style={"display": "inline-block", "width": "1%"}),
                                                    html.Div(header.with_open_button),
                                                    header.with_open_trigger,
                                                ],
                                                style={
                                                    "display": "flex"
                                                }
                                            ),
                                            style={
                                                "width": "100%",
                                                "display": "inline-block"
                                            }
                                        ),
                                        html.Div(
                                            [
                                                html.Div(
                                                    [
                                                        header.auto_save_button,
                                                        header.update_interval_button,
                                                        header.update_interval,
                                                        header.update_interval_trigger,
                                                    ],
                                                    style={
                                                        "textAlign": "end",
                                                    }
                                                ),
                                            ],
                                            style={
                                                "position": "absolute",
                                                "top": 0,
                                                "right": 0,
                                                "textAlign": "end",
                                            }
                                        ),
                                    ],
                                    style={
                                              "width": "100%",
                                              "display": "flex"
                                          } | styles.misc.header
                                ),
                            ],
                            id="gridR1"
                        ),
                        html.Div(
                            [
                                c_1 := html.Div(
                                    [
                                        tradinglog,
                                    ],
                                    id="gridC1",
                                    className="col-div col-div-flex border-div",
                                    style={
                                        "width": __env__.c1Width,
                                        "height": "100%"
                                    }
                                ),
                                split_handle := html.Div(
                                    id="gridSplitter",
                                    style={
                                              "height": "inherit",
                                          } | (styles.misc.balance_split_handle if __env__.sideInitBalance else styles.misc.statistics_split_handle),
                                    className="noselect"
                                ),
                                c_2 := html.Div(
                                    [
                                        statistics.STATISTICS,
                                        balance.BALANCE
                                    ],
                                    id="gridC2",
                                    className="col-div col-div-flex border-div",
                                    style={
                                        "width": __env__.c2Width,
                                        "height": "100%",
                                    }
                                )
                            ],
                            id="gridR2",
                            style={
                                "display": "flex"
                            }
                        )
                    ]
                ),
            ],
            style={
                "backgroundColor": __env__.color_theme.table_bg_main
            }
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.Div(style={"display": "inline-block", "width": "1%"}),
                        exiting.exit_button,
                        about.about_button,
                        header.history_button,
                        header.reset_columns_button,
                        header.import_button,
                        header.export_button,
                    ],
                    style={
                        "width": "50%",
                        "textAlign": "left",
                        "display": "inline-block"
                    }
                ),
                html.Div(
                    [
                        header.balance_button,
                        header.statistics_button,
                    ],
                    style={
                        "width": "50%",
                        "textAlign": "right",
                        "display": "inline-block"
                    }
                ),
            ],
            id="bottomBar",
            style={
                "position": "absolute",
                "bottom": __env__.bottomBarDistanceBottom,
                "right": __env__.bottomBarDistanceRight,
                "width": "100%",
                "zIndex": 1,
                "display": "none"
            }
        ),
        summary_footer := html.Div(
            id="gridR3",
            style={
                "width": "100%",
                "position": "absolute",
                "bottom": 0,
            } | styles.misc.summary_footer
        ),
        (html.Div(
            __env__.PROFILE,
            style={
                "position": "absolute",
                "bottom": 0,
                "left": 0,
                "fontSize": 12,
                "borderTop": "2px outset",
                "borderRight": "2px outset",
                "paddingLeft": 3,
                "paddingRight": 4,
            } | styles.misc.summary_footer | {"backgroundColor": ""}
        ) if __env__.PROFILE else html.Div()),
        renderer_trigger := html.Div(id="renderer_trigger_", n_clicks=0),
        c2Hide_trigger := html.Div(id="c2Hide_trigger_", n_clicks=0),
        drag_event_receiver := dcc.Input(type="text", id="dragEventReceiver", style={'visibility': 'hidden', "display": "none"}),
        drag_event_receiver2 := dcc.Input(type="text", id="dragEventReceiver2", style={'visibility': 'hidden', "display": "none"}),
        edit_event_receiver := dcc.Input(type="text", id="editEventReceiver", style={'visibility': 'hidden', "display": "none"}),
        quick_search_receiver := dcc.Input(type="text", id="quickSearchReceiver", style={'visibility': 'hidden', "display": "none"}),
        history.MODAL,
        statistics.POP,
        init_trigger := html.Div(id="init_trigger_"),
        init_done_trigger := html.Div(id="init_done_trigger_"),
        init_done_trigger2 := html.Div(id="init_done_trigger2_"),
        colstate_done_trigger := html.Div(id="colstate_done_trigger_"),
        esc_trigger := dcc.Input(id="esc_trigger"),
        statistics_pop_trigger := html.Div(id="statistics_pop_trigger_", n_clicks=0),
        exiting_modal_trigger := html.Div(id="exiting_modal_trigger_", n_clicks=0),
        autocomplet.COMPONENTS,
        note.COMPONENTS,
        about.COMPONENTS,
        exiting.COMPONENTS,
        modal.COMPONENTS,
        html.Div(style={"position": "absolute", "zIndex": -1, "height": "100%", "width": "100%", "backgroundColor": __env__.color_theme.table_bg_header})
    ],
)
