import numpy as np
from Config import Config as p
from Primitives.HarmonyONE.Node import Node
from Consensus.BaseConsensus import Consensus as BaseConsensus
import random
from statistics import median

class ShardAssignment:
    def assign_leaders():
        p.slotLeaders = []
        for s in range(0,p.numShards):
            x = []
            for node in p.NODES:
                if node.committees[s] != 0:
                    x.append(node)
            p.slotLeaders.append(x)

    def shuffle_committees():
        committeeOptions = []
        for i in range(0,p.numShards):
            x = np.zeros(p.numShards)
            x[i] = 1
            committeeOptions.append(x)

        for s in range(0,p.numShards):
            committee = [node.id for node in p.NODES if node.committees[s] != 0]
            numReassign = int(p.cuckooRuleConstant * len(committee))
            random.shuffle(committee)
            for nodeID in committee:
                p.NODES[nodeID].committees = random.choice(committeeOptions) #note this can send members back to their own shard, do we want this?


