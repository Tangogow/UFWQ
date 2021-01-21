import datetime

# version
currentVersion = "0.1.0"
lastUpdateDate = "21/01/2021"

# args globals

# read /etc/config
verb = True
debug = False
actions = ["start", "stop", "restart"]

defaultSavePath = "~"
defaultSaveFormat = "ufwq_" + str(datetime.date.today()) + ".save"

bl_port = [80, 443]
