'''
Copyright (c) 2022 Algorand Name Service DAO LLC

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

import unittest, time
from algosdk import mnemonic
import json, random, string
import helper
import mysecrets
from pyteal import *

unittest.TestLoader.sortTestMethodsUsing = None

class TestContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.algod_client = helper.SetupClient("purestake")
        cls.funding_addr, cls.funding_acct_mnemonic = helper.GetFundingAccount(cls.algod_client)
        cls.algod_indexer = helper.SetupIndexer("purestake")

        cls.new_acct_addr, cls.new_acct_mnemonic = helper.GenerateAccount()

        print("Generated new account: "+cls.new_acct_addr)

        cls.name = ''.join(random.choice(string.ascii_lowercase) for i in range(6))
        cls.app_index = 0

    def test_a_prep_lsig(self):#algod_client, expiry, name="lalith", method="subscribe"):
        #logic_sig_teal = compileTeal(ValidateRecord(name, expiry), Mode.Signature, version=4)
        helper.prep_test_lsig(TestContract.algod_client)

    def test_b_deploynameregistry(self):
        
        #random code here
        #helper.prep_lsig(TestContract.algod_client, int(time.time()))
        
        helper.FundNewAccount(TestContract.algod_client, TestContract.new_acct_addr, 901000, TestContract.funding_acct_mnemonic)    

        print("Funded 1801000 to new account for the purpose of deploying registry")
        print("Funding account: "+TestContract.funding_addr)

        # Set App index
        TestContract.app_index = helper.DeployContract(TestContract.algod_client, TestContract.new_acct_mnemonic)

        print("Deployed contract to APP_ID: "+str(TestContract.app_index))
        '''
        time.sleep(5)
        response=TestContract.algod_indexer.applications(TestContract.app_index)
        self.assertEqual(TestContract.app_index, response["application"]["id"])
        self.assertEqual(TestContract.new_acct_addr,response["application"]["params"]["creator"])
        '''



# TODO: See where tearDown goes, class or outside
def tearDownClass(self) -> None:
    # TODO: clear all variables?
    return super().tearDown()

if __name__ == '__main__':
    unittest.main()
