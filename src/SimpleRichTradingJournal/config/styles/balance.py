import __env__

cell_default = {"fontSize": "13px", "fontFamily": "monospace", "color": "black", "paddingRight": "10px", "paddingLeft": "10px"}
col1_cell_default = cell_default | {"textAlign": "left", "borderRight": "1px solid " + __env__.color_theme.sheet_col1_sep}
header_default = {"fontWeight": "bold", "borderBottom": "2px solid black"}
col1_header_default = header_default

sep = {"fontSize": "0px", "borderTop": "1px solid", "padding": "0px"}
sep2 = {"fontSize": "0px", "border": "1px solid", "padding": "0px"}
space = {"fontSize": "0px", "border": "0px", "padding": "10px"}
space1 = {"fontSize": "0px", "padding": "4px", "borderLeft": "0px", "borderRight": "0px", "borderBottom": "0px"}


year_cell = {"backgroundColor": __env__.color_theme.sheet_col_year}
q1_cell = {"borderRight": "1px solid " + __env__.color_theme.sheet_quarter_sep}
q4_cell = {"borderLeft": "1px solid " + __env__.color_theme.sheet_quarter_sep}

year_header = {"backgroundColor": __env__.color_theme.sheet_header_year}
q1_header = q1_cell
q4_header = q4_cell

_current_sep = {"borderRight": "1px solid " + __env__.color_theme.sheet_current_sep}
t52w_cell = _current_sep | {"backgroundColor": __env__.color_theme.sheet_col_t52}
t52w_header = _current_sep | {"backgroundColor": __env__.color_theme.sheet_header_t52}
current_cell = _current_sep | {"backgroundColor": __env__.color_theme.sheet_col_current}
current_header = _current_sep | {"backgroundColor": __env__.color_theme.sheet_header_current}

active = {"border": "unset !important", "backgroundColor": __env__.color_theme.sheet_cell_active_bg}
selected = {"border": "unset !important", "backgroundColor": __env__.color_theme.sheet_cell_selected_bg}

t52w_button_on = {"backgroundColor": __env__.color_theme.sheet_header_t52, "border": "3px double #000", "color": "black"}
current_button_on = {"backgroundColor": __env__.color_theme.sheet_header_current, "border": "3px double #000", "color": "black"}
year_button_on = {"backgroundColor": __env__.color_theme.sheet_header_year, "border": "3px double #000", "color": "black"}
quarter_button_on = {"backgroundColor": "#FFF", "border": "3px double #000", "color": "black"}

t52w_button_off = t52w_button_on | {"border": "2px solid #FFF"}
current_button_off = current_button_on | {"border": "2px solid #FFF"}
year_button_off = year_button_on | {"border": "2px solid #FFF"}
quarter_button_off = quarter_button_on | {"border": "2px solid #FFF"}
