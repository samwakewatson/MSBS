from Scheduler import Scheduler
from Config import Config as p
from Primitives.HarmonyONE.Node import Node
from Statistics import Statistics
from Primitives.HarmonyONE.Transaction import LightTransaction as LT, FullTransaction as FT
#from Consensus.HarmonyONE import Consensus as c
#from Consensus.Consensus import Consensus as c
from Consensus.FBFT import Consensus as c
from Primitives.BlockCommit import BlockCommit as BaseBlockCommit
from Primitives.Block import Block
from ShardAssignment.HarmonyONE import ShardAssignment
from StateCompaction.Checkpoints import StateCompaction
import random
import numpy as np

class BlockCommit(BaseBlockCommit):

    # Handling and running Events
    def handle_event(event):
        if event.type == "create_block":
            BlockCommit.generate_block(event)
        elif event.type == "new_slot":
            BlockCommit.check_leader(event)
        elif event.type == "receive_block":
            BlockCommit.receive_block(event)
        elif event.type == "new_epoch": #need to add the code for this
            BlockCommit.shuffle_committees(event)

    # Block Creation Event
    def generate_block (event):

        '''block = Block()
        block.miner = miner.id
        block.depth = len(miner.blockchain[shard])
        block.id = random.randrange(100000000000)
        block.previous = miner.last_block(shard).id
        block.timestamp = eventTime
        block.shard = shard'''

        miner = p.NODES[event.block.miner]
        minerId = miner.id
        eventTime = event.time
        event.block.previous = miner.last_block(event.block.shard).id
        event.block.depth = miner.last_block(event.block.shard).depth + 1
        blockPrev = event.block.previous
        blockShard = event.block.shard

        if blockPrev == miner.last_block(blockShard).id:
            Statistics.totalBlocks += 1 # count # of total blocks created!
            if p.hasTrans:
                if p.Ttechnique == "Light": blockTrans,blockSize = LT.execute_transactions()
                elif p.Ttechnique == "Full": blockTrans,blockSize = FT.execute_transactions(miner,blockShard,eventTime)

                event.block.transactions = blockTrans
                event.block.usedgas= blockSize

            #miner.blockchain[blockShard].append(event.block)
            miner.change_block(blockShard, event.block.depth, event.block)

            if p.hasTrans and p.Ttechnique == "Light":LT.create_transactions() # generate transactions

            BlockCommit.propagate_block(event.block)
            #BlockCommit.generate_next_block(miner,eventTime)# Start mining or working on the next block
        else:
            print("useless block scheduled")

    #confusingly named - each node checks if it is the leader/ allowed to make a block at the start of the slot
    #this isnt really how it works in harmony, each node is assigned slots
    def check_leader(event):
        for s in range(0,p.numShards):
            Scheduler.create_block_event(p.slotLeaders[s][int(event.time/p.slotTime) % len(p.slotLeaders[s])], s, event.time) 
        '''for node in p.NODES:
            for s in range(0,p.numShards):
                if c.Protocol(node, s):
                    Scheduler.create_block_event(node, s, event.time)'''
        

    #this version shuffles all of the committees, which would have a massive overhead
    #also this is what handles the entire new epoch event, so we probably need to alter it
    def shuffle_committees(event):
        #this assigns committees randomly based on the number of votes they have, not really how Harmony works
        '''allVotes = []
        for node in p.NODES:
            node.committees = []
            votes = c.calculate_votes(node)
            for v in range(0, votes):
                allVotes.append(node.id)
        random.shuffle(allVotes)
        committeeSize = int(len(allVotes) / p.numShards)
        committees = [allVotes[x:x+committeeSize] for x in range(0, len(allVotes), committeeSize)]
        for node in p.NODES:
            for s in range(0, p.numShards):
                node.committees.append(committees[s].count(node.id))'''
        '''committeeOptions = []
        for i in range(0,p.numShards):
            x = np.zeros(p.numShards)
            x[i] = 1
            committeeOptions.append(x)

        for node in p.NODES:
            node.committees = random.choice(committeeOptions)'''

        #Scheduler.clear_event_stack()

        for node in p.NODES:
            node.epoch += 1

        Scheduler.cancel_new_blocks()

        #we want to make sure there's a delay before the next block (for each chain)

        ShardAssignment.shuffle_committees()

        ShardAssignment.assign_leaders()

        c.fork_resolution()
        for s in range(0,p.numShards):
            StateCompaction.checkpointChain(s)

        for s in range(0, p.numShards):
            Scheduler.create_block_event(p.slotLeaders[s][0], s, event.time + ShardAssignment.sync_delay())

    # Block Receiving Event - we want to modify this, or where it's called so that we don't instantly update the chain.
    #We have to take into account the time it takes to download and verify each block
    def receive_block (event):

        miner = p.NODES[event.block.miner]
        minerId = miner.id
        currentTime = event.time
        blockPrev = event.block.previous # previous block id
        blockShard = event.block.shard


        node = p.NODES[event.node] # recipient
        lastBlockId= node.last_block(blockShard).id # the id of last block

        if node.committees[blockShard] != 0:
            #### case 1: the received block is built on top of the last block according to the recipient's blockchain ####
            if blockPrev == lastBlockId:
                node.blockchain[blockShard].append(event.block) # append the block to local blockchain
                if p.hasTrans and p.Ttechnique == "Full": BlockCommit.update_transactionsPool(node, event.block)
                #BlockCommit.generate_next_block(node,currentTime)# Start mining or working on the next block

            #### case 2: the received block is  not built on top of the last block ####
            elif miner.blockchain_height(blockShard) > node.blockchain_height(blockShard): #this line is maybe redundant?? probably caught by the line below
                depth = event.block.depth #+ 1
                if (depth > node.blockchain_height(blockShard)):
                    BlockCommit.update_local_blockchain(node,miner,blockShard,depth)
                    #BlockCommit.generate_next_block(node,currentTime)# Start mining or working on the next block

                if p.hasTrans and p.Ttechnique == "Full": BlockCommit.update_transactionsPool(node,event.block) # not sure yet.

    # Upon generating or receiving a block, the miner start working on the next block as in POW
    '''def generate_next_block(node,currentTime):
	    if node.hashPower > 0:
                 blockTime = currentTime + c.Protocol(node) # time when miner x generate the next block
                 Scheduler.create_block_event(node,blockTime)'''

    def generate_initial_events():
        currentTime=0
        allVotes = []
        #put in all the slots and epochs
        '''while (currentTime < p.simTime):
            if (currentTime % (p.epochLength * p.slotTime)) == 0:
                Scheduler.new_epoch_event(currentTime)
            currentTime = currentTime + p.slotTime
            Scheduler.new_slot_event(currentTime)'''

        Scheduler.new_slot_event(2)
        #assign all of the nodes votes in the various committees
        #this needs to be completely changed -effective stake changes the game
        '''for node in p.NODES:
            votes = c.calculate_votes(node)
            for v in range(0, votes):
                allVotes.append(node.id)
        random.shuffle(allVotes)
        committeeSize = int(len(allVotes) / p.numShards)
        #print(allVotes)
        committees = [allVotes[x:x+committeeSize] for x in range(0, len(allVotes), committeeSize)]
        for node in p.NODES:
            for s in range(0, p.numShards):
                node.committees.append(committees[s].count(node.id))'''
        committeeOptions = []
        for i in range(0,p.numShards):
            x = np.zeros(p.numShards)
            x[i] = 1
            committeeOptions.append(x)

        for node in p.NODES:
            node.committees = random.choice(committeeOptions)
        #for node in p.NODES:
            #print(node.committees)
        ShardAssignment.assign_leaders()
        #for node in p.NODES:
        #    BlockCommit.generate_next_block(node,currentTime)
                
    def propagate_block(block):
        '''for recipient in p.NODES:
            if recipient.id != block.miner:
                blockDelay= Network.block_prop_delay(Network, block.miner, recipient.id) # draw block propagation delay from a distribution !! or you can assign 0 to ignore block propagation delay
                Scheduler.receive_block_event(recipient,block,blockDelay)'''
        #delay = FBFT.timeToReachConsensus(block.miner, [node.id for node in p.NODES if node.committees[block.shard] != 0])#
        
        if block.shard == 0:
            print(block.timestamp)
            print(block.depth)
            print(block.shard)
            print(block.miner)
            print("\n")
        
        delay = c.timeToReachConsensus()
        for recipient in p.NODES:
            if recipient.id != block.miner:
                Scheduler.receive_block_event(recipient, block, 0)
        #Scheduler.new_slot_event(block.timestamp + delay + 0.001) #note the 0.001 is just to make sure a new slot doesnt happen before all the receive eventsE
        if ((block.depth % p.epochLength) == 0) and (block.shard == 0) and (block.depth != 0):
            Scheduler.new_epoch_event(block.timestamp + 0.001)
            #print(block.depth)
            #print(block.shard)
            #print(block.miner)
            return
        Scheduler.create_block_event(p.slotLeaders[block.shard][(block.depth + 1) % len(p.slotLeaders[block.shard])], block.shard, block.timestamp + delay)#we need to add the network delay