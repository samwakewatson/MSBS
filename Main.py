from Config import Config as p
from Event import Event, Queue
from Scheduler import Scheduler
from Statistics import Statistics

'''elif p.model == 1:
    from Models.Bitcoin.BlockCommit import BlockCommit
    from Models.Bitcoin.Consensus import Consensus
    from Models.Transaction import LightTransaction as LT, FullTransaction as FT
    from Models.Bitcoin.Node import Node
    from Models.Incentives import Incentives

elif p.model == 0:
    from Models.BlockCommit import BlockCommit
    from Models.Consensus import Consensus
    from Models.Transaction import LightTransaction as LT, FullTransaction as FT
    from Models.Node import Node
    from Models.Incentives import Incentives

elif p.model == 4:
    from Models.HarmonyONE.BlockCommit import BlockCommit
    from Models.HarmonyONE.Consensus import Consensus
    from Models.HarmonyONE.Transaction import LightTransaction as LT, FullTransaction as FT
    from Models.HarmonyONE.Node import Node
    from Models.Incentives import Incentives'''

#note that we have 2 consensus files required for a lot of stuff
match p.shardConsensus:
    case 0:
        from Consensus.Delay import Consensus
    case 1:
        from Consensus.FBFT import Consensus
    case 2: 
        #from Consensus.HarmonyONE import Consensus
        from Consensus.Consensus import Consensus

match p.stateCompaction:
    case 0:
        from StateCompaction.Checkpoints import StateCompaction

from Primitives.HarmonyONE.Transaction import LightTransaction as LT, FullTransaction as FT
from Primitives.HarmonyONE.Node import Node
from Primitives.HarmonyONE.BlockCommit import BlockCommit

########################################################## Start Simulation ##############################################################
def main():
    for i in range(p.Runs):
        clock = 0  # set clock to 0 at the start of the simulation
        if p.hasTrans:
            if p.Ttechnique == "Light":
                LT.create_transactions()  # generate pending transactions
            elif p.Ttechnique == "Full":
                FT.create_transactions()  # generate pending transactions

        Node.generate_gensis_block()  # generate the gensis block for all miners
        # initiate initial events >= 1 to start with
        BlockCommit.generate_initial_events()

        while not Queue.isEmpty() and clock <= p.simTime:
            next_event = Queue.get_next_event()
            clock = next_event.time  # move clock to the time of the event
            BlockCommit.handle_event(next_event)
            Queue.remove_event(next_event)


        Consensus.fork_resolution()  # apply the longest chain to resolve the forks
        # distribute the rewards between the particiapting nodes
        #Incentives.distribute_rewards()
        # calculate the simulation results (e.g., block statstics and miners' rewards)
        Statistics.calculate()

        ########## reset all global variable before the next run #############
        Statistics.reset()  # reset all variables used to calculate the results
        Node.resetState()  # reset all the states (blockchains) for all nodes in the network
        fname = "(Allverify)1day_{0}M_{1}K.xlsx".format(
            p.Bsize/1000000, p.Tn/1000)
        # print all the simulation results in an excel file
        Statistics.print_to_excel(fname)
        fname = "(Allverify)1day_{0}M_{1}K.xlsx".format(
                p.Bsize/1000000, p.Tn/1000)
        # print all the simulation results in an excel file
        Statistics.print_to_excel(fname)
        Statistics.reset2()  # reset profit results


######################################################## Run Main method #####################################################################
if __name__ == '__main__':
    main()
