import __env__

_rc = {
    "w": 1,
    "m": 4,
    "q": 13,
    0: 0,
    12: 52,
    24: 104,
    48: 208,
}

performance_steps = {
    1: "Week Frames",
    4: "Month Frames",
    13: "Quarter Frames",
}
performance_steps_default = _rc[__env__.statisticsPerformanceStepsDefault]

performance_interval = {
    1: "Week Interval",
    4: "Month Interval",
    13: "Quarter Interval",
}
performance_interval_default = _rc[__env__.statisticsPerformanceIntervalDefault]

performance_frame = {
    1: "Week Frame",
    4: "Month Frame",
    13: "Quarter Frame",
}
performance_frame_default = _rc[__env__.statisticsPerformanceFrameDefault]

performance_range = {
    0: "All Time",
    52: "12 Months",
    104: "24 Months",
    208: "48 Months",
}
performance_range_default = _rc[__env__.statisticsPerformanceRangeDefault]
