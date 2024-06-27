from __future__ import annotations

import json
from base64 import b64decode
from os import listdir
from re import sub, DOTALL
from urllib.parse import quote

from dash import callback, Output, Input, State, no_update

import __env__
import layout
from config import msg

if __env__.noteCellVariableFormatter:
    from string import Formatter

    class _Formatter(Formatter):

        def get_value(self, key, args, kwargs):
            return msg.note_error_none if (v := kwargs[key]) is None else v

        def get_field(self, field_name, args, kwargs):
            try:
                val = super().get_field(field_name, args, kwargs)
            except (KeyError, AttributeError, IndexError):
                val = None, field_name
            return val

        def format_field(self, value, spec):
            if value is None:
                return msg.note_error_missing_field
            try:
                return super().format_field(value, spec)
            except ValueError:
                return msg.note_error_bad_format

        def format(self, __format_string, kwargs):
            try:
                return self.vformat(__format_string, (), kwargs)
            except ValueError as e:
                return msg.note_error_fatal.format(error=e)


    _formatter = _Formatter()

    def _format(__content, __row):
        return _formatter.format(
            __content,
            {
                "cat": None,
                "Name": None,
                "Symbol": None,
                "ISIN": None,
                "Type": None,
                "Category": None,
                "Short": False,
                "Sector": None,
                "Rating": None,
                "n": None,
                "InvestTime": None,
                "InvestAmount": None,
                "InvestCourse": None,
                "TakeTime": None,
                "TakeAmount": None,
                "TakeCourse": None,
                "ITC": None,
                "Performance": None,
                "Profit": None,
                "Dividend": None,
                "Note": None,
                "HoldTime": None,
                "Performance/Day": None,
                "Profit/Day": None,
              } | __row
        )
    if __env__.noteMathJax and __env__.noteMathJaxMasker:

        def content(obj):
            _content = sub("\\$\\$.*?\\$\\$", lambda m: m.group().replace("{", "{{").replace("}", "}}"), obj["content"], flags=DOTALL)
            return _format(_content, obj["row"])

    else:
        def content(obj):
            return _format(obj["content"], obj["row"])

else:
    def content(obj):
        return obj["content"]


if __env__.noteUnifying:

    @callback(
        Output(layout.note.notepaper, "children"),
        Output(layout.note.noteContentPipe, "value"),
        Input(layout.note.noteContentPipe, "value"),
        State(layout.tradinglog, "rowData"),
        config_prevent_initial_callbacks=True
    )
    def noteContentPipe(obj, row_data):
        if obj:
            obj = json.loads(obj)
            _content = content(obj)
            _id = obj["row"]["id"]
            if _name := obj["row"].get("Name"):
                for i in range(len(row_data)):
                    if row_data[i]["id"] == _id:
                        for row in row_data[i + 1:]:
                            if row.get("Name") == _name:
                                _content += content({"content": row.get("Note") or "", "row": row})
                        break
            return _content, None
        else:
            return "", None
else:
    @callback(
        Output(layout.note.notepaper, "children"),
        Output(layout.note.noteContentPipe, "value"),
        Input(layout.note.noteContentPipe, "value"),
        config_prevent_initial_callbacks=True
    )
    def noteContentPipe(obj):
        if obj:
            obj = json.loads(obj)
            return content(obj), None
        else:
            return "", None


def make_filelink(
        drop_obj,
        clone=True
):
    if drop_obj["file"] == "file":
        link_name = quote(drop_obj["name"])
        if drop_obj["type"].startswith("image/"):
            if __env__.noteFileDropClonerImgAltName:
                name = drop_obj["name"]
            else:
                name = ""
            link = f"![{name}]({__env__.FILE_CLONES_URL}/{link_name})"
        else:
            link = f"[{drop_obj['name']}]({__env__.FILE_CLONES_URL}/{link_name})"
        if clone:
            header, encoded = drop_obj["data"].split(",", 1)
            data = b64decode(encoded)
            with open(f"{__env__.FILE_CLONES}/{drop_obj['name']}", "wb") as f:
                f.write(data)
    elif drop_obj["file"] in ("link", "path"):
        link = f"[{drop_obj['name']}]({drop_obj['data']})"
    else:
        link = drop_obj['data']
    return link


