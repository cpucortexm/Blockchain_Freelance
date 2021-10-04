# @Filename:    ns_blockchain.py
# @Author:      Yogesh K for not-satoshi and Finxter academy

import hashlib
from pylogger import pylog
import proof_of_work

class NSChain:
    def __init__(self):
        self.nschain = []   # chain of blocks = blockchain
        self.genesis_init = False
        self.logger = pylog.get_logger(__name__)

    def __repr__(self):
        return (f'{self.__class__.__name__}')

    def init_blockchain(self):
        self.__CreateBlock("NS-Genesis")
        self.genesis_init = True

    def add_block(self,data):
        if not self.genesis_init:
            assert False, ('Must Initialize the Blockchain first!!')
        if type(data) is not str: # data must be of string type
            data = str(data)
        self.__CreateBlock(data)
        

    @staticmethod 
    def DeriveHash(block=None):
        complete_block = block['data']  + block['prevHash'] + str(block['nonce'])
        msg = bytes(complete_block, 'utf-8')
        return hashlib.sha256(msg).hexdigest()
        

    def __CreateBlock(self, data):
        #represents one block. Dont use global block i.e. in __init__ as dicts 
        # use references and hence append dict to list will reference the last item only. 
        block ={
            'hash': "", 
            'data': "",
            'prevHash':"", # for genesis block, there is no prev hash. It is null
            'nonce' : 0
        }

        prevblock = self.get_prev_block()
        if prevblock:               # only if valid block, for genesis block, prev hash=NULL
            block['prevHash'] = prevblock['hash']

        block['data'] = data
        block['hash'] = proof_of_work.Proof_Of_Work.mineBlock(block)
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
