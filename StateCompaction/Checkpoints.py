'''We want to model the node only downloading the blocks it needs
So in the case of checkpointing (in harmonyONE for example) we only need
the checkpoint blocks and however many blocks currently exist

What do we want this module to do?
    Simulate time taken to get up to speed with the network?
    Manage what each node stores to its blockchain?
    Do we want to move parts of BlockCommit to this module?
    
    In fact, this is going to have to control almost all of the blockchain stuff
    
    Otherwise how on earth are we going to get it to work?
    
    We can't use an up to date flag in all systems'''