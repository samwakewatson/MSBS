import random
'''Specify the individual modules of the sharded blockchain and 
any necessary network parameters
'''

class Config:

    '''Specify the six key components of a sharded blockchain protocol'''

    #0 = PBFT
    shardConsensus = 0

    #0 = PoS, 1 = PoW
    sybilResistance = 0

    #0 = shard driven, 1 = client driven, 2 = beacon chain driven
    crossShardCommunication = 0

    #0 = fully random each epoch, 1 = Bounded Cuckoo Rule
    committeeDispersal = 0

    #0 = don't simulate
    distributedRandomness = 0

    #0 = don't simulate
    stateCompaction = 0

    #0 = HarmonyONE
    presetConfig = 0

    #is this a bad solution? it's probably bad to put all the nodes here, though where else would they go?
    ''' Block Parameters '''
    Binterval = 30  # Average time (in seconds)for creating a block in the blockchain
    Bsize = 1.0
    Blimit = 8000000  # Gas limit
    Bdelay = 0.2  # average block propogation delay in seconds, #Ref: https://bitslog.wordpress.com/2016/04/28/uncle-mining-an-ethereum-consensus-protocol-flaw/
    Breward = 12.5  # Reward for mining a block
    slotTime = 4 #time each slot takes - doesn't exactly mimic harmony
    epochLength = 100 #how many slots in an epoch - node only the beacon chain determines epoch in harmonyONE
    slotLeaders = [] 

    ''' Transaction Parameters '''
    hasTrans = True  # True/False to enable/disable transactions in the simulator
    Ttechnique = "Full"  # Full/Light to specify the way of modelling transactions
    Tn = 100  # The rate of the number of transactions to be created per second
    # The average transaction propagation delay in seconds (Only if Full technique is used)
    Tdelay = 1
    Tfee = 0.000062  # The average transaction fee
    Tsize = 0.000546  # The average transaction size  in MB

    ''' Node Parameters '''
    Nn = 100  # the total number of nodes in the network
    NODES = []
    from Primitives.HarmonyONE.Node import Node

    for i in range(0, Nn):
        NODES.append(Node(id=i, stake=random.randint(1,100)))

    '''Shard Parameters'''
    numShards = 4
    cuckooRuleConstant = 0.3 #proportion of nodes that need to be moved each 

    ''' Simulation Parameters '''
    simTime = 1000  # the simulation length (in seconds)
    Runs = 1  # Number of simulation runs



