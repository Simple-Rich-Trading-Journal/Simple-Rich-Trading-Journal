try:
    import sys
    from pathlib import Path
    sys.path.append(str(Path(__file__).parent))
except Exception:
    raise

from atexit import register, unregister
from multiprocessing import Process, util
from subprocess import Popen
from time import sleep

from dash import Dash

import __ini__.cmdl
import __ini__.logtags

__project_name__ = "Simple Rich Trading Journal"


def run():
    if __ini__.cmdl.ADMINISTRATIVE:
        import __env__
    else:
        red = [sys.executable, __file__] + sys.argv[1:]
        red = Popen(red, stdin=sys.stdin, stderr=sys.stderr, stdout=sys.stdout, )
        print(__ini__.logtags.proc, red.pid)
        if not __ini__.cmdl.FLAGS.detach:
            while red.returncode is None:
                print(__ini__.logtags.proc, "communicate")
                try:
                    red.communicate()
                except KeyboardInterrupt:
                    break
            print(__ini__.logtags.proc, "exit", red.returncode)
        else:
            print(__ini__.logtags.proc, "detach")


class Server(Process):

    def run(self):
        import __env__
        import layout

        __env__.SERVER_PROC = self

        app = Dash(
            __project_name__,
            title=__env__.PROFILE or __project_name__,
            update_title="working...",
            assets_folder=__env__.DASH_ASSETS,
            assets_url_path=__env__._files.folder_profile_assets,
        )
        app.layout = layout.LAYOUT
        app._favicon = ".favicon.ico"
        try:
            import callbacks
        except Exception:
            raise
        
        if __ini__.cmdl.FLAGS.quiet:
            print(__ini__.logtags.quiet, "reassign stderr")

            class null:

                @staticmethod
                def write(*_): return
                flush = write

            sys.stderr = null

        app.run(debug=__ini__.cmdl.FLAGS.debug, host=__env__.appHost, port=__env__.appPort)


def _suppress_exc(*args, **kwargs):
    try:
        util._exit_function(*args, **kwargs)
    except KeyboardInterrupt:
        print()
        print(__ini__.logtags.server_proc, "exit 0", flush=True)


if __name__ == "__main__":
    import __env__

    if ping := __env__.ping():
        print(__ini__.logtags.ping, "was successful:", flush=True)
        print(ping.decode())
        print(__ini__.logtags.ping, "skip server start...", flush=True)
    else:
        server_proc = Server(name="srtj-server")
        server_proc.start()

        print(__ini__.logtags.server_proc, server_proc.pid, flush=True)

        # suppress exception ##############################################################################

        unregister(util._exit_function)
        register(_suppress_exc)

        ###################################################################################################

        # wait for server #################################################################################

        __env__.make_pong_file(server_proc.pid)

        for i in range(1, 21):
            print(__ini__.logtags.ping, f"({i})", __env__.URL, flush=True)
            if __env__.ping():
                break
            sleep(.1)
        else:
            print(__ini__.logtags.ping, "no success, continue...", flush=True)

        ###################################################################################################

    __env__.CALL_GUI()

    print(__ini__.logtags.main_proc, "DONE", flush=True)
