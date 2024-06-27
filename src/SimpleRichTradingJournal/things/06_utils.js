function syncColumns (_) {
    function refresh () {
        logApi.refreshCells({force: true, columns: ['Name', 'n', 'InvestTime', 'InvestAmount', 'InvestCourse', 'TakeTime', 'TakeAmount', 'TakeCourse', 'ITC', 'Profit', 'Performance', 'Dividend']})
    }
    refresh()
    setTimeout(refresh, 1)
    return window.dash_clientside.no_update
}