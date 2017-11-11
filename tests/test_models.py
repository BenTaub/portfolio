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
        result_recs = balancer.models.get_holdings_and_values(test_holdings[0]['as_of_dt'])
        pass


# def test_no_records_in_future
# def test_some_records_in_future
# def test_all_records_in_future
# def test_mult_price_dates(self):
# def test_0_holdings(self):
#     # BEN - make sure there are security and account records
# def test_1_holding(self):
# def test_mult_holdings(self):
# def test_mult_holdings_mult_holding_dates(self):
# def test_1_holding_no_security_recs(self):
# def test_1_holding_no_acct_recs(self):


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
