import beatmap as bt
import numpy as np
import pandas as pd
import unittest


class Testcore(unittest.TestCase):

    def setup_class(self):
        # setting up test cases for check_1
        self.c1_ok_intercepts = np.array([[2, 3], [-1, 0]])
        self.c1_ok_ints_result = np.array([[True, True], [False, False]])

        self.c1_empty = np.array([[], []])
        self.c1_empty_result = np.array([])

        self.c1_non_list = 3

        self.c1_strings = np.array([['a', 'e'], ['p', 'l']])

        # setting up test cases for check_2
        d_c2_ok = {'relp': [.1, .2, .21], 'n': [.003, .0031, .0031]}
        self.c2_ok_df = pd.DataFrame(data=d_c2_ok)
        self.c2_ok_df_result = np.array([[1., 1., 1.], [0., 0., 0.],
                                         [0., 0., 0.]])

        d_c2_empty = {'relp': [], 'n': []}
        self.c2_empty_df = pd.DataFrame(data=d_c2_empty)
        self.c2_empty_df_result = np.empty((0, 0))

        d_c2_string = {'relp': ['a', 'sdf', ' '], 'n': ['w', '/', 'po']}
        self.c2_string_df = pd.DataFrame(data=d_c2_string)

        d_c2_misname = {'pressure': [.1, .2, .21], 'mols': [.003, .0031, .0031]}
        self.c2_misname_df = pd.DataFrame(data=d_c2_misname)

        self.c2_array = np.array([[2, 3], [-1, 0]])

        # setting up test cases for check_3
        d_c3_ok = {'relp': [.1, .2, .21], 'n': [.001, .003, .004]}
        nm_c3_ok = np.array([[0,0,0],[.001, 0, 0],[.0025, .0035, 0]])
        self.c3_ok = {'df' : pd.DataFrame(data=d_c3_ok), 'nm' : nm_c3_ok}
        self.c3_ok_result = np.array([[0,0,0],[1, 0, 0],[1, 1, 0]])
        

        # setting up test cases for check_4

        # setting up test cases for check_5

    def test_check_1(self):
        # test check_1 when a proper array is passed
        temp = bt.core.check_1(self.c1_ok_intercepts)
        assert np.all(temp == self.c1_ok_ints_result)

        # test check_1 when an empty array is passed
        temp = bt.core.check_1(self.c1_empty)
        assert np.all(temp == self.c1_empty_result)

        # test check_1 when a non list type is passed
        self.assertRaises(TypeError, bt.core.check_1, self.c1_non_list)

        # test check_1 when an array of strings is passed
        self.assertRaises(TypeError, bt.core.check_1, self.c1_strings)

    def test_check_2(self):
        # test check 2 when a proper dataframe is passed
        temp = bt.core.check_2(self.c2_ok_df)
        assert np.all(temp == self.c2_ok_df_result)

        # test check 2 when an empty dataframe is passed
        temp = bt.core.check_2(self.c2_empty_df)
        assert np.all(temp == self.c2_empty_df_result)

        # test check 2 when a dataframe of strings is passed
        self.assertRaises(TypeError, bt.core.check_2, self.c2_string_df)

        # test check 2 when a misnamed dataframe is passed
        self.assertRaises(AttributeError, bt.core.check_2, self.c2_misname_df)

        # test check 2 when an array is passed
        self.assertRaises(AttributeError, bt.core.check_2, self.c2_array)
'''

    def test_check_3(self):
        # test check 3 when a proper dataframe and array are passed
        temp = bt.core.check_3(**self.c3_ok)
        assert np.all(temp == self.c3_ok_result)

        # test check 3 when an empty dataframe and an array of floats is passed
        temp = bt.core.check_3(**self.c3_empty)
        assert np.all(temp == self.c3_empty_result)

        # test check 3 when a dataframe of strings and
        # an array of floats is passed
        self.assertRaises(TypeError, bt.core.check_3, )

        # test check 3 when a misnamed dataframe and
        # an array of floats is passed
        self.assertRaises(AttributeError, bt.core.check_3, )

        # test check 3 when an array of strings is passed for nm
        self.assertRaises(TypeError, bt.core.check_3, )


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


    def test_bet(self):

        # test bet when all are proper

        # test bet when a_o is non numeric

        # test bet when a_o is empty

        # test bet when info is empty

        # test bet when iso_df contains non numeric

        # test bet when iso_df is empty

        # test bet when iso_df is misnamed
'''

if __name__ == '__main__':

    t = Testcore()
    self = t
    t.setup_class()
    for item in t.__dir__():
        if item.startswith('test'):
            print('running test: '+item)
            t.__getattribute__(item)()
