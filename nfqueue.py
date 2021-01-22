import config
#from netfilterqueue import NetfilterQueue

#(sudo iptables -I INPUT -d localhost -j NFQUEUE --queue-num 1)
#setupQueue()
#checkIfQueueSetted()
'''
nfqueue = NetfilterQueue()
nfqueue.bind(1, firewall)

try:
    print("Incomming traffic:")
    nfqueue.run()
except KeyboardInterrupt:
    pass
finally:
    print("Ended")

nfqueue.unbind()
'''
