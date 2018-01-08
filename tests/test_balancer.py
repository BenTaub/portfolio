# test_balancer.py

import datetime

from django.test import TestCase

import portfolio.balancer


class TestBalancePortfolio(TestCase):
    def test_no_holdings(self):
        required_changes = portfolio.balancer.balance_portfolio(curr_holdings_and_values=[], balance_pcts=[])
        self.assertEqual(len(required_changes), 0)

    def test_acct(self):
        self.assertTrue(False)

    def test_mult_accts(self):
        self.assertTrue(False)

    def test_some_holdings_go_to_zero(self):
        self.assertTrue(False)


class TestCalcAcctValues(TestCase):
    def test_no_holdings(self):
        val_dict = portfolio.balancer.calc_acct_values([])
        self.assertEqual(len(val_dict), 0)
        self.assertDictEqual(val_dict, {})

    def test_one_acct_one_holding(self):
        holdings = [{'VALUE_DATE': datetime.datetime.today(), 'HOLDING_ID': 1, 'ACCOUNT_ID': 1,
                     'ACCOUNT_NAME': 'Acct 1', 'ASSET_ID': 1, 'ASSET_NAME': 'Ass 1',
                     'HOLDING_DATE': datetime.datetime.today(), 'NUM_SHARES': 100.5, 'PRICE_ID': 1,
                     'PRICE_DATE': datetime.datetime.now(), 'PRICE': 2, 'VALUE': 201}]
        val_dict = portfolio.balancer.calc_acct_values(holdings)
        self.assertEqual(len(val_dict), 1)
        self.assertTrue(1 in val_dict)
        self.assertEqual(val_dict[1]['name'], 'Acct 1')
        self.assertEqual(val_dict[1]['value'], 201)
        self.assertEqual(val_dict[1]['holdings'][1]['asset_name'], 'Ass 1')
        self.assertEqual(val_dict[1]['holdings'][1]['curr_price'], 2)
        self.assertEqual(val_dict[1]['holdings'][1]['curr_value'], 201)
        self.assertEqual(val_dict[1]['holdings'][1]['curr_shares'], 100.5)

    def test_one_acct_mult_holding(self):
        holdings = [{'VALUE_DATE': datetime.datetime.today(), 'HOLDING_ID': 1, 'ACCOUNT_ID': 1,
                     'ACCOUNT_NAME': 'Acct 1', 'ASSET_ID': 1, 'ASSET_NAME': 'Ass 1',
                     'HOLDING_DATE': datetime.datetime.today(), 'NUM_SHARES': 100.5, 'PRICE_ID': 1,
                     'PRICE_DATE': datetime.datetime.now(), 'PRICE': 2, 'VALUE': 201.55},
                    {'VALUE_DATE': datetime.datetime.today(), 'HOLDING_ID': 2, 'ACCOUNT_ID': 1,
                     'ACCOUNT_NAME': 'Acct 1', 'ASSET_ID': 2, 'ASSET_NAME': 'Ass 2',
                     'HOLDING_DATE': datetime.datetime.today(), 'NUM_SHARES': 10000, 'PRICE_ID': 2,
                     'PRICE_DATE': datetime.datetime.now(), 'PRICE': 200000, 'VALUE': 1}
                    ]
        val_dict = portfolio.balancer.calc_acct_values(holdings)
        self.assertEqual(len(val_dict), 1)
        self.assertEqual(val_dict[1]['name'], 'Acct 1')
        self.assertEqual(val_dict[1]['value'], 202.55)
        self.assertEqual(val_dict[1]['holdings'][1]['asset_name'], 'Ass 1')
        self.assertEqual(val_dict[1]['holdings'][1]['curr_price'], 2)
        self.assertEqual(val_dict[1]['holdings'][1]['curr_value'], 201.55)
        self.assertEqual(val_dict[1]['holdings'][1]['curr_shares'], 100.5)
        self.assertEqual(val_dict[1]['holdings'][2]['asset_name'], 'Ass 2')
        self.assertEqual(val_dict[1]['holdings'][2]['curr_price'], 200000)
        self.assertEqual(val_dict[1]['holdings'][2]['curr_value'], 1)
        self.assertEqual(val_dict[1]['holdings'][2]['curr_shares'], 10000)



    def test_mult_acct(self):
        # Make sure that one acct has one holding and the other has mult holdings
        holdings = [{'VALUE_DATE': datetime.datetime.today(), 'HOLDING_ID': 1, 'ACCOUNT_ID': 1,
                     'ACCOUNT_NAME': 'Acct 1', 'ASSET_ID': 1, 'ASSET_NAME': 'Ass 1',
                     'HOLDING_DATE': datetime.datetime.today(), 'NUM_SHARES': 100.5, 'PRICE_ID': 1,
                     'PRICE_DATE': datetime.datetime.now(), 'PRICE': 2, 'VALUE': 201.55},
                    {'VALUE_DATE': datetime.datetime.today(), 'HOLDING_ID': 2, 'ACCOUNT_ID': 1,
                     'ACCOUNT_NAME': 'Acct 1', 'ASSET_ID': 2, 'ASSET_NAME': 'Ass 2',
                     'HOLDING_DATE': datetime.datetime.today(), 'NUM_SHARES': 10000, 'PRICE_ID': 2,
                     'PRICE_DATE': datetime.datetime.now(), 'PRICE': 200000, 'VALUE': 1},
                    {'VALUE_DATE': datetime.datetime.today(), 'HOLDING_ID': 3, 'ACCOUNT_ID': 2,
                     'ACCOUNT_NAME': 'Acct 2', 'ASSET_ID': 1, 'ASSET_NAME': 'Ass 1',
                     'HOLDING_DATE': datetime.datetime.today(), 'NUM_SHARES': 10000, 'PRICE_ID': 1,
                     'PRICE_DATE': datetime.datetime.now(), 'PRICE': 200000, 'VALUE': 1}]
        val_dict = portfolio.balancer.calc_acct_values(holdings)
        self.assertEqual(len(val_dict), 2)
        self.assertEqual(val_dict[1]['name'], 'Acct 1')
        self.assertEqual(val_dict[1]['value'], 202.55)
        self.assertEqual(val_dict[1]['holdings'][1]['asset_name'], 'Ass 1')
        self.assertEqual(val_dict[1]['holdings'][1]['curr_price'], 2)
        self.assertEqual(val_dict[1]['holdings'][1]['curr_value'], 201.55)
        self.assertEqual(val_dict[1]['holdings'][1]['curr_shares'], 100.5)
        self.assertEqual(val_dict[1]['holdings'][2]['asset_name'], 'Ass 2')
        self.assertEqual(val_dict[1]['holdings'][2]['curr_price'], 200000)
        self.assertEqual(val_dict[1]['holdings'][2]['curr_value'], 1)
        self.assertEqual(val_dict[1]['holdings'][2]['curr_shares'], 10000)
        self.assertEqual(val_dict[2]['name'], 'Acct 2')
        self.assertEqual(val_dict[2]['value'], 1)
        self.assertEqual(val_dict[2]['holdings'][1]['asset_name'], 'Ass 1')
        self.assertEqual(val_dict[2]['holdings'][1]['curr_price'], 200000)
        self.assertEqual(val_dict[2]['holdings'][1]['curr_value'], 1)
        self.assertEqual(val_dict[2]['holdings'][1]['curr_shares'], 10000)
