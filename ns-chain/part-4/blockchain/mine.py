# @Filename:    mine.py
# @Author:      Yogesh K
# @Date:        13/10/2021
"""
  This file is part of ns-chain.

    ns-chain is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    ns-chain is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with ns-chain.  If not, see <https://www.gnu.org/licenses/>.
 """
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

import random
import ns_block

# Further improvements: use Mine class to init the consensus mechanism using CLI.
# Activate the consensus class accordingly

class Proof_Of_Work:    
  def __init__(self):
    self.difficulty = 4
  
  def mine_block(self,block):
      # Can be directly accessed from the blockchain class
    calculated_hash = ns_block.NSBlock.derive_hash(block)
    target = '0'.zfill(self.difficulty)
    # keep looping until the calculated hash meets the target
    while(calculated_hash[:self.difficulty].startswith(target) is False):
      block['nonce'] += random.randrange(1, 1024) # you can also use getrandombits(64bit)
      calculated_hash = ns_block.NSBlock.derive_hash(block)

    return calculated_hash  # if it exits while, means condition match, return the hash



class Proof_Of_Stake:
  def __init__(self):
    pass
  
  def mine_block(block):
    pass


class Mine:
  mine_with = None
  
  @classmethod
  def init_consensus(cls):  # TBD: a param can be passed, to choose consensus mechanism
    cls.mine_with =  Proof_Of_Work() # create the instance of the class for consensus
  
  @classmethod
  def start_mining(cls, block):
    return cls.mine_with.mine_block(block)


'''
Using single dispatch function overriding technique
from functools import singledispatch
@singledispatch
def mine_block(any_object):
  raise NotImplementedError


@mine_block.register
def _(any_object: Proof_Of_Work, block):
  # Can be directly accessed from the blockchain class
  calculated_hash = ns_block.NSBlock.derive_hash(block)        
  target = '0'.zfill(any_object.difficulty)
  # keep looping until the calculated hash meets the target
  while(calculated_hash[:any_object.difficulty].startswith(target) is False):
    block['nonce'] += random.randrange(1, 1024) # you can also use getrandombits(64bit)
    calculated_hash = ns_block.NSBlock.derive_hash(block)

  return calculated_hash  # if it exits while, means condition match, return the hash



@mine_block.register
def _(any_object: Proof_Of_Stake):
  return None
'''
