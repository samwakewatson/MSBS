from Config import Config as p

#Currently BlockCommit kinda does way too much
#We can maybe stand it doing most of the stuff set out here
#But a lot of what it does in the specialised models really shouldn't be there
#Ideally we'll move a lot of stuff to the consensus classes, or maybe make them properties of the nodes themselves
#We want to keep it general though, so maybe a BlockCommit isn't too bad

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
        i=0
        while (i < depth):
            if (i < len(node.blockchain[shard])):
                if (node.blockchain[shard][i].id != miner.blockchain[shard][i].id): # and (self.node.blockchain[i-1].id == Miner.blockchain[i].previous) and (i>=1):
                    #node.unclechain.append(node.blockchain[i]) # move block to unclechain
                    newBlock = miner.blockchain[shard][i]
                    node.blockchain[shard][i]= newBlock
                    if p.hasTrans and p.Ttechnique == "Full": BlockCommit.update_transactionsPool(node,newBlock)
            else:
                newBlock = miner.blockchain[shard][i]
                node.blockchain[shard].append(newBlock)
                if p.hasTrans and p.Ttechnique == "Full": BlockCommit.update_transactionsPool(node,newBlock)
            i+=1

    # Update local blockchain, if necessary, upon receiving a new valid block. This method is only triggered if Full technique is used
    def update_transactionsPool(node,block):
        j=0
        while j < len(block.transactions):
            for t in node.transactionsPool:
                if  block.transactions[j].id == t.id:
                    del t
                    break
            j+=1