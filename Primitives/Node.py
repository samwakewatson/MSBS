from Primitives.Block import Block

class Node(object):

    """ Defines the base Node model.

        :param int id: the unique id of the node
        :param list blockchain: the local blockchains (a list to store lists of shard state locally) for the node
        :param list transactionsPool: the transactions pool. Each node has its own pool if and only if Full technique is chosen
        :param int blocks: the total number of blocks mined in the main chain
        :param int balance: the amount of cryptocurrencies a node has
    """
    def __init__(self,id):
        self.id= id
        self.blockchain= []
        self.transactionsPool= []
        self.blocks= []
        self.balance= 0

    # Generate the Genesis block for each shard and append it to the local blockchain for all nodes
    def generate_gensis_block():
        from Config import Config as p
        for node in p.NODES:
            for s in range(0, p.numShards):
                node.blockchain.append([Block()])

    # Get the last block at the node's local blockchain
    def last_block(self, shard):
        return self.blockchain[shard][-1]

    # Get the length of the blockchain (number of blocks)
    def blockchain_length(self, shard):
        return len(self.blockchain[shard])-1

    #be careful using this one and the one above
    def blockchain_height(self, shard):
        return self.blockchain[shard][-1].depth

    # reset the state of blockchains for all nodes in the network (before starting the next run) 
    def resetState():
        from Config import Config as p
        for node in p.NODES:
            node.blockchain= [] # create an array for each miner to store chain state locally
            node.transactionsPool= []
            node.blocks=[] # total number of blocks mined in the main chain
            node.balance= 0 # to count all reward that a miner made
