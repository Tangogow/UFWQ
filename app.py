#!/usr/bin/python3

# sudo iptables -I INPUT -d localhost -j NFQUEUE --queue-num 1
# sudo python3 nfq.py
# echo text | netcat 10.0.0.0 12

import sys, subprocess, datetime
from scapy.all import *
#import urllib.request
import config, protocols

db = ""
wl_addr = []
bl_addr = []
wl_rule = []
bl_rule = []
bl_port = [80, 443]
debug = True

def downloadDB():
    with urllib.request.urlopen("http://urlhaus.abuse.ch/downloads/text_recent/") as f:
        html = f.read().decode('utf-8')
    return html

def blockIP(ip, port):
    if not port:
        p = subprocess.Popen(["iptables", "-A", "INPUT", "-s", ip, "-j", "DROP"], stdout=subprocess.PIPE)
        output , err = p.communicate()
        print(output)
    else:
        p = subprocess.Popen(["iptables", "-A", "INPUT", "-s", ip, "-p", "tcp", "--destination-port", port, "-j", "DROP"], stdout=subprocess.PIPE)
        output , err = p.communicate()
        print(output)

def blockPort(port):
    p = subprocess.Popen(["iptables", "-A", "INPUT", "-s", ip, "-j", "DROP"], stdout=subprocess.PIPE)
    output , err = p.communicate()
    print(output)

def logfile(message, info, packet):
    f = open('/var/log/nfqueue_' + str(datetime.date.today()), 'a+')
    f.write(message + " " + str(info) + " " + str(packet) + "\n")
    f.close

def printlog(message, info, packet=None, accept=None):
    print(message, info)
    logfile(message, info, packet)
    if accept:
        packet.accept()
    elif not accept:
        packet.drop()
    else:
        pass

def firewall2(packet):
    pkt = IP(packet.get_payload())
    src = pkt[IP].src
    dst = pkt[IP].dst
    info = str(src) + " -> " + str(dst)
    if debug:
        print(packet, info)
    if pkt.haslayer(TCP):
        dport = pkt[TCP].dport
        info += ":" + str(dport)
        rule = [src, dst, str(dport)]
        if dport in bl_port:
            printlog("DROP: blocked port ", info, packet, False)
        elif src in wl_addr:
            printlog("ACCEPT: whitelisted address ", info, packet, True)
        elif src in bl_addr:
            printlog("DROP: blacklisted address ", info, packet, False)
        elif rule in wl_rule:
            printlog("ACCEPT: whitelisted rule ", info, packet, True)
        elif rule in bl_rule:
            printlog("DROP: blacklisted rule  ", info, packet, False)
        else:
            print("Hint: Yes/No/Skip/YesRule/YesAddr/NoRule/NoAddr OR skip and show Whitelist/Blacklist for Address/Rules/Ports.")
            new = input("NEW: " + info + " [y/n/s/yr/ya/nr/na] or [wa/ba/wr/br/p] ? ")
            if new == "y":
                printlog("ACCEPTED: ", info, packet, True)
            elif new == "n":
                printlog("DROPPED: ", info, packet, True)
            elif new == "ya":
                printlog("WHITELISTED ADDRESS: ", info, packet, True)
                wl_addr.append(src)
            elif new == "yr":
                printlog("WHITELISTED RULE: ", info, packet, True)
                wl_rule.append(rule)
            elif new == "na":
                printlog("BLACKLISTED ADDRESS: ", info, packet, False)
                bl_addr.append(src)
            elif new == "nr":
                printlog("BLACKLISTED RULE: ", info, packet, False)
                bl_rule.append(rule)
            elif new == "wa":
                printlog("WHITELIST ADDRESS: ", str(wl_addr), packet, False)
            elif new == "ba":
                printlog("BLACKLIST ADDRESS: ", str(bl_addr), packet,  False)
            elif new == "wr":
                printlog("WHITELIST RULES: ", str(wl_rule), packet,  False)
            elif new == "br":
                printlog("BLACKLIST RULES: ", str(bl_rule), packet,  False)
            elif new == "p":
                printlog("BLOCKED PORT: ", str(bl_port), packet,  False)
            else:
                printlog("SKIPPED: ", info, packet, False)

if __name__ == '__main__':
    print(""" MENU
    Show blacklisted addresses
    Show blacklisted rules

    Show whitelisted rules
    Show whitelistes addresses

    Add rule
    Delete rule

    View log # tail /var/log

    Show blocked ports
    Show blacklisted database

    """)
    choice = input("Choice: ")
    print(protocols.getPortNumber(choice))
