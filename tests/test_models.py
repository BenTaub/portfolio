# test_models.py
import datetime

from django.db import connection
from django.test import TestCase

import balancer.models


class Dictfetchall(TestCase):

    def create_test_recs(self, num_recs: int = 1):
        """
        Sets up the tests. Uses Security table / model for the test
        :param num_recs: The number of test records to create
        :return: list of dicts were each dict is a new rec
        """
        rec_list = []
        for rec in range(num_recs):
            test_vals = {
                'id': rec,
                'name': 'name ' + str(rec),
                'symbol': 'symbol ' + str(rec),
                'notes': 'notes ' + str(rec)
            }
            new_rec = balancer.models.Security(**test_vals)
            new_rec.save()
            test_vals['effective_dt'] = new_rec.effective_dt.replace(tzinfo=None)
            rec_list.append(test_vals)
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM balancer_security')
        return rec_list, cursor

    def test_no_recs(self):
        test_recs, cursor = self.create_test_recs(num_recs=0)
        self.assertListEqual(test_recs, balancer.models.dictfetchall(cursor=cursor))

    def test_1_rec(self):
        test_recs, cursor = self.create_test_recs(num_recs=1)
        self.assertListEqual(test_recs, balancer.models.dictfetchall(cursor=cursor))

    def test_mult_recs(self):
        test_recs, cursor = self.create_test_recs(num_recs=3)
        self.assertListEqual(test_recs, balancer.models.dictfetchall(cursor=cursor))


