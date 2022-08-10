from Primitives.HarmonyONE.Distribution.DistFit import DistFit
import random
from Config import Config as p
import numpy as np
from Network.Network import Network
import operator
from Primitives.HarmonyONE.Distribution.DistFit import DistFit

class Transaction(object):

    """ Defines the Ethereum Block model.

    :param int id: the uinque id or the hash of the transaction
    :param int timestamp: the time when the transaction is created. In case of Full technique, this will be array of two value (transaction creation time and receiving time)
    :param int sender: the id of the node that created and sent the transaction
    :param int to: the id of the recipint node
    :param int value: the amount of cryptocurrencies to be sent to the recipint node
    :param int size: the transaction size in MB
    :param int gasLimit: the maximum amount of gas units the transaction can use. It is specified by the submitter of the transaction
    :param int usedGas: the amount of gas used by the transaction after its execution on the EVM
    :param int gasPrice: the amount of cryptocurrencies (in Gwei) the submitter of the transaction is willing to pay per gas unit
    :param float fee: the fee of the transaction (usedGas * gasPrice)
    """

    def __init__(self,
	 id=0,shardFrom=0,shardTo=0,isReceipt=False,
	 timestamp=0 or [],
	 sender=0,
         to=0,
         value=0,
	 size=0.000546,
         gasLimit= 8000000,
         usedGas=0,
         gasPrice=0,
         fee=0):

        self.id = id
        self.shardFrom = shardFrom
        self.shardTo = shardTo
        self.isReceipt = isReceipt
        self.timestamp = timestamp
        self.sender = sender
        self.to= to
        self.value=value
        self.size = size
        self.gasLimit=gasLimit
        self.usedGas = usedGas
        self.gasPrice=gasPrice
        self.fee= usedGas * gasPrice



class LightTransaction():

    pool=[] # shared pool of pending transactions
    #x=0 # counter to only fit distributions once during the simulation

    def create_transactions():

        LightTransaction.pool=[]
        Psize= int(p.Tn * p.simTime)

        #if LightTransaction.x<1:
        DistFit.fit() # fit distributions
        gasLimit,usedGas,gasPrice,_ = DistFit.sample_transactions(Psize) # sampling gas based attributes for transactions from specific distribution

        for i in range(Psize):
            # assign values for transactions' attributes. You can ignore some attributes if not of an interest, and the default values will then be used
            tx= Transaction()

            tx.id= random.randrange(100000000000)
            tx.shardFrom = random.randint(0,p.numShards-1)

            if i < p.crossShardProportion * Psize:
                tx.shardTo = random.randint(0,p.numShards-1)#this doesn't really give us as many as we want it to, can return sameshard tx
            else:
                tx.shardTo = tx.shardFrom


            tx.timestamp = random.randint(0,p.simTime-1) #don't really see why this should be an integer
            tx.isReceipt = False
            tx.sender = random.choice (p.NODES).id
            tx.to= random.choice (p.NODES).id
            tx.gasLimit=gasLimit[i]
            tx.usedGas=usedGas[i]
            tx.gasPrice=gasPrice[i]/1000000000
            tx.fee= tx.usedGas * tx.gasPrice

            LightTransaction.pool += [tx]

        print(len(LightTransaction.pool))
        #random.shuffle(LightTransaction.pool) might need to add this back?


    ##### Select and execute a number of transactions to be added in the next block #####
    def execute_transactions(currentTime, shard):
        transactions= [] # prepare a list of transactions to be included in the block
        limit = 0 # calculate the total block gaslimit
        count=0
        blocklimit = p.Blimit

        #add the logic for cross shard transactions
        pool = sorted(LightTransaction.pool, key=lambda x: x.gasPrice, reverse=True) # sort pending transactions in the pool based on the gasPrice value
        while count < len(pool):
                if  (blocklimit >= pool[count].gasLimit and pool[count].timestamp <= currentTime and pool[count].shardTo == shard and pool[count].shardFrom == shard):
                    blocklimit -= pool[count].usedGas
                    transactions += [pool[count]]
                    limit += pool[count].usedGas
                    LightTransaction.pool.remove(pool[count]) #this is probably the slowest thing in existence
                elif (blocklimit >= pool[count].gasLimit and pool[count].timestamp[1] <= currentTime and pool[count].shardTo != shard and pool[count].shardFrom == shard):
                    #we need to include the transaction, then make another one to go to the other shard
                    blocklimit -= pool[count].usedGas
                    transactions += [pool[count]]
                    limit += pool[count].usedGas
                    pool[count].isReceipt = True
                elif (blocklimit >= pool[count].gasLimit and pool[count].timestamp[1] <= currentTime and pool[count].shardTo == shard and pool[count].shardFrom != shard and pool[count].isReceipt == True):
                    blocklimit -= pool[count].usedGas
                    transactions += [pool[count]]
                    limit += pool[count].usedGas
                count+=1

        return transactions, limit

