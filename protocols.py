import config

protocolsList = {
    'ftp': 21,
    'ssh': 22,
    'sftp': 22,
    'scp': 22,
    'telnet': 23,
    'smtp': 25,
    'dns': 53,
    'http': 80,
    'pop3': 110,
    'nntp': 119,
    'ntp': 123,
    'imap': 143,
    'snmp': 161,
    'irc': 194,
    'ldap': 389,
    'https': 443,
    'smb': 445,
    'smtp': 465,
    'syslog': 514,
    'ldaps': 636,
    'telnets': 992,
    'imaps': 993,
    'ircs': 994,
    'pop3': 995
}

def getPortNumber(name):
    if name not in protocols:
        error(100, "Protocol not found, enter port number", 1, True)
    if config.debug:
        print("Port number found for " + name + ": " + protocolsList[name])
    return protocolsList[name]
