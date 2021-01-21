import config

#(sudo iptables -I INPUT -d localhost -j NFQUEUE --queue-num 1)
#setupQueue()
#checkIfQueueSetted()

nfqueue = NetfilterQueue()
nfqueue.bind(1, firewall)
#db = downloadDB()
try:
    print("Incomming traffic:")
    nfqueue.run()
except KeyboardInterrupt:
    pass
finally:
    print("Ended")

nfqueue.unbind()
