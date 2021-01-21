import config, utils

def checkArgAction(action):
    check("Action argument")
    if action not in config.actions:
        if not action:
            error(0, "No action given", fail=True)
        else:
            error(1, "Unknown action '" + action + "'", fail=True)
    statusOk()

def checkArgs(args):
    if args.version:
        info("UFWQ v." + str(currentVersion) + " - " + str(lastUpdateDate))
        exit(0)
    if args.debug:
        config.debug = True
        args.verbose = True
        info("Debug [" + color("ON", "green") + "]")
    if args.verbose:
        config.verb = True
        info("Verbose [" + color("ON", "green") + "]")
    debug("arg_action=" + str(args))

def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument("action", nargs='?', help="status, allow, deny, load, save, start, stop, restart, enable, disable, reset, log")
    parser.add_argument("rule", nargs='?', help="")
    parser.add_argument("-d", "--debug", action="store_true", help="debug mode (activate verbose)")
    parser.add_argument("-v", "--verbose", action="store_true", help="increase verbosity")
    parser.add_argument("-V", "--version", action="store_true", help="show version")
    return parser.parse_args()
