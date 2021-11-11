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

# test an existing blockchain

class TestNSChain(unittest.TestCase):
    blockchain = None        # Declare static variable
    def test_blockchain(self):
      chain = self.blockchain.get_blockchain()
      h = chain[0]['hash'] # chain is a list. Row will be block no, column will be key content 
      for _, block in enumerate(chain[1:]):
        h_c = block['hash']   #current hash
        h_p = block['prevHash'] # prev hash
        # compare previous hash of current block (h_p) with hash of previous block (h)
        self.assertEqual(h, h_p) 
        h = h_c

# unittest.main looks at sys.argv by default, which is what started IPython,
# You can pass an explicit list to main to avoid looking up sys.argv.
# Otherwise an error occurs if unittest.main is called from another file
def start_blockchain_tests():
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(unittest.makeSuite(TestNSChain))
