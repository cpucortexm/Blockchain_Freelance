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
from ns_mine import NSMine
from ns_db import NSDb
import ns_transaction as transaction
import sys

class NSChain:

    def __init__(self):
        self.lasthash = None
        self.db = None
        self.genesis_init = False
        self.logger = pylog.get_logger(__name__)

    def __repr__(self):
        return (f'{self.__class__.__name__}')

    def init_blockchain(self, address):
        self.db = NSDb()  # init database
        NSMine.init_consensus()
        genesisData = "First transaction from Genesis"
        self.genesis_init = True
        if self.Dbexists():
            self.logger.info("Blockchain already exists!")
            sys.exit()
        # else if  the database does not exist
        coinbaseTx = transaction.CoinbaseTx(genesisData, address)
        block = nsblock.init_block(coinbaseTx)
        self.logger.info("Genesis created")
        self.db.write_block(block) # write genesis to database
        self.db.write_last_hash(block)
        self.lasthash = self.db.read_last_hash() # read last hash

    def continue_blockchain(self, address):
        if not self.Dbexists():    # if db does not exist , exit the program
            self.logger.info("No existing blockchain found, create one!")
            sys.exit()

        return self.get_blockchain()  # return the blockchain

    
    def add_block(self,transactions):
        if not self.genesis_init:
            assert False, ('Must Initialize the Blockchain first!!')
        if type(transactions) is not NSTx: # data must be of NSTx type
            raise Exception("Sorry, input must be of transaction type")
        lastblock = self.get_prev_block()
        block = nsblock.add_block_(data, lastblock)
        self.logger.info("Block hash: %s",block['hash'])
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

    # UTXO : Unspent transaction Outputs helps solve double spend
    # The theory :
    '''
    An unspent transaction output (UTXO) refers to a transaction output that can be used as
    input in a new transaction. In essence, UTXOs define where each blockchain transaction 
    starts and finishes. The UTXO model is a fundamental element of Bitcoin and many other 
    cryptocurrencies.

    In other words, cryptocurrency transactions are made of inputs and outputs. Anytime a 
    transaction is made, a user takes one or more UTXOs to serve as the input(s). Next, the
    user provides their digital signature to confirm ownership over the inputs, which finally
    result in outputs. The UTXOs consumed are now considered "spent," and can no longer be 
    used. Meanwhile, the outputs from the transaction become new UTXOs – which can be spent 
    in a new transaction later.

    This is probably better explained with an example. Alice has 0.45 BTC in her wallet. This
    isn’t a fraction of a coin as we might conceptualize it. It’s rather a collection of UTXOs.
    Specifically, two UTXOs worth 0.4 BTC, and 0.05 BTC – outputs from past transactions. Now 
    let's imagine that Alice needs to make a payment to Bob of 0.3 BTC.

    Her only option here is to break up the 0.4 BTC unit and to send 0.3 BTC to Bob, and 0.1
    BTC back to herself. She would normally reclaim less than 0.1 BTC due to mining fees, but
    let's simplify and leave the miner out.
    Alice creates a transaction that essentially says to the network: take my 0.4 BTC UTXO as
    an input, break it up, send 0.3 BTC of it to Bob’s address and return the 0.1 BTC to my
    address. The 0.4 BTC is now a spent output, and can’t be reused. Meanwhile, two new UTXOs
    have been created (0.3 BTC and 0.1 BTC).
    Note that we broke up a UTXO in this example, but if Alice had to pay 0.42 BTC, she could
    just as easily have combined her 0.4 BTC with another 0.05 BTC to produce a UTXO worth
    0.42 BTC, while returning 0.03 BTC to herself.
    Summing up, the UTXO model serves as the protocol’s mechanism for keeping track of where
    coins are at any given time. In a sense, they operate much like cheques: they’re addressed
    to specific users (or rather, their public addresses). UTXOs cannot be spent in part –
    instead, new cheques must be created from the old one and passed along accordingly.
    '''

    def find_UnspentTransactions(self, address):
        unspentTxs = [] # holds a list of type class NSTx = transactions
        spentTXOs = {}  # map of strings(ID) to list(array) of int value(NSTxIn.Out)

        currhash  = self.db.read_last_hash() # start from last hash
        while(len(currhash) != 0)  # for genesis block, prev hash is empty="", hence len(currhash) == 0
            currblock = self.db.read_block(currhash) # read the last block

                # Loop through all the transactions of the current block
                for idx, tx in enumerate(currblock['Tx']): # each tx = object of class NSTx
                    txID = tx.ID   # get the ID= hash for the transaction
                    for outIdx, outTx in enumerate(tx.TxOut):
                        if spentTXOs[txID]:   # if the value for the key exists (true or false)
                            for spentOut in  spentTXOs[txID]: # iterate through the map value (list or array of int's)
                                if spentOut == outIdx:
                                    break    # break from inner loop and continue back to outer for loop (outIdx, outTx)

                        if transaction.CanBeUnlocked(address, outTx):
                            unspentTxs.append(tx)

                    if(transaction.IsCoinbase(tx) == False):
                        # Loop through the list of all the tx inputs(TxIn) of the current tx
                        for inIdx, inTx in enumerate(tx.TxIn):
                            if(transaction.CanUnlock(address, inTx)): # as we are using user's address as Signature in input
                                spentTXOs[inTx.ID].append(inTx.Out)  #append value = Out, to the key=ID
        return unspentTxs


        def find_UTXO(self,address):
            UTXOs = []  # variable of type NSTxOut
            unspenttxs = self.find_UnspentTransactions(address)

            for tx in unspenttxs:
                for out in tx.TxOut:
                    if transaction.CanBeUnlocked(address, out):
                        UTXOs.append(out)
            return UTXOs

        def find_SpendableOutputs(self, address, amount):
            unspentOuts = {}   #  map of strings(ID) to list(array) of int value(NSTxIn.Out)
            unspentTxs = self.find_UnspentTransactions(address)
            accumulated = 0

            for tx in unspentTxs:
                txID = tx.ID   # get the ID= hash for the transaction
                for outIdx, outTx in enumerate(tx.TxOut):
                    if transaction.CanBeUnlocked(address, outTx) and (accumulated < amount):
                        accumulated += outTx.value
                        unspentOuts[txID].append(outIdx)
                        if accumulated >= amount:   # break from all the loops and return
                            return accumulated, unspentOuts
            return accumulated, unspentOuts

    def __del__(self):
        del self.db    # Cleanup operation during exit
