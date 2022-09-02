import numpy as np
from Config import Config as p
from Primitives.HarmonyONE.Node import Node
from Consensus.BaseConsensus import Consensus as BaseConsensus
import random
from statistics import median

class Consensus(BaseConsensus):

    #determines if a validator is allowed to produce a block at a given time 
    def Protocol(miner, shard):
        voteShare = 10 
        TOTAL_STAKE = sum([miner.committees[shard] for miner in p.NODES])
        stake = miner.committees[shard]/TOTAL_STAKE #we need to divide by the total stake on the committee, not the overall total stake
        return (random.random() < voteShare * stake)

    def calculate_effective_stakes():
        c = 0.15 # protocol parameter 
        stakes = []
        for node in p.NODES:
            stakes.append(node.stake)
        medianStake = median(stakes)
        for node in p.NODES:
            node.effectiveStake = max(min((1+c)*medianStake,node.hashPower),(1-c)*medianStake)
            

    def calculate_votes(miner):
        TOTAL_STAKE = sum([miner.stake for miner in p.NODES])
        securityParam = 600 #harmony one says > 600, maybe too high for the tiny network we're looking at, or maybe need to increase node stakes idk
        
        
        pVote = TOTAL_STAKE/(p.numShards*securityParam)
        return int(miner.stake / pVote)

    #resolve any potential forks and form the chain with majority consensus
    def fork_resolution():
        BaseConsensus.global_chain = []

        longestChains = [0] * p.numShards 
        for i in range(0,p.Nn):
            for s in range(0,p.numShards):
                if p.NODES[i].blockchain_height(s) > longestChains[s]:
                    longestChains[s] = p.NODES[i].blockchain_height(s)
        for s in range(0, p.numShards):
            BaseConsensus.global_chain.append([])

            for i in range(0, longestChains[s]+1):
                for node in p.NODES:
                    if node.return_block(s, i) != 0:
                        BaseConsensus.global_chain[s].append(node.return_block(s, i))
                        break


