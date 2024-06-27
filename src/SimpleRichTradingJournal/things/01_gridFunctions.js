var dagfuncs = (window.dashAgGridFunctions = window.dashAgGridFunctions || {});

dagfuncs.dateFilterComparator = (filterLocalDateAtMidnight, cellValue) => {

    if (cellValue == null) {
        return 0;
    }

    // transaction_time_format = "%d/%m/%y %H:%M"
    const dateParts = cellValue.split(" ")[0].split("/");
    const year = Number("20" + dateParts[dateFormat.indexOf("y")]);
    const month = Number(dateParts[dateFormat.indexOf("m")]) - 1;
    const day = Number(dateParts[dateFormat.indexOf("d")]);
    const cellDate = new Date(year, month, day);

    if (cellDate < filterLocalDateAtMidnight) {
        return -1;
    } else if (cellDate > filterLocalDateAtMidnight) {
        return 1;
    }
    return 0;
};

dagfuncs.dateOrderComparator = (date1, date2) => {
    if (!date1 && !date2) {
        return 0;
    }
    if (!date1) {
        return -1;
    }
    if (!date2) {
        return 1;
    }

    function p (date) {
        timeParts = date.split(" ");
        dateParts = timeParts[0].split("/");
        HM = timeParts[1].split(":");
        year = Number("20" + dateParts[dateFormat.indexOf("y")]);
        month = Number(dateParts[dateFormat.indexOf("m")]) - 1;
        day = Number(dateParts[dateFormat.indexOf("d")]);
        return new Date(year, month, day, Number(HM[0]), Number(HM[1]));
    }

    return p(date1) - p(date2);
};

dagfuncs.timedeltaParser = (value) => {

    if (!value) {
        return null;
    }

    let inp = value;

    let timedelta = 0;

    let H = 0;
    let M = 0;
    let y = 0;
    let m = 0;
    let d = 0;

    // durationformat = y + " | " + m + " | " + d + " | " + H + " , " + M
    if (inp.includes("|")) {
      inp = inp.split("|");
      const inpN = inp.slice(-1)[0]
      if (inpN.includes(",")) {
        let HM = inpN.split(",");
        H = HM[0];
        M = HM[1];
        inp.splice(-1, 1)
      }
      y = inp[0];
      m = inp[1];
      d = inp[2];
    }
    else if (inp.includes(",")) {
        let HM = inp.split(",");
        H = HM[0];
        M = HM[1];
    }
    else {
      y = inp
    }

    timedelta = timedelta + (y ? y * 31557600 : 0);
    timedelta = timedelta + (m ? m * 2629800 : 0);
    timedelta = timedelta + (d ? d * 86400 : 0);
    timedelta = timedelta + (H ? H * 3600 : 0);
    timedelta = timedelta + (M ? M * 60 : 0);

    return timedelta;
};


dagfuncs.timedeltaFormatter = (cellValue) => {

    if (!cellValue) {
      return null;
    }

    let timedelta = cellValue;

    let y = ~~(timedelta / 31557600);
    y = y ? y.toString() : '';
    timedelta = timedelta % 31557600;

    let m = ~~(timedelta / 2629800);
    m = m ? m.toString() : '';
    if (m || y) {
      m = ("00" + m).slice(-2)
    }
    timedelta = timedelta % 2629800;

    let d = ~~(timedelta / 86400);
    d = d ? d.toString() : '';
    if (d || m) {
      d = ("00" + d).slice(-2)
    }
    timedelta = timedelta % 86400;

    let H = ~~(timedelta / 3600);
    H = H ? H.toString() : '';
    if (H || d) {
      H = ("00" + H).slice(-2)
    }
    timedelta = timedelta % 3600;

    let M = ("00" + (~~(timedelta / 60)).toString()).slice(-2);

    // durationformat = y + " | " + m + " | " + d + " | " + H + " , " + M
    const timedeltaString = y + " | " + m + " | " + d + " | " + H + " , " + M;

    return timedeltaString;
};


dagfuncs.calc = (cellValue) => {

    const npat = /[^-+*/%&|^\d\(\),. ]/;
    const swgr = /\d\,\d+[\D$]/;

    if (typeof cellValue === "string") {
        value = cellValue.replaceAll(" ", "");

        if (!value || value.match(npat)) {
          return null;
        } else if (value.includes(",") && value.includes(".")) {
            if (value.match(swgr)) {
                value = value.replaceAll(".", "");
                value = value.replaceAll(",", ".");
            }
            return eval(value);
        } else {
            value = value.replaceAll(",", ".");
            return eval(value);
        }
    } else {
        return cellValue;
    }
};


dagfuncs.tabToNextCell = (params) => {
    if (params.editing) {
        p = params.previousCellPosition.column.colId
        n = params.nextCellPosition.column.colId
        i = params.previousCellPosition.rowIndex
        if (p == "InvestAmount" && n == "InvestCourse") {
            params.api.stopEditing()
            setTimeout(
                function () {
                    logApi.setFocusedCell(i, 'InvestCourse')
                },
                3
            )
            return true
        } else if (p == "InvestCourse" && n == "InvestAmount") {
            params.api.stopEditing()
            setTimeout(
                function () {
                    logApi.setFocusedCell(i, 'InvestAmount')
                },
                3
            )
            return true
        } else if (p == "TakeAmount" && n == "TakeCourse") {
            params.api.stopEditing()
            setTimeout(
                function () {
                    logApi.setFocusedCell(i, 'TakeCourse')
                },
                3
            )
            return true
        } else if (p == "TakeCourse" && n == "TakeAmount") {
            params.api.stopEditing()
            setTimeout(
                function () {
                    logApi.setFocusedCell(i, 'TakeAmount')
                },
                3
            )
            return true
        }
    }
    return params.nextCellPosition;
}
