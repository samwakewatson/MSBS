from Config import Config as p
from Primitives.Transaction import LightTransaction


class BlockCommit:

    # Handling and running Events
    def handle_event(event):
        if event.type == "create_block":
            BlockCommit.generate_block(event)
        elif event.type == "receive_block":
            BlockCommit.receive_block(event)

    # Block Creation Event
    def generate_block (event):
        pass

    # Block Receiving Event
    def receive_block (event):
        pass

    # Select a new miner to build a new block
    def generate_next_block(node,currentTime):
        pass
    # Generate initial blocks to start the simulation with
    def generate_initial_events():
        pass
    # Propagate the generated block to other nodes in the network
    def propagate_block (block):
        pass
    # Update local blockchain, if necessary, upon receiving a new valid block
    def update_local_blockchain(node,miner,shard,depth):
        # the node here is the one that needs to update its blockchain, while miner here is the one who owns the last block generated
        # the node will update its blockchain to match the miner's blockchain

        #only update from the latest checkpoint onwards
        '''i= miner.epoch * p.epochLength
        while (i < depth):
            if (i < node.blockchain[shard][-1].depth and miner.return_block(shard, i) != 0):
                if (node.return_block(shard, i) == 0):

                if (node.return_block(shard, i).id != miner.return_block(shard, i).id): # and (self.node.blockchain[i-1].id == Miner.blockchain[i].previous) and (i>=1):
                    #node.unclechain.append(node.blockchain[i]) # move block to unclechain
                    newBlock = miner.return_block(shard, i).id
                    node.change_block(shard, i, newBlock)
                    if p.hasTrans and p.Ttechnique == "Full": BlockCommit.update_transactionsPool(node,newBlock)
            else:
                newBlock = miner.return_block(shard, i).id
                node.blockchain[shard].append(newBlock)
                if p.hasTrans and p.Ttechnique == "Full": BlockCommit.update_transactionsPool(node,newBlock)
            i+=1'''
        
        '''i= miner.epoch * p.epochLength
        while (i < depth):
            if (i < node.blockchain[shard][-1].depth and miner.return_block(shard, i) != 0):
                newBlock = miner.return_block(shard, i)
                node.change_block(shard, i, newBlock)
                if p.hasTrans and p.Ttechnique == "Full": BlockCommit.update_transactionsPool(node,newBlock)
            else:
                newBlock = miner.return_block(shard, i)
                node.blockchain[shard].append(newBlock)
                if p.hasTrans and p.Ttechnique == "Full": BlockCommit.update_transactionsPool(node,newBlock)
            i+=1'''
        #need to change this
        newBlock = miner.last_block(shard)
        node.change_block(shard, newBlock.depth, newBlock)


    def sync_shards():
        #find the longest possible combination of shards
        blockchain = []
        longestChains = [0] * p.numShards #store node IDs that have the longest chain of each shard - note that we might have a difference of like 1 block
        for i in range(0,p.Nn):
            for s in range(0,p.numShards):
                if len(p.NODES[i].blockchain[s]) > len(p.NODES[longestChains[s]].blockchain[s]):
                    longestChains[s] = i
        for s in range(0,p.numShards):
            blockchain.append(p.NODES[longestChains[s]].blockchain[s])
        #so we now have a global blockchain, we want to make sure each node in each committee is up to date with its relevant shards
        for i in range(0,p.numShards):
            for node in p.NODES:
                if node.committees[i] != 0 and node.blockchain_height() < blockchain[i][-1].depth:
                    #we only want to download the checkpoint blocks
                    for x in range(0, blockchain[i][-1].depth, p.epochLength):
                        try:
                            node.blockchain[i].append(blockchain[x])
                        except:
                            break





    # Update local blockchain, if necessary, upon receiving a new valid block. This method is only triggered if Full technique is used
    def update_transactionsPool(node,block):
        if p.Ttechnique == "Full":
            j=0
            while j < len(block.transactions):
                for t in node.transactionsPool:
                    if  block.transactions[j].id == t.id:
                        del t
                        break
                j+=1
        elif p.Ttechnique == "Light":
            '''j=0
            #print(len(LightTransaction.pool))
            while j < len(block.transactions):
                for t in LightTransaction.pool:
                    if  block.transactions[j].id == t.id:
                        print("deleting {0}".format(t.id))
                        del t
                        break
                j+=1'''