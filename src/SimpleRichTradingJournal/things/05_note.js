function noteLinkPipe (value) {
    if (value) {
        cursorFrom = noteEditor.getCursor('from')
        cursorTo = noteEditor.getCursor('to')
        noteEditor.replaceRange(value, cursorFrom, cursorTo)
        noteEditor.focus()
        return null
    }
}


async function make_note (fileDropClone) {

    cur_focCell = null
    cur_row = null

    function backtocell() {
        if (cur_focCell) {
            logApi.ensureColumnVisible(cur_focCell)
            logApi.setFocusedCell(cur_focCell.rowIndex, cur_focCell.column.colId)
        }
    }

    function editor_to_cell () {
        if (cur_row) {
            cur_row.setDataValue("Note", noteEditor.getValue())
        }
    }

    if (noteCellVariableFormatter || noteUnifying) {
        function wr_pipe (content) {
            setter(noteContentPipe, JSON.stringify({"content": content, "row": cur_row.data}))
        }
    } else {
        function wr_pipe (content) {
            setter(noteContentPipe, JSON.stringify({"content": content, }))
        }
    }

    function editor_set (value) {
        wr_pipe(value)
        noteEditor.setValue(value)
    }

    function swich () {
        if (noteEditorContainer.style.left == "10px") {
            noteEditorContainer.style.right = "10px"
            noteEditorContainer.style.left = "calc(50% + 10px)"
            notepaperContainer.style.left = "10px"
            notepaperContainer.style.right = "calc(50% + 10px)"
        }
        else {
            notepaperContainer.style.right = "10px"
            notepaperContainer.style.left = "calc(50% + 10px)"
            noteEditorContainer.style.left = "10px"
            noteEditorContainer.style.right = "calc(50% + 10px)"
        }
    }

    noteEditor.on("changes", function (_, e) {
        if (notepaperContainer.style.zIndex == 20) {
            wr_pipe(noteEditor.getValue())
        }
    })
    noteEditor.on('focusout', function (_, e) {editor_to_cell()})
    window.addEventListener('focusout', function (e) {editor_to_cell()})
    window.addEventListener('beforeunload', function (e) {editor_to_cell()})

    logElement.addEventListener('click', function (e) {
        if (notepaperContainer.style.zIndex == 20 || noteEditorContainer.style.zIndex == 20) {
            e.preventDefault()
            focCell = logApi.getFocusedCell()
            _cur_row = logApi.getDisplayedRowAtIndex(focCell.rowIndex)
            editor_to_cell()
            cur_focCell = focCell
            cur_row = _cur_row
            editor_set(_cur_row.data["Note"] || "")
            return false
        }
    })

    logElement.addEventListener('keydown', function (e) {
        if ((notepaperContainer.style.zIndex == 20 || noteEditorContainer.style.zIndex == 20) && (e.code == 'ArrowUp' || e.code == 'ArrowDown')) { // ↑||↓
            e.preventDefault()
            focCell = logApi.getFocusedCell()
            _cur_row = logApi.getDisplayedRowAtIndex(focCell.rowIndex)
            editor_to_cell()
            cur_focCell = focCell
            cur_row = _cur_row
            editor_set(_cur_row.data["Note"] || "")
            return false
        }
    })

    window.addEventListener('keydown', function (e) {
        if (e.ctrlKey && e.code == ccNote) { // ctrl+i
            e.preventDefault()

            if (e.shiftKey) {
                if (notepaperContainer.style.zIndex == 20 || noteEditorContainer.style.zIndex == 20) {
                    swich()
                } else {
                    notepaperContainer.style.left = "10px"
                    notepaperContainer.style.right = "calc(50% + 10px)"
                    noteEditorContainer.style.right = "10px"
                    noteEditorContainer.style.left = "calc(50% + 10px)"
                    cur_focCell = logApi.getFocusedCell()
                    cur_row = logApi.getDisplayedRowAtIndex(cur_focCell.rowIndex)
                    editor_set(cur_row.data["Note"] || "")
                    noteEditorContainer.style.zIndex = 20
                    noteEditor.focus()
                }
            } else if (document.activeElement.role == "gridcell" && noteEditorContainer.style.zIndex == 20) {
                noteEditor.focus()
            } else if (notepaperContainer.style.zIndex == -3) {
                if (noteEditorContainer.style.zIndex == -3) {
                    notepaperContainer.style.right = "10px"
                    notepaperContainer.style.left = "calc(50% + 10px)"
                    noteEditorContainer.style.left = "10px"
                    noteEditorContainer.style.right = "calc(50% + 10px)"
                    cur_focCell = logApi.getFocusedCell()
                    cur_row = logApi.getDisplayedRowAtIndex(cur_focCell.rowIndex)
                    editor_set(cur_row.data["Note"] || "")
                }
                wr_pipe(noteEditor.getValue())
                notepaperContainer.style.zIndex = 20
            } else if (noteEditorContainer.style.zIndex == -3) {
                cur_focCell = logApi.getFocusedCell()
                cur_row = logApi.getDisplayedRowAtIndex(cur_focCell.rowIndex)
                editor_set(cur_row.data["Note"] || "")
                swich()
                noteEditorContainer.style.zIndex = 20
                noteEditor.focus()
            } else {
                notepaperContainer.style.zIndex = -3
            }

            return false

        } else if (e.key == "Escape") {
            if (!noteEditorFileRequest.style.display) {
                setter(noteFileCloneC, e.timeStamp.toString())
                return false

            } else if (notepaperContainer.style.zIndex == 20 || noteEditorContainer.style.zIndex == 20) {
                notepaperContainer.style.zIndex = -3
                noteEditorContainer.style.zIndex = -3
                editor_to_cell()
                backtocell()
                return false
            }
        }
    })

    noteEditorContainer.addEventListener('keydown', function (e) {
        if (e.ctrlKey && e.code == ccNoteBack) { // ctrl+#
            e.preventDefault()
            backtocell()
            return false
        }
    })

    function fontsize (e) {
        if (e.shiftKey && e.ctrlKey) {
            e.preventDefault()
            if (e.detail < 0) {
                noteEditorContainer.style.fontSize = (parseInt(noteEditorContainer.style.fontSize) + 1) + "px"
            }
            else {
                noteEditorContainer.style.fontSize = (parseInt(noteEditorContainer.style.fontSize) - 1) + "px"
            }
            noteEditor.refresh()
            return false
        }
    }

    noteEditorContainer.addEventListener('mousewheel', function (e) {
        return fontsize(e)
    })

    noteEditorContainer.addEventListener('DOMMouseScroll', function (e) {
        return fontsize(e)
    })

    if (fileDropClone) {
        noteEditor.on("drop", function (_, e) {
            noteEditor.setCursor(noteEditor.coordsChar({left: e.pageX, top: e.pageY}, "page"))
            e.preventDefault()
            file = e.dataTransfer.files[0]
            if (file) {
                reader = new FileReader()
                reader.onload = function (event) {
                    cursorFrom = noteEditor.getCursor("from")
                    cursorTo = noteEditor.getCursor("to")
                    insert_obj = {
                        "file": "file",
                        "data": event.target.result,
                        "name": file.name,
                        "type": file.type,
                        "ctrl": e.ctrlKey,
                        "shift": e.shiftKey,
                        "time": e.timeStamp
                    }
                    setter(noteFileClonePipe, JSON.stringify(insert_obj))
                }
                reader.readAsDataURL(file)
                return false
            } else {
                text = e.dataTransfer.getData("text")
                if (text) {
                    cursorFrom = noteEditor.getCursor("from")
                    cursorTo = noteEditor.getCursor("to")
                    name = text.match(/[^\/|\\]*$/)
                    if (!name) {
                        name = text
                    }
                    if (text.match(noteLinkDropPattern)) {
                        file = "link"
                        if (!text.match(/^\w+:/)) {
                            text = "http://" + text
                        }
                    } else if (text.match(notePathDropPattern)) {
                        file = "path"
                        if (!text.match(/^file:/)) {
                            text = "file:///" + text
                        }
                    } else {
                        file = false
                    }
                    insert_obj = {
                        "file": file,
                        "data": text,
                        "name": name,
                        "time": e.timeStamp
                    }
                    setter(noteFileClonePipe, JSON.stringify(insert_obj))
                    return false
                }
            }
        })
    }
}
