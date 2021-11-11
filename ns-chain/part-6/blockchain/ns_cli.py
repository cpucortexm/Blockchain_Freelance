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


def print_blockchain():
  bc.print_nschain()

def block_add(args):
  logger.info("Adding block to the chain : %s", args.block)
  bc.add_block(args.block)

def test_chain():
  # Set the static class variable of test file(=blockchain) to the blockchain(bc) to be tested
  # There can be other better methods like using parameterized constructors with pytest,
  # instead of using static class variables for writing tests.
  ns_blockchain_test.TestNSChain.blockchain = bc
  ns_blockchain_test.start_blockchain_tests()


if __name__ == '__main__':

    # variables here will be global
    bc = NSChain()      # Create blockchain
    bc.init_blockchain()   # initialise blockchain

    # Use subparser if you want different arguments to be permitted
    # based on the command being run
    parser     = argparse.ArgumentParser()
    subparser  = parser.add_subparsers(dest='command')
    printchain = subparser.add_parser('print')
    addblock   = subparser.add_parser('add')
    verifychain = subparser.add_parser('test')

    addblock.add_argument('-block', type=str, required = True, help ='Add block data')

    if len(sys.argv) < 2:
      parser.print_help()
      sys.exit()


    args = parser.parse_args()
    # args.command is either 'print' or 'add', see subparser above
    logger = pylog.get_logger(__name__)
    if args.command == 'print':   # print an existing blockchain
      print_blockchain()
    elif args.command == 'add':   # add block to the blockchain
      block_add(args)
    elif args.command == 'test': # verify the blockchain created is fine by performing unit tests 
      test_chain()
