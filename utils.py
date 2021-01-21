import sys, subprocess, time, socket, errno
from datetime import datetime
from termcolor import colored as color

import config

def error(errcode, message, exitcode=1, fail=False):
    if fail:
        statusFail()
    print(color("Error", "red") + ": " + message + " (code " + str(errcode) + ")")
    exit(exitcode)

def warning(warncode, message):
    if config.verb:
        print(color("Warning", "yellow") + ": " + message + " (code " + str(warncode) + ")")

def info(message):
    if config.verb:
        print(color("Info", "cyan") + ": " + message)

def debug(message):
    if config.debug:
        print(color("Debug", "magenta") + ": " + message)

def check(message):
    if config.verb:
        print(color("Check", "blue") + ": " + message, end = '\t')

def statusOk():
    if config.verb:
        print("[" + color("OK", "green") + "]")

def statusFail():
    if config.verb:
        print("[" + color("FAIL", "red") + "]")

def dump(obj): # print object with attributes
   for attr in dir(obj):
       if hasattr(obj, attr):
            print("obj.%s = %s" % (attr, getattr(obj, attr)))

def obj(obj, name=""): # print object with keys
    debug("Object: " + name + "\n" + str(obj.__dict__))

def printwb(list): # print list, set or dict without brackets
    return ", ".join(str(i) for i in list)

def printlist(list):
    for i in list:
        print(str(i.__dict__) + "\n")

def getLogDatetime(): # FR format with day
    now = datetime.now()
    return now.strftime("%a %d/%m/%Y %H:%M:%S")

def getFullDatetime(): # FR format with day
    now = datetime.now()
    return now.strftime("%A %d-%m-%Y %H:%M:%S")

def replaceStringInFile(file, oldstr, newstr): # replace only the str
    try:
        with open(file, "r") as f:
            text = f.read().replace(oldstr, newstr)
        writeFile(file, text, "w", nl=False)
    except FileNotFoundError:
        error(70, "File '" + file + "' not found")
    except OSError:
        error(71, "Can't read file or insufficient permissions for '" + file + "'")

def replaceLineInFile(file, oldstr, newstr): # replace the whole line
    text = ""
    try:
        with open(file, "r") as f:
            for line in f:
                if oldstr in line:
                    text += newstr + "\n"
                else:
                    text += line
        writeFile(file, text, "w", nl=False)
    except FileNotFoundError:
        error(70, "File '" + file + "' not found")
    except OSError:
        error(71, "Can't read file or insufficient permissions for '" + file + "'")

def fileExist(path):
    try:
        f = open(path)
        return True
    except FileNotFoundError:
        return False
    except IOError:
        return False
    finally:
        f.close()

def writeFile(file, text, mode="a+", type="write", nl=True):
    try:
        with open(file, mode) as f:
            if nl == True:
                if type == "write":
                    f.write(text + "\n")
                elif type == "writelines":
                    f.writelines(text + "\n")
            else:
                if type == "write":
                    f.write(text)
                elif type == "writelines":
                    f.writelines(text)
    except FileNotFoundError:
        error(70, "File '" + file + "' not found")
    except OSError:
        error(72, "Can't write file or insufficient permissions for '" + file + "'")

def readFile(file, mode="r+", type="read"): # read = parse entire file as str, readline = parse by line
    try:
        with open(file, mode) as f:
            if type == "read":
                print(f.read())
            elif type == "readlines":
                print(f.readlines())
    except FileNotFoundError:
        error(70, "File '" + file + "' not found")
    except OSError:
        error(71, "Can't read file or insufficient permissions for '" + file + "'")

def createDirectory(path):
    perms = 0o755
    info("Creating '" + path + "' directory")
    try:
        os.mkdir(path, perms)
    except:
        error(73, "Can't create directory '" + path + "'")

def moveDirectory(oldpath, newpath):
    info("Moving directory '" + oldpath + "' to '" + newpath + "'")
    try:
        shutil.move(oldpath, newpath)
    except:
        error(74, "Cannot move '" + oldpath + "' maybe insufficient permissions")

def removeDirectory(path):
    info("Removing '" + path + "' directory")
    try:
        shutil.rmtree(path)
    except:
        error(75, "Can't delete directory '" + path + "' ")

def checkIfPortInUse(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind(("localhost", int(port)))
        return True
    except socket.error as e:
        if e.errno == errno.EADDRINUSE:
            return False
        else:
            error(111, "Socket bind failed while testing if port is in use: " + str(e))
    s.close()

#exec linux command. Capture= stdout + stderr, secs= before timeout, merge= stderr in stdout, workdir= set workdir path, nl= newline
def cmd(command, capture=True, secs=3, merge=False, workdir=None, nl=True):
    if merge:
        errpipe = subprocess.STDOUT
    else:
        errpipe = subprocess.PIPE

    if not capture: # 2>&1 /dev/null
        outpipe = subprocess.DEVNULL
        errpipe = subprocess.DEVNULL
    else:
        outpipe = subprocess.PIPE

    process = subprocess.run(command,
                        stdout=outpipe,
                        stderr=errpipe,
                        universal_newlines=nl,
                        shell=True,
                        cwd=workdir,
                        timeout=secs)
    if config.debug:
        debug("\n>>> CMD"
        + "\n\tstdin: '" + command + "'"
        + "\n\texitcode: " + str(process.returncode)
        + "\n\tstdout: " + process.stdout
        + "\n\tstderr: " + process.stderr
        + "\n\ttimeout: " + str(secs) + " secs"
        + "\n\tmerge: " + str(merge)
        + "\n\tworkdir: " + str(workdir)
        + "\n\tcapture: " + str(capture)
        + "\n<<< CMD")
    return process
