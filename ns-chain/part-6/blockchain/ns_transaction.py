# @Filename:    ns_transaction.py
# @Author:      Yogesh K
# @Date:        08/11/2021

# In Bitcoin Tx handling is done using script language. Script allows you to program
# the bitcoin such as sending BTC from wallet, create multi user accounts etc.
# With script you can basically create smart contracts on Bitcoin, though with
# limited functionality compared to that of Ethereum.
# Here we will not use script, but define our own transactions

# Transactions represent activity. The more the transactions, the more the people
# are using the blockchain for projects, dapps, smart contracts. 

import hashlib

class NSTxOut:
    def __init__(self,):
        self.value = None    # int
        self.PublicKey = None # string

class NSTxIn:
    def __init__(self, id, out, sig):
        self.ID = id     # list of bytes (hash value of type string)
        self.Out = out   # integer: Index to output (i.e previous output index)
        self.Signature = sig   # string

class NSTx:
    def __init__(self, id, txins, txouts):
        self.ID = id    # list of bytes (hash value of type string)
        self.TxIn = txins  # list of NSTxIn
        self.TxOut = txouts # list of NSTxOut

    def SetID(self):
        complete_block = str(self.ID)  + str(self.TxIn) + str(self.TxOut)
        msg = bytes(complete_block, 'utf-8')
        self.ID = hashlib.sha256(msg).hexdigest()     # self.ID will be of string type



# Called during Genesis block creation. The first tx is called Coinbase tx
# ToDo: Can be a class method as it creating a new object of type NSTx
def CoinbaseTx(data, to):
    if not data:    # if data is empty string (i.e. data = "")
        data = 'Coins to {}'.format(to)

    txin  = NSTxIn([], -1, data) # start with empty hash and -1 for coinbaseTx
    txout = NSTxOut(100, to)
    tx  = NSTx(None, txin, txout)

    tx.SetID()
    return tx

def IsCoinbase(tx):   # returns true or false
    if type(tx) is not NSTx:
        raise Exception("Input must be of NSTx type")
    return len(tx.TxIn) == 1  && len(tx.TxIn[0].ID == 0   && tx.TxIn[0].Out == -1)

def CanUnlock(data, txin):
    if type(txin) is not NSTxIn:
        raise Exception("Input must be of NSTxIn type")
    return txin.Signature == data

def CanBeUnlocked(data, txout):
    if type(txout) is not NSTxOut:
        raise Exception("Output must be of NSTxOut type")
    return txout.PublicKey == data

'''
self.__chain = []
self.__current_transactions = []

@property
def last_block(self):
    return self.__chain[-1]

@property
def last_transaction(self):
    return self.__current_transactions[-1]

@property
def pending_transactions(self):
    return self.__current_transactions

@property
def full_chain(self):
    return self.__chain

__chain: A list of Blocks representing the blockchain [private]
__current_transactions: The list of transactions which are not yet part of a block [private]
last_block: The last block added to the chain
last_transaction: The last transaction added to the chain
pending_transactions: returns the __current_transactions attribute
full_chain: returns the __chain attribute
'''