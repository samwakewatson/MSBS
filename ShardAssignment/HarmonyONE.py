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
            for nodeID in committee[0:numReassign]:
                p.NODES[nodeID].committees = random.choice(committeeOptions) #note this can send members back to their own shard, do we want this?

    #time taken for enough (all) nodes in each committee to be synched with the overall committee
    #note this is a bit cursed as it's just an oversimplistic delay model
    def sync_delay():
        return 1
