from dash import html, dcc

import __env__
from config import styles
from config.functional import performance_trailing


POP = html.Div([
    html.Div([
        html.Div([
            pop_title := html.H4(id="pop_title_", style={"display": "inline-block", "width": "15%"}),
            html.Div(
                pop_size_slider := dcc.Slider(**styles.figures.size_slider_kwargs_pop, id="pop_size_slider_"),
                style={"display": "inline-block", "width": "85%"}
            )
        ],
            style={"width": "100%", "display": "flex"}
        )
    ]),
    html.Div([
        pop_graph := dcc.Graph(id="pop_graph_")
    ])
],
    id="pop_modal",
    style={
        "position": "absolute",
        "zIndex": -2,
        "width": "100%",
        "height": "100%",
        "top": 0,
        "bottom": 0,
        "left": 0,
        "backgroundColor": __env__.color_theme.table_bg_2,
        "color": __env__.color_theme.table_fg_main,
        "padding": 10,
        "borderRadius": 10,
        "overflow": "scroll"
    }
)

_dragcontainer = list()
_dragcontainer_ids = list()
for i in __env__.statisticsPerformanceOrder:
    if i not in _dragcontainer_ids:
        _dragcontainer_ids.append(i)
        _dragcontainer.append(
            html.Div(
                [
                    html.Div("☰", style={"border": "1px solid", "width": "5240%", "height": "100%"})
                ],
                id=f"drag_component-{i}",
                style={
                    "height": f"calc(100% / {__env__.nStatisticsDrag})",
                    "cursor": "row-resize",
                    "fontSize": "18px",
                    "borderRight": "1px solid",
                    "width": "100%",
                }
            )
        )

_dragcontainer2 = [None] * len(__env__.statisticsGroupDefault)
_dragcontainer2_unselect = list()
_dragcontainer2_opts = (
                           ({"label": "\u2007\u2007L/S", "value": "Short"}, __env__.logColWidths[4]),
                           ({"label": "\u2007\u2007Type", "value": "Type"}, __env__.logColWidths[3]),
                           ({"label": "\u2007\u2007Sector", "value": "Sector"}, __env__.logColWidths[5]),
                           ({"label": "\u2007\u2007Category", "value": "Category"}, __env__.logColWidths[6]),
                       ) + (
                           ({"label": "\u2007\u2007Symbol", "value": "Symbol"}, 1)
                           if __env__.statisticsIdBySymbol else
                           ({"label": "\u2007\u2007Name", "value": "Name"}, 1),
                       )
_group_by_checks = list()

for i, p in zip(_dragcontainer2_opts, __env__.statisticsGroupDefault):
    def rec(selected):
        check = dcc.Checklist(
            [i[0]],
            value=([i[0]["value"]] if selected else []),
            inline=True,
            id=f"group_by-{i[0]['value']}",
            style={
                "cursor": "row-resize",
            },
            labelStyle={
                "cursor": "row-resize",
            },
        )
        _group_by_checks.append(check)
        return html.Div(
            check,
            id=f"drag_component-{i[0]['value']}",
            style={
                "display": ("" if i[1] else "none"),
                "cursor": "row-resize",
                "border": "1px solid",
                "padding": 3,
                "margin": 1
            }
        ), i[0]['value']


    if p:
        _dragcontainer2[p - 1] = rec(True)
    else:
        _dragcontainer2_unselect.append(rec(False))

try:
    while True:
        _dragcontainer2.remove(None)
except ValueError:
    pass

_dragcontainer2 = _dragcontainer2[:-1] + _dragcontainer2_unselect + _dragcontainer2[-1:]
_dragcontainer2.reverse()

_group_by_default_order = list(i[1] for i in _dragcontainer2)
_group_by_default_order.reverse()

group_by_settings = html.Div(
    [
        drag_container2 := html.Div(
            [i[0] for i in _dragcontainer2],
            id="dragContainer2",
            style={
                "border": "1px solid",
                "padding": 3,
            }
        ),
        html.Div(
            show_all := dcc.Checklist(
                [{"label": "\u2007\u2007show all", "value": True}],
                value=[not __env__.statisticsUseSunMaxDepth],
                id="statisticsUseSunMaxDepth_"
            ),
            style={
                "padding": 6,
                "borderBottom": "1px solid",
            }
        )
    ],
    id="groupBySettings",
    style={
        "position": "absolute",
        "zIndex": -3,
        "backgroundColor": __env__.color_theme.table_bg_main + "cc",
        "margin": 10,
        "fontSize": 13
    }
)


