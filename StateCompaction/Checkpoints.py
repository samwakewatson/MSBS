from Config import Config as p
match p.shardConsensus:
    case 1:
        from Consensus.HarmonyONE import Consensus as c
    case 2:
        from Consensus.HarmonyONE import Consensus as c
    case 3:
        from Consensus.SlotBased import Consensus as c
'''We want to model the node only downloading the blocks it needs
So in the case of checkpointing (in harmonyONE for example) we only need
the checkpoint blocks and however many blocks currently exist

What do we want this module to do?
    Simulate time taken to get up to speed with the network?
    Manage what each node stores to its blockchain?
    Do we want to move parts of BlockCommit to this module?
    
    In fact, this is going to have to control almost all of the blockchain stuff
    
    Otherwise how on earth are we going to get it to work?
    
    We can't use an up to date flag in all systems
    
    I guess we just replace the blockchain with a custom blockchain containing only checkpoint blocks'''

class StateCompaction:

    #we want this to return a chain of checkpoints i.e. epoch start blocks
    #then the most recent block is classed as something
    #this is going to break a lot of stuff


    #this isnt accurate, as the shards arent synched so we dont know exactly when the checkpoint blocks will be
    def checkpointChain(shard):
        #c.fork_resolution()
        c.fork_resolution()
        checkpoints = c.global_chain[shard][0::p.epochLength]
        print(checkpoints)
        for node in p.NODES:
            lastBlock = node.blockchain_height(shard)
            '''if lastBlock != c.global_chain[shard][-1].depth:
                node.blockchain[shard] = node.blockchain[shard] + checkpoints[int(node.blockchain_height(shard)/p.epochLength):] 
            lastBlock = node.blockchain_height(shard)'''
            if lastBlock != c.global_chain[shard][-1].depth:
                node.change_block(shard, c.global_chain[shard][-1].depth, c.global_chain[shard][-1])
