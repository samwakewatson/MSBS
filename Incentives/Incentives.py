from Config import Config as p

'''match p.shardConsensus:
    case 0:
        from Consensus.Delay import Consensus as c
    case 1:
        from Consensus.FBFT import Consensus as c
    case 2: 
        #from Consensus.HarmonyONE import Consensus
        from Consensus.Consensus import Consensus as c
    case 3:
        from Consensus.SlotBased import Consensus as c'''

if p.shardConsensus == 0:
    from Consensus.Delay import Consensus as c
elif p.shardConsensus == 2:
    from Consensus.Consensus import Consensus as c

class Incentives:

    """
	 Defines the rewarded elements (block + transactions), calculate and distribute the rewards among the participating nodes
    """
    def distribute_rewards():
        for i in range(0,p.numShards):
            for bc in c.global_chain[i]:
                for m in p.NODES:
                    if bc.miner == m.id:
                        m.blocks +=1
                        m.balance += p.Breward # increase the miner balance by the block reward
                        tx_fee= Incentives.transactions_fee(bc)
                        m.balance += tx_fee # add transaction fees to balance


    def transactions_fee(bc):
        fee=0
        for tx in  bc.transactions:
            fee += tx.fee
        return fee
