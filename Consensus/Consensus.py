from Config import Config as p

#im sure this is horrible practice and i really should find another way to do this

match p.shardConsensus:
    case 0:
        from Consensus.Delay import Consensus as c
    case 1:
        from Consensus.FBFT import Consensus as c
    case 2: 
        from Consensus.HarmonyONE import Consensus as c

class Consensus(c):
    i = 0