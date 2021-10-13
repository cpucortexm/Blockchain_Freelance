# @Filename:    ns_blockchain.py
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

from pylogger import pylog
from ns_block import NSBlock as nsblock
from mine import Mine

class NSChain:

    def __init__(self):
        self.nschain = []   # chain of blocks = blockchain
        self.genesis_init = False
        self.logger = pylog.get_logger(__name__)

    def __repr__(self):
        return (f'{self.__class__.__name__}')


    def init_blockchain(self):
        Mine.init_consensus()
        block = nsblock.init_block("NS-Genesis")
        self.nschain.append(block) # append the genesis block to chain
        self.genesis_init = True
    
    def add_block(self,data):
        if not self.genesis_init:
            assert False, ('Must Initialize the Blockchain first!!')
        if type(data) is not str: # data must be of string type
            data  = str(data)
        lastblock = self.get_prev_block()
        block = nsblock.add_block_(data, lastblock)
        self.nschain.append(block) # append the block to the chain


    def get_prev_block(self):
        # for genesis block , prev block is none
        return None if not self.nschain else (self.nschain[-1])

    def get_blockchain(self):
        return self.nschain

    def print_nschain(self):
        for block in self.nschain:
            self.logger.info("hash:%s",block['hash'])
            self.logger.info("data:%s", block['data'])
            self.logger.info("prevHash:%s",block['prevHash'])
            self.logger.info("-----------------------")

