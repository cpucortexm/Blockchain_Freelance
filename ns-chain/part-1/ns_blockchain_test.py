import unittest
from ns_blockchain import nsChain

class TestNSChain(unittest.TestCase):

    def test_blockchain(self):
        bc = nsChain()
        bc.init_blockchain()
        bc.add_block("First Block after Genesis")
        bc.add_block("Second Block after Genesis")
        bc.add_block("Third Block after Genesis")
        bc.add_block("Fourth Block after Genesis")
        bc.add_block("Fifth Block after Genesis")
        bc.print_nschain()
        chain = bc.get_blockchain()
        h = chain[0]['hash']
        for _, block in enumerate(chain[1:]):
            h_c = block['hash']   #current hash
            h_p = block['prevHash'] # prev hash
            self.assertEqual(h, hp)
            h = hc

if __name__ == '__main__':
    unittest.main()
