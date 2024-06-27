import __env__

from .autocomplete import *
from .clientside import *
from .columnstate import *
from .courseupdate import *
from .main import *
from .note import *
from .onoffbuttons import *
from .openmodal import *
from .scopes import *
from .wingrid import *
from .exiting import *


clientside_callback(
    """async function (_) {
        logApi = await dash_ag_grid.getApiAsync('logElement')

        docRoot = document.documentElement
        gridSplitter = document.getElementById('gridSplitter')
        gridC1 = document.getElementById('gridC1')
        gridC2 = document.getElementById('gridC2')
        gridR1 = document.getElementById('gridR1')
        gridR2 = document.getElementById('gridR2')
        gridR3 = document.getElementById('gridR3')
        bottomBar = document.getElementById('bottomBar')
        dragContainer = document.getElementById('dragContainer')
        dragContainer2 = document.getElementById('dragContainer2')
        dragEventReceiver = document.getElementById('dragEventReceiver')
        dragEventReceiver2 = document.getElementById('dragEventReceiver2')
        editEventReceiver = document.getElementById('editEventReceiver')
        logElement = document.getElementById('logElement')
        autoCDropdown = document.getElementById('autoCDropdown')
        autoCTrigger = document.getElementById('autoCTrigger')
        notepaperContainer = document.getElementById('notepaperContainer')
        notepaperElement = document.getElementById('notepaperElement')
        noteEditorContainer = document.getElementById("noteEditorContainer")
        noteContentPipe = document.getElementById('noteContentPipe')
        noteFileClonePipe = document.getElementById('noteFileClonePipe')
        noteEditorFileRequest = document.getElementById('noteEditorFileRequest')
        noteFileCloneC = document.getElementById('noteFileCloneC')
        groupBySettings = document.getElementById('groupBySettings')
        quickSearch = document.getElementById('quickSearch')
        quickSearchReceiver = document.getElementById('quickSearchReceiver')
        
        esc_trigger = document.getElementById('esc_trigger')

        noteEditor = CodeMirror(noteEditorContainer, {
                lineNumbers: true,
                mode: 'markdown',
                autoCloseBrackets: true,
                matchBrackets: true,
        })

        logApi.setFocusedCell(0, 'Name')

        make_wingrid()
        make_draggable(dragContainer, dragEventReceiver)
        make_draggable(dragContainer2, dragEventReceiver2)
        if (!%d) {
            make_copypaste()
        }
        make_autocomplete()
        make_note(%d)
        make_quicksearch()
        make_markable()
        
        make_esc_trigger()
        
        document.documentElement.setAttribute("data-bs-theme", %r)

        return window.dash_clientside.no_update
    }""" % (
        __env__.disableCopyPaste,
        int(__env__.noteFileDropCloner and __env__.noteFileDropCloner != '0'),
        ("dark" if __env__.colorTheme == "dark" else "light")
    ),
    Output(layout.init_done_trigger, "id"),
    Input(layout.init_done_trigger, "n_clicks"),
    prevent_initial_call=True
)


@callback(
    Output(layout.init_trigger, "n_clicks"),
    Input(layout.init_trigger, "id"),
)
def init(_): return 1
