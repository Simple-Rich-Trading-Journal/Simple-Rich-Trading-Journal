async function make_quicksearch () {
    quickSearch.addEventListener('keydown', function (e) {
        if (e.ctrlKey && e.code == "Enter" && quickSearch.value) { // ctrl+<enter>
            e.preventDefault()

            setter(quickSearchReceiver, quickSearch.value)
            dispatch_event(quickSearchReceiver)

            quickSearch.style.borderStyle = "dashed"

            return false
        }
    })
    quickSearch.addEventListener('input', function (e) {
        if (!quickSearch.value) {
            e.preventDefault()

            setter(quickSearchReceiver, quickSearch.value)
            dispatch_event(quickSearchReceiver)

            quickSearch.style.borderStyle = ""

            return false
        }
    })
}
