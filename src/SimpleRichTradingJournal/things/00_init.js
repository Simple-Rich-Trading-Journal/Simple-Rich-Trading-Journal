if (!window.dash_clientside) {
    window.dash_clientside = {}
    var __setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, "value").set
}

function dispatch_event (ele) {
    var client_event = new Event('input', { bubbles: true })
    ele.dispatchEvent(client_event)
}

function setter (ele, val) {
    __setter.call(ele, val)
    var client_event = new Event('input', { bubbles: true })
    dispatch_event(ele)
}

function make_esc_trigger () {
    window.addEventListener('keydown', function (e) {
        if (e.key == "Escape") {
            setter(esc_trigger, e.timeStamp)
        }
    })
}
