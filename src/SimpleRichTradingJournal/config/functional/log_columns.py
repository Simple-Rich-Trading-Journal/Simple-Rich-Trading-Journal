import __env__
from config.styles.log import *


dataTypeDefinitions = {
    'percentage': {
        'extendsDataType': 'number',
        'baseDataType': 'number',
        "valueFormatter": {"function": "params.value == null ? '' :  d3.format('+,.2%')(params.value)"},
        "columnTypes": "rightAligned",
        "appendColumnTypes": True
    },
    'percentage3': {
        'extendsDataType': 'number',
        'baseDataType': 'number',
        "valueFormatter": {"function": "params.value == null ? '' :  d3.format('+,.3%')(params.value)"},
        "columnTypes": "rightAligned",
        "appendColumnTypes": True
    },
    'prefixed': {
        'extendsDataType': 'number',
        'baseDataType': 'number',
        "valueFormatter": {"function": "params.value == null ? '' :  d3.format('+,.2f')(params.value)"},
        "columnTypes": "rightAligned",
        "appendColumnTypes": True
    },
    'prefixed3': {
        'extendsDataType': 'number',
        'baseDataType': 'number',
        "valueFormatter": {"function": "params.value == null ? '' :  d3.format('+,.3f')(params.value)"},
        "columnTypes": "rightAligned",
        "appendColumnTypes": True
    },
    'grouped': {
        'extendsDataType': 'number',
        'baseDataType': 'number',
        "valueFormatter": {"function": "params.value == null ? '' :  d3.format(',.2f')(params.value)"},
        "columnTypes": "rightAligned",
        "appendColumnTypes": True
    },
    'timedelta': {
        'extendsDataType': 'number',
        'baseDataType': 'number',
        "columnTypes": "rightAligned",
        "appendColumnTypes": True
    },
}


_calcCell = {
    "valueFormatter": {"function": "params.value == null ? '' :  d3.format(',.2f')(params.value)"},
    "valueParser": {"function": "calc(params.newValue)"},
}


Name = {
    'cellStyle': {
        "styleConditions": [
            {
                "condition": "params.data.cat == ''",
                "style": name_undefined,
            },
            {
                "condition": "params.data.cat == 'd' && params.data.Note",
                "style": name_DEPOSIT_tag | name_has_note,
            },
            {
                "condition": "params.data.cat == 'p' && params.data.Note",
                "style": name_PAYOUT_tag | name_has_note,
            },
            {
                "condition": "params.data.cat == 'i' && params.data.Note",
                "style": name_ITC_tag | name_has_note,
            },
            {
                "condition": "params.data.cat == 'd'",
                "style": name_DEPOSIT_tag,
            },
            {
                "condition": "params.data.cat == 'p'",
                "style": name_PAYOUT_tag,
            },
            {
                "condition": "params.data.cat == 'i'",
                "style": name_ITC_tag,
            },
            {
                "condition": "params.data.cat == 'v' && params.data.Note",
                "style": name_dividend | name_has_note,
            },
            {
                "condition": "params.data.cat == 'v'",
                "style": name_dividend,
            },
            {
                "condition": "params.data.cat == 'to' && params.data.Note && params.data.Dividend",
                "style": name_opentrade | name_has_note | name_has_dividend,
            },
            {
                "condition": "params.data.cat == 'to'  && params.data.Dividend",
                "style": name_opentrade | name_has_dividend,
            },
            {
                "condition": "params.data.cat == 'to' && params.data.Note",
                "style": name_opentrade | name_has_note,
            },
            {
                "condition": "params.data.cat == 'to'",
                "style": name_opentrade,
            },
            {
                "condition": "params.data.Note",
                "style": name_has_note,
            },
            {
                "condition": "params.data.Dividend",
                "style": name_has_dividend,
            },
            {
                "condition": "params.data.cat == 'tf'",
                "style": name_finalized_trade,
            },
        ],
        "defaultStyle": name_undefined,
    },
    "width": __env__.logColWidths[0],
    "hide": not __env__.logColWidths[0]
}

Name["cellStyle"]["styleConditions"] = [
    {
        "condition": "params.data.mark == 1 && " + sc["condition"],
        "style": sc["style"] | name_row_mark
    } for sc in Name["cellStyle"]["styleConditions"]
] + Name["cellStyle"]["styleConditions"]

Symbol = {
    'cellStyle': {} | symbol,
    "width": __env__.logColWidths[1],
    "hide": not __env__.logColWidths[1]
}

