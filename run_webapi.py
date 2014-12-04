from webapi import app

import argparse
parser = argparse.ArgumentParser(description='Development Server Help')
parser.add_argument("-d", "--debug", action="store_true", dest="debug_mode",
              help="run in debug mode (for use with PyCharm)", default=False)
parser.add_argument("-p", "--port", dest="port",
              help="port of server (default:%(default)s)", type=int, default=5000)
parser.add_argument("-i", "--ip", dest="host",
              help="ip of server (default:%(default)s)", type=str, default='127.0.0.1')

cmd_args = parser.parse_args()
app_options = {"port": cmd_args.port, "host": cmd_args.host}

if cmd_args.debug_mode:
    app_options["debug"] = True
    app_options["use_debugger"] = True
    app_options["use_reloader"] = False

app.run(**app_options)
