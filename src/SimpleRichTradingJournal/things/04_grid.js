var winWidth = null
var winHeight = null
var isDown = false
var isHover = false
var minWidth = null
var maxWidth = null
var defWidth = null

function c2Hide (doHide) {
    if (doHide % 2) {
        if (gridC1.classList.contains('col-div-flex')) {
            gridC1.classList.remove('col-div-flex')
        }
        gridC1.style.width = winWidth  + 'px'
        if (gridC2.classList.contains('col-div-flex')) {
            gridC2.classList.remove('col-div-flex')
        }
        gridC2.style.width = '0px'
        docRoot.style.setProperty('--handle-x', winWidth + 'px')
        docRoot.style.setProperty('--handle-xi', '0px')
    }
    else if (gridC2.clientWidth == 0) {
        if (gridC1.classList.contains('col-div-flex')) {
            gridC1.classList.remove('col-div-flex')
        }
        gridC1.style.width = (winWidth - defWidth)  + 'px'
        if (gridC2.classList.contains('col-div-flex')) {
            gridC2.classList.remove('col-div-flex')
        }
        gridC2.style.width = defWidth + 'px'
        docRoot.style.setProperty('--handle-x', defWidth + 'px')
        docRoot.style.setProperty('--handle-xi', (winWidth - defWidth) + 'px')
    }
    return 0
}


async function make_wingrid () {

    mouseInbottomBar = false

    bottomBar.addEventListener(
        'mouseout',
        function (e) {
                mouseInbottomBar = false
                setTimeout(
                function () {
                    if (mouseInbottomBar) {
                        return
                    }
                    bottomBar.style.display = "none"
                },
                30
            )
        }
    )
    gridR3.addEventListener(
        'mouseover',
        function (e) {
            mouseInbottomBar = true
            bottomBar.style.display = ""
        }
    )

    function resizeGrid (e) {
        winWidth = (window.innerWidth > 0) ? window.innerWidth : screen.width
        winHeight = (window.innerHeight > 0) ? window.innerHeight : screen.height
        docRoot.style.setProperty('--handle-x', maxWidth + 'px')
        docRoot.style.setProperty('--handle-xi', (winWidth - maxWidth) + 'px')
        gridR3.style.height = gridRow3Height + 'px'
        gridR2.style.height = (winHeight - gridRow3Height - gridR1.clientHeight) + 2 + 'px'
        defWidth = winWidth * gridDefWidthScale
        minWidth = winWidth * gridMinWidthScale
        maxWidth = winWidth - minWidth
        var cl = this.document.querySelector('.col-div')
        if (cl) {
            docRoot.style.setProperty('--handle-x', (cl.offsetWidth) + 'px')
            docRoot.style.setProperty('--handle-xi', (winWidth - (cl.offsetWidth)) + 'px')
        }
    }
    resizeGrid()
    function moveTo (e) {
        if (e.clientX > minWidth && e.clientX < maxWidth) {
            if (gridC1.classList.contains('col-div-flex')) {
                gridC1.classList.remove('col-div-flex')
            }
            gridC1.style.width = e.clientX  + 'px'
            if (gridC2.classList.contains('col-div-flex')) {
                gridC2.classList.remove('col-div-flex')
            }
            gridC2.style.width = winWidth - e.clientX  + 'px'
            docRoot.style.setProperty('--handle-x', (e.clientX) + 'px')
            docRoot.style.setProperty('--handle-xi', (winWidth - (e.clientX)) + 'px')
        }
    }
    window.addEventListener('DOMContentLoaded', resizeGrid)
    window.addEventListener('resize', resizeGrid)
    docRoot.addEventListener('mousedown', function (e) {
        if (isHover) {
            isDown = true
        }
    }, true)
    document.addEventListener('mouseup', function (e) {
        isDown = false
        if (isHover) {
            //...
        }
    }, true)
    document.addEventListener('mousemove', function (e) {
        if (isDown) {
            moveTo(e)
        }
    })
    gridSplitter.addEventListener('mouseenter', function (e) {
        isHover = true
        gridSplitter.style.cursor = 'col-resize'
    })
    gridSplitter.addEventListener('mouseout', function (e) {
        isHover = false
    })
    gridSplitter.addEventListener('dblclick', function (e) {
        let defWidth2 = winWidth - defWidth
        let c1W = defWidth
        let c2W = defWidth2

        if ((defWidth * 0.09) <= gridC1.clientWidth && gridC1.clientWidth <= (defWidth * 1.01)) {
            c1W = defWidth2
            c2W = defWidth
        }
        gridC1.style.width = c1W  + 'px'
        gridC2.style.width = c2W  + 'px'
        docRoot.style.setProperty('--handle-x', c1W + 'px')
        docRoot.style.setProperty('--handle-xi', (winWidth - c1W) + 'px')
    })
}


async function make_draggable (container, receiver) {
    dragul = dragula([container])
    dragul.on("drop", function (el, target, source, sibling) {
        var result = {
            'element': el.id,
            'target_id': target.id,
            'target_children': Array.from(target.children).map(function (child) {return child.id})
        }
        if (source.id != target.id) {
            result['source_id'] = source.id
            result['source_children'] = Array.from(source.children).map(function (child) {return child.id})
        }
        setter(receiver, JSON.stringify(result))
    })
}
