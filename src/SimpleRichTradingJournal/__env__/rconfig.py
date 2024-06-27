from typing import Literal

# MISC #######################################################################################

##########################################################################
# Warning: the journal file is not thread safe.
# So do not use these parameters to edit the same journal in several apps.
appHost: str = "127.0.0.1"
appPort: int = 8050
##########################################################################

startupFlushOpenTakeAmount: Literal[0, 1] = 1
disableCopyPaste: Literal[0, 1] = 0
disableFooterLifeSignal: Literal[0, 1] = 1
dateFormat: Literal["ISO 8601", "american", "international", "ydm", "mdy", "dmy"] = "international"
dateFormatFirstDayOfWeek = 1
# 0=Sunday ...
bindKeyCodes: list[str] = [
    # javascript::Event.code    function      representation
    # ------------------------------------------------------
    'KeyC',                     # copy              'c'
    'KeyX',                     # cut               'x'
    'KeyV',                     # paste             'v'
    'KeyA',                     # copy row          'a'
    'KeyY',                     # copy row          'y'
    'KeyZ',                     # copy row          'z'
    'Space',                    # autocomplete      ' '
    'KeyI',                     # note              'i'
    'Backslash',                # note back to      '#'
    'KeyM',                     # mark              'm'
]
colorTheme: Literal["dark", "light", "blank"] = "dark"
useDefaultAltColors: Literal[0, 1] = 0
checkboxLongShortStyling: Literal["", "0", "s", "ls"] = "s"
autocleanIntervalS: int = 2592000  # 30 days *
# Unused clone files and position colors are deleted every * to maintain the file system.
nHistorySlots: int = 10
# Upper limit of history entries.


# _Window Grid Options_
sideInitBalance: Literal[0, 1] = 0
#   Whether the `balance` section should be shown at startup instead of the
#   `statistics` section.
gridSideSizeInitScale: float = 0.2  # 0 ... 1
#   Set this configuration to `0` if none of the sections should be shown at startup.
gridDefWidthScale: float = 0.2  # 0 ... 1
gridMinWidthScale: float = 0.1  # 0 ... 1
gridRow3Height: int = 120
bottomBarDistanceBottom: int = 105
bottomBarDistanceRight: int = 10

##############################################################################################

# SCOPE VALUES ###############################################################################

indexByTakeTime: Literal[0, 1] = 0
#   Otherwise by `InvestTime`.
scopeByIndex: Literal[0, 1] = 1
#   Otherwise by both
strictScopeByBoth: Literal[0, 1] = 1
#   Defines the behavior of the period selection when `Scope by Both` is active.
#   Activates the individual sorting for trades after selecting a time range,
#   this will only display those trades that are explicitly are open in the selected time
#   range.
#   If deactivated, the entries in connection with the indexing are selected according to
#   the defined range.
calcWithOpens: Literal[0, 1] = 1

##############################################################################################

# JOURNAL ####################################################################################

