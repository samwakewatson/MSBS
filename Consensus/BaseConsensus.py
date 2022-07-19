import numpy as np
from Config import Config as p
from Primitives.Node import Node
import random


#Realisitically all of this needs tearing apart
class Consensus:
    global_chain=[] # the accepted global chain after resovling the forks


    """
	This is to model the consensus protocol
    """
    def Protocol(node):
        pass

    """
	This method is to resolve the forks that occur when nodes have multiple differeing copies of the blockchain ledger
    """
    def fork_resolution():
        pass
