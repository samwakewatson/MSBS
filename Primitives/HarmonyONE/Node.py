from Primitives.Block import Block
from Primitives.Node import Node as BaseNode


#change this to storing multiple chains. will be a massive pain and will break like half the program.
#need to fix consensus in particular
class Node(BaseNode):
    def __init__(self,id,stake):
        '''Initialize a new miner named name with hashrate measured in hashes per second.'''
        super().__init__(id)#,blockchain,transactionsPool,blocks,balance)
        self.stake = stake
        self.blockchain= []# create an array for each miner to store chain state locally
        self.epoch = 0
        self.transactionsPool= []
        self.blocks= 0#[]# total number of blocks mined in the main chain
        self.balance= 0# to count all reward that a miner made, including block rewards + uncle rewards + transactions fees
        self.effectiveStake = 0
        self.committees = [] #number of votes on each shard that this node has - note we need to be very careful about how we assign this, maybe dictionary would be better?
        
