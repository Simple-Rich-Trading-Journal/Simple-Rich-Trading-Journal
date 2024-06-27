from dash import html, dcc
from config import styles
import __env__

noteeditor_container = html.Div(
    [
        noteEditorFileRequest := html.Div(
            [
                html.Div(
                    [
                        html.Span("A file with the name "),
                        noteeditor_file_request_msg := html.Span(id="noteeditor_file_request_msg_", style={"fontStyle": "italic", "fontWeight": "bold"}),
                        html.Span(" has already been cloned."),
                        html.Br(),
                        html.Span("Select an action or press "),
                        html.Span("<esc>", style={"fontWeight": "bold"}),
                        html.Span(" to cancel."),
                    ]
                ),
                noteeditor_file_request_ig := html.Button(
                    "keep clone",
                    style={
                        "backgroundColor": __env__.color_theme.noteeditor_dialog_ignore,
                        "border": "1px solid",
                        "margin": "1px",
                        "width": "100%"
                    },
                    id="noteeditor_file_request_ig_"
                ),
                noteeditor_file_request_rn := html.Button(
                    [
                        html.Span("create "),
                        noteeditor_file_request_rnto := html.Span(id="noteeditor_file_request_rnto_", style={"fontStyle": "italic"})
                    ],
                    style={
                        "backgroundColor": __env__.color_theme.noteeditor_dialog_rename,
                        "border": "1px solid",
                        "margin": "1px",
                        "width": "100%"
                    },
                    id="noteeditor_file_request_rn_"
                ),
                noteeditor_file_request_ow := html.Button(
                    "overwrite clone",
                    style={
                        "backgroundColor": __env__.color_theme.noteeditor_dialog_overwrite,
                        "border": "1px solid",
                        "margin": "1px",
                        "width": "100%"
                    },
                    id="noteeditor_file_request_ow_"
                ),
                html.Div(
                    [
                        html.Br(),
                        html.Div("Shortcuts: ", style={"fontWeight": "bold"}),
                        html.Span("Hold "),
                        html.Span("ctrl", style={"width": "50%", "fontWeight": "bold", "border": "1px solid", "backgroundColor": __env__.color_theme.noteeditor_dialog_ignore}),
                        html.Span(" (keep), "),
                        html.Span("shift", style={"width": "50%", "fontWeight": "bold", "border": "1px solid", "backgroundColor": __env__.color_theme.noteeditor_dialog_rename}),
                        html.Span(" (create) or "),
                        html.Span("ctrl+shift", style={"width": "50%", "fontWeight": "bold", "border": "1px solid", "backgroundColor": __env__.color_theme.noteeditor_dialog_overwrite}),
                        html.Span(" (overwrite) "),
                        html.Br(),
                        html.Span("when dropping to bypass the dialog."),
                    ],
                    style={"fontStyle": "italic", "fontSize": "10px"}
                ),
            ],
            style={
                "position": "absolute",
                "zIndex": 3,
                "display": "none",
                "padding": "10px",
                "margin": "10px",
                "color": __env__.color_theme.noteeditor_dialog_fg,
                "backgroundColor": __env__.color_theme.noteeditor_dialog_bg,
                "border": "1px solid " + __env__.color_theme.noteeditor_dialog_border,
                "fontSize": "13px"
            },
            id="noteEditorFileRequest"
        )
    ],
    style={
        "position": "absolute",
        "fontSize": "13px",
        "top": 20,
        "right": 20,
        "bottom": 20,
        "left": "calc(50% + 5px)",
        "display": "flex",
        "zIndex": -3
    },
    id="noteEditorContainer"
)

notepaper_container = html.Div(
    notepaper := dcc.Markdown(
        style={
            "padding": "10px",
            "width": "100%",
            "overflow": "scroll",
        } | styles.note.notepaper,
        className="notepaper",
        mathjax=bool(__env__.noteMathJax),
        link_target="_blank",
        id="notepaperElement"
    ),
    style={
        "position": "absolute",
        "top": 20,
        "left": 20,
        "bottom": 20,
        "right": "calc(50% + 5px)",
        "display": "flex",
        "zIndex": -3
    },
    id="notepaperContainer"
)

COMPONENTS = html.Div([
    noteeditor_container,
    notepaper_container,
    noteContentPipe := dcc.Input(id="noteContentPipe", style={"display": "none"}),
    noteFileClonePipe := dcc.Input(id="noteFileClonePipe", style={"display": "none"}),
    noteLinkPipe := dcc.Input(id="noteEditorPipe", style={"display": "none"}),
    noteFileCloneC := dcc.Input(id="noteFileCloneC", style={"display": "none"}),
])
