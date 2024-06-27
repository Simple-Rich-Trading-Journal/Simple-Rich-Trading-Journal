from __future__ import annotations

from datetime import datetime
from re import search

import __env__


def tradetimeparser(spec: str):
    if spec:
        now = datetime.now()
        # n N 0 # -> $now
        if m := search("^[nN0#]$", spec):
            date = now
        # MM
        elif m := search("^(\\d{1,2})$", spec):
            date = datetime(now.year, now.month, now.day, now.hour, int(m.group(1)))
        # HH:MM
        elif m := search("^(\\d{1,2})[ .,:/-]?(\\d\\d)$", spec):
            date = datetime(now.year, now.month, now.day, int(m.group(1)), int(m.group(2)))
        # dd/HH:MM
        elif m := search("^(\\d{1,2})[ .,:/-]?(\\d\\d)[ .,:/-]?(\\d\\d)$", spec):
            date = datetime(now.year, now.month, int(m.group(1)), int(m.group(2)), int(m.group(3)))
        # dd/mm/HH:MM
        elif m := search("^(\\d{1,2})[ .,:/-]?(\\d\\d)[ .,:/-]?(\\d\\d)[ .,:/-]?(\\d\\d)$", spec):
            date = datetime(now.year, int(m.group(2)), int(m.group(1)), int(m.group(3)), int(m.group(4)))
        # dd/mm/yy/HH:MM
        elif m := search("^(\\d{1,2})[ .,:/-]?(\\d\\d)[ .,:/-]?(\\d\\d)[ .,:/-]?(\\d\\d)[ .,:/-]?(\\d\\d)$", spec):
            date = datetime(int(m.group(3)), int(m.group(2)), int(m.group(1)), int(m.group(4)), int(m.group(5)))
        else:
            raise ValueError("FormatError: %r" % spec)
        return date.strftime(__env__.timeFormatTransaction)
    else:
        return ""


def datetime_from_tradetimeformat(spec: str, default=None):
    try:
        return datetime.strptime(spec, __env__.timeFormatTransaction)
    except (ValueError, TypeError):
        return default


def do_add_row(table_data: list[dict]) -> bool:
    try:
        row0 = table_data[0]
    except IndexError:
        return True
    if ((N := row0.get("n")) or 0) < 0:
        return True
    elif N is not None:
        if row0.get("InvestTime") and (row0.get("InvestAmount") or row0.get("InvestCourse") or row0.get("ITC")):
            return True
        elif row0.get("TakeTime") and (row0.get("TakeAmount") is not None or row0.get("TakeCourse") is not None or row0.get("ITC")):
            return True


def durationformat(duration: float) -> str:
    duration = int(duration)
    y = str((duration // 31557600) or "")
    duration = (duration % 31557600)
    m = str((duration // 2629800) or "")
    if m or y:
        m = ("00" + m)[-2:]
    duration = (duration % 2629800)
    d = str((duration // 86400) or "")
    if d or m:
        d = ("00" + d)[-2:]
    duration = (duration % 86400)
    H = str((duration // 3600) or "")
    if H or d:
        H = ("00" + H)[-2:]
    duration = (duration % 3600)
    M = str((duration // 60) or "")
    return y + " | " + m + " | " + d + " | " + H + " , " + M


def preventZeroDiv(a, b, default):
    try:
        return a / b
    except ZeroDivisionError:
        return default
