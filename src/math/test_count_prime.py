import unittest
from count_prime import *

class TestPrime(unittest.TestCase):
    def test_is_prime(self):
        """素数に対する素数判定テスト"""
        self.assertTrue(is_prime(2))
        self.assertTrue(is_prime(3))
        self.assertTrue(is_prime(5))
        self.assertTrue(is_prime(7))

    def test_is_not_prime(self):
        """合成数に対する素数判定テスト"""
        self.assertFalse(is_prime(0))
        self.assertFalse(is_prime(1))
        self.assertFalse(is_prime(4))
        self.assertFalse(is_prime(-1))
        self.assertFalse(is_prime(-6))

    def test_count_prime(self):
        """素数の個数を数えるテスト"""
        self.assertEqual(0, count_prime(1))
        self.assertEqual(1, count_prime(2))
        self.assertEqual(2, count_prime(3))
        self.assertEqual(4, count_prime(10))
        self.assertEqual(8, count_prime(20))
        self.assertEqual(10, count_prime(29))


# エントリポイント
if __name__ == "__main__":
    unittest.main()
