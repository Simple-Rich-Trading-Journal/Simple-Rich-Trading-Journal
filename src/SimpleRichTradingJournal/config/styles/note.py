import __env__

notepaper = {
    "fontSize": "13px",
    "fontFamily": "monospace",
    "color": __env__.color_theme.notepaper_fg,
    "backgroundColor": __env__.color_theme.notepaper_bg + (__env__.color_theme.notepaper_def_transparency if __env__.notePaperDefaultTransparency else ""),
    "border": "1px solid " + __env__.color_theme.notepaper_border
}
