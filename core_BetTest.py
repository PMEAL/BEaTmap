import beatmap as bt
import numpy as np
import unittest

class BaseTest (unittest.TestCase):

    def setup_class(self):
        self.c1_positive_ints = np.array([[4, 7], [.001, .5]])
        self.c1_negative_ints = np.array([[-1, -5],[-.1, 0]])
        self.c1_mixed_ints = np.array([[2, 3],[-1, 0]])
        self.c1_bad_ints =np.array([['a', 'e'], ['p', 'l']])

    def test_check_1(self):
        temp = bt.core.check_1(self.c1_positive_ints)
        pos_ints_result = [[1, 1], [1, 1]]
        assert np.all(temp == pos_ints_result)
        temp = bt.core.check_1(self.c1_negative_ints)
        neg_ints_results = [[0, 0], [0, 0]]
        assert np.all(temp == neg_ints_results)
        temp = bt.core.check_1(self.c1_mixed_ints)
        mixed_ints_results = [[1,1],[0,0]]
        assert np.all(temp == mixed_ints_results)
        self.assertRaises(TypeError, bt.core.check_1, self.c1_bad_ints)


    def test_check_2(self):
        # temp = beatmap.core.check_1(self.data_b)
        # desired = [True, False]
        # Test against single values
        a = 2
        b = 2
        assert a == b
        # Test against an array or list (list-like)
        a = [1, 3]
        b = [1, 3]
        assert np.allclose(a, b)
        np.testing.assert_allclose(a, b)


if __name__ == '__main__':

    t = BaseTest()
    self = t
    t.setup_class()
    for item in t.__dir__():
        if item.startswith('test'):
            print('running test: '+item)
            t.__getattribute__(item)()
