import dash_ag_grid as dag

import __env__
import __ini__.cmdl
from config.functional import log_columns

_default_col_def = {
    "editable": True,
    "filter": "agNumberColumnFilter",
    "filterParams": {"buttons": ["clear"]},
    "cellEditorParams": {"color": "white"}
}

_asset_ids = [
    _default_col_def | {
        "field": "Name",
        "filter": "agTextColumnFilter",
        "filterParams": {"buttons": ["clear"]},
        "headerTooltip": "{Name}"
    } | log_columns.Name,
    _default_col_def | {
        "field": "Symbol",
        "filter": "agTextColumnFilter",
        "filterParams": {"buttons": ["clear"]},
        "headerTooltip": "{Symbol}",
    } | log_columns.Symbol,
    _default_col_def | {
        "field": "ISIN",
        "filter": "agTextColumnFilter",
        "filterParams": {"buttons": ["clear"]},
        "headerTooltip": "{ISIN}",
    } | log_columns.ISIN,
    _default_col_def | {
        "field": "Short",
        "cellDataType": "boolean",
        "filterParams": {"buttons": ["clear"]},
        "headerTooltip": "{Short}",
    } | log_columns.Short,
    _default_col_def | {
        "field": "Type",
        "filter": "agTextColumnFilter",
        "filterParams": {"buttons": ["clear"]},
        "headerTooltip": "{Type}",
    } | log_columns.Type,
    _default_col_def | {
        "field": "Category",
        "filter": "agTextColumnFilter",
        "filterParams": {"buttons": ["clear"]},
        "headerTooltip": "{Category}",
    } | log_columns.Category,
    _default_col_def | {
        "field": "Sector",
        "filter": "agTextColumnFilter",
        "filterParams": {"buttons": ["clear"]},
        "headerTooltip": "{Sector}",
    } | log_columns.Sector,
    _default_col_def | {
        "field": "Rating",
        "type": "rightAligned",
        "cellDataType": "number",
        "filterParams": {
            "buttons": ["clear"],
            "defaultOption": "greaterThan",
            "filterOptions": ["greaterThan", "lessThan", "greaterThanOrEqual", "lessThanOrEqual", "inRange"],
        },
        "headerTooltip": "{Rating} = 1 ... 9"
    } | log_columns.Rating,
    _default_col_def | {
        "field": "n",
        "type": "rightAligned",
        "cellDataType": "number",
        "filterParams": {
            "buttons": ["clear"],
            "defaultOption": "greaterThan",
            "filterOptions": ["greaterThan", "lessThan", "greaterThanOrEqual", "lessThanOrEqual", "inRange"],
        },
        "headerTooltip": "{n}"
    } | log_columns.N,
]


_asset_ids1_ = [None] * len(__env__.logColOrderAssetId)

_asset_ids2_ = [None] * len(__env__.logColOrderAssetId)

for i, o in enumerate(__env__.logColOrderAssetId):
    if o < 0:
        _asset_ids1_[abs(o) - 1] = _asset_ids[i] | {"pinned": "left"}
    elif o:
        _asset_ids2_[o - 1] = _asset_ids[i]

for _l in (_asset_ids1_, _asset_ids2_):
    try:
        while True:
            _l.remove(None)
    except ValueError:
        pass

_notes_ = [None] * len(__env__.logColOrderNote)

for i, o in enumerate(__env__.logColOrderNote[:-1], 1):
    if o:
        _notes_[o - 1] = _asset_ids[i]

_note = _default_col_def | {
    "field": "Note",
    "filter": "agTextColumnFilter",
} | log_columns.Note

_notes_[__env__.logColOrderNote[-1] - 1] = _note

try:
    while True:
        _notes_.remove(None)
except ValueError:
    pass

if len(_notes_) == 1:
    _note_ = _note
else:
    _note_ = _default_col_def | {
        "headerName": "Notes",
        "children": _notes_
    }

