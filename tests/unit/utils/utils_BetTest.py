import beatmap as bt
import numpy as np
import pandas as pd
import unittest


class BaseTest(unittest.TestCase):

    def setup_class(self):
        self.array_test = np.array([[1., 2., 3., 4., 5., 6.],
                                    [11., 12., 13., 14., 15., 16.],
                                    [1.1, 1.2, 1.4, 1.5, 1.6, 1.7],
                                    [9., 8., 7., 6., 5., 4.4],
                                    [0.4, 0.6, 0.8, 0.1, 0.2, 0.22],
                                    [40., 50., 60., 70., 80., 90.]])

        self.mult_value_array_test = np.array([[0.1, 2., 3., 4., 5., 6.],
                                               [11., 12., .1, 14., 15., 16.],
                                               [1.1, 1.2, 1.4, 1.5, 1.6, 1.7],
                                               [9., 8., 7., 6., 5., 4.4],
                                               [0.4, 0.6, 0.8, 0.1, 0.2, 0.22],
                                               [40., 50., 60., 70., 80., 90.]])

        self.str_value_array_test = np.array([[0.1, 2., 3., 4., 5., 6.],
                                              [11., 12., 13., 14., 15., 16.],
                                              [1.1, 1.2, 'a', 1.5, 1.6, 1.7],
                                              [9., 8., 7., 6., 5., 4.4],
                                              [0.4, 0.6, 0.8, 0.1, 0.2, 0.22],
                                              [40., 50., 60., 70., 80., 90.]])

        self.empty_array_test = np.array([[], [], [], [], []])

        d_lin_interp = {'relp': [.1, .2, .21, .3, .4, .5],
                        'n': [.001, .002, .004, .005, .0055, .006]}
        self.lin_interp_df = pd.DataFrame(d_lin_interp)

        d_empty_lin_interp = {'relp': [], 'n': []}
        self.empty_lin_interp_df = pd.DataFrame(d_empty_lin_interp)

    def test_index_of_value(self):
        temp = bt.utils.index_of_value(self.array_test, 13)
        assert temp == ([1], [2])

        temp = bt.utils.index_of_value(self.mult_value_array_test, .1)
        assert (temp[0] == [0, 1, 4]).all()
        assert (temp[1] == [0, 2, 3]).all()

        temp = bt.utils.index_of_value(self.mult_value_array_test, 1300)
        assert temp[0].size == 0
        assert temp[1].size == 0

        with self.assertRaises(np.core._exceptions.UFuncTypeError):
            bt.utils.index_of_value(self.str_value_array_test, '1.5')

    def test_max_min(self):
        temp = bt.utils.max_min(self.array_test)
        assert temp[0] == 90
        assert temp[1] == ([5], [5])
        assert temp[2] == 0.1
        assert temp[3] == ([4], [3])

        temp = bt.utils.max_min(self.mult_value_array_test)
        assert temp[0] == 90
        assert temp[1] == ([5], [5])
        assert temp[2] == 0.1
        assert (temp[3][0] == [0, 1, 4]).all()
        assert (temp[3][1] == [0, 2, 3]).all()

        with self.assertRaises(TypeError):
            bt.utils.max_min(self.str_value_array_test)

    def test_lin_interp(self):
        temp = bt.utils.lin_interp(self.lin_interp_df, .0015)
        assert temp == .15

        temp = bt.utils.lin_interp(self.lin_interp_df, .007)
        assert temp == 0.6999999999999997

        with self.assertRaises(KeyError):
            bt.utils.lin_interp(self.empty_lin_interp_df, .007)


if __name__ == '__main__':

    t = BaseTest()
    self = t
    t.setup_class()
    for item in t.__dir__():
        if item.startswith('test'):
            print('running test: '+item)
            t.__getattribute__(item)()
