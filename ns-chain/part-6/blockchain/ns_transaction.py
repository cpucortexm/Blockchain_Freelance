# @Filename:    ns_transaction.py
# @Author:      Yogesh K
# @Date:        08/11/2021

# In Bitcoin Tx handling is done using script language. Script allows you to program
# the bitcoin such as sending BTC from wallet, create multi user accounts etc.
# With script you can basically create smart contracts on Bitcoin, though with
# limited functionality compared to that of Ethereum.
# Here we will not use script, but define our own transactions

# The trustless system is because of the transactions. In trustless systems everyone
# can verify everything

# Transactions(Tx) represent activity. The more the transactions, the more the people
# are using the blockchain for projects, dapps, smart contracts.

# In Tx, inputs specify which outputs of previous tx to spend
# outputs specify where the money goes.



import hashlib
import ns_blockchain as blockchain
from pylogger import pylog
# Class representing transaction outputs
class NSTxOut:
    def __init__(self, _value, _pubkey):
        self.value = _value    # is an integer (value are mostly in tokens)

        # string (is also called public key hash PKH).This is needed to unlock the tokens in the value field
        # In bitcoin, the PublicKey is calculated using a language called script and is complicated.
        # In our implementation, we will use users address as the PublicKey.
        # e.g. if users address is "Jack" then PublicKey = "Jack" and using this we can unlock
        # the tokens in the value field
        self.PublicKey = _pubkey

    def __str__(self):
        return str(self.__dict__)


# Class representing transaction inputs
class NSTxIn:
        # The inputs specify which transaction outputs to spend.
        # Please read UTXO in ns_blockchain file.
    def __init__(self, id, out, sig):
        # e.g. if the transaction(say x) has 30 outputs, and we want to reference 
        # only one of them,then the transaction x is represented by ID, and the output with index = Out
        self.ID = id     # list of bytes (hash value of type string), represents a transaction hash
        self.Out = out   # integer: Index to output (i.e previous output index), basically index to the PublicKey of the output

        # The inputs need to be signed. In bitcoin, this is again done using the language script.
        # The signing involves both public key and private key of the user. Public key is the output
        # public key (PKH) while private key is the one which is private to the user.
        # In our case as we will just use the PublicKey of the output (i.e.the user's address) as
        # our signature.
        self.Signature = sig   # string (same as PublicKey of output = users address)

    def __str__(self):
        return str(self.__dict__)


# Class representing a transaction
class NSTx:
    def __init__(self, id, txins=[], txouts=[]):
        self.ID = id    # list of bytes (hash value of type string), represents a transaction hash of current transaction.
        self.TxIn = txins  # list of NSTxIn
        self.TxOut = txouts # list of NSTxOut

    def __str__(self):
        return str(self.__dict__)

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
    tx  = NSTx(None, [txin], [txout])

    tx.SetID()
    return tx

def IsCoinbase(tx):   # returns true or false
    if type(tx) is not NSTx:
        raise Exception("Input must be of NSTx type")
    return (len(tx.TxIn) == 1  and len(tx.TxIn[0].ID) == 0  and tx.TxIn[0].Out == -1)

def CanUnlock(data, txin): # returns true or false
    if type(txin) is not NSTxIn:
        raise Exception("Input must be of NSTxIn type")
    return txin.Signature == data

def CanBeUnlocked(data, txout): # returns true or false
    if type(txout) is not NSTxOut:
        raise Exception("Output must be of NSTxOut type")
    return txout.PublicKey == data


def New_Transaction(tx_from, tx_to, amount, acc,validOutputs):
    inputs = []   # list of type class NSTxIn
    outputs = []  # list of type class NSTxOut
    #acc = 0  # int accumulated
    #validOutputs = {} #  map of strings(ID) to list(array) of int value(NSTxIn.Out)
    logger = pylog.get_custom_logger(__name__)
    #acc, validOutputs = blockchain.find_SpendableOutputs(tx_from, amount)
    if acc < amount:
        logger.error("Error: not enough funds")

    print("acc:", acc)
    print("validOutputs:",validOutputs.items())

    for txID, outs in validOutputs.items():  # iterate through dict (key = string(ID), value = list(array) of int's)
        for out in outs:    # loop through the values (list(array) of int's)
            tx_input =  NSTxIn(txID, out, tx_from)
            inputs.append(tx_input)


    outputs.append(NSTxOut(amount, tx_to))
    if acc > amount:  # if there is a leftover token of the senders account
        outputs.append(NSTxOut(acc-amount, tx_from))

    tx = NSTx(None,inputs,outputs)
    tx.SetID()    # sets the hash of the transaction
    return tx












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