from os import scandir
from re import sub

from __env__ import _files


def make_assets():
    with (
        open(_files.proj_things_js, "wb") as js,
        open(_files.proj_things_css, "wb") as css,
    ):
        for e in scandir(_files.proj_things):

            if e.name.endswith(".js"):
                of = js
            elif e.name.endswith(".css"):
                of = css
            else:
                continue

            with open(e.path, "rb") as _if:
                of.write(
                    sub(b"(?<=\n)[\n\\s]*", b"", _if.read())
                )