# _Column Specifications_
logColOrderAssetId: list[int] = [
    # Defines the arrangement of the columns in the column group `Asset`.
    # Negative numbers define the arrangement in the pinned part of the column group.
    # A zero can be entered to hide a column in the group.
    #
    # order     column
    # --------------------
    -1,         # Name
    1,          # Symbol
    2,          # ISIN
    3,          # Short
    4,          # Type
    5,          # Category
    6,          # Sector
    7,          # Rating
    8,          # n
]
logColOrderNote: list[int] = [
    # Defines the arrangement of the columns in the column group `Note`.
    # A zero can be entered to hide a column in the group.
    #
    # order     column
    # --------------------
    0,          # Symbol
    0,          # ISIN
    0,          # Short
    0,          # Type
    0,          # Category
    0,          # Sector
    0,          # Rating
    8,          # Note
]
logColOrder: list[int] = [
    # Defines the arrangement of the column groups in the journal.
    #
    # order     column group
    # ----------------------
    1,          # Asset Ids
    2,          # Invest
    3,          # Take
    4,          # ITC
    5,          # Result
    6,          # Note
    7,          # Hold Time
    8,          # Hypotheses
]
logColWidths: list[int] = [
    # Defines the column widths in the journal.
    # A zero can be entered to hide a column.
    #
    # width     column
    # -------------------------------
    140,        # 0  Name
    0,          # 1  Symbol
    0,          # 2  ISIN
    0,          # 3  Type
    0,          # 4  Short
    0,          # 5  Sector
    0,          # 6  Category
    0,          # 7  Rating
    80,         # 8  n
    170,        # 9  InvestTime
    150,        # 10 InvestAmount
    110,        # 11 InvestCourse
    170,        # 12 TakeTime
    150,        # 13 TakeAmount
    110,        # 14 TakeCourse
    80,         # 15 ITC
    110,        # 16 Profit
    110,        # 17 Performance
    80,         # 18 Dividend
    120,        # 19 Note
    170,        # 20 HoldTime
    160,        # 21 Profit/Day
    160,        # 22 Performance/Day
    160,        # 23 Profit/Year                                                # ++ since v0.5
    160,        # 24 Performance/Year                                           # ++ since v0.5
]

columnStateCache: Literal["", "0", "global", "own"] = "global"
#       Uses a cross-profile column state cache when "global".
#       To use a cache isolated in the profile, "own" can be selected.
#       An empty string ("") or "0" deactivates the feature.

# _Enable Change Deltas_
cellRendererChangeTakeAmount: Literal[0, 1] = 0
cellRendererChangeTakeCourse: Literal[0, 1] = 0
cellRendererChangePerformance: Literal[0, 1] = 1
cellRendererChangeProfit: Literal[0, 1] = 1

##############################################################################################

# SIDE SECTIONS ##############################################################################

# _BALANCE section_
balanceT52W: Literal[0, 1] = 1
balanceCurrent: Literal[0, 1] = 1
balanceYears: Literal[0, 1] = 1
balanceQuarters: Literal[0, 1] = 1

# _STATISTIC section_

#   _Positions Graphs_
statisticsGroupDefault: list[int] = [
        # Standard grouping (0=ignored).
        #
        # order     meta
        # ---------------------------------
        0,          # Short
        0,          # Type
        0,          # Sector
        0,          # Category
        1,          # ID* (Name || Symbol)
]
statisticsSunMaxDepth: int = 4
#       Defines the maximal resolution of the position graph.
statisticsUseSunMaxDepth: Literal[0, 1] = 1
#       Whether the resolution should be used by default,
#       otherwise all available levels are displayed.
statisticsIdBySymbol: Literal[0, 1] = 0
#       else *ID = Name

statisticsUsePositionColorCache: Literal["", "0", "global", "own"] = "global"
#       Uses a cross-profile color cache for the coloring of segments in the graph when
#       "global". To use a cache isolated in the profile, "own" can be selected.
#       An empty string ("") or "0" deactivates the feature.

#   _Performance Graphs_
statisticsPerformanceStepsDefault: Literal["w", "m", "q"] = "w"
#       Calculation block frame (week | month | quarters).
statisticsPerformanceIntervalDefault: Literal["w", "m", "q"] = "w"
#       Calculation trailing interval (week | month | quarters).
statisticsPerformanceFrameDefault: Literal["w", "m", "q"] = "q"
#       Calculation trailing block frame (week | month | quarters).
statisticsPerformanceRangeDefault: Literal[0, 12, 24, 48] = 0
#       Calculation period parameter (months, 0=alltime).
statisticsHypothesisPerDay: Literal[0, 1] = 0                                   # ++ since v0.5
#       Create the corresponding graphs based on <Hypothesis>/Day instead of <Hypothesis>/Year by default.
statisticsPerformanceOrder: list[int] = [
        # order     graph
        # ------------------------------------------
        1,          # Trading Profit & Performance
        2,          # Summary Profit & Rate
        3,          # Deposits, Payouts & Money
        4,          # Trading Amount
        5,          # Ø Profit/Day, Ø Perf./Day
        6,          # ~Amount, ~Ø Perf.
        7,          # ~Ø Profit/Day, ~Ø Perf./Day
        8,          # ~Activity, ~Ø Hold Days
        # (how diagrams are merged)
        # 1,        # Trading Profit & Performance
        # 1,        # Summary Profit & Rate
        # 2,        # Deposits, Payouts & Money
        # 3,        # Trading Amount
        # 4,        # Ø Profit/Day, Ø Perf./Day
        # 5,        # ~Amount, ~Ø Perf.
        # 6,        # ~Ø Profit/Day, ~Ø Perf./Day
        # 7,        # ~Activity, ~Ø Hold Days
]

