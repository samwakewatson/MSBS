import numpy as np
from Config import Config as p
from Primitives.HarmonyONE.Node import Node
from Consensus.BaseConsensus import Consensus as BaseConsensus
import random
from statistics import median

#Need massive changes here - Epoch based PoS
class Consensus(BaseConsensus):

    """
	We modelled PoW consensus protocol by drawing the time it takes the miner to finish the PoW from an exponential distribution
        based on the invested hash power (computing power) fraction
    """
    ##This needs to go, does it though? - is this so different from being elected based on stake? or do we know that stake has a different distribution?
    '''def Protocol(miner):
        ##### Start solving a fresh PoW on top of last block appended #####
        TOTAL_HASHPOWER = sum([miner.hashPower for miner in p.NODES])
        hashPower = miner.hashPower/TOTAL_HASHPOWER
        return random.expovariate(hashPower * 1/p.Binterval)'''

    #We only model for the validating nodes - percentage hashpower can be viewed as the same as the active stake
    '''def Protocol(miner):
        voteShare = 0.5
        TOTAL_STAKE = sum([miner.hashPower for miner in p.NODES])
        stake = miner.hashPower/TOTAL_STAKE
        return (random.random() < voteShare * stake)'''

    #determines if a validator is allowed to produce a block at a given time (i.e. when called)
    #Note this is currently redundant
    def Protocol(miner, shard):
        voteShare = 0.3 #this doesn't really make a great deal of sense in the current system
        TOTAL_STAKE = sum([miner.committees[shard] for miner in p.NODES])
        stake = miner.committees[shard]/TOTAL_STAKE #we need to divide by the total stake on the committee, not the overall total stake
        return (random.random() < voteShare * stake)

    def calculate_effective_stakes():
        #we just want to assign each node a slot based on their votes?
        c = 0.15 # protocol parameter - probably not the same as used in harmony ONE?
        stakes = []
        for node in p.NODES:
            stakes.append(node.stake)
        medianStake = median(stakes)
        for node in p.NODES:
            node.effectiveStake = max(min((1+c)*medianStake,node.hashPower),(1-c)*medianStake)
            #print(node.effectiveStake)

    #SUS AF - doesn't actually do anything even vaguely similar to what we want to do
    def assign_leaders():
        p.slotLeaders = []
        for s in range(0,p.numShards):
            x = []
            for node in p.NODES:
                if node.committees[s] != 0:
                    x.append(node)
            p.slotLeaders.append(x)
            
    #this probably shouldn't be here
    def calculate_votes(miner):
        TOTAL_STAKE = sum([miner.stake for miner in p.NODES])
        securityParam = 600 #harmony one says > 600, maybe too high for the tiny network we're looking at, or maybe need to increase node stakes idk
        #implementing Harmony ONE's Pvote method                            
        # 
        
        
        pVote = TOTAL_STAKE/(p.numShards*securityParam)
        return int(miner.stake / pVote)

        #convert each miner's stake into a number of votes
        #randomly assign each vote to a committee
        #badabing badaboom 


    """
	This method apply the longest-chain approach to resolve the forks that occur when nodes have multiple differing copies of the blockchain ledger
    
    We want to alter this to represent different ways of picking the longest chain (i.e. ouroboros picking most "dense" chain)
    We also need it to work shardwise
    """
    #this works globally - doesn't really matter rn except for outputting stats that work and look nice
    #as a hacky fix we can just take the chain from node 0? will need fixing later
    '''def fork_resolution():
        return 0
        BaseConsensus.global_chain = [] # reset the global chain before filling it
        
        #this determines the length of the longest global chain
        a=[]
        for i in p.NODES:
            a+=[i.blockchain_length()]
        x = max(a)

        
        b=[]
        z=0
        for i in p.NODES:
            if i.blockchain_length() == x:
                b+=[i.id]
                z=i.id

        if len(b) > 1:
            c=[]
            for i in p.NODES:
                if i.blockchain_length() == x:
                    c+=[i.last_block().miner]
            z = np.bincount(c)
            z= np.argmax(z)

        for i in p.NODES:
            if i.blockchain_length() == x and i.last_block().miner == z:
                for bc in range(len(i.blockchain)):
                    BaseConsensus.global_chain.append(i.blockchain[bc])
                break'''

    #OMEGA CURSED - just takes the blockchain of the first node, needs urgent fixing
    #def fork_resolution():
    #s    BaseConsensus.global_chain=p.NODES[0].blockchain

    def fork_resolution():
        #we need to find the longest chain for each node
        #so if we have a proper model of the consensus structure, we can 
        #need to be careful about a new epoch occurring right at the end

        #we now need to find valid bits between checkpoints
        #maybe we want to build up from genesis?
        #all nodes in the same committee should have the same epochs
        
        #iterate through the nodes until we have a target depth?
        '''for node in p.NODES:
            for s in range(0, p.numShards):'''



        longestChains = [0] * p.numShards #store node IDs that have the longest chain of each shard - note that we might have a difference of like 1 block
        for i in range(0,p.Nn):
            for s in range(0,p.numShards):
                if len(p.NODES[i].blockchain[s]) > len(p.NODES[longestChains[s]].blockchain[s]):
                    longestChains[s] = i
            BaseConsensus.global_chain.append(p.NODES[longestChains[s]].blockchain[s])


