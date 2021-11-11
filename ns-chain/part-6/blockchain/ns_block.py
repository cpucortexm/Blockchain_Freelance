# @Filename:    ns_block.py
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


import hashlib
from ns_mine import NSMine


# Most functions are utility functions (perform local calculations and return)
# and hence are static. i.e.Totally self-contained code.

class NSBlock:
    @staticmethod
    def init_block(coinbaseTx):
        return NSBlock.create_block(coinbaseTx)

    @staticmethod
    def add_block_(data, prev):
        return NSBlock.create_block(data, prev)

    @staticmethod 
    def derive_hash(block=None):
        if block is not None:
            complete_block = NSBlock.hash_of_tx(block)  + block['prevHash'] + str(block['nonce'])
            msg = bytes(complete_block, 'utf-8')
            return hashlib.sha256(msg).hexdigest()
        
    @staticmethod
    def create_block(txs, prevblock=None):
        # represents one block. Dont use global block i.e. in __init__ as dicts 
        # use references and hence append dict to list will reference the last item only. 
        block ={
            'hash': "",

            'Tx': [],# each block needs to have at least one transaction.It can always
                     # have multiple transactions as well.
                     # Tx is a list of type class NSTx
            
            'prevHash':"", # for genesis block, there is no prev hash. It is null
            
            'nonce' : 0
        }

        if prevblock:  # only if valid block, for genesis block, prev hash=NULL
            block['prevHash'] = prevblock['hash']

        block['Tx'] = txs
        block['hash'] = NSMine.start_mining(block)
        return block

        @staticmethod
        def hash_of_tx(block):
            idlist = [] # list to collect all the tx hashes of the block
            hash_sum = ''  # empty

            for index, tx in enumerate(block['Tx'])    # get each tx from the list block['Tx']
                idlist.append(tx.ID)                   # each tx is an object of type class NSTx
                                                       # tx.ID gives the hash of every transaction
                                                       # Note: tx.ID is already a string


            for index, id in enumerate(idlist)    # Go through each ID (hash) and join them
                hash_sum = ''.join(id[index])

            msg = bytes(hash_sum, 'utf-8')
            return hashlib.sha256(msg).hexdigest()   # Find hash of all the hashes in the transactions


