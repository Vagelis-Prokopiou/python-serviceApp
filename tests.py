from unittest import TestCase


class Tests(TestCase):
    def test_validate_num(self):
        self.assertTrue(isinstance(1, int))


if __name__ == '__main__':
    unittest.main()
