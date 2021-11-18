# @Filename:    ns_cli.py
# @Author:      Yogesh K
# @Date:        03/11/2021
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

import argparse
import sys
from ns_blockchain import NSChain
from pylogger import pylog
import ns_blockchain_test
import ns_transaction


def print_blockchain():
  bc.print_nschain()

def create_blockchain(args):
  logger.info("Adding address to the chain : %s", args.address)
  bc.init_blockchain(args.address)
  logger.info("Finished!")

def get_balance(args):
  chain = bc.continue_blockchain(args.address)
  balance = 0
  UTXOs = bc.find_UTXO(args.address)

  for out in UTXOs:
    balance += out.value

  logger.info("Balance of %s:%d", args.address, balance)

def send(args):
  chain = bc.continue_blockchain(args.comingfrom)
  acc, validOutputs = bc.find_SpendableOutputs(args.comingfrom, args.amount)
  tx = ns_transaction.New_Transaction(args.comingfrom, args.to, args.amount, acc, validOutputs)
  bc.add_block(tx)
  logger.info("Success!")

def test_chain():
  # Set the static class variable of test file(=blockchain) to the blockchain(bc) to be tested
  # There can be other better methods like using parameterized constructors with pytest,
  # instead of using static class variables for writing tests.
  ns_blockchain_test.TestNSChain.blockchain = bc
  ns_blockchain_test.start_blockchain_tests()


if __name__ == '__main__':

    # variables here will be global
    bc = None# = NSChain()      # Create blockchain

    # Use subparser if you want different arguments to be permitted
    # based on the command being run
    parser     = argparse.ArgumentParser()
    subparser  = parser.add_subparsers(dest='command')
    getbalance = subparser.add_parser('getbalance')
    createchain= subparser.add_parser('createblockchain')
    printchain = subparser.add_parser('printchain')
    transact   = subparser.add_parser('send')
    verifychain = subparser.add_parser('test')

    getbalance.add_argument('--address',type=str,required= True, help='get balance for the address')
    createchain.add_argument('--address',type=str,required= True, help='create blockchain for the address')
    transact.add_argument('--comingfrom',type=str,required= True, help='source wallet address')
    transact.add_argument('--to',type=str,required= True, help='destination wallet address')
    transact.add_argument('--amount',type=int,required= True, help='amount to be sent')


    if len(sys.argv) < 2:
      parser.print_help()
      sys.exit()


    args = parser.parse_args()
    bc = NSChain()  # Create blockchain object
    # args.command is either 'print' or 'add', see subparser above
    logger = pylog.get_logger(__name__)
    if args.command == 'printchain':   # print an existing blockchain
      print_blockchain()

    elif args.command == 'createblockchain':   # create a blockchain
      create_blockchain(args)

    elif args.command == 'getbalance':
      get_balance(args)

    elif args.command == 'send':
      send(args)

    elif args.command == 'test': # verify the blockchain created is fine by performing unit tests 
      test_chain()
