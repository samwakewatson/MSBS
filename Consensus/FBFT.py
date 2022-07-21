from Consensus.BaseConsensus import Consensus as BaseConsensus
from Config import Config as p
from Network.Network import Network
import math

'''ok lets try to simulate a round or two of FBFT and see how it goes

1: First the leader broadcasts the block to the validators
2: Then they check the block is valid, and sign it and send that back to the leader
3: After 2f+1 signatures, leader makes a BLS aggregrated multisig and sends that back to the validators
4: The validators check that there indeed is 2f+1 signatures, sign the message from step 3 then send it back to the leader
5: The leader waits for 2f+1 valid signatures and then commits the block, and broadcasts the block for all the validators to commit

So we want to know: the network latencies, who the leader is, which nodes are updated and how long it all takes

But we know due to the nature of the algorithm, that all non-faulty nodes will receive the update so that answers q3
We are given the first two, so we only need to convert them into a solution


for a quick approximation, surely we can just sum the network latencies and add some constant for processing time?
'''



#what do we actually want consensus class to do?
#this is to work out the per shard consensus
#so we want it to tell us: how long it takes to reach consensus, and who has received any updates to do with this consensus
#so in a PBFT system, it will take some amount of time to reach consensus, and all functional nodes will have received the update
class Consensus(BaseConsensus):
    def timeToReachConsensus(leader, committee): #leader is the id of leader, committee is list of node ids in committee
        latencies = []
        for node in committee:
            if leader > node:
                latencies.append(Network.latencyTable[node][leader])
            else:
                latencies.append(Network.latencyTable[leader][node])
        latencies.sort()
        print(latencies)
        roundDelay = max(latencies[0:math.ceil(2*len(latencies)/3)])
        return roundDelay * 5 + 1 #the second value is some constant representing the time taken due to processing

    
    def fork_resolution():
        BaseConsensus.global_chain = []
        #we need to find the longest chain for each node
        #so if we have a proper model of the consensus structure, we can 
        #need to be careful about a new epoch occurring right at the end

        #we now need to find valid bits between checkpoints
        #maybe we want to build up from genesis?
        #all nodes in the same committee should have the same epochs
        
        #iterate through the nodes until we have a target depth?
        '''for node in p.NODES:
            for s in range(0, p.numShards):'''
        
        #BELOW IS SOME AWFUL AWFUL CODE, we only need run it once though


        longestChains = [0] * p.numShards #store node IDs that have the longest chain of each shard - note that we might have a difference of like 1 block
        for i in range(0,p.Nn):
            for s in range(0,p.numShards):
                if p.NODES[i].blockchain_height(s) > longestChains[s]:
                    #longestChains[s] = i
                    longestChains[s] = p.NODES[i].blockchain_height(s)
        for s in range(0, p.numShards):
            BaseConsensus.global_chain.append([])

            '''i = 0
            while i < longestChains[s]:'''

            #this can inject invalid blocks
            for i in range(0, longestChains[s]):
                for node in p.NODES:
                    if node.return_block(s, i) != 0:
                        BaseConsensus.global_chain[s].append(node.return_block(s, i))
                        break
            #BaseConsensus.global_chain.append(p.NODES[longestChains[s]].blockchain[s])