@callback(
    Output(layout.note.noteLinkPipe, "value", allow_duplicate=True),
    Output(layout.note.noteEditorFileRequest, "style", allow_duplicate=True),
    Output(layout.note.noteeditor_file_request_msg, "children"),
    Output(layout.note.noteeditor_file_request_rnto, "children"),
    Output(layout.note.noteFileClonePipe, "value", allow_duplicate=True),
    Input(layout.note.noteFileClonePipe, "value"),
    State(layout.note.noteEditorFileRequest, "style"),
    config_prevent_initial_callbacks=True
)
def fileClone(obj, style):
    if obj:
        obj = json.loads(obj)
        err_rnto = no_update
        err_msg = no_update
        file_pipe = no_update

        name = obj["name"]
        dirlist = listdir(__env__.FILE_CLONES)

        if name in dirlist:

            def new_name():
                i = 2
                while (_name := f"{name}-{i}") in dirlist:
                    i += 1
                return _name

            if obj["ctrl"]:
                link = make_filelink(obj, clone=obj["shift"])
                style = no_update
                file_pipe = None
            elif obj["shift"]:
                obj["name"] = new_name()
                link = make_filelink(obj)
                style = no_update
                file_pipe = None
            else:
                link = no_update
                style |= {"display": ""}
                err_msg = name
                err_rnto = new_name()
        else:
            link = make_filelink(obj)
            style = no_update
            file_pipe = None
        return link, style, err_msg, err_rnto, file_pipe
    else:
        return no_update


@callback(
    Output(layout.note.noteLinkPipe, "value", allow_duplicate=True),
    Output(layout.note.noteEditorFileRequest, "style", allow_duplicate=True),
    Output(layout.note.noteFileClonePipe, "value", allow_duplicate=True),
    State(layout.note.noteFileClonePipe, "value"),
    State(layout.note.noteeditor_file_request_rnto, "children"),
    Input(layout.note.noteeditor_file_request_rn, "n_clicks"),
    State(layout.note.noteEditorFileRequest, "style"),
    config_prevent_initial_callbacks=True
)
def fileCloneRN(obj, rnto, rn, style):
    obj = json.loads(obj)
    obj["name"] = rnto
    return make_filelink(obj), style | {"display": "none"}, None


@callback(
    Output(layout.note.noteLinkPipe, "value", allow_duplicate=True),
    Output(layout.note.noteEditorFileRequest, "style", allow_duplicate=True),
    Output(layout.note.noteFileClonePipe, "value", allow_duplicate=True),
    State(layout.note.noteFileClonePipe, "value"),
    Input(layout.note.noteeditor_file_request_ow, "n_clicks"),
    State(layout.note.noteEditorFileRequest, "style"),
    config_prevent_initial_callbacks=True
)
def fileCloneOW(obj, ow, style):
    obj = json.loads(obj)
    return make_filelink(obj), style | {"display": "none"}, None


@callback(
    Output(layout.note.noteLinkPipe, "value", allow_duplicate=True),
    Output(layout.note.noteEditorFileRequest, "style", allow_duplicate=True),
    Output(layout.note.noteFileClonePipe, "value", allow_duplicate=True),
    State(layout.note.noteFileClonePipe, "value"),
    State(layout.note.noteEditorFileRequest, "style"),
    Input(layout.note.noteeditor_file_request_ig, "n_clicks"),
    config_prevent_initial_callbacks=True
)
def fileCloneIG(obj, style, _):
    if obj:
        obj = json.loads(obj)
        return make_filelink(obj, clone=False), style | {"display": "none"}, None
    else:
        return no_update


@callback(
    Output(layout.note.noteLinkPipe, "value", allow_duplicate=True),
    Output(layout.note.noteEditorFileRequest, "style", allow_duplicate=True),
    Output(layout.note.noteFileClonePipe, "value", allow_duplicate=True),
    State(layout.note.noteEditorFileRequest, "style"),
    Input(layout.note.noteFileCloneC, "value"),
    config_prevent_initial_callbacks=True
)
def fileCloneC(style, _):
    return None, style | {"display": "none"}, None
