from Block import Block

#we want to make a blockchain object which is easier to use and has simpler behaviour
#we want it to be able to accomodate checkpointing etc.

class Blockchain:
    chain = []

    #maybe replace this with a proper constructor
    def initialise(self, numShards):
        self.chain = [[] for i in range(0, numShards)]

    def generate_genesis_blocks(self, numShards):
        self.chain = [[Block()] for i in range(0, numShards)]

    # Get the last block at the node's local blockchain
    def last_block(self, shard):
        return self.chain[shard][-1]

    #we want to add blockchain logic to this
    def append_block(self,shard, block):
        self.chain[shard].append(block)

    def blockchain_height(self, shard):
        return self.chain[shard][-1].depth

    