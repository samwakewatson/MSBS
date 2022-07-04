from Consensus.BaseConsensus import Consensus as BaseConsensus
from Network.Network import Network
import Config as p

'''ok lets try to simulate a round or two of PBFT and see how it goes'''

#what do we actually want consensus class to do?
#this is to work out the per shard consensus
#so we want it to tell us: how long it takes to reach consensus, and who has received any updates to do with this consensus
#so in a PBFT system, it will take some amount of time to reach consensus, and all functional nodes will have received the update
class Consensus(BaseConsensus):
    def timeToReachConsensus():
        return 1
