from Config import Config as p

'''match p.shardConsensus:
    case 0:
        from Consensus.Delay import Consensus as c
    case 1:
        from Consensus.FBFT import Consensus as c
    case 2: 
        from Consensus.HarmonyONE import Consensus as c'''

if p.shardConsensus == 0:
    from Consensus.Delay import Consensus as c
elif p.shardConsensus == 2:
    from Consensus.HarmonyONE import Consensus as c

class Consensus(c):
    i = 0