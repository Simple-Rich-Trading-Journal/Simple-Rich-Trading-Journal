from pathlib import Path


def make_path(*elem):
    return str("/").join(elem)


file_rc = "rconfig.py"
file_cc = "colors.py"
file_plugin = "plugin.py"
file_call_gui = "call-gui-engine.txt"
inactive_prefix = "#"
file_journal = "journal.pkl"
file_history = "history.pkl"
file_position_colors = "position-colors.pkl"
file_column_state = "column-state.pkl"
file_column_settings = "column-settings.pkl"
file_clean_time = "cleaner.timestamp"
folder_trash = "cleaner.trash"
folder_file_clones = "clones"
folder_profile_assets = "files"
file_rc_css = ".rc.css"
file_rc_js = ".rc.js"
file_favicon = ".favicon.ico"
file_pong = ".pong"
userhome = str(Path.home())
default_install_root = userhome
proj_root = str(Path(__file__).parent.parent)
proj_things = make_path(proj_root, "things")
proj_things_assets = make_path(proj_things, "assets")
proj_things_js = make_path(proj_things_assets, ".misc.js")
proj_things_css = make_path(proj_things_assets, ".misc.css")
env = make_path(proj_root, "__env__")
profiles_home_folder = "Trading-Journals.srtj"
profile_prefix = "%"
profiles_home_path_file = make_path(userhome, ".srtj")
demo_env = make_path(proj_root, "__env__", "#demo")
demo_profiles_home_folder = "#demo"
