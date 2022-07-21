from Consensus.BaseConsensus import Consensus as BaseConsensus
#so this is supposed to mimic an ouroboros like system
#so we have a load of slots which may or may not have a leader elected
#note that a lot of the changes here have to be in BlockCommit, as it currently governs
#wayyyyy too much in terms of blockchain logic (and also doesn't really play very nicely with a modular 
# design)

#do we need a few different blockcommits as well?

class Consensus(BaseConsensus):
    def timeToReachConsensus():
        return 1
        #obviously this makes no sense at all in the scheme we're using