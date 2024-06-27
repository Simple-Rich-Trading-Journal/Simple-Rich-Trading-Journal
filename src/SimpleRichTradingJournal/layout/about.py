from json import loads
from urllib.request import urlopen
from traceback import print_exception

from dash import html, dcc

from SimpleRichTradingJournal import __version__
import __env__
import __ini__.logtags
from config import imgs


_url_version = "https://pypi.python.org/pypi/SimpleRichTradingJournal/json"
_url_about =  "https://raw.githubusercontent.com/Simple-Rich-Trading-Journal/Simple-Rich-Trading-Journal/master/src/SimpleRichTradingJournal/ABOUT.md"
_url_update = "https://raw.githubusercontent.com/Simple-Rich-Trading-Journal/Simple-Rich-Trading-Journal/master/UPDATE.md"

_alt_about = __env__._files.proj_root + "/ABOUT.md"

try:
    with urlopen(_url_about) as u:
        about = u.read().decode()
except Exception as e:
    print_exception(e)
    print(__ini__.logtags.error, "The above exception occurred during the about query.")
    with open(_alt_about) as f:
        about = "*\n\n" + f.read()

update_header = ""
update_note = ""
about_button_color = __env__.color_theme.table_bg_main

try:
    with urlopen(_url_version) as u:
        available = loads(u.read())["info"]["version"]
    if __version__ != available:
        about_button_color = __env__.color_theme.cell_negvalue
        update_header = f"---\n\n### Version {available} is available!"
        try:
            with urlopen(_url_update) as u:
                update_note = u.read().decode()
        except Exception as e:
            print_exception(e)
            print(__ini__.logtags.error, "The above exception occurred during the update note query.")
    else:
        about_button_color = __env__.color_theme.cell_posvalue
except Exception as e:
    print_exception(e)
    print(__ini__.logtags.error, "The above exception occurred during the version query.")
    update_note = f"An error occurred during the version query: **{e}**"

about = about.format(version=__version__, update_header=update_header, update_note=update_note)


about_button = html.Button(
    imgs.information,
    id="info_button_",
    n_clicks=0,
    style={
        "display": "inline-block",
        "margin": "7px",
        "fontSize": "12px",
        "color": __env__.color_theme.table_fg_header,
        "backgroundColor": about_button_color,
        "border": "1px solid " + __env__.color_theme.table_sep,
        "paddingLeft": "10px",
        "paddingRight": "10px",
        "borderRadius": "15px",
        "opacity": 0.7,
    }
)


MODAL = html.Div(
    html.Div(
        dcc.Markdown(
            about,
            style={
                "padding": "10px",
                "width": "100%",
            },
            link_target="_blank",
        ),
    ),
    id="about_modal_",
    style={
        "position": "absolute",
        "zIndex": -2,
        "width": 500,
        "top": 50,
        "bottom": 10,
        "left": "calc(50% - 250px)",
        "backgroundColor": __env__.color_theme.table_bg_2,
        "color": __env__.color_theme.table_fg_main,
        "padding": 10,
        "borderRadius": 10,
        "overflow": "scroll"
    }
)

COMPONENTS = MODAL
