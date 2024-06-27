from datetime import datetime

import __env__


def make_history_list(history: list[tuple[int, int]]):
    return [
        {"value": v, "label": datetime.fromtimestamp(l).strftime(__env__.timeFormatHistory)}
        for v, l in history
    ]
