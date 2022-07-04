import random
import numpy 
from Config import Config as p

#This is very simplistic and also does not retain the same values for each pair of nodes. 
#We want to expand this and also allow us to change the values as time goes on, i.e. schedule in nodes going offline etc.
#Note that this will massively increase the overall complexity

'''
class Network:
    
    # Delay for propagating blocks in the network
    def block_prop_delay():
        return random.expovariate(1/p.Bdelay)

    # Delay for propagating transactions in the network
    def tx_prop_delay():
        return random.expovariate(1/p.Tdelay)

'''


    
class Network:

    #Note this is not currently symmetric, so we have some bizarre consistency stuff, try to alter this
    latencyTable = numpy.zeros((p.Nn, p.Nn))
    for i in range (0, p.Nn):
        for j in range(i, p.Nn):
            latencyTable[i][j] = random.expovariate(1/p.Bdelay)
            #latencyTable[i][j] = random.uniform(0,p.Bdelay)

    #for i in range(0,p.Nn):
    #    latencyTable[0][i] = 100
    #    latencyTable[i][0] = 100
    #latencyTable = [p.Nn][p.Nn]

    #def __init__(self):
        #self.latencyTable = [p.Nn][p.Nn]
    #    for i in range (0, p.Nn-1):
    #        for j in range(0, p.Nn-1):
    #            self.latencyTable[i][j] = random.expovariate(1/p.Bdelay)

    
    #make this actually work, and add another function to put a node back online
    def node_offline(self, node):
        self.latencyTable[node] = numpy.zeros(p.Nn)
    
    def block_prop_delay(self, miner, recipient):
        if miner > recipient:
            return self.latencyTable[recipient][miner]
        else:
            return self.latencyTable[miner][recipient]

    # Delay for propagating transactions in the network
    def tx_prop_delay():
        return random.expovariate(1/p.Tdelay)

