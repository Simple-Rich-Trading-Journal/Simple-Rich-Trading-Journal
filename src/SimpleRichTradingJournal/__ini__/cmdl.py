
from argparse import ArgumentParser, RawDescriptionHelpFormatter, SUPPRESS

_parser = ArgumentParser(
    "srtj",
    formatter_class=RawDescriptionHelpFormatter,
    usage="srtj [-<option> ...] [<directive> ...]"
)


_parser.add_argument(
    "-d", "--detach",
    action="store_true",
    help="Skip the communication loop and release the process."
)

_parser.add_argument(
    "-q", "--quiet",
    action="store_true",
    help="Suppress outputs on stderr."
)

_parser.add_argument(
    "-p", "--ping",
    action="store_true",
    help="Ping the server url and exit (exits with 0 on success)."
)

_parser.add_argument(
    "-k", "--kill",
    action="store_true",
    help="Kill all processes of the session if the server is reachable (exits with 0 on success)."
)

_parser.add_argument(
    "-v", "--version",
    action="store_true",
    help="directive: version"
)

_parser.add_argument(
    "--help-rc",
    action="store_true",
    help="directive: help"
)

_parser.add_argument(
    "--debug",
    action="store_true",
    help=SUPPRESS
)


_parser.add_argument_group(
    "directives",
    """\
install [<path>]
    Install the journal directory (by default in the home directory).
upgrade [/ <profile>]
    Upgrade the [sub-]profile files.
upgrade all
    Upgrade all [sub-]profile files.
version
    Exit with the version number.
help
    Show the origin rconfig file on stdout and exit.
/ <profile> [<rc key> <rc value> ...]
    Load or create a sub-profile.
demo [init] [<rc key> <rc value> ...]
    Start [and initialize] the demo.
"""
)


FLAGS, DIRECTIVES = _parser.parse_known_args()

if FLAGS.help_rc:
    DIRECTIVES.insert(0, "help")
elif FLAGS.version:
    DIRECTIVES.insert(0, "version")

ADMINISTRATIVE: bool = (
    FLAGS.ping or FLAGS.kill
    or (DIRECTIVES and DIRECTIVES[0] in ("help", "version", "upgrade"))
)
