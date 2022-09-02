import random
'''Specify the individual modules of the sharded blockchain and 
any necessary network parameters
'''

class Config:

    '''Specify the six key components of a sharded blockchain protocol'''

    #0 = delay, 1=FBFT, 3=SlotBased (Ouroboros like) 
    shardConsensus = 2

    #0 = PoS, 1 = PoW
    sybilResistance = 0

    #0 = shard driven, 1 = client driven, 2 = beacon chain driven
    crossShardCommunication = 0

    #0 = fully random each epoch, 1 = Bounded Cuckoo Rule
    committeeDispersal = 1

    #0 = don't simulate
    distributedRandomness = 0

    #0 = don't simulate
    stateCompaction = 0

    #0 = HarmonyONE
    presetConfig = 0

    ''' Block Parameters '''
    Binterval = 2  # Average time (in seconds)for creating a block in the blockchain
    Bsize = 1.0
    Blimit = 80000000  # Gas limit
    Bdelay = 0.2  # average block propogation delay in seconds, #Ref: https://bitslog.wordpress.com/2016/04/28/uncle-mining-an-ethereum-consensus-protocol-flaw/
    Breward = 12.5  # Reward for mining a block
    slotTime = 2 #time each slot takes
    epochLength = 1000 #how many slots in an epoch
    slotLeaders = [] 

    ''' Transaction Parameters '''
    hasTrans = True  # True/False to enable/disable transactions in the simulator
    Ttechnique = "Light"  # Full/Light to specify the way of modelling transactions
    Tn = 140  # The rate of the number of transactions to be created per second
    Tdelay = 1
    Tfee = 0.000062  # The average transaction fee
    Tsize = 0.000546  # The average transaction size  in MB
    crossShardProportion = 0.25 #The fraction of transaction that are cross shard

    ''' Node Parameters '''
    Nn = 150  # the total number of nodes in the network
    NODES = []
    from Primitives.HarmonyONE.Node import Node

    for i in range(0, Nn):
        NODES.append(Node(id=i, stake=random.randint(1,100)))

    '''Shard Parameters'''
    numShards = 4
    cuckooRuleConstant = 0.3 #proportion of nodes that need to be moved each epoch

    ''' Simulation Parameters '''
    simTime = 200 # the simulation length (in seconds)
    Runs = 4  # Number of simulation runs



