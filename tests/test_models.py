# test_models.py
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
    def create_test_recs_security(self, num_recs: int):
        while num_recs > 0:
            num_recs -= 1

            security_rec = balancer.models.Security()

    def test_send_one_date(self):

# def test_send_mult_dates(self):
# def test_0_holdings(self):
#     # BEN - make sure there are security and account records
# def test_1_holding(self):
# def test_mult_holdings(self):
# def test_1_holding_no_security_recs(self):
# def test_1_holding_no_acct_recs(self):

# if __name__ == '__main__':
#     unittest.main()
#     # unittest.main()