framing_settings = html.Div(
    [
        html.Div(
            [
                html.Div(
                    "Main Scope",
                    style={
                        "position": "absolute",
                        "marginTop": -16
                    }
                ),
                performance_range := dcc.Slider(
                    marks=performance_trailing.performance_range,
                    step=None,
                    value=performance_trailing.performance_range_default,
                    id="performance_range_",
                ),
            ],
            style={
                "padding": 10,
                "borderBottom": "1px solid",
                "marginTop": 8
            }
        ),
        html.Div(
            [
                html.Div(
                    "Calculating block frame",
                    style={
                        "position": "absolute",
                        "marginTop": -16
                    }
                ),
                performance_steps := dcc.Slider(
                    marks=performance_trailing.performance_steps,
                    step=None,
                    value=performance_trailing.performance_steps_default,
                    id="performance_steps_",
                ),
            ],
            style={
                "padding": 10,
                "borderBottom": "1px solid",
                "marginTop": 8
            }
        ),
        html.Div(
            [
                html.Div(
                    "Trailing (~) calculation block frame",
                    style={
                        "position": "absolute",
                        "marginTop": -16
                    }
                ),
                performance_trailing_frame := dcc.Slider(
                    marks=performance_trailing.performance_frame,
                    step=None,
                    value=performance_trailing.performance_frame_default,
                    id="performance_trailing_frame_",
                ),
            ],
            style={
                "padding": 10,
                "borderBottom": "1px solid",
                "marginTop": 8
            }
        ),
        html.Div(
            [
                html.Div(
                    "Trailing (~) calculation block interval",
                    style={
                        "position": "absolute",
                        "marginTop": -16
                    }
                ),
                performance_trailing_interval := dcc.Slider(
                    marks=performance_trailing.performance_interval,
                    step=None,
                    value=performance_trailing.performance_interval_default,
                    id="performance_trailing_interval_",
                ),
            ],
            style={
                "padding": 10,
                "borderBottom": "1px solid",
                "marginTop": 8
            }
        ),
        html.Div(
            [
                performance_hypothesis_per := dcc.RadioItems(
                    ["\u2007Hypothesis/Day\u2007\u2007", "\u2007Hypothesis/Year\u2007\u2007"],
                    value=("\u2007Hypothesis/Day\u2007\u2007" if __env__.statisticsHypothesisPerDay else "\u2007Hypothesis/Year\u2007\u2007"),
                    inline=True,
                    id="performance_hypothesis_per_",
                ),
            ],
            style={
                "padding": 10,
                "borderBottom": "1px solid",
                "marginTop": 8
            }
        ),
    ],
    id="framing_settings_",
    style={
        "position": "absolute",
        "zIndex": -3,
        "backgroundColor": __env__.color_theme.table_bg_main + "cc",
        "margin": 10,
        "fontSize": 13,
        "width": "var(--handle-xi)"
    },
)


STATISTICS = html.Div([
    html.Div([
        html.H4("Statistics", style={"display": "inline-block"}),
        html.Div(
            [
                html.Div(
                    [
                        group_by_button := html.Button(
                            "Group by ...",
                            id="group_by_button_",
                            n_clicks=0,
                            style={
                                      "display": "inline-block",
                                      "margin": "7px",
                                      "fontSize": "13px",
                                      "paddingLeft": "10px",
                                      "paddingRight": "10px",
                                  } | styles.misc.group_by_options_off
                        ),
                        framing_button := html.Button(
                            "Framing…",
                            id="framing_button_",
                            style={
                                      "display": "inline-block",
                                      "margin": "7px",
                                      "fontSize": "13px",
                                      "paddingLeft": "10px",
                                      "paddingRight": "10px",
                                  } | styles.misc.framing_options_off
                        ),
                        html.Div(
                            html.Div(
                                performance_size_slider := dcc.Slider(
                                    **styles.figures.size_slider_kwargs_performance,
                                    id="performance_size_slider_",
                                    className="nopadding"
                                ),
                                style={
                                          "padding": "0px 10px",
                                          "paddingBottom": "5px",
                                          "width": 450
                                      } | styles.misc.performance_size
                            ),
                            style={
                                "display": "inline-block"
                            }
                        )
                    ],
                    style={
                        "whiteSpace": "nowrap"
                    }
                )
            ],
            style={
                "overflow": "hidden",
                "position": "absolute",
                "zIndex": 1,
                "display": "inline-block"
            },
            className="fill-available-width"
        ),
    ]),
    group_by_settings,
    framing_settings,
    html.Div(
        [
            html.Div(
                [
                    pop_open_positions := html.Div(
                        [
                            html.Span("⇱\u2007", style={"display": "inline-block", "fontSize": "16px"}),
                            html.H6("Open Positions", style={"display": "inline-block"}),
                        ],
                        id="pop_open_positions_",
                        n_clicks=0,
                        style={"cursor": "pointer"}
                    ),
                    open_positions_graph := dcc.Graph("open_positions_graph_", config={'displaylogo': False}),
                ],
                style={
                    "width": "100%",
                    "padding": "10px"
                }
            ),
            html.Div(
                [
                    pop_all_positions := html.Div(
                        [
                            html.Span("⇱\u2007", style={"display": "inline-block", "fontSize": "16px"}),
                            html.H6("Positions of Alltime", style={"display": "inline-block"}),
                        ],
                        id="pop_all_positions_",
                        n_clicks=0,
                        style={"cursor": "pointer"}
                    ),
                    all_positions_graph := dcc.Graph("all_positions_graph_", config={'displaylogo': False}),
                ],
                style={
                    "width": "100%",
                    "padding": "10px"
                }
            ),
            html.Div(
                [
                    pop_performance := html.Div(
                        [
                            html.Span("⇱\u2007", style={"display": "inline-block", "fontSize": "16px"}),
                            html.H6("Performance", style={"display": "inline-block"}),
                        ],
                        id="pop_performance_",
                        n_clicks=0,
                        style={"cursor": "pointer"}
                    ),
                    html.Div([
                        drag_container := html.Div(
                            _dragcontainer,
                            id="dragContainer",
                            style={
                                "display": "inline-block",
                                "width": "2%",
                                "height": "%dpx" % styles.figures.size_slider_kwargs_performance["value"]
                            }
                        ),
                        html.Div(
                            performance_graph := dcc.Graph("performance_graph_", config={'displaylogo': False}),
                            style={
                                "display": "inline-block",
                                "width": "98%"
                            }
                        )
                    ],
                        style={"display": "flex"}
                    )
                ],
                style={
                    "width": "100%"
                }
            ),
        ]
    ),
],
    id="statistics_",
    style={
        "height": "100%",
        "overflowY": "scroll",
        "overflowX": "hidden",
        "display": ("" if __env__.sideInitStatisticValue else "none")
    }
)
