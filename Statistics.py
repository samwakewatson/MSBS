from audioop import cross
from Config import Config as p
from Consensus.BaseConsensus import Consensus as c
from Incentives.Incentives import Incentives
from Network.Network import Network
import statistics
import pandas as pd


class Statistics:

    ########################################################### Global variables used to calculate and print simuation results ###########################################################################################
    totalBlocks=0
    mainBlocks= 0
    totalUncles=0
    uncleBlocks=0
    staleBlocks=0
    uncleRate=0
    staleRate=0
    numTransactions=0
    transactionLatency=0
    crossShardTxLatency=0
    perShardFees=[]
    blockData=[]
    blocksResults=[]
    profits= [[0 for x in range(7)] for y in range(p.Runs * len(p.NODES))] # rows number of miners * number of runs, columns =7
    index=0
    chain=[]
    #network = Network.latencyTable #VERY VERY SUS IMPLEMENTATION - DO WE KNOW THIS IS THE SAME INSTANCE THAT IS USED IN THE REST OF THE PROGRAM?????

    def calculate():
        Statistics.global_chain() # print the global chain
        Statistics.blocks_results() # calcuate and print block statistics e.g., # of accepted blocks and stale rate etc
        Statistics.profit_results() # calculate and distribute the revenue or reward for miners

    ########################################################### Calculate block statistics Results ###########################################################################################
    def blocks_results():
        transactionDelays = []
        crossShardTxDelays = []
        fees = []

        Statistics.mainBlocks= sum([len(i) for i in c.global_chain])
        Statistics.staleBlocks = Statistics.totalBlocks - Statistics.mainBlocks
        for s in range(0,p.numShards):
            fees.append([])
            for b in c.global_chain[s]:
                Statistics.uncleBlocks = 0
                Statistics.numTransactions += len(b.transactions)
                for t in b.transactions:
                    #print(t)
                    #print(t.timestamp)
                    #print(b)
                    #print(b.timestamp)
                    #transactionDelays.append(float(b.timestamp - t.timestamp[0]))
                    fees[s].append(t.fee)
                    if t.isReceipt == False:
                        transactionDelays.append(float(b.timestamp - t.timestamp))
                    else:
                        crossShardTxDelays.append(float(b.timestamp - t.timestamp))
        #this breaks if we have no cross shard tx
        try:
            Statistics.transactionLatency = statistics.mean(transactionDelays)
        except:
            Statistics.transactionLatency = 0

        try:
            Statistics.crossShardTxLatency = statistics.mean(crossShardTxDelays)
        except:
            Statistics.crossShardTxLatency = 0
   
        Statistics.staleRate= round(Statistics.staleBlocks/Statistics.totalBlocks * 100, 2)
        Statistics.uncleRate==0
        Statistics.blockData = [ Statistics.totalBlocks, Statistics.mainBlocks,  Statistics.uncleBlocks, Statistics.uncleRate, Statistics.staleBlocks, Statistics.staleRate, Statistics.numTransactions, Statistics.transactionLatency, Statistics.crossShardTxLatency]
        Statistics.blocksResults+=[Statistics.blockData]
        Statistics.perShardFees += [statistics.mean(fees[s]) for s in range(0,p.numShards)]

    ########################################################### Calculate and distibute rewards among the miners ###########################################################################################
    def profit_results():

        

        for m in p.NODES:
            i = Statistics.index + m.id * p.Runs
            Statistics.profits[i][0]= m.id
            Statistics.profits[i][1]= m.stake
            Statistics.profits[i][2]= m.blocks
            Statistics.profits[i][3]= round(m.blocks/Statistics.mainBlocks * 100,2)
            Statistics.profits[i][4]=0
            Statistics.profits[i][5]=0
            Statistics.profits[i][6]= m.balance

        #remove this once we fix the above
        '''for m in p.NODES:
            i = Statistics.index + m.id * p.Runs
            Statistics.profits[i][0]= m.id
            Statistics.profits[i][1]= "NA"'''

        Statistics.index+=1

    ########################################################### prepare the global chain  ###########################################################################################
    def global_chain():
        for s in range(0,p.numShards):
            Statistics.chain.append([])
            for i in c.global_chain[s]:
                    blockCopies = 0
                    for j in range(0,p.Nn):
                        if p.NODES[j].return_block(s,i.depth) != 0:
                            if p.NODES[j].return_block(s,i.depth).id == i.id:
                                blockCopies += 1
                    block= [i.depth, i.id, i.previous, i.timestamp, i.miner, len(i.transactions), i.size, blockCopies]
                    Statistics.chain[s] +=[block]

    ########################################################### Print simulation results to Excel ###########################################################################################
    def print_to_excel(fname):

        df1 = pd.DataFrame({'Block Time': [p.Binterval], 'Block Propagation Delay': [p.Bdelay], 'No. Miners': [len(p.NODES)], 'Simulation Time': [p.simTime], 'Tx Generated per second': [p.Tn], 'CrossShard proportion':[p.crossShardProportion]})
        #data = {'Stale Rate': Results.staleRate,'Uncle Rate': Results.uncleRate ,'# Stale Blocks': Results.staleBlocks,'# Total Blocks': Results.totalBlocks, '# Included Blocks': Results.mainBlocks, '# Uncle Blocks': Results.uncleBlocks}

        df2= pd.DataFrame(Statistics.blocksResults)
        df2.columns= ['Total Blocks', 'Main Blocks', 'Uncle blocks', 'Uncle Rate', 'Stale Blocks', 'Stale Rate', '# transactions', 'transaction latency', 'cross shard tx latency']

        df3 = pd.DataFrame(Statistics.profits)
        df3.columns = ['Miner ID', '% Hash Power','# Mined Blocks', '% of main blocks','# Uncle Blocks','% of uncles', 'Profit (in ETH)']

        df4 = []
        for s in range(0,p.numShards):
            df4.append(pd.DataFrame(Statistics.chain[s]))
            #df4.columns= ['Block Depth', 'Block ID', 'Previous Block', 'Block Timestamp', 'Miner ID', '# transactions','Block Size']
            df4[s].columns= ['Block Depth', 'Block ID', 'Previous Block', 'Block Timestamp', 'Miner ID', '# transactions', 'Block Size', 'Block Copies']

        df5 = pd.DataFrame(Network.latencyTable)
        df5.columns = [i for i in range(0, p.Nn)]

        df6 = pd.DataFrame(Statistics.perShardFees)
        #df6.columns = [s for s in range(0, 4)]
        
        writer = pd.ExcelWriter(fname, engine='openpyxl')
        df1.to_excel(writer, sheet_name='InputConfig')
        df2.to_excel(writer, sheet_name='SimOutput')
        df3.to_excel(writer, sheet_name='Profit')
        for s in range(0,p.numShards):
            df4[s].to_excel(writer,sheet_name='Shard '+str(s))
        df5.to_excel(writer, sheet_name='Network')
        df6.to_excel(writer, sheet_name='Per Shard Fees')

        writer.save()

    def returnValue(value):
        if value == "totalTx":
            return Statistics.numTransactions
        elif value == "sameShardTxLatency":
            return Statistics.transactionLatency
        elif value == "crossShardTxLatency":
            return Statistics.crossShardTxLatency
        

    ########################################################### Draw some graphs ##########################################################
    #so we want to save all the results of the various simulations and output some graphs all at once
    #so we need to fix the multithreading, or at least store some data between runs
    #what in particular do we need graphs of? tps generated vs latency, tps vs ?, miner profits?

    ########################################################### Reset all global variables used to calculate the simulation results ###########################################################################################
    def reset():
        Statistics.totalBlocks=0
        Statistics.totalUncles=0
        Statistics.mainBlocks= 0
        Statistics.uncleBlocks=0
        Statistics.staleBlocks=0
        Statistics.uncleRate=0
        Statistics.staleRate=0
        Statistics.blockData=[]

    def reset2():
        Statistics.blocksResults=[]
        Statistics.perShardFees=[]
        Statistics.profits= [[0 for x in range(7)] for y in range(p.Runs * len(p.NODES))] # rows number of miners * number of runs, columns =7
        Statistics.index=0
        Statistics.chain=[]
        Statistics.transactionLatency=0
        Statistics.crossShardTxLatency=0
        Statistics.numTransactions=0
