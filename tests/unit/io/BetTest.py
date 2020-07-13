import beatmap
import numpy as np


class BaseTest:

    def setup_class(self):
        self.data_A = 1.5
        self.data_B = [1, 5.6]

    def test_check_1(self):
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
