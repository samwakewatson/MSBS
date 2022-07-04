import operator
from Config import Config as p

#We need to make this more general
#Take it down to just type and time?
class Event(object):

    """ Defines the Event.

        :param str type: the event type (block creation or block reception)
        :param int node: the id of the node that the event belongs to
        :param float time: the simualtion time in which the event will be executed at
        :param obj block: the event content "block" to be generated or received
    """
    def __init__(self,type, node, time, block):
        self.type = type
        self.node = node
        self.time = time
        self.block = block



class Queue:
    event_list=[] # this is where future events will be stored
    def add_event(event):
        Queue.event_list += [event]
    def remove_event(event):
        del Queue.event_list[0]
    def get_next_event():
        Queue.event_list.sort(key=operator.attrgetter('time'), reverse=False) # sort events -> earliest one first
        print(Queue.event_list[0].type, Queue.event_list[0].time)
        return Queue.event_list[0]
    def size():
        return len(Queue.event_list)
    def isEmpty():
        return len(Queue.event_list) == 0
