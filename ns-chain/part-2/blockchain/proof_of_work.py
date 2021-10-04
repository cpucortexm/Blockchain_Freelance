# What Does Proof of Work Mean (also called mining)?
# PoW requires nodes on a network to provide evidence that they have expended 
# computational power (i.e. work) in order to achieve consensus in a
# decentralized manner and to prevent bad actors from overtaking the network.
# Without proof of work, there can be two major problems
# 1. anyone can spam the network with multiple blocks as calculating hashes is trivial
#    on any modern computer, clogging the blockchain network
# 2. anyone can tamper the data of a block, recalculate the block and subsequent block
#    hashes and still make the chain valid

# With PoW, the computer needs to spend resources and time to calculate the hash that
# meets a target so as to make the block valid. This solves the above problems as it 
# provides a proof that the miner did some work to add the block to the blockchain




import ns_blockchain
import random

class Proof_Of_Work:
    difficulty = 4
        
    @classmethod   # Can be directly accessed from the blockchain class
    def mineBlock(cls, block):
        calculated_hash = ns_blockchain.NSChain.DeriveHash(block)        
        target = '0'.zfill(cls.difficulty)

        # keep looping until the calculated hash meets the target
        while(calculated_hash[:cls.difficulty].startswith(target) is False):
            block['nonce'] += random.randrange(1, 1024) # also use getrandombits(64bit)
            calculated_hash = ns_blockchain.NSChain.DeriveHash(block)
        return calculated_hash   
