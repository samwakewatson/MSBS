from Config import Config as p
from Consensus.BaseConsensus import Consensus as c
#from Models.Incentives import Incentives
from Network.Network import Network
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
    blockData=[]
    blocksResults=[]
    profits= [[0 for x in range(7)] for y in range(p.Runs * len(p.NODES))] # rows number of miners * number of runs, columns =7
    index=0
    chain=[]
    #network = Network.latencyTable #VERY VERY SUS IMPLEMENTATION - DO WE KNOW THIS IS THE SAME INSTANCE THAT IS USED IN THE REST OF THE PROGRAM?????

    def calculate():
        Statistics.global_chain() # print the global chain
        Statistics.blocks_results() # calcuate and print block statistics e.g., # of accepted blocks and stale rate etc
        #Statistics.profit_results() # calculate and distribute the revenue or reward for miners

    ########################################################### Calculate block statistics Results ###########################################################################################
    def blocks_results():
        trans = 0

        Statistics.mainBlocks= sum([len(i) - 1 for i in c.global_chain]) #needs fixing
        Statistics.staleBlocks = Statistics.totalBlocks - Statistics.mainBlocks
        for s in range(0,p.numShards):
            for b in c.global_chain[s]:
                Statistics.uncleBlocks = 0
                trans += len(b.transactions)
        Statistics.staleRate= round(Statistics.staleBlocks/Statistics.totalBlocks * 100, 2)
        Statistics.uncleRate==0
        Statistics.blockData = [ Statistics.totalBlocks, Statistics.mainBlocks,  Statistics.uncleBlocks, Statistics.uncleRate, Statistics.staleBlocks, Statistics.staleRate, trans]
        Statistics.blocksResults+=[Statistics.blockData]

    ########################################################### Calculate and distibute rewards among the miners ###########################################################################################
    def profit_results():

        

        '''for m in p.NODES:
            i = Statistics.index + m.id * p.Runs
            Statistics.profits[i][0]= m.id
            if p.model== 0: Statistics.profits[i][1]= "NA"
            else: Statistics.profits[i][1]= m.hashPower
            Statistics.profits[i][2]= m.blocks
            Statistics.profits[i][3]= round(m.blocks/Statistics.mainBlocks * 100,2)
            if p.model==2:
                Statistics.profits[i][4]= m.uncles
                Statistics.profits[i][5]= round((m.blocks + m.uncles)/(Statistics.mainBlocks + Statistics.totalUncles) * 100,2)
            else: Statistics.profits[i][4]=0; Statistics.profits[i][5]=0
            Statistics.profits[i][6]= m.balance'''

        #remove this once we fix the above
        for m in p.NODES:
            i = Statistics.index + m.id * p.Runs
            Statistics.profits[i][0]= m.id
            Statistics.profits[i][1]= "NA"

        Statistics.index+=1

    ########################################################### prepare the global chain  ###########################################################################################
    def global_chain():
        for s in range(0,p.numShards):
            Statistics.chain.append([])
            for i in c.global_chain[s]:
                    blockCopies = 0
                    for j in range(0,p.Nn):
                        if len(p.NODES[j].blockchain[s]) > i.depth:
                            blockCopies += 1
                    block= [i.depth, i.id, i.previous, i.timestamp, i.miner, len(i.transactions), i.size, blockCopies]
                    Statistics.chain[s] +=[block]

    ########################################################### Print simulation results to Excel ###########################################################################################
    def print_to_excel(fname):

        df1 = pd.DataFrame({'Block Time': [p.Binterval], 'Block Propagation Delay': [p.Bdelay], 'No. Miners': [len(p.NODES)], 'Simulation Time': [p.simTime]})
        #data = {'Stale Rate': Results.staleRate,'Uncle Rate': Results.uncleRate ,'# Stale Blocks': Results.staleBlocks,'# Total Blocks': Results.totalBlocks, '# Included Blocks': Results.mainBlocks, '# Uncle Blocks': Results.uncleBlocks}

        df2= pd.DataFrame(Statistics.blocksResults)
        df2.columns= ['Total Blocks', 'Main Blocks', 'Uncle blocks', 'Uncle Rate', 'Stale Blocks', 'Stale Rate', '# transactions']

        df3 = pd.DataFrame(Statistics.profits)
        df3.columns = ['Miner ID', '% Hash Power','# Mined Blocks', '% of main blocks','# Uncle Blocks','% of uncles', 'Profit (in ETH)']

        df4 = []
        for s in range(0,p.numShards):
            df4.append(pd.DataFrame(Statistics.chain[s]))
            #df4.columns= ['Block Depth', 'Block ID', 'Previous Block', 'Block Timestamp', 'Miner ID', '# transactions','Block Size']
            df4[s].columns= ['Block Depth', 'Block ID', 'Previous Block', 'Block Timestamp', 'Miner ID', '# transactions', 'Block Size', 'Block Copies']

        df5 = pd.DataFrame(Network.latencyTable)
        df5.columns = [i for i in range(0, p.Nn)]

        writer = pd.ExcelWriter(fname, engine='xlsxwriter')
        df1.to_excel(writer, sheet_name='InputConfig')
        df2.to_excel(writer, sheet_name='SimOutput')
        #df3.to_excel(writer, sheet_name='Profit')
        for s in range(0,p.numShards):
            df4[s].to_excel(writer,sheet_name='Shard '+str(s))
        df5.to_excel(writer, sheet_name='Network')

        writer.save()

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
        Statistics.profits= [[0 for x in range(7)] for y in range(p.Runs * len(p.NODES))] # rows number of miners * number of runs, columns =7
        Statistics.index=0
        Statistics.chain=[]
