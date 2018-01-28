# test_balancer.py

import datetime
from operator import itemgetter

from django.test import TestCase

import balancer.models
import portfolio.balancer


class TestBalancePortfolio(TestCase):
    def test_no_holdings(self):
        required_changes = portfolio.balancer.balance_portfolio(curr_holdings_and_values=[], balance_pcts=[])
        self.assertEqual(len(required_changes), 0)

    def test_one_acct(self):
        holdings = [{'VALUE_DATE': datetime.datetime.today(), 'HOLDING_ID': 1, 'ACCOUNT_ID': 1,
                     'ACCOUNT_NAME': 'Acct 1', 'ASSET_ID': 1, 'ASSET_NAME': 'Ass 1 - Bond',
                     'HOLDING_DATE': datetime.datetime.today(), 'NUM_SHARES': 2, 'PRICE_ID': 1,
                     'PRICE_DATE': datetime.datetime.now(), 'PRICE': 50, 'VALUE': 100},
                    {'VALUE_DATE': datetime.datetime.today(), 'HOLDING_ID': 2, 'ACCOUNT_ID': 1,
                     'ACCOUNT_NAME': 'Acct 1', 'ASSET_ID': 2, 'ASSET_NAME': 'Ass 2- Stock',
                     'HOLDING_DATE': datetime.datetime.today(), 'NUM_SHARES': 1, 'PRICE_ID': 2,
                     'PRICE_DATE': datetime.datetime.now(), 'PRICE': 100, 'VALUE': 100}]
        new_balance = [balancer.models.TargetBalance(category='bonds', notes='bond notes', percent=90, security_id=1),
                       balancer.models.TargetBalance(category='stocks', notes='stock notes', percent=10, security_id=2)]

        required_changes = \
            portfolio.balancer.balance_portfolio(curr_holdings_and_values=holdings, balance_pcts=new_balance)

        self.assertEqual(len(required_changes), 1)
        self.assertEqual(required_changes[1]['name'], 'Acct 1')
        self.assertEqual(required_changes[1]['value'], 200)
        self.assertEqual(len(required_changes[1]['holdings']), 2)
        # SORT THE HOLDINGS SO THEY ARE IN THE RIGHT ORDER
        required_changes[1]['holdings'] = sorted(required_changes[1]['holdings'], key=itemgetter('asset_id'))
        self.assertEqual(required_changes[1]['holdings'][0]['asset_id'], 1)
        self.assertEqual(required_changes[1]['holdings'][0]['asset_name'], 'Ass 1 - Bond')
        self.assertEqual(required_changes[1]['holdings'][0]['curr_price'], 50)
        self.assertEqual(required_changes[1]['holdings'][0]['curr_value'], 100)
        self.assertEqual(required_changes[1]['holdings'][0]['curr_shares'], 2)
        self.assertEqual(required_changes[1]['holdings'][0]['tgt_value'], 180)
        self.assertEqual(required_changes[1]['holdings'][0]['tgt_shares'], 3.6)
        self.assertEqual(required_changes[1]['holdings'][0]['value_change'], 80)
        self.assertEqual(required_changes[1]['holdings'][0]['share_change'], 1.6)
        self.assertEqual(required_changes[1]['holdings'][1]['asset_id'], 2)
        self.assertEqual(required_changes[1]['holdings'][1]['asset_name'], 'Ass 2- Stock')
        self.assertEqual(required_changes[1]['holdings'][1]['curr_price'], 100)
        self.assertEqual(required_changes[1]['holdings'][1]['curr_value'], 100)
        self.assertEqual(required_changes[1]['holdings'][1]['curr_shares'], 1)
        self.assertEqual(required_changes[1]['holdings'][1]['tgt_value'], 20)
        self.assertEqual(required_changes[1]['holdings'][1]['tgt_shares'], 0.2)
        self.assertEqual(required_changes[1]['holdings'][1]['value_change'], -80)
        self.assertEqual(required_changes[1]['holdings'][1]['share_change'], -0.8)

    def test_mult_accts(self):
        self.assertTrue(False)

    def test_some_holdings_go_to_zero(self):
        holdings = [{'VALUE_DATE': datetime.datetime.today(), 'HOLDING_ID': 1, 'ACCOUNT_ID': 1,
                     'ACCOUNT_NAME': 'Acct 1', 'ASSET_ID': 1, 'ASSET_NAME': 'Ass 1 - Bond',
                     'HOLDING_DATE': datetime.datetime.today(), 'NUM_SHARES': 2, 'PRICE_ID': 1,
                     'PRICE_DATE': datetime.datetime.now(), 'PRICE': 50, 'VALUE': 100},
                    {'VALUE_DATE': datetime.datetime.today(), 'HOLDING_ID': 2, 'ACCOUNT_ID': 1,
                     'ACCOUNT_NAME': 'Acct 1', 'ASSET_ID': 2, 'ASSET_NAME': 'Ass 2- Stock',
                     'HOLDING_DATE': datetime.datetime.today(), 'NUM_SHARES': 1, 'PRICE_ID': 2,
                     'PRICE_DATE': datetime.datetime.now(), 'PRICE': 100, 'VALUE': 100}]
        new_balance = [balancer.models.TargetBalance(category='stocks',
                                                     notes='stock notes', percent=100, security_id=2)]

        required_changes = \
            portfolio.balancer.balance_portfolio(curr_holdings_and_values=holdings, balance_pcts=new_balance)

        self.assertEqual(len(required_changes), 1)  # There's only one account
        self.assertEqual(required_changes[1]['name'], 'Acct 1')
        self.assertEqual(required_changes[1]['value'], 200)
        self.assertEqual(len(required_changes[1]['holdings']), 2)
        # SORT THE HOLDINGS SO THEY ARE IN THE RIGHT ORDER
        required_changes[1]['holdings'] = sorted(required_changes[1]['holdings'], key=itemgetter('asset_id'))
        self.assertEqual(required_changes[1]['holdings'][0]['asset_id'], 1)
        self.assertEqual(required_changes[1]['holdings'][0]['asset_name'], 'Ass 1 - Bond')
        self.assertEqual(required_changes[1]['holdings'][0]['curr_price'], 50)
        self.assertEqual(required_changes[1]['holdings'][0]['curr_value'], 100)
        self.assertEqual(required_changes[1]['holdings'][0]['curr_shares'], 2)
        self.assertEqual(required_changes[1]['holdings'][0]['tgt_value'], 0)
        self.assertEqual(required_changes[1]['holdings'][0]['tgt_shares'], 0)
        self.assertEqual(required_changes[1]['holdings'][0]['value_change'], -100)
        self.assertEqual(required_changes[1]['holdings'][0]['share_change'], -2)
        self.assertEqual(required_changes[1]['holdings'][1]['asset_id'], 2)
        self.assertEqual(required_changes[1]['holdings'][1]['asset_name'], 'Ass 2- Stock')
        self.assertEqual(required_changes[1]['holdings'][1]['curr_price'], 100)
        self.assertEqual(required_changes[1]['holdings'][1]['curr_value'], 100)
        self.assertEqual(required_changes[1]['holdings'][1]['curr_shares'], 1)
        self.assertEqual(required_changes[1]['holdings'][1]['tgt_value'], 200)
        self.assertEqual(required_changes[1]['holdings'][1]['tgt_shares'], 2)
        self.assertEqual(required_changes[1]['holdings'][1]['value_change'], 100)
        self.assertEqual(required_changes[1]['holdings'][1]['share_change'], 1)

    def test_balance_adds_some_new_holdings(self):
        self.assertTrue(False)

    def test_bal_pcts_under_100(self):
        # DO WE NEED TO TEST THIS OR WILL THIS NEVER HAPPEN?
        self.assertTrue(False)

    def test_bal_pcts_over_100(self):
        # DO WE NEED TO TEST THIS OR WILL THIS NEVER HAPPEN?
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
        self.assertEqual(val_dict[1]['holdings'][0]['asset_id'], 1)
        self.assertEqual(val_dict[1]['holdings'][0]['asset_name'], 'Ass 1')
        self.assertEqual(val_dict[1]['holdings'][0]['curr_price'], 2)
        self.assertEqual(val_dict[1]['holdings'][0]['curr_value'], 201)
        self.assertEqual(val_dict[1]['holdings'][0]['curr_shares'], 100.5)

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
        self.assertEqual(val_dict[1]['holdings'][0]['asset_id'], 1)
        self.assertEqual(val_dict[1]['holdings'][0]['asset_name'], 'Ass 1')
        self.assertEqual(val_dict[1]['holdings'][0]['curr_price'], 2)
        self.assertEqual(val_dict[1]['holdings'][0]['curr_value'], 201.55)
        self.assertEqual(val_dict[1]['holdings'][0]['curr_shares'], 100.5)
        self.assertEqual(val_dict[1]['holdings'][1]['asset_id'], 2)
        self.assertEqual(val_dict[1]['holdings'][1]['asset_name'], 'Ass 2')
        self.assertEqual(val_dict[1]['holdings'][1]['curr_price'], 200000)
        self.assertEqual(val_dict[1]['holdings'][1]['curr_value'], 1)
        self.assertEqual(val_dict[1]['holdings'][1]['curr_shares'], 10000)

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
        self.assertEqual(val_dict[1]['holdings'][0]['asset_id'], 1)
        self.assertEqual(val_dict[1]['holdings'][0]['asset_name'], 'Ass 1')
        self.assertEqual(val_dict[1]['holdings'][0]['curr_price'], 2)
        self.assertEqual(val_dict[1]['holdings'][0]['curr_value'], 201.55)
        self.assertEqual(val_dict[1]['holdings'][0]['curr_shares'], 100.5)
        self.assertEqual(val_dict[1]['holdings'][1]['asset_id'], 2)
        self.assertEqual(val_dict[1]['holdings'][1]['asset_name'], 'Ass 2')
        self.assertEqual(val_dict[1]['holdings'][1]['curr_price'], 200000)
        self.assertEqual(val_dict[1]['holdings'][1]['curr_value'], 1)
        self.assertEqual(val_dict[1]['holdings'][1]['curr_shares'], 10000)
        self.assertEqual(val_dict[2]['name'], 'Acct 2')
        self.assertEqual(val_dict[2]['value'], 1)
        self.assertEqual(val_dict[2]['holdings'][0]['asset_id'], 1)
        self.assertEqual(val_dict[2]['holdings'][0]['asset_name'], 'Ass 1')
        self.assertEqual(val_dict[2]['holdings'][0]['curr_price'], 200000)
        self.assertEqual(val_dict[2]['holdings'][0]['curr_value'], 1)
        self.assertEqual(val_dict[2]['holdings'][0]['curr_shares'], 10000)
