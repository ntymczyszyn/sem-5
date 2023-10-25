import unittest
from io import StringIO
from lab3 import decimal_to_binary, decimal_to_hexadecimal

class TestDecimalConversion(unittest.TestCase):
    def test_decimal_to_binary(self):
        self.assertEqual(decimal_to_binary(10), '1010')  # 10 (dziesiętny) to 1010 (dwójkowy)
        self.assertEqual(decimal_to_binary(0), '0')  # 0 (dziesiętny) to 0 (dwójkowy)
        self.assertEqual(decimal_to_binary(255), '11111111')  # 255 (dziesiętny) to 11111111 (dwójkowy)

    def test_decimal_to_hexadecimal(self):
        self.assertEqual(decimal_to_hexadecimal(10), 'A')  # 10 (dziesiętny) to A (szesnastkowy)
        self.assertEqual(decimal_to_hexadecimal(0), '0')  # 0 (dziesiętny) to 0 (szesnastkowy)
        self.assertEqual(decimal_to_hexadecimal(255), 'FF')  # 255 (dziesiętny) to FF (szesnastkowy)


if __name__ == '__main__':
    unittest.main()