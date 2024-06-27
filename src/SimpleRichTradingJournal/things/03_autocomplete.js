function autocomplete (value) {
    if (value) {
        trigger = JSON.parse(autoCTrigger.value)
        if (trigger) {
            if (trigger._eid) {
                cell = document.getElementById(trigger._eid)
                setter(cell, value)
                cell.focus()
            }
            else {
                focCell = logApi.getFocusedCell()
                row = logApi.getDisplayedRowAtIndex(focCell.rowIndex)
                row.setDataValue(focCell.column.colId, value)
                logApi.setFocusedCell(trigger._idx, trigger._col)
                // logApi.startEditingCell({"rowIndex": trigger._idx, "colKey": trigger._col})
            }
        }
        autoCDropdown.style.zIndex = -3
    }
    return null
}

async function make_autocomplete () {
    logElement.addEventListener('keydown', function (e) {
        if (e.ctrlKey && e.code == ccAComplete) { // ctrl+<space>
            e.preventDefault()

            focCell = logApi.getFocusedCell()
            row = logApi.getDisplayedRowAtIndex(focCell.rowIndex)

            if (["Name", "Symbol", "ISIN", "Type", "Sector", "Category"].includes(focCell.column.colId)) {

                trigger = JSON.parse(JSON.stringify(row.data))
                trigger._col = focCell.column.colId
                trigger._idx = focCell.rowIndex
                trigger._eid = e.target.id
                setter(autoCTrigger, JSON.stringify(trigger))

                rect = e.target.getBoundingClientRect()
                autoCDropdown.style.top = (rect.top + rect.height) + "px"
                autoCDropdown.style.left = rect.left + "px"
                autoCDropdown.style.zIndex = 15
                autocdropdown_inp = autoCDropdown.children[0].children[0].children[0].children[1].children[0]
                if (e.target.tagName === "INPUT") {
                    setter(autocdropdown_inp, e.target.value)
                } else if (e.target.tagName === "DIV") {
                    setter(autocdropdown_inp, e.target.textContent)
                }
                autocdropdown_inp.focus()
            }
            return false
        }
    })

    function autocexit () {
        trigger = JSON.parse(autoCTrigger.value)
        if (trigger) {
            if (trigger._eid) {
                cell = document.getElementById(trigger._eid)
                if (cell) {
                    setter(cell, cell.value)
                    setTimeout(
                        function () {
                            cell.focus()
                        },
                        3
                    )
                }
            }
            else {
                setTimeout(
                    function () {
                        logApi.setFocusedCell(trigger._idx, trigger._col)
                        // logApi.startEditingCell({"rowIndex": trigger._idx, "colKey": trigger._col})
                    },
                    3
                )
            }
        }
        autoCDropdown.style.zIndex = -3
    }

    autoCDropdown.addEventListener('keydown', function (e) {
        if (e.key === "Escape") {
            e.preventDefault()
            autocexit()
            return false
        }
    })

    autoCDropdown.addEventListener('focusout', function (e) {
        autocexit()
    })
}
