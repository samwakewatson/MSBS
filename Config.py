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




    ''' Node Parameters '''
    Nn = 10  # the total number of nodes in the network
    NODES = []
    from Primitives.Node import Node

    for i in range(0, Nn):
        NODES.append(Node(id=i, hashPower=random.randint(1,100)))