ISIN = {
    'cellStyle': {} | isin,
    "width": __env__.logColWidths[2],
    "hide": not __env__.logColWidths[2]
}

Type = {
    'cellStyle': {} | type,
    "width": __env__.logColWidths[3],
    "hide": not __env__.logColWidths[3]
}

Short = {
    'cellStyle': {} | short,
    "width": __env__.logColWidths[4],
    "hide": not __env__.logColWidths[4]
}

Sector = {
    'cellStyle': {} | sector,
    "width": __env__.logColWidths[5],
    "hide": not __env__.logColWidths[5]
}

Category = {
    'cellStyle': {} | sector,
    "width": __env__.logColWidths[6],
    "hide": not __env__.logColWidths[6]
}

Rating = {
    'cellStyle': {
        "styleConditions": [
            {
                "condition": "params.value > 8",
                "style": rating | {"backgroundColor": __env__.color_theme.rating_scale[8]},
            },
            {
                "condition": "params.value > 7",
                "style": rating | {"backgroundColor": __env__.color_theme.rating_scale[7]},
            },
            {
                "condition": "params.value > 6",
                "style": rating | {"backgroundColor": __env__.color_theme.rating_scale[6]},
            },
            {
                "condition": "params.value > 5",
                "style": rating | {"backgroundColor": __env__.color_theme.rating_scale[5]},
            },
            {
                "condition": "params.value > 4",
                "style": rating | {"backgroundColor": __env__.color_theme.rating_scale[4]},
            },
            {
                "condition": "params.value > 3",
                "style": rating | {"backgroundColor": __env__.color_theme.rating_scale[3]},
            },
            {
                "condition": "params.value > 2",
                "style": rating | {"backgroundColor": __env__.color_theme.rating_scale[2]},
            },
            {
                "condition": "params.value > 1",
                "style": rating | {"backgroundColor": __env__.color_theme.rating_scale[1]},
            },
            {
                "condition": "params.value > 0",
                "style": rating | {"backgroundColor": __env__.color_theme.rating_scale[0]},
            },
        ],
        "defaultStyle": rating,
    },
    "width": __env__.logColWidths[7],
    "hide": not __env__.logColWidths[7]
}

N = {
    'cellStyle': {
        "styleConditions": [
            {
                "condition": "params.value == 0",
                "style": n_special,
            },
            {
                "condition": "params.value < 0",
                "style": n_ignore,
            },
        ],
        "defaultStyle": n_default,
    },
    "width": __env__.logColWidths[8],
    "hide": not __env__.logColWidths[8]
}

InvestTime = {
    'cellStyle': {
        "styleConditions": [
            {
                "condition": "params.data.cat == 'd' && params.data.InvestAmount == params.data.TakeAmount + params.data.ITC",
                "style": invest_deposit_null,
            },
            {
                "condition": "params.data.cat == ''",
                "style": invest_col | undefined,
            },
            {
                "condition": "params.data.cat == 'd'",
                "style": invest_deposit,
            },
            {
                "condition": "params.data.cat == 'p'",
                "style": invest_payout,
            },
            {
                "condition": "params.data.cat == 'i'",
                "style": invest_itc,
            },
            {
                "condition": "params.data.cat == 'v'",
                "style": invest_dividend,
            },
        ],
        "defaultStyle": invest_col,
    },
    "width": __env__.logColWidths[9],
    "hide": not __env__.logColWidths[9]
}

InvestAmount = {
    'cellStyle': {
        "styleConditions": [
            {
                "condition": "params.data.cat == 'd'",
                "style": invest_amount_deposit,
            },
        ] + InvestTime["cellStyle"]["styleConditions"],
        "defaultStyle": invest_col,
    },
    "width": __env__.logColWidths[10],
    "hide": not __env__.logColWidths[10]
} | _calcCell

InvestCourse = InvestTime | {
    "width": __env__.logColWidths[11],
    "hide": not __env__.logColWidths[11],
} | _calcCell

TakeTime = {
    'cellStyle': {
        "styleConditions": [
            {
                "condition": "params.data.cat == 'd' && params.data.InvestAmount == params.data.TakeAmount + params.data.ITC",
                "style": take_deposit_null,
            },
            {
                "condition": "params.data.cat == ''",
                "style": take_col | undefined,
            },
            {
                "condition": "params.data.cat == 'd'",
                "style": take_deposit,
            },
            {
                "condition": "params.data.cat == 'p'",
                "style": take_payout,
            },
            {
                "condition": "params.data.cat == 'i'",
                "style": take_itc,
            },
            {
                "condition": "params.data.cat == 'v'",
                "style": take_dividend,
            },
        ],
        "defaultStyle": take_col,
    },
    "width": __env__.logColWidths[12],
    "hide": not __env__.logColWidths[12]
}

