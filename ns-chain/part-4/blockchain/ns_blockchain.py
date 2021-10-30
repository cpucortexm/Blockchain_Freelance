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
from ns_db import NSDb

class NSChain:

    def __init__(self):
        self.lasthash = None
        self.db = None
        self.genesis_init = False
        self.logger = pylog.get_logger(__name__)

    def __repr__(self):
        return (f'{self.__class__.__name__}')

    def init_blockchain(self):
        self.db = NSDb()  # init database
        Mine.init_consensus()
        self.lasthash = self.db.read_last_hash() # read last hash
        if self.lasthash is None:  # first time you need to create genesis
            self.logger.info("No existing blockchain found..!")
            block = nsblock.init_block("NS-Genesis")
            self.db.write_block(block) # write genesis to database
            self.db.write_last_hash(block)

        self.genesis_init = True
    
    def add_block(self,data):
        if not self.genesis_init:
            assert False, ('Must Initialize the Blockchain first!!')
        if type(data) is not str: # data must be of string type
            data  = str(data)
        lastblock = self.get_prev_block()
        block = nsblock.add_block_(data, lastblock)
        self.db.write_block(block) # append the block to the chain in database
        self.db.write_last_hash(block) # also write last hash to the database

    def get_prev_block(self):
        lasthash  = self.db.read_last_hash() # read last hash
        lastblock = self.db.read_block(lasthash)
        return lastblock

    def get_blockchain(self):
        nschain = []  # start with empty list
        currhash  = self.db.read_last_hash() # start from last hash
        while currhash: # for genesis block, prev hash is empty=""
            currblock = self.db.read_block(currhash) # read the last block
            # we use insert instead of append. We need to append in reverse direction
            # is an expensive operation because of shift involved. Use deque()
            # instead of list
            nschain.insert(0, currblock)
            currhash = currblock['prevHash']
        return nschain

    def print_nschain(self):
        nschain = self.get_blockchain()
        for block in nschain:
            self.logger.info("hash:%s",block['hash'])
            self.logger.info("prevHash:%s",block['prevHash'])
            self.logger.info("data:%s", block['data'])
            self.logger.info("-----------------------")
