import beatmap as bt
import numpy as np
import pandas as pd
import unittest


class BaseTest(unittest.TestCase):
    def setup_class(self):
        self.array_test = np.array(
            [
                [1.0, 2.0, 3.0, 4.0, 5.0, 6.0],
                [11.0, 12.0, 13.0, 14.0, 15.0, 16.0],
                [1.1, 1.2, 1.4, 1.5, 1.6, 1.7],
                [9.0, 8.0, 7.0, 6.0, 5.0, 4.4],
                [0.4, 0.6, 0.8, 0.1, 0.2, 0.22],
                [40.0, 50.0, 60.0, 70.0, 80.0, 90.0],
            ]
        )

        self.mult_value_array_test = np.array(
            [
                [0.1, 2.0, 3.0, 4.0, 5.0, 6.0],
                [11.0, 12.0, 0.1, 14.0, 15.0, 16.0],
                [1.1, 1.2, 1.4, 1.5, 1.6, 1.7],
                [9.0, 8.0, 7.0, 6.0, 5.0, 4.4],
                [0.4, 0.6, 0.8, 0.1, 0.2, 0.22],
                [40.0, 50.0, 60.0, 70.0, 80.0, 90.0],
            ]
        )

        self.str_value_array_test = np.array(
            [
                [0.1, 2.0, 3.0, 4.0, 5.0, 6.0],
                [11.0, 12.0, 13.0, 14.0, 15.0, 16.0],
                [1.1, 1.2, "a", 1.5, 1.6, 1.7],
                [9.0, 8.0, 7.0, 6.0, 5.0, 4.4],
                [0.4, 0.6, 0.8, 0.1, 0.2, 0.22],
                [40.0, 50.0, 60.0, 70.0, 80.0, 90.0],
            ]
        )

        self.empty_array_test = np.array([[], [], [], [], []])

        d_lin_interp = {
            "relp": [0.1, 0.2, 0.21, 0.3, 0.4, 0.5],
            "n": [0.001, 0.002, 0.004, 0.005, 0.0055, 0.006],
        }
        self.lin_interp_df = pd.DataFrame(d_lin_interp)

        d_empty_lin_interp = {"relp": [], "n": []}
        self.empty_lin_interp_df = pd.DataFrame(d_empty_lin_interp)

    def test_index_of_value(self):
        temp = bt.utils.index_of_value(self.array_test, 13)
        assert temp == ([1], [2])

        temp = bt.utils.index_of_value(self.mult_value_array_test, 0.1)
        assert (temp[0] == [0, 1, 4]).all()
        assert (temp[1] == [0, 2, 3]).all()

        temp = bt.utils.index_of_value(self.mult_value_array_test, 1300)
        assert temp[0].size == 0
        assert temp[1].size == 0

        with self.assertRaises(np.core._exceptions.UFuncTypeError):
            bt.utils.index_of_value(self.str_value_array_test, "1.5")

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
        temp = bt.utils.lin_interp(self.lin_interp_df, 0.0015)
        assert temp == 0.15

        temp = bt.utils.lin_interp(self.lin_interp_df, 0.007)
        assert temp == 0.6999999999999997

        with self.assertRaises(KeyError):
            bt.utils.lin_interp(self.empty_lin_interp_df, 0.007)


if __name__ == "__main__":

    t = BaseTest()
    self = t
    t.setup_class()
    for item in t.__dir__():
        if item.startswith("test"):
            print("running test: " + item)
            t.__getattribute__(item)()
