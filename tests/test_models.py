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

    # def compare_results(self, securities: list, accounts: list, prices: list, holdings: list, results: list):
    #     """Compares results from the db to the data captured when the underlying records were created
    #     :param securities: A list of Security records containing test data
    #     :param accounts: A list of Account records containing test data
    #     :param prices: A list of SecurityPrice records containing test data
    #     :param holdings: A list of Holdings records containing test data
    #     :param results: A list of dicts containing the results of the query that got the holdings & values
    #     :return:
    #     """



    def test_one_date(self):
        test_securities = create_test_recs_security(num_recs=1)
        test_accounts = create_test_recs_acct(num_recs=1)
        test_prices = [{'security': test_securities[0], 'price_dt': datetime.date.today(),
                        'price': 1, 'notes': 'Price Notes 1'}]
        test_prices = create_test_recs_prices(price_list=test_prices)
        test_holdings = [{'asset': test_securities[0], 'account': test_accounts[0],
                          'notes': 'Holdings Notes 1',
                          'num_shares': 1, 'as_of_dt': datetime.datetime.now()}]
        test_holdings = create_test_recs_holdings(test_holdings)
        test_dt = test_holdings[0].as_of_dt.date()
        result_recs = balancer.models.get_holdings_and_values(test_dt)

        self.assertEqual(len(test_holdings), 1)  # Make sure we got the right # of records back
        self.assertIn(test_dt, result_recs)  # Make sure the dates we sent are in results
        self.assertEqual(test_accounts[0].id, result_recs[test_dt][0]['ACCOUNT_ID'])  # Test acct id
        self.assertEqual(test_accounts[0].name, result_recs[test_dt][0]['ACCOUNT_NAME'])  # Test acct name
        self.assertEqual(test_securities[0].id, result_recs[test_dt][0]['ASSET_ID'])  # Test security ID
        self.assertEqual(test_securities[0].name, result_recs[test_dt][0]['ASSET_NAME'])  # Test security name
        self.assertEqual(test_holdings[0].id, result_recs[test_dt][0]['HOLDING_ID'])  # Test holding ID
        self.assertEqual(test_holdings[0].as_of_dt.date(), result_recs[test_dt][0]['HOLDING_DATE'])  # Test holding date
        self.assertEqual(test_holdings[0].num_shares, result_recs[test_dt][0]['NUM_SHARES'])  # Test # shares
        self.assertEqual(test_prices[0].id, result_recs[test_dt][0]['PRICE_ID'])  # Test price rec ID
        self.assertEqual(test_prices[0].price_dt, result_recs[test_dt][0]['PRICE_DATE'])  # Test price rec date
        self.assertEqual(test_prices[0].price, result_recs[test_dt][0]['PRICE'])  # Test price rec price
        self.assertEqual(test_prices[0].price * test_holdings[0].num_shares,
                         result_recs[test_dt][0]['VALUE'])  # Test value



# def test_no_records_in_future
# def test_some_records_in_future
# def test_all_records_in_future
# def test_mult_price_dates(self):  SOME SHOULD BE EARLIER THAN OUR EARLIEST DATE
# def test_0_holdings(self):
#     # BEN - make sure there are security and account records
# def test_1_holding(self):
# def test_mult_holdings(self):
# def test_mult_holdings_mult_holding_dates(self):
# def test_1_holding_no_security_recs(self):
# def test_1_holding_no_acct_recs(self):
# def test_1_holding_no_price_recs(self):
# def test_mult_accts


def create_test_recs_prices(price_list: list):
    """A common routine for creating test price records. Returns a list of dicts containing the data that
    went into those records to use in comparing results to data in the sample records
    price_list: a list of dicts where each dict contains the fields required to create a price record
    """
    ret_recs = []
    for rec in price_list:
        rec = balancer.models.SecurityPrice(**rec)
        rec.save()
        # this_rec = rec.__dict__
        # this_rec.pop('_state')  # state is a Django field that will just throw things off
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
        # this_rec = rec.__dict__
        # this_rec.pop('_state')  # state is a Django field that will just throw things off
        ret_recs.append(rec)
        del rec
    return ret_recs


# TODO: change to accept test_dt, num_past, num_today, num_future
def create_test_recs_acct(num_recs: int):
    """A common routine for creating test account records. Returns a list of dicts containing the data that
    went into those records to use in comparing results to data in the sample records"""
    ret_recs = []
    for rec_num in range(num_recs):
        month_num = rec_num + 1
        while month_num > 12:
            month_num -= 12
        day_num = rec_num + 1  # NOTE: Will fail if rec_num > num days in a month. But, not worth fixing
        kwargs = {'name': 'Account Name ' + str(rec_num), 'institution': 'Institution ' + str(rec_num),
                  'acct_num': 'Acct Num ' + str(rec_num), 'notes': 'Account Notes ' + str(rec_num),
                  'open_dt': datetime.date(year=2017, month=month_num, day=day_num),
                  'close_dt': datetime.date(year=2017 + rec_num, month=month_num, day=day_num)}
        rec = balancer.models.Account(**kwargs)
        rec.save()
        # this_rec = rec.__dict__
        # this_rec.pop('_state')  # state is a Django field that will just throw things off
        # ret_recs.append(this_rec)
        ret_recs.append(rec)
        del rec
    return ret_recs


def create_test_recs_security(num_recs: int):
    """A common routine for creating test security records. Returns a list of dicts containing the data that
    went into those records to use in comparing results to data in the sample records"""
    ret_recs = []
    for rec_num in range(num_recs):
        kwargs = {'name': 'Security Name ' + str(rec_num), 'symbol': 'SYM' + str(rec_num),
                  'notes': 'Security notes ' + str(rec_num)}
        rec = balancer.models.Security(**kwargs)
        rec.save()
        # this_rec = rec.__dict__
        # this_rec.pop('_state')  # state is a Django field that will just throw things off
        # ret_recs.append(this_rec)
        ret_recs.append(rec)
        del rec
    return ret_recs


# if __name__ == '__main__':
#     unittest.main()
#     # unittest.main()
