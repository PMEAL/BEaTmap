import beatmap as bt
import numpy as np
import unittest

class Testcore(unittest.TestCase):

    def setup_class(self):
        # setting up test cases for check_1
        self.c1_mixed_ints = np.array([[2, 3],[-1, 0]])
        self.c1_mixed_ints_result = np.array([[True, True],[False, False]])
        self.c1_bad_ints =np.array([['a', 'e'], ['p', 'l']])

        # setting up test cases for check_2

        # setting up test cases for check_3

        # setting up test cases for check_4

        # setting up test cases for check_5

    def test_bet(self):

        # test bet when all are proper

        # test bet when a_o is non numeric

        # test bet when a_o is empty

        # test bet when info is empty

        # test bet when iso_df contains non numeric

        # test bet when iso_df is empty

        # test bet when iso_df is misnamed

        

    def test_check_1(self):
        # test check_1 when a proper array is passed
        temp = bt.core.check_1(self.c1_mixed_ints)
        assert np.all(temp == self.c1_mixed_ints_result)
        # test check_1 when an array of strings is passed
        self.assertRaises(TypeError, bt.core.check_1, self.c1_bad_ints)
        # test check_1 when an empty array is passed

        # test check_1 when a non list type is passed


    def test_check_2(self):
        # test check 2 when a proper dataframe is passed

        # test check 2 when a dataframe of strings is passed

        # test check 2 when a misnamed dataframe is passed

        # test check 2 when an empty dataframe is passed

        # test check 2 when an array is passed
        

    def test_check_3(self):
        # test check 3 when a proper dataframe and array are passed

        # test check 3 when a dataframe of strings and an array of floats is passed

        # test check 3 when a misnamed dataframe and an array of floats is passed

        # test check 3 when an empty dataframe and an array of floats is passed

        # test check 3 when an array of strings is passed


    def test_check_4(self):
        # test check 4 when all are proper

        # test check 4 when df contains non numeric

        # test check 4 when df is empty

        # test check 4 when df is misnamed

        # test check 4 when nm is non numeric

        # test check 4 when nm is empty

        # test check 4 when slope is non numeric

        # test check 4 when slope is empty

        # test check 4 when intercept is non numeric

        # test check 4 when intercept is empty


    def test_check_5(self):
        # test check 5 when all are proper

        # test check 5 when points > size

        # test check 5 when points are negative

        # test check 5 when points are non numeric

    def test_ssa_answer(self):
        # test ssa_answer when all are proper

        # test ssa_answer when bet_results is empty

        # test ssa_answer when mask_results is empty

        # test ssa_answer when bet_results is non numeric

        # test ssa_answer when mask_results is non numeric

        # test ssa_answer when criterion != 'error' or 'points'


if __name__ == '__main__':

    t = Testcore()
    self = t
    t.setup_class()
    for item in t.__dir__():
        if item.startswith('test'):
            print('running test: '+item)
            t.__getattribute__(item)()
