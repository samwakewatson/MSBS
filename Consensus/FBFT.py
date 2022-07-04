from Consensus.BaseConsensus import Consensus as BaseConsensus
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

    
