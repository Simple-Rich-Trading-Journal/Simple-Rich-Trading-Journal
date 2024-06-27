async function make_copypaste () {

    // fixme: Uncaught (in promise) DOMException: Clipboard write was blocked due to lack of user activation.

    function paste (value) {
        focCell = logApi.getFocusedCell()
        row = logApi.getDisplayedRowAtIndex(focCell.rowIndex)
        old_row = JSON.stringify(row.data)
        colId = null
        console.log("PASTE: value=", value)
        if (value.startsWith('{')) {
            value = JSON.parse(value)
            value.id = row.data.id
            row.setData(value)
            new_row = JSON.stringify(value)
        }
        else {
            numCols = ["n", "InvestAmount", "InvestCourse", "TakeAmount", "TakeCourse", "cit", "Rating"]
            if (numCols.includes(focCell.column.colId)) {
               value = parseFloat(value)
            }
            colId = focCell.column.colId
            row.setDataValue(focCell.column.colId, value)
            row = logApi.getDisplayedRowAtIndex(focCell.rowIndex)
            new_row = JSON.stringify(row.data)
        }
        update = {
            "new_row": new_row,
            "old_row": old_row,
            "colId": colId,
        }
        setTimeout(
            function () {
                setter(editEventReceiver, JSON.stringify(update))
            },
            3
        )
    }

    logElement.addEventListener('paste', function (e) {
        console.log("PASTE: EventListener @ ", document.activeElement)
        if (document.activeElement.role == "gridcell") {
            console.log("PASTE: e=", e)
            paste(e.clipboardData.getData('text/plain'))
        }
    })

    logElement.addEventListener('keydown', function (e) {
        // console.log("KEYDOWN: e=", e)
        if (e.ctrlKey && e.code == ccCopy) {  // ctrl+c
            e.preventDefault()
            focCell = logApi.getFocusedCell()
            row = logApi.getDisplayedRowAtIndex(focCell.rowIndex)
            value = row.data[focCell.column.colId]
            console.log("CLIPBOARD write:", value)
            navigator.clipboard.writeText(value)
            return false
        }
        else if (e.ctrlKey && e.code == ccCut) {  // ctrl[+shift]+x
            e.preventDefault()
            focCell = logApi.getFocusedCell()
            row = logApi.getDisplayedRowAtIndex(focCell.rowIndex)
            old_row = JSON.stringify(row.data)
            if (e.shiftKey) {
                value = JSON.stringify(row.data)
                new_row = {"id": row.data.id}
                update = {
                    "new_row": JSON.stringify(new_row),
                    "old_row": old_row,
                }
                row.setData(new_row)
            }
            else {
                value = row.data[focCell.column.colId]
                row.setDataValue(focCell.column.colId, null)
                row = logApi.getDisplayedRowAtIndex(focCell.rowIndex)
                update = {
                    "new_row": JSON.stringify(row.data),
                    "old_row": old_row,
                    "colId": focCell.column.colId,
                }
            }
            console.log("CLIPBOARD write:", value)
            navigator.clipboard.writeText(value)
            setter(editEventReceiver, JSON.stringify(update))
            return false
        }
        else if (e.ctrlKey && e.code == ccPaste) { // ctrl+v
            console.log("PASTE: Ctrl+V @ ", document.activeElement)
            if (document.activeElement.role == "gridcell") {
                navigator.clipboard.readText()
                    .then(text => {
                        paste(text)
                    })
                    .catch(err => {
                        console.log("PASTE: err=", err);
                    })
            }
        }
        else if ((e.ctrlKey && e.code == ccCopyRow1) || (e.ctrlKey && e.code == ccCopyRow2) || (e.ctrlKey && e.code == ccCopyRow3)) { // ctrl+a || ctrl+y || ctrl+z
            e.preventDefault()
            focCell = logApi.getFocusedCell()
            row = logApi.getDisplayedRowAtIndex(focCell.rowIndex)
            value = JSON.stringify(row.data)
            console.log("CLIPBOARD: write", value)
            navigator.clipboard.writeText(value)
            return false
        }
    })
}
