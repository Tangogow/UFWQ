#!/usr/bin/python3

# sudo iptables -I INPUT -d localhost -j NFQUEUE --queue-num 1
# sudo python3 nfq.py
# echo text | netcat 10.0.0.0 12

import sys, subprocess, datetime
from scapy.all import *
from netfilterqueue import NetfilterQueue
#import urllib.request

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

def printlog(message, info):
    print(message, str(info))
    packet.drop()
    #f = open('/var/log/nfqueue_' + datetime.date.today(), 'a+')
    #f.write(message)
    #f.close

def firewall(packet):
    pkt = IP(packet.get_payload())
    src = pkt[IP].src
    dst = pkt[IP].dst
    info = str(src) + " -> " + str(dst)
    if src in db:
        printlog("DROP: blacklisted IP in database")
        bl_addr.append(src)
        packet.drop()
    if debug:
        printlog(packet, info)
    if pkt.haslayer(TCP):
        dport = pkt[TCP].dport
        info += ":" + str(dport)
        rule = [src, dst, str(dport)]
        if dport in bl_port:
            printlog("DROP: blocked port ", str(info))
            packet.drop()
        elif src in wl_addr:
            printlog("ACCEPT: whitelisted address ", str(info))
            packet.accept()
        elif src in bl_addr:
            printlog("DROP: blacklisted address ", str(info))
            packet.drop()
        elif rule in wl_rule:
            printlog("ACCEPT: whitelisted rule ", str(info))
            packet.accept()
        elif rule in bl_rule:
            printlog("DROP: blacklisted rule  ", str(info))
            packet.drop()
        else:
            print("Hint: Yes/No/Skip/YesRule/YesAddr/NoRule/NoAddr OR skip and show Whitelist/Blacklist for Address/Rules/Ports.")
            new = input("NEW: " + info + " [y/n/s/yr/ya/nr/na] or [wa/ba/wr/br/p] ? ")
            if new == "y":
                printlog("ACCEPTED: ", str(info))
                packet.accept()
            elif new == "n":
                printlog("DROPPED: ", str(info))
                packet.accept()
            elif new == "ya":
                printlog("WHITELISTED ADDRESS: ", str(info))
                packet.accept()
                wl_addr.append(src)
            elif new == "yr":
                printlog("WHITELISTED RULE: ", str(info))
                packet.accept()
                wl_rule.append(rule)
            elif new == "na":
                printlog("BLACKLISTED ADDRESS: ", str(info))
                packet.drop()
                bl_addr.append(src)
            elif new == "nr":
                printlog("BLACKLISTED RULE: ", str(info))
                packet.drop()
                bl_rule.append(rule)
            elif new == "wa":
                printlog("WHITELIST ADDRESS: ", str(wl_addr))
                packet.drop()
            elif new == "ba":
                printlog("BLACKLIST ADDRESS: ", str(bl_addr))
                packet.drop()
            elif new == "wr":
                printlog("WHITELIST RULES: ", str(wl_rule))
                packet.drop()
            elif new == "br":
                printlog("BLACKLIST RULES: ", str(bl_rule))
                packet.drop()
            elif new == "p":
                printlog("BLOCKED PORT: ", str(bl_port))
                packet.drop()
            else:
                printlog("SKIPPED: ", str(info))
                packet.drop()

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

Setup queue
""")

if __name__ == '__main__':
    choice = input("Choice: ")
    print(protocols.getPortNumber(choice))