TakeAmount = {
    'cellStyle': {
        "styleConditions": [
            {
                "condition": "params.data.cat == 'p'",
                "style": take_amount_payout,
            },
            {
                "condition": "params.data.cat == 'v'",
                "style": take_amount_dividend,
            },
        ] + TakeTime["cellStyle"]["styleConditions"],
        "defaultStyle": take_col,
    },
    "width": __env__.logColWidths[13],
    "hide": not __env__.logColWidths[13]
} | __env__.cellRendererChangeTakeAmount | _calcCell

TakeCourse = TakeTime | {
    "width": __env__.logColWidths[14],
    "hide": not __env__.logColWidths[14],
} | __env__.cellRendererChangeTakeCourse | _calcCell


Itc = {
    'cellStyle': {
        "styleConditions": [
            {
                "condition": "params.data.cat == ''",
                "style": itc_col | undefined,
            },
            {
                "condition": "params.data.cat == 'i'",
                "style": itc_itc,
            },
            {
                "condition": "params.data.cat == 'v'",
                "style": itc_dividend,
            },
            {
                "condition": "params.data.cat == 'p'",
                "style": itc_payout,
            },
            {
                "condition": "params.data.cat == 'd'",
                "style": itc_deposit,
            },
        ],
        "defaultStyle": itc_col,
    },
    "width": __env__.logColWidths[15],
    "hide": not __env__.logColWidths[15]
} | _calcCell

Performance = {
    'cellStyle': {
        "styleConditions": [
            {
                "condition": "params.data.cat == 'i'",
                "style": performance_itc,
            },
            {
                "condition": "params.data.cat == 'p'",
                "style": performance_payout,
            },
            {
                "condition": "params.data.cat == 'd' && params.value > 0",
                "style": performance_pos_deposit,
            },
            {
                "condition": "params.data.cat == 'd' && params.value <= 0",
                "style": performance_neg_deposit,
            },
            {
                "condition": "params.data.cat == 'v'",
                "style": result_dividend,
            },
            {
                "condition": "params.value > 0",
                "style": performance_pos,
            },
        ],
        "defaultStyle": performance_neg,
    },
    "width": __env__.logColWidths[16],
    "hide": not __env__.logColWidths[16]
} | __env__.cellRendererChangePerformance

Profit = {
    'cellStyle': {
        "styleConditions": [
            {
                "condition": "params.data.cat == 'd' && params.value > 0",
                "style": profit_pos_deposit,
            },
            {
                "condition": "params.data.cat == 'd' && params.value <= 0",
                "style": profit_neg_deposit,
            },
            {
                "condition": "params.value > 0",
                "style": profit_pos,
            },
        ],
        "defaultStyle": profit_neg,
    },
    "width": __env__.logColWidths[17],
    "hide": not __env__.logColWidths[17]
} | __env__.cellRendererChangeProfit

Dividend = {
    'cellStyle': {
        "styleConditions": [
            {
                "condition": "params.data.cat == 'd'",
                "style": result_deposit,
            },
        ],
        "defaultStyle": result,
    },
    "width": __env__.logColWidths[18],
    "hide": not __env__.logColWidths[18]
}

Note = {
    'cellStyle': {"white-space": "pre"} | note,
    "width": __env__.logColWidths[19],
    "hide": not __env__.logColWidths[19]
}

HoldTime = {
    'cellStyle': holdtime,
    "width": __env__.logColWidths[20],
    "hide": not __env__.logColWidths[20]
}

ProfitDay = {
    'cellStyle': {
        "styleConditions": [
            {
                "condition": "params.value > 0",
                "style": statistic_pos,
            },
        ],
        "defaultStyle": statistic_neg,
    },
    "width": __env__.logColWidths[21],
    "hide": not __env__.logColWidths[21]
}

PerformanceDay = ProfitDay | {
    "width": __env__.logColWidths[22],
    "hide": not __env__.logColWidths[22],
}

ProfitYear = {
    'cellStyle': {
        "styleConditions": [
            {
                "condition": "params.value > 0",
                "style": statistic_pos,
            },
        ],
        "defaultStyle": statistic_neg,
    },
    "width": __env__.logColWidths[23],
    "hide": not __env__.logColWidths[23]
}

PerformanceYear = ProfitDay | {
    "width": __env__.logColWidths[24],
    "hide": not __env__.logColWidths[24],
}
