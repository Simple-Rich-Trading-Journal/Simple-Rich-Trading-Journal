from __future__ import annotations

from ast import literal_eval

try:
    import __env__ as env
except ImportError:
    pass

from re import search, sub, DOTALL
from os import unlink, scandir


def _u5_0(profile_path: str, env=env):
    try:
        rc_path = env._files.make_path(profile_path, env._files.file_rc)
        with open(rc_path) as f:
            rc = f.read()
        if m := search("(^|\n)logColWidths.*", rc, DOTALL):
            val = ""
            sector = ""
            lines = m.group().splitlines(keepends=True)
            while lines:
                line = lines.pop(0)
                sector += line
                if not search("^\\s*#", line):
                    if _m := search("(?<==)[^]]*]?", line):
                        val += _m.group()
                        break
            if not val.endswith("]"):
                while lines:
                    line = lines.pop(0)
                    sector += line
                    if not search("^\\s*#", line):
                        if _m := search("[^]#]*]", line):
                            val += _m.group()
                            break
                        else:
                            val += line
                    else:
                        val += line
            loaded = literal_eval(val)
            logColWidths = env.logColWidths
            if len(loaded) != len(logColWidths):
                if input(f"vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv\n"
                         f"{sector}\n"
                         f"^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n"
                         f"of {profile_path}\n"
                         f"has the wrong length!\n"
                         f"  ![ This function assumes that the value is not faulty for versions <=0.4 ]\n"
                         f"Should the standard values ({logColWidths[23]=}, {logColWidths[24]=}) "
                         f"be added? > ").lower() in ("1", "y", "yes"):
                    bu_file = rc_path + "-srtj-lt0.5-backup.py"
                    print(f"[ Create Backup ] {bu_file}")
                    with open(bu_file, "w") as f:
                        f.write(rc)
                    print(f"[ Overwrite ] {rc_path}\n"
                          "-------------------------------\n")
                    _val = sub("#.*\n", "", val).replace("\n", "")
                    if search(",[^]\\d,]*]$", _val):
                        comma = "\n"
                    else:
                        comma = "  ,\n"
                    new_val = sub(
                        "]$",
                        f"{comma}"
                        f"  {env.logColWidths[23]},  # ++ since v0.5 (added by `upgrade all')\n"
                        f"  {env.logColWidths[24]},  # ++ since v0.5 (added by `upgrade all')\n"
                        f"]",
                        val
                    )
                    new_sector = sector.replace(
                        val,
                        new_val
                    )
                    rc = rc.replace(
                        sector,
                        new_sector
                    )
                    with open(rc_path, "w") as f:
                        f.write(rc)
                else:
                    print(f"[ Skip ] {rc_path}\n"
                          "-------------------------------\n")
    except FileNotFoundError:
        pass


def _u6_0(profile_path: str, env=env):
    assets = env._files.make_path(profile_path, env._files.folder_profile_assets)
    if input(f"[ clean ] This upgrade cleans the folder\n"
             f" {assets}\n"
             f"by removing all files and folders except\n"
             f" {env._files.make_path(profile_path, env._files.folder_file_clones)}.\n"
             "Make sure there are no non-project files in it!\n"
             f"done? > ").lower() in ("1", "y", "yes"):
        for e in scandir(assets):
            if e.name == env._files.folder_file_clones:
                continue
            unlink(e.path)


def call(profile_path: str, env=env):
    _u5_0(profile_path, env)
    _u6_0(profile_path, env)
