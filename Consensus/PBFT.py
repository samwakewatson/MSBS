from Consensus.BaseConsensus import Consensus as BaseConsensus
from Network.Network import Network
import Config as p


class Consensus(BaseConsensus):
    def timeToReachConsensus(leader, committee): #leader is the id of leader, committee is list of node ids in committee
        return 1

    
