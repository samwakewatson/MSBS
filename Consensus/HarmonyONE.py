import numpy as np
from Config import Config as p
from Primitives.HarmonyONE.Node import Node
from Consensus.BaseConsensus import Consensus as BaseConsensus
import random
from statistics import median

class Consensus(BaseConsensus):

    def timeToReachConsensus():
        return 2 #this is accurate for all the shard chains, might not be for shard 0

    #determines if a validator is allowed to produce a block)
    def Protocol(miner, shard):
        voteShare = 0.3 #see harmonyONE documentation
        TOTAL_STAKE = sum([miner.committees[shard] for miner in p.NODES])
        stake = miner.committees[shard]/TOTAL_STAKE 
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
        securityParam = 600 #harmony one paper says > 600, difficult to find actual value
        
        pVote = TOTAL_STAKE/(p.numShards*securityParam)
        return int(miner.stake / pVote)


    def fork_resolution():
        BaseConsensus.global_chain = []

        longestChains = [0] * p.numShards #store node IDs that have the longest chain of each shard - note that we might have a difference of 1 block
        for i in range(0,p.Nn):
            for s in range(0,p.numShards):
                if p.NODES[i].blockchain_height(s) > longestChains[s]:
                    longestChains[s] = p.NODES[i].blockchain_height(s)
        for s in range(0, p.numShards):
            BaseConsensus.global_chain.append([])

            for i in range(0, longestChains[s]):
                for node in p.NODES:
                    if node.return_block(s, i) != 0:
                        BaseConsensus.global_chain[s].append(node.return_block(s, i))
                        break


