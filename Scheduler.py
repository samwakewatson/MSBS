from Config import Config as p
import random
from Primitives.Block import Block
from Event import Event, Queue

'''if p.model == 2:
    from Models.Ethereum.Block import Block
else:
    from Primitives.Block import Block'''


class Scheduler:

    # Schedule a block creation event for a miner and add it to the event list
    #Do we need to modify this? Or can we leave it as it represents a leader election
    def create_block_event(miner, shard, eventTime):
        eventType = "create_block"
        if eventTime <= p.simTime:
            # prepare attributes for the event
            block = Block()
            block.miner = miner.id
            block.depth = len(miner.blockchain[shard])
            block.id = random.randrange(100000000000)
            block.previous = miner.last_block(shard).id
            block.timestamp = eventTime
            block.shard = shard

            event = Event(eventType, block.miner, eventTime,block)  # create the event
            Queue.add_event(event)  # add the event to the queue

    def new_slot_event(eventTime):
        eventType = "new_slot"
        if eventTime <= p.simTime:
            event = Event(eventType, None, eventTime, None)  # create the event
            Queue.add_event(event)  # add the event to the queue

    def new_epoch_event(eventTime):
        eventType = "new_epoch"
        if eventTime <= p.simTime:
            event = Event(eventType, None, eventTime, None)
            Queue.add_event(event)

    # Schedule a block receiving event for a node and add it to the event list
    def receive_block_event(recipient, block, blockDelay): #Is this blockdelay any different from the hardcoded one???
        receive_block_time = block.timestamp + blockDelay
        if receive_block_time <= p.simTime:
            e = Event("receive_block", recipient.id, receive_block_time, block)
            Queue.add_event(e)