_columns_ = [
    _default_col_def | {
        "headerName": "Asset",
        "children": [
            _default_col_def | {
                "field": "cat",
                "hide": not __ini__.cmdl.FLAGS.debug,
                "width": 50
            },
            _default_col_def | {
                "field": "id",
                "hide": not __ini__.cmdl.FLAGS.debug,
                "width": 50
            },
            _default_col_def | {
                "field": "mark",
                "hide": not __ini__.cmdl.FLAGS.debug,
                "width": 50
            },
        ] + _asset_ids1_
    },
    _default_col_def | {
        "headerName": "",
        "children": _asset_ids2_
    },
    _default_col_def | {
        "headerName": "Invest",
        "children": [
            _default_col_def | {
                "field": "InvestTime",
                "headerName": "Time",
                "filter": "agDateColumnFilter",
                "comparator": {"function": "dateOrderComparator"},
                "filterParams": {
                    "comparator": {"function": "dateFilterComparator"},
                    "buttons": ["clear"],
                    "defaultOption": "greaterThan",
                    "filterOptions": ["equals", "greaterThan", "lessThan", "greaterThanOrEqual", "lessThanOrEqual", "inRange"],
                },
                "type": "rightAligned",
                "headerTooltip": "{InvestTime}"
            } | log_columns.InvestTime,
            _default_col_def | {
                "field": "InvestAmount",
                "headerName": "Amount",
                "type": "rightAligned",
                "filterParams": {
                    "buttons": ["clear"],
                    "defaultOption": "greaterThan",
                    "filterOptions": ["greaterThan", "lessThan", "greaterThanOrEqual", "lessThanOrEqual", "inRange"],
                },
                "headerTooltip": "{InvestAmount}"
            } | log_columns.InvestAmount,
            _default_col_def | {
                "field": "InvestCourse",
                "headerName": "Course",
                "type": "rightAligned",
                "editable": True,
                "filterParams": {
                    "buttons": ["clear"],
                    "defaultOption": "greaterThan",
                    "filterOptions": ["greaterThan", "lessThan", "greaterThanOrEqual", "lessThanOrEqual", "inRange"],
                },
                "headerTooltip": "{InvestCourse}"
            } | log_columns.InvestCourse,
        ]
    },
    _default_col_def | {
        "headerName": "Take",
        "children": [
            _default_col_def | {
                "field": "TakeTime",
                "headerName": "Time",
                "filter": "agDateColumnFilter",
                "comparator": {"function": "dateOrderComparator"},
                "filterParams": {
                    "comparator": {"function": "dateFilterComparator"},
                    "buttons": ["clear"],
                    "defaultOption": "greaterThan",
                    "filterOptions": ["equals", "greaterThan", "lessThan", "greaterThanOrEqual", "lessThanOrEqual", "inRange"],
                },
                "type": "rightAligned",
                "headerTooltip": "{TakeTime}"
            } | log_columns.TakeTime,
            _default_col_def | {
                "field": "TakeAmount",
                "headerName": "Amount",
                "type": "rightAligned",
                "filterParams": {
                    "buttons": ["clear"],
                    "defaultOption": "greaterThan",
                    "filterOptions": ["greaterThan", "lessThan", "greaterThanOrEqual", "lessThanOrEqual", "inRange"],
                },
                "headerTooltip": "{TakeAmount}"
            } | log_columns.TakeAmount,
            _default_col_def | {
                "field": "TakeCourse",
                "headerName": "Course",
                "type": "rightAligned",
                "editable": True,
                "filterParams": {
                    "buttons": ["clear"],
                    "defaultOption": "greaterThan",
                    "filterOptions": ["greaterThan", "lessThan", "greaterThanOrEqual", "lessThanOrEqual", "inRange"],
                },
                "headerTooltip": "{TakeCourse}"
            } | log_columns.TakeCourse,
        ]
    },
    _default_col_def | {
        "field": "ITC",
        "headerName": "+ITC",
        "type": "rightAligned",
        "filterParams": {
            "buttons": ["clear"],
            "defaultOption": "greaterThan",
            "filterOptions": ["greaterThan", "lessThan", "greaterThanOrEqual", "lessThanOrEqual", "inRange"],
        },
        "headerTooltip": "{ITC} = Interests, Taxes, Costs ..."
    } | log_columns.Itc,
    _default_col_def | {
        "headerName": "Result",
        "children": [
            _default_col_def | {
                "field": "Performance",
                "type": "rightAligned",
                "editable": False,
                "cellDataType": "percentage",
                "filterParams": {
                    "buttons": ["clear"],
                    "defaultOption": "greaterThan",
                    "filterOptions": ["greaterThan", "lessThan", "greaterThanOrEqual", "lessThanOrEqual", "inRange"],
                },
                "headerTooltip": "{Performance}"
            } | log_columns.Performance,
            _default_col_def | {
                "field": "Profit",
                "type": "rightAligned",
                "editable": False,
                "cellDataType": "prefixed",
                "filterParams": {
                    "buttons": ["clear"],
                    "defaultOption": "greaterThan",
                    "filterOptions": ["greaterThan", "lessThan", "greaterThanOrEqual", "lessThanOrEqual", "inRange"],
                },
                "headerTooltip": "{Profit}"
            } | log_columns.Profit,
            _default_col_def | {
                "field": "Dividend",
                "type": "rightAligned",
                "editable": False,
                "cellDataType": "grouped",
                "filterParams": {
                    "buttons": ["clear"],
                    "defaultOption": "greaterThan",
                    "filterOptions": ["greaterThan", "lessThan", "greaterThanOrEqual", "lessThanOrEqual", "inRange"],
                },
                "headerTooltip": "{Dividend}"
            } | log_columns.Dividend,
        ]
    },
    _note_,
    _default_col_def | {
        "field": "HoldTime",
        "headerName": "Hold Time",
        "type": "rightAligned",
        "editable": False,
        "cellDataType": "timedelta",
        "filter": "agNumberColumnFilter",
        "filterParams": {
            "allowedCharPattern": "\\d\\|\\., ",
            "filterPlaceholder": "y | m | d | H , M",
            "numberParser": {"function": "timedeltaParser(params)"},
            "numberFormatter": {"function": "timedeltaFormatter(params)"},
            "buttons": ["clear"],
            "defaultOption": "greaterThan",
            "filterOptions": ["greaterThan", "lessThan", "greaterThanOrEqual", "lessThanOrEqual", "inRange"],
        },
        "valueFormatter": {"function": "timedeltaFormatter(params.value)"},
        "headerTooltip": "{HoldTime} = y | m | d | H , M"
    } | log_columns.HoldTime,
    _default_col_def | {
        "headerName": "Hypotheses",
        "children": [
            _default_col_def | {
                "field": "Performance/Day",
                "type": "rightAligned",
                "editable": False,
                "cellDataType": "percentage3",
                "filterParams": {
                    "buttons": ["clear"],
                    "defaultOption": "greaterThan",
                    "filterOptions": ["greaterThan", "lessThan", "greaterThanOrEqual", "lessThanOrEqual", "inRange"],
                },
                "headerTooltip": "{Performance/Day} = Performance / (rounded 24h or 1)"
            } | log_columns.PerformanceDay,
            _default_col_def | {
                "field": "Profit/Day",
                "type": "rightAligned",
                "editable": False,
                "cellDataType": "prefixed3",
                "filterParams": {
                    "buttons": ["clear"],
                    "defaultOption": "greaterThan",
                    "filterOptions": ["greaterThan", "lessThan", "greaterThanOrEqual", "lessThanOrEqual", "inRange"],
                },
                "headerTooltip": "{Profit/Day} = Profit / (rounded 24h or 1)"
            } | log_columns.ProfitDay,
            _default_col_def | {
                "field": "Performance/Year",
                "type": "rightAligned",
                "editable": False,
                "cellDataType": "percentage3",
                "filterParams": {
                    "buttons": ["clear"],
                    "defaultOption": "greaterThan",
                    "filterOptions": ["greaterThan", "lessThan", "greaterThanOrEqual", "lessThanOrEqual", "inRange"],
                },
                "headerTooltip": "{Performance/Year} = {Performance/Day} * 365.25"
            } | log_columns.PerformanceDay,
            _default_col_def | {
                "field": "Profit/Year",
                "type": "rightAligned",
                "editable": False,
                "cellDataType": "prefixed3",
                "filterParams": {
                    "buttons": ["clear"],
                    "defaultOption": "greaterThan",
                    "filterOptions": ["greaterThan", "lessThan", "greaterThanOrEqual", "lessThanOrEqual", "inRange"],
                },
                "headerTooltip": "{Profit/Year} = {Profit/Day} * 365.25"
            } | log_columns.ProfitDay,
        ]
    },
]

columnDefs = [_columns_[0]] + ([None] * len(__env__.logColOrder))

for i, o in enumerate(__env__.logColOrder, 1):
    columnDefs[o] = _columns_[i]

del _columns_

_dashGridOptions = {
    "dataTypeDefinitions": log_columns.dataTypeDefinitions,
    "tooltipShowDelay": 0,
    # xxx (does not seem to work when the grid is edited with row transaction)
    # "undoRedoCellEditing": True,
    # "undoRedoCellEditingLimit": 20,
    "tabToNextCell": {"function": "tabToNextCell(params)"}
}

tradinglog = dag.AgGrid(
    id="logElement",
    columnDefs=columnDefs,
    dashGridOptions=_dashGridOptions,
    getRowId="params.data.id",
    className=__env__.color_theme.table_theme + " ag-alt-colors",
    dangerously_allow_code=True,
    style={
        "height": "100%",
        "width": "100%",
        "fontSize": "13px"
    },
)
