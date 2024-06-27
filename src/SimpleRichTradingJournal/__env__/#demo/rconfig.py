from typing import Literal

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
    0,          # Type
    0,          # Category
    0,          # Sector
    -2,          # Rating
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
    1,          # Type
    2,          # Category
    7,          # Sector
    0,          # Rating
    8,          # Note
]
logColWidths: list[int] = [
    # Defines the column widths in the journal.
    # A zero can be entered to hide a column.
    #
    # width     column
    # -------------------------------
    140,        # 0  Name
    70,          # 1  Symbol
    0,          # 2  ISIN
    70,          # 3  Type
    50,          # 4  Short
    90,          # 5  Sector
    50,          # 6  Category
    30,          # 7  Rating
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
    160,        # 23 Profit/Year
    160,        # 24 Performance/Year
]

columnStateCache: Literal["", "0", "global", "own"] = "own"
#       Uses a cross-profile column state cache when "global".
#       To use a cache isolated in the profile, "own" can be selected.
#       An empty string ("") or "0" deactivates the feature.

# _Enable Change Deltas_
cellRendererChangeTakeAmount: Literal[0, 1] = 0
cellRendererChangeTakeCourse: Literal[0, 1] = 1
cellRendererChangePerformance: Literal[0, 1] = 1
cellRendererChangeProfit: Literal[0, 1] = 1

##############################################################################################

# NOTE INTERFACE #############################################################################

#   _File Drop_
noteFileDropCloner: Literal["", "global", "own"] = "own"
#       Enable the dropping of files, url's/link's and file paths
#       and their automatic processing to Markdown syntax.
#       To ensure that the page can access the file, a copy of the dropped
#       file is created in the asset folder (this also means that updates
#       to the original file are not applied).
#       Uses a cross-profile cache when "global". To use a cache isolated in the profile,
#       "own" can be selected. An empty string ("") deactivates the feature.

#   _Formatters_
noteMathJax: Literal[0, 1] = 1
#       Activate the rendering of LaTeX/Mathematics.
#       (https://dash.plotly.com/dash-core-components/markdown#latex)
#       (https://en.wikibooks.org/wiki/LaTeX/Mathematics)

##############################################################################################

# PLUGIN #####################################################################################

coursePluginUpdateInterval: Literal[0, 1] = 1
coursePluginUpdateIntervalOn: Literal[0, 1] = 1
coursePluginUpdateIntervalMs: int = 10_000
# Activation and specification of an interval for the course plugin.
# Only useful if the corresponding plugin is implemented.
# The program can significantly lose performance, especially if `with open`
# is enabled and one of the sections `STATISTIC` or `BALANCE` is open,
# as these are recalculated.

pluginQuickDisable: Literal[0, 1] = 0
# Deactivate all plugins even if they are implemented.

##############################################################################################