class GetHoldingsAndValues(TestCase):
    """Tests the SQL that returns holdings & their values.
    NOTE: MAKE SURE TO TEST ALL THE TABLES THAT GO INTO THIS: Security, SecurityPrice, Holdings, Accounts"""

    def test_one_acct_one_holding(self):
        """Basic test case - also tests no records in the future"""
        test_dt = datetime.date.today()
        test_securities = create_test_recs_security(dates=[test_dt])
        test_accounts = create_test_recs_acct(dates=[test_dt])
        test_prices = [{'security': test_securities[0], 'price_dt': test_dt,
                        'price': 1, 'notes': 'Price Notes 1'}]
        test_prices = create_test_recs_prices(price_list=test_prices)
        test_holdings = [{'asset': test_securities[0], 'account': test_accounts[0],
                          'notes': 'Holdings Notes 1',
                          'num_shares': 1, 'as_of_dt': test_dt}]
        test_holdings = create_test_recs_holdings(test_holdings)
        result_recs = balancer.models.get_holdings_and_values(test_dt)

        self.assertEqual(len(result_recs), 1)  # Make sure we got the right # of records back
        self.assertIn(test_dt, result_recs)  # Make sure the dates we sent are in results
        self.assertEqual(test_accounts[0].id, result_recs[test_dt][0]['ACCOUNT_ID'])  # Test acct id
        self.assertEqual(test_accounts[0].name, result_recs[test_dt][0]['ACCOUNT_NAME'])  # Test acct name
        self.assertEqual(test_securities[0].id, result_recs[test_dt][0]['ASSET_ID'])  # Test security ID
        self.assertEqual(test_securities[0].name, result_recs[test_dt][0]['ASSET_NAME'])  # Test security name
        self.assertEqual(test_holdings[0].id, result_recs[test_dt][0]['HOLDING_ID'])  # Test holding ID
        self.assertEqual(test_holdings[0].as_of_dt, result_recs[test_dt][0]['HOLDING_DATE'])  # Test holding date
        self.assertEqual(test_holdings[0].num_shares, result_recs[test_dt][0]['NUM_SHARES'])  # Test # shares
        self.assertEqual(test_prices[0].id, result_recs[test_dt][0]['PRICE_ID'])  # Test price rec ID
        self.assertEqual(test_prices[0].price_dt, result_recs[test_dt][0]['PRICE_DATE'])  # Test price rec date
        self.assertEqual(test_prices[0].price, result_recs[test_dt][0]['PRICE'])  # Test price rec price
        self.assertEqual(test_prices[0].price * test_holdings[0].num_shares,
                         result_recs[test_dt][0]['VALUE'])  # Test value

    def test_one_acct_two_holdings(self):
        """Also tests more price recs than what are requested"""
        test_dt = datetime.date.today()
        yesterday = test_dt - datetime.timedelta(days=1)
        # test_securities = create_test_recs_security(dates=[test_dt])
        test_securities = create_test_recs_security(dates=[test_dt, yesterday])
        test_accounts = create_test_recs_acct(dates=[test_dt])
        test_prices = [{'security': test_securities[0], 'price_dt': test_dt,
                        'price': 1, 'notes': 'Price Notes 1'},
                       {'security': test_securities[1], 'price_dt': test_dt,
                        'price': 2, 'notes': 'Price Notes 2'},
                       {'security': test_securities[0], 'price_dt': yesterday,
                        'price': 3, 'notes': 'Price Notes 3'},
                       {'security': test_securities[1], 'price_dt': yesterday,
                        'price': 4, 'notes': 'Price Notes 4'}
                       ]
        test_prices = create_test_recs_prices(price_list=test_prices)
        test_holdings = [{'asset': test_securities[0], 'account': test_accounts[0],
                          'notes': 'Holdings Notes 1',
                          'num_shares': 1, 'as_of_dt': yesterday},
                         {'asset': test_securities[1], 'account': test_accounts[0],
                          'notes': 'Holdings Notes 2',
                          'num_shares': 2, 'as_of_dt': yesterday}
                         ]
        test_holdings = create_test_recs_holdings(test_holdings)
        result_recs = balancer.models.get_holdings_and_values(test_dt)

        self.assertEqual(len(result_recs[test_dt]), 2)  # Make sure we got the right # of records back
        self.assertIn(test_dt, result_recs)  # Make sure the dates we sent are in results
        self.assertEqual(test_accounts[0].id, result_recs[test_dt][0]['ACCOUNT_ID'])  # Test acct id
        self.assertEqual(test_accounts[0].id, result_recs[test_dt][1]['ACCOUNT_ID'])  # Test acct id
        self.assertEqual(test_accounts[0].name, result_recs[test_dt][0]['ACCOUNT_NAME'])  # Test acct name
        self.assertEqual(test_accounts[0].name, result_recs[test_dt][1]['ACCOUNT_NAME'])  # Test acct name
        self.assertEqual(test_securities[0].id, result_recs[test_dt][0]['ASSET_ID'])  # Test security ID
        self.assertEqual(test_securities[1].id, result_recs[test_dt][1]['ASSET_ID'])  # Test security ID
        self.assertEqual(test_securities[0].name, result_recs[test_dt][0]['ASSET_NAME'])  # Test security name
        self.assertEqual(test_securities[1].name, result_recs[test_dt][1]['ASSET_NAME'])  # Test security name
        self.assertEqual(test_holdings[0].id, result_recs[test_dt][0]['HOLDING_ID'])  # Test holding ID
        self.assertEqual(test_holdings[1].id, result_recs[test_dt][1]['HOLDING_ID'])  # Test holding ID
        self.assertEqual(test_holdings[0].as_of_dt, result_recs[test_dt][0]['HOLDING_DATE'])  # Test holding date
        self.assertEqual(test_holdings[1].as_of_dt, result_recs[test_dt][1]['HOLDING_DATE'])  # Test holding date
        self.assertEqual(test_holdings[0].num_shares, result_recs[test_dt][0]['NUM_SHARES'])  # Test # shares
        self.assertEqual(test_holdings[1].num_shares, result_recs[test_dt][1]['NUM_SHARES'])  # Test # shares
        self.assertEqual(test_prices[0].id, result_recs[test_dt][0]['PRICE_ID'])  # Test price rec ID
        self.assertEqual(test_prices[1].id, result_recs[test_dt][1]['PRICE_ID'])  # Test price rec ID
        self.assertEqual(test_prices[0].price_dt, result_recs[test_dt][0]['PRICE_DATE'])  # Test price rec date
        self.assertEqual(test_prices[1].price_dt, result_recs[test_dt][1]['PRICE_DATE'])  # Test price rec date
        self.assertEqual(test_prices[0].price, result_recs[test_dt][0]['PRICE'])  # Test price rec price
        self.assertEqual(test_prices[1].price, result_recs[test_dt][1]['PRICE'])  # Test price rec price
        self.assertEqual(test_prices[0].price * test_holdings[0].num_shares,
                         result_recs[test_dt][0]['VALUE'])  # Test value
        self.assertEqual(test_prices[1].price * test_holdings[1].num_shares,
                         result_recs[test_dt][1]['VALUE'])  # Test value

    def test_0_holdings(self):
        test_dt = datetime.date.today()
        result_recs = balancer.models.get_holdings_and_values(test_dt)
        self.assertEqual(len(result_recs[test_dt]), 0)  # Make sure we got the right # of records back

    def test_prices_non_requested_dates(self):  # these shouldn't come back
        """Tests w/ recs before test date, on test date, and after test date -
           should only get data back for test date"""
        test_dt = datetime.date.today()
        yesterday = test_dt - datetime.timedelta(days=1)
        tomorrow = test_dt + datetime.timedelta(days=1)
        test_securities = create_test_recs_security(dates=[test_dt])
        test_accounts = create_test_recs_acct(dates=[test_dt])
        test_prices = [{'security': test_securities[0], 'price_dt': yesterday,
                        'price': 0, 'notes': 'Price Notes yesterday'},
                       {'security': test_securities[0], 'price_dt': test_dt,
                        'price': 1, 'notes': 'Price Notes today'},
                       {'security': test_securities[0], 'price_dt': tomorrow,
                        'price': 2, 'notes': 'Price Notes tomorrow'}]
        test_prices = create_test_recs_prices(price_list=test_prices)
        test_holdings = [{'asset': test_securities[0], 'account': test_accounts[0],
                          'notes': 'Holdings Notes 1',
                          'num_shares': 1, 'as_of_dt': yesterday}]
        test_holdings = create_test_recs_holdings(test_holdings)
        result_recs = balancer.models.get_holdings_and_values(test_dt)
        self.assertEqual(len(result_recs[test_dt]), 1)  # Make sure we got the right # of records back
        self.assertIn(test_dt, result_recs)  # Make sure the dates we sent are in results
        self.assertEqual(test_accounts[0].id, result_recs[test_dt][0]['ACCOUNT_ID'])  # Test acct id
        self.assertEqual(test_accounts[0].name, result_recs[test_dt][0]['ACCOUNT_NAME'])  # Test acct name
        self.assertEqual(test_securities[0].id, result_recs[test_dt][0]['ASSET_ID'])  # Test security ID
        self.assertEqual(test_securities[0].name, result_recs[test_dt][0]['ASSET_NAME'])  # Test security name
        self.assertEqual(test_holdings[0].id, result_recs[test_dt][0]['HOLDING_ID'])  # Test holding ID
        self.assertEqual(test_holdings[0].as_of_dt, result_recs[test_dt][0]['HOLDING_DATE'])  # Test holding date
        self.assertEqual(test_holdings[0].num_shares, result_recs[test_dt][0]['NUM_SHARES'])  # Test # shares
        self.assertEqual(test_prices[1].id, result_recs[test_dt][0]['PRICE_ID'])  # Test price rec ID
        self.assertEqual(test_prices[1].price_dt, result_recs[test_dt][0]['PRICE_DATE'])  # Test price rec date
        self.assertEqual(test_prices[1].price, result_recs[test_dt][0]['PRICE'])  # Test price rec price
        self.assertEqual(test_prices[1].price * test_holdings[0].num_shares,
                         result_recs[test_dt][0]['VALUE'])  # Test value

    def test_all_holdings_in_future(self):
        """Tests w/ price recs after test date - should get nothing back"""
        test_dt = datetime.date.today()
        tomorrow = test_dt + datetime.timedelta(days=1)
        test_securities = create_test_recs_security(dates=[test_dt])
        test_accounts = create_test_recs_acct(dates=[test_dt])
        test_prices = [{'security': test_securities[0], 'price_dt': test_dt,
                        'price': 2, 'notes': 'Price Notes today'}]
        create_test_recs_prices(price_list=test_prices)
        test_holdings = [{'asset': test_securities[0], 'account': test_accounts[0],
                          'notes': 'Holdings Notes 1',
                          'num_shares': 1, 'as_of_dt': tomorrow}]  # Holding starts tomorrow
        create_test_recs_holdings(test_holdings)
        result_recs = balancer.models.get_holdings_and_values(test_dt)
        self.assertEqual(len(result_recs[test_dt]), 0)  # Make sure we got the right # of records back
        self.assertIn(test_dt, result_recs)  # Make sure the dates we sent are in results

    def test_mult_price_dates(self):
        """Store four price dates for one holding but request only two back"""
        today = datetime.date.today()
        yesterday = today - datetime.timedelta(days=1)
        purch_dt = today - datetime.timedelta(days=2)
        tomorrow = today + datetime.timedelta(days=1)
        # test_securities = create_test_recs_security(dates=[today])
        test_securities = create_test_recs_security(dates=[today])
        test_accounts = create_test_recs_acct(dates=[today])
        test_prices = [{'security': test_securities[0], 'price_dt': purch_dt,
                        'price': 1, 'notes': 'Price Notes purch dt'},
                       {'security': test_securities[0], 'price_dt': yesterday,
                        'price': 2, 'notes': 'Price Notes yesterday'},
                       {'security': test_securities[0], 'price_dt': today,
                        'price': 3, 'notes': 'Price Notes today'},
                       {'security': test_securities[0], 'price_dt': tomorrow,
                        'price': 4, 'notes': 'Price Notes tomorrow'}]
        test_prices = create_test_recs_prices(price_list=test_prices)
        test_holdings = [{'asset': test_securities[0], 'account': test_accounts[0],
                          'notes': 'Holdings Notes 1',
                          'num_shares': 1, 'as_of_dt': yesterday}]
        test_holdings = create_test_recs_holdings(test_holdings)
        result_recs = balancer.models.get_holdings_and_values([yesterday, today])

        self.assertEqual(len(result_recs), 2)  # Make sure we got the right # of records back
        self.assertEqual(len(result_recs[yesterday]), 1)  # Make sure we got the right # of records back
        self.assertEqual(len(result_recs[today]), 1)  # Make sure we got the right # of records back
        self.assertIn(yesterday, result_recs)  # Make sure the dates we sent are in results
        self.assertIn(today, result_recs)  # Make sure the dates we sent are in results
        self.assertEqual(test_accounts[0].id, result_recs[yesterday][0]['ACCOUNT_ID'])  # Test acct id
        self.assertEqual(test_accounts[0].id, result_recs[today][0]['ACCOUNT_ID'])  # Test acct id
        self.assertEqual(test_accounts[0].name, result_recs[yesterday][0]['ACCOUNT_NAME'])  # Test acct name
        self.assertEqual(test_accounts[0].name, result_recs[today][0]['ACCOUNT_NAME'])  # Test acct name
        self.assertEqual(test_securities[0].id, result_recs[yesterday][0]['ASSET_ID'])  # Test security ID
        self.assertEqual(test_securities[0].id, result_recs[today][0]['ASSET_ID'])  # Test security ID
        self.assertEqual(test_securities[0].name, result_recs[yesterday][0]['ASSET_NAME'])  # Test security name
        self.assertEqual(test_securities[0].name, result_recs[today][0]['ASSET_NAME'])  # Test security name
        self.assertEqual(test_holdings[0].id, result_recs[yesterday][0]['HOLDING_ID'])  # Test holding ID
        self.assertEqual(test_holdings[0].id, result_recs[today][0]['HOLDING_ID'])  # Test holding ID
        self.assertEqual(test_holdings[0].as_of_dt, result_recs[yesterday][0]['HOLDING_DATE'])  # Test holding date
        self.assertEqual(test_holdings[0].as_of_dt, result_recs[today][0]['HOLDING_DATE'])  # Test holding date
        self.assertEqual(test_holdings[0].num_shares, result_recs[yesterday][0]['NUM_SHARES'])  # Test # shares
        self.assertEqual(test_holdings[0].num_shares, result_recs[today][0]['NUM_SHARES'])  # Test # shares
        self.assertEqual(test_prices[1].id, result_recs[yesterday][0]['PRICE_ID'])  # Test price rec ID
        self.assertEqual(test_prices[2].id, result_recs[today][0]['PRICE_ID'])  # Test price rec ID
        self.assertEqual(test_prices[1].price_dt, result_recs[yesterday][0]['PRICE_DATE'])  # Test price rec date
        self.assertEqual(test_prices[2].price_dt, result_recs[today][0]['PRICE_DATE'])  # Test price rec date
        self.assertEqual(test_prices[1].price, result_recs[yesterday][0]['PRICE'])  # Test price rec price
        self.assertEqual(test_prices[2].price, result_recs[today][0]['PRICE'])  # Test price rec price
        self.assertEqual(test_prices[1].price * test_holdings[0].num_shares,
                         result_recs[yesterday][0]['VALUE'])  # Test value
        self.assertEqual(test_prices[2].price * test_holdings[0].num_shares,
                         result_recs[today][0]['VALUE'])  # Test value


