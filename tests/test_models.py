# test_models.py
from django.db import connection
from django.test import TestCase

import balancer.models


class Dictfetchall(TestCase):
    def tearDown(self):
        test_tbl = balancer.models.Security()
        test_tbl.objects.all().delete()

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
            test_vals['effective_dt'] = new_rec.effective_dt
            rec_list.append(test_vals)
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM balancer_security')
        return rec_list, cursor

    def compare_result_to_test_recs(self, test_recs: list, cursor: connection.cursor):
        db_recs = balancer.models.dictfetchall(cursor=cursor)
        if db_recs == test_recs:
            return True
        else:
            return False

    # def test_no_recs(self):
    #     self.assertEqual(True, False)

    def test_1_rec(self):
        test_recs, cursor = self.create_test_recs(num_recs=1)
        self.assertEqual(self.compare_result_to_test_recs(test_recs=test_recs, cursor=cursor), True)


        # def test_mult_recs(self):

# if __name__ == '__main__':
#     unittest.main()
#     # unittest.main()
