import beatmap as bt
import numpy as np
import pandas as pd
import unittest


class Testcore(unittest.TestCase):
    def setup_class(self):
        # mock isotherm data for check and mask tests
        # same data as all the 'ok' data import tests
        self.ok_test = {"file": "test_ok.csv", "info": "test ok file", "a_o": 11.11}

        d_bet_ok = {
            "relp": [0.1, 0.2, 0.21, 0.3, 0.4, 0.5],
            "n": [0.001, 0.002, 0.004, 0.005, 0.0055, 0.006],
            "bet": [
                111.111111,
                125.000000,
                66.455696,
                85.714286,
                121.212121,
                166.666667,
            ],
        }

        self.ok_iso_df = pd.DataFrame(data=d_bet_ok)

        self.ok_bet_results = bt.core.bet(self.ok_iso_df, 11.11, "test ok file")
        self.ok_mask_results = bt.core.rouq_mask(*self.ok_bet_results)

        # mock results for check_1
        self.ok_check_1_result = np.array(
            [
                [False, False, False, False, False, False],
                [True, False, False, False, False, False],
                [True, True, False, False, False, False],
                [True, True, True, False, False, False],
                [True, True, True, False, False, False],
                [True, True, False, False, False, False],
            ]
        )

        # mock results for check_2
        self.ok_check_2_result = np.array(
            [
                [1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
                [1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
                [1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
                [1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
                [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            ]
        )

        # mock results for check_3
        self.ok_check_3_result = np.array(
            [
                [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                [0.0, 0.0, 1.0, 0.0, 0.0, 0.0],
                [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                [1.0, 1.0, 0.0, 0.0, 0.0, 0.0],
            ]
        )

        # mock results for check_4
        self.ok_check_4_result = np.array(
            [
                [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                [0.0, 0.0, 1.0, 0.0, 0.0, 0.0],
                [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            ]
        )

        # mock results for check_5, points = 5
        self.ok_check_5_result = np.array(
            [
                [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                [1.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                [1.0, 1.0, 0.0, 0.0, 0.0, 0.0],
            ]
        )

        # mock results for combo mask
        self.ok_rouq_mask_result = np.array(
            [
                [True, True, True, True, True, True],
                [True, True, True, True, True, True],
                [True, True, True, True, True, True],
                [True, True, True, True, True, True],
                [True, True, True, True, True, True],
                [True, True, True, True, True, True],
            ]
        )

        # mock results for ssa_answer test vulcan_chex.csv data
        d_ssa_test = {
            "file": "vulcan_chex.csv",
            "info": "chex on carbon black",
            "a_o": 39,
        }
        ssa_imported = bt.io.import_data(**d_ssa_test)
        self.ssa_test_bet_results = bt.core.bet(*ssa_imported)
        self.ssa_test_mask_results = bt.core.rouq_mask(*self.ssa_test_bet_results)

        self.ok_bet_results = bt.core.bet(self.ok_iso_df, 11.11, "test ok file")

    def test_check_1(self):
        temp = bt.core.check_1(self.ok_bet_results.intercept)
        assert np.all(temp == self.ok_check_1_result)

    def test_check_2(self):
        temp = bt.core.check_2(self.ok_bet_results.iso_df)
        assert np.all(temp == self.ok_check_2_result)

    def test_check_3(self):
        temp = bt.core.check_3(self.ok_bet_results.iso_df, self.ok_bet_results.nm)
        assert np.all(temp == self.ok_check_3_result)

    def test_check_4(self):
        temp = bt.core.check_4(
            self.ok_bet_results.iso_df,
            self.ok_bet_results.nm,
            self.ok_bet_results.slope,
            self.ok_bet_results.intercept,
        )
        assert np.all(temp == self.ok_check_4_result)

    def test_check_5(self):
        temp = bt.core.check_5(self.ok_bet_results.iso_df)
        assert np.all(temp == self.ok_check_5_result)

        with self.assertRaises(TypeError):
            bt.core.check_5(self.ok_bet_results.iso_df, "five")

    def test_bet(self):
        temp = bt.core.bet(self.ok_iso_df, 11.11, "test ok file")
        assert (temp.intercept == self.ok_bet_results.intercept).all()
        assert temp.iso_df.equals(self.ok_bet_results.iso_df)
        assert (temp.nm == self.ok_bet_results.nm).all()
        assert (temp.slope == self.ok_bet_results.slope).all()
        assert (temp.ssa == self.ok_bet_results.ssa).all()
        assert (temp.c == self.ok_bet_results.c).all()
        assert (temp.err == self.ok_bet_results.err).all()
        assert (temp.r == self.ok_bet_results.r).all()
        assert (temp.num_pts == self.ok_bet_results.num_pts).all()
        assert temp.info == self.ok_bet_results.info

    def test_rouq_mask(self):
        # testing with ok data
        temp = bt.core.rouq_mask(
            self.ok_bet_results.intercept,
            self.ok_bet_results.iso_df,
            self.ok_bet_results.nm,
            self.ok_bet_results.slope,
        )
        assert np.all(temp.mask == self.ok_rouq_mask_result)

    def test_ssa_answer(self):
        temp = bt.core.ssa_answer(
            self.ssa_test_bet_results, self.ssa_test_mask_results, "error"
        )
        assert temp == 231.47986411971542
        temp = bt.core.ssa_answer(
            self.ssa_test_bet_results, self.ssa_test_mask_results, "points"
        )
        assert temp == 228.96104514464378

        with self.assertRaises(ValueError):
            bt.core.ssa_answer(
                self.ssa_test_bet_results, self.ssa_test_mask_results, "incorrect"
            )

        with self.assertRaises(ValueError):
            bt.core.ssa_answer(self.ok_bet_results, self.ok_mask_results)


if __name__ == "__main__":

    t = Testcore()
    self = t
    t.setup_class()
    for item in t.__dir__():
        if item.startswith("test"):
            print("running test: " + item)
            t.__getattribute__(item)()