def create_test_recs_prices(price_list: list) -> list:
    """A common routine for creating test price records. Returns a list of dicts containing the data that
    went into those records to use in comparing results to data in the sample records

    price_list: a list of dicts where each dict contains the fields required to create a price record
    :rtype: list
    """
    ret_recs = []
    for rec in price_list:
        rec = balancer.models.SecurityPrice(**rec)
        rec.save()
        ret_recs.append(rec)
        del rec
    return ret_recs


def create_test_recs_holdings(holding_list: list):
    """A common routine for creating test holding records. Returns a list of dicts containing the data that
    went into those records to use in comparing results to data in the sample records
    holding_list: a list of dicts where each dict contains the fields required to create a holding record
    """
    ret_recs = []
    for rec in holding_list:
        rec = balancer.models.Holding(**rec)
        rec.save()
        ret_recs.append(rec)
        del rec
    return ret_recs


def create_test_recs_acct(dates: list):
    """
    A common routine for creating test account records. Returns a list of dicts containing the data that
    went into those records to use in comparing results to data in the sample records
    :param dates: List of dates for which accounts s/b created
    :return: List of account records for the recs created
    """
    ret_recs = []
    for rec_dt in dates:
        kwargs = {'name': 'Account Name ' + str(rec_dt), 'institution': 'Institution ' + str(rec_dt),
                  'acct_num': 'Acct Num ' + str(rec_dt), 'notes': 'Account Notes ' + str(rec_dt),
                  'open_dt': rec_dt,
                  'close_dt': None}
        rec = balancer.models.Account(**kwargs)
        rec.save()
        ret_recs.append(rec)
        del rec
    return ret_recs


def create_test_recs_security(dates: list):
    """A common routine for creating test security records. Returns a list of dicts containing the data that
    went into those records to use in comparing results to data in the sample records
    :param dates: List of dates for which securities s/b created
    :return: List of security records for the recs created
    """
    ret_recs = []
    for rec_date in dates:
        kwargs = {'name': 'Security Name ' + str(rec_date), 'symbol': 'SYM' + str(rec_date),
                  'notes': 'Security notes ' + str(rec_date)}
        rec = balancer.models.Security(**kwargs)
        rec.save()
        ret_recs.append(rec)
        del rec
    return ret_recs


# if __name__ == '__main__':
#     unittest.main()
#     # unittest.main()
