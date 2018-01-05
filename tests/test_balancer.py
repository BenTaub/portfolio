# test_balancer.py

import datetime

from django.test import TestCase

import portfolio.balancer


class TestCalcAcctValues(TestCase):
    def test_no_holdings(self):
        val_dict = portfolio.balancer.calc_acct_values([])
        self.assertEqual(len(val_dict), 0)
        self.assertDictEqual(val_dict, {})

    def test_one_acct_one_holding(self):
        holdings = [{'VALUE_DATE': datetime.datetime.today(), 'HOLDING_ID': 1, 'ACCOUNT_ID': 1,
                     'ACCOUNT_NAME': 'Acct 1', 'ASSET_ID': 1, 'ASSET_NAME': 'Ass 1', 'HOLDING_ID': 'Holding 1',
                     'HOLDING_DATE': datetime.datetime.today(), 'NUM_SHARES': 100.5, 'PRICE_ID': 1,
                     'PRICE_DATE': datetime.datetime.now(), 'PRICE': 2, 'VALUE': 201}]
        val_dict = portfolio.balancer.calc_acct_values(holdings)
        self.assertEqual(len(val_dict), 1)
        self.assertDictEqual(val_dict, {1: 201})

    def test_one_acct_mult_holding(self):
        self.assertTrue(False, 'Test not yet written')
        # val_dict = portfolio.balancer.calc_acct_values([])
        # self.assertEqual(len(val_dict), 0)
        # self.assertDictEqual(val_dict, {})

    def test_mult_acct(self):
        # Make sure that one acct has one holding and the other has mult holdings
        self.assertTrue(False, 'Test not yet written')
        # val_dict = portfolio.balancer.calc_acct_values([])
        # self.assertEqual(len(val_dict), 0)
        # self.assertDictEqual(val_dict, {})
