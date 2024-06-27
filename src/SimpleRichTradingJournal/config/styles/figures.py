import __env__


size_open_positions = __env__.statisticsOpenPositionsGraphSize
size_all_positions = __env__.statisticsAllPositionsGraphSize
size_slider_kwargs_performance = dict(
    min=500, max=6000, step=500, value=__env__.statisticsPerformanceGraphSize,
)
size_slider_kwargs_pop = dict(
    min=500, max=6000, step=500, value=__env__.statisticsPopGraphSize,
)

color_bg_plot = __env__.color_theme.figure_plot
color_bg_paper = __env__.color_theme.figure_paper
color_fg_plot = __env__.color_theme.figure_font
color_grid_y = __env__.color_theme.figure_grid
color_spike_y = __env__.color_theme.figure_spike
spike_thickness_y = 1

color_grid_x = color_grid_y
color_spike_x = color_spike_y
spike_thickness_x = spike_thickness_y


