async function make_markable () {

    function mark (e) {
        i = e.target.parentElement.getAttribute("row-index")
        if (i) {
            focCell = logApi.getFocusedCell()
            row = logApi.getDisplayedRowAtIndex(focCell.rowIndex)
            elements = document.querySelectorAll('[row-index="' + i + '"]')
            if (elements[0].classList.contains("row-mark")) {
                for (let i = 0; i < elements.length; i++) {
                    elements[i].classList.remove("row-mark")
                    row.setDataValue("mark", null)
                    logApi.refreshCells({force: true, columns: ['Name']})
                }
            } else {
                for (let i = 0; i < elements.length; i++) {
                    elements[i].classList.add("row-mark")
                    row.setDataValue("mark", 1)
                    logApi.refreshCells({force: true, columns: ['Name']})
                }
            }
        }
    }

    logElement.addEventListener('click', function (e) {
        if (e.ctrlKey) {
            mark(e)
        }
    })

    logElement.addEventListener('keydown', function (e) {
        if (e.ctrlKey && e.code == ccMark) {
            e.preventDefault()
            mark(e)
            return false
        }
    })
}