#   Layouts
statisticsPerformanceGraphSize: int = 1000
statisticsPopGraphSize: int = 2000
statisticsOpenPositionsGraphSize: int = 500
statisticsAllPositionsGraphSize: int = 500

##############################################################################################

# NOTE INTERFACE #############################################################################

#   _Styling_
notePaperDefaultTransparency: Literal[0, 1] = 1
noteEditorDefaultTransparency: Literal[0, 1] = 1

#   _File Drop_
noteFileDropCloner: Literal["", "0", "global", "own"] = "global"
#       Enable the dropping of files, url's/link's and file paths
#       and their automatic processing to Markdown syntax.
#       To ensure that the page can access the file, a copy of the dropped
#       file is created in the asset folder (this also means that updates
#       to the original file are not applied).
#       Uses a cross-profile cache when "global". To use a cache isolated in the profile,
#       "own" can be selected. An empty string ("") or "0" deactivates the feature.
noteFileDropClonerImgAltName: Literal[0, 1] = 0
#       Enable the alternative text for embedded images (by default,
#       browsers default (broken image icon) is shown if the file is not found).
noteLinkDropPattern: str = "^(https?:\\/\\/|www\\.)"
#       Recognize the following pattern as url/link.
notePathDropPattern: str = "^(\\/|[A-Z]:\\\\)"
#       Recognize the following pattern as a filesystem path.
noteFileDropClonerFlushTrashing: Literal[0, 1] = 1
#       First move the clone files to a trash folder before they are
#       completely deleted in the next iteration.

#   _Formatters_
noteMathJax: Literal[0, 1] = 0
#       Activate the rendering of LaTeX/Mathematics.
#       (https://dash.plotly.com/dash-core-components/markdown#latex)
#       (https://en.wikibooks.org/wiki/LaTeX/Mathematics)
noteCellVariableFormatter: Literal[0, 1] = 1
#       Activate the formatter for cell variables.
#       The string format syntax of the python library is used for this (https://docs.python.org/3/library/string.html#format-string-syntax).
#       Thus, for example, the field 'Name' of the record can be inserted via '{Name}'
#       (look in file plugin/__init__.py for a list of available fields).
noteMathJaxMasker: Literal[0, 1] = 1
#           Since the mathematical formulas often contain curly brackets, but these are
#           part of the formatter syntax, they must be masked in order to use them as plain
#           text (e.g. '}}' becomes '}'). This can be done automatically for the LaTeX units in the text.

noteUnifying: Literal[0, 1] = 1
#   Merge all notes matching the field Name of previous lines, in the Markdown component.

##############################################################################################

# PLUGIN #####################################################################################

coursePluginUpdateInterval: Literal[0, 1] = 0
coursePluginUpdateIntervalOn: Literal[0, 1] = 0
coursePluginUpdateIntervalMs: int = 10_000
# Activation and specification of an interval for the course plugin.
# Only useful if the corresponding plugin is implemented.
# The program can significantly lose performance, especially if `with open`
# is enabled and one of the sections `STATISTIC` or `BALANCE` is open,
# as these are recalculated.

pluginQuickDisable: Literal[0, 1] = 0
# Deactivate all plugins even if they are implemented.

##############################################################################################
