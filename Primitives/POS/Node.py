from Primitives.Block import Block #can I remove this?
from Primitives.Node import Node as BaseNode


class Node(BaseNode):
    def __init__(self,id,stake):
        '''Initialize a new miner named name with hashrate measured in hashes per second.'''
        super().__init__(id)#,blockchain,transactionsPool,blocks,balance)
        self.stake = stake
        self.blockchain= []# create an array for each miner to store chain state locally
        self.transactionsPool= []
        self.blocks= []# total number of blocks mined in the main chain
        self.balance= 0# to count all reward that a miner made, including block rewards + uncle rewards + transactions fees
        self.effectiveStake = 0 #harmony ONE effective stake
        self.committees = [] #number of votes on each shard that this node has
        
