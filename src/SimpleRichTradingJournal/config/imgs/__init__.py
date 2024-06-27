from dash import html

here = __path__[0]


def _html_img(src):
    return html.Img(
        src=src,
        style={
            "height": 11
        }
    )


with open(here + "/cross.b64") as f:
    cross = _html_img(f.read())

with open(here + "/information.b64") as f:
    information = _html_img(f.read())

with open(here + "/refresh.b64") as f:
    refresh = _html_img(f.read())

with open(here + "/stats.b64") as f:
    stats = _html_img(f.read())