class FullTransaction():
    x=0 # counter to only fit distributions once during the simulation

    def create_transactions():
        Psize= int(p.Tn * p.Binterval)

        if FullTransaction.x<1:
            DistFit.fit() # fit distributions
        gasLimit,usedGas,gasPrice,_ = DistFit.sample_transactions(Psize) # sampling gas based attributes for transactions from specific distribution

        for i in range(Psize):
            # assign values for transactions' attributes. You can ignore some attributes if not of an interest, and the default values will then be used
            tx= Transaction()

            tx.id= random.randrange(100000000000)
            tx.shardFrom = random.randint(0,p.numShards-1)
            
            if i < p.crossShardProportion * Psize:
                tx.shardTo = random.randint(0,p.numShards-1)#this doesn't really give us as many as we want it to, can return sameshard tx
            else:
                tx.shardTo = tx.shardFrom

            creation_time= random.randint(0,p.simTime-1)
            receive_time= creation_time
            tx.timestamp= [creation_time,receive_time]
            sender= random.choice (p.NODES)
            tx.sender = sender.id
            tx.to= random.choice (p.NODES).id
            tx.gasLimit=gasLimit[i]
            tx.usedGas=usedGas[i]
            tx.gasPrice=gasPrice[i]/1000000000
            tx.fee= tx.usedGas * tx.gasPrice

            sender.transactionsPool.append(tx)
            FullTransaction.transaction_prop(tx)

    # Transaction propogation & preparing pending lists for miners
    #Do we want to ignore transactions not relevant to a particular node?
    def transaction_prop(tx):
        # Fill each pending list. This is for transaction propogation
        for i in p.NODES:
            if tx.sender != i.id:
                t= tx
                t.timestamp[1] = t.timestamp[1] + Network.tx_prop_delay() # transaction propogation delay in seconds
                i.transactionsPool.append(t)



    def execute_transactions(miner,shard,currentTime):
        transactions= [] # prepare a list of transactions to be included in the block
        limit = 0 # calculate the total block gaslimit
        count=0
        blocklimit = p.Blimit
        miner.transactionsPool.sort(key=operator.attrgetter('gasPrice'), reverse=True)
        pool= miner.transactionsPool

        while count < len(pool):
                if  (blocklimit >= pool[count].gasLimit and pool[count].timestamp[1] <= currentTime and pool[count].shardTo == shard and pool[count].shardFrom == shard):
                    blocklimit -= pool[count].usedGas
                    transactions += [pool[count]]
                    limit += pool[count].usedGas
                elif (blocklimit >= pool[count].gasLimit and pool[count].timestamp[1] <= currentTime and pool[count].shardTo != shard and pool[count].shardFrom == shard):
                    #we need to include the transaction, then make another one to go to the other shard
                    blocklimit -= pool[count].usedGas
                    transactions += [pool[count]]
                    limit += pool[count].usedGas
                    receiptTx = pool[count]
                    receiptTx.isReceipt = True
                    FullTransaction.transaction_prop(receiptTx)
                elif (blocklimit >= pool[count].gasLimit and pool[count].timestamp[1] <= currentTime and pool[count].shardTo == shard and pool[count].shardFrom != shard and pool[count].isReceipt == True):
                    blocklimit -= pool[count].usedGas
                    transactions += [pool[count]]
                    limit += pool[count].usedGas
                count+=1

        return transactions, limit