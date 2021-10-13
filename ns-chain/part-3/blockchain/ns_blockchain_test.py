# @Filename:    ns_blockchain_test.py
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
import unittest
from ns_blockchain import NSChain

class TestNSChain(unittest.TestCase):

    def test_blockchain(self):
        bc = NSChain()
        bc.init_blockchain()
        bc.add_block("First Block after Genesis")
        bc.add_block("Second Block after Genesis")
        bc.add_block("Third Block after Genesis")
        bc.add_block("Fourth Block after Genesis")
        bc.add_block("Fifth Block after Genesis")
        bc.print_nschain()
        chain = bc.get_blockchain()
        h = chain[0]['hash'] # chain is a list. Row will be block no, column will be key content 
        for _, block in enumerate(chain[1:]):
            h_c = block['hash']   #current hash
            h_p = block['prevHash'] # prev hash
            # compare previous hash of current block (h_p) with hash of previous block (h)
            self.assertEqual(h, h_p) 
            h = h_c

if __name__ == '__main__':
    unittest.main()
