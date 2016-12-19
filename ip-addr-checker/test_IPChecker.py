from unittest import TestCase
from IPChecker import IPChecker

__author__ = 'ash'


class TestIPChecker(TestCase):
    def test_words(self):
        ipc = IPChecker()
        self.assertEqual(ipc.is_valid("10.s.32.52"),False)
        self.assertEqual(ipc.is_valid("asd"),False)

    def test_prefix_suffix(self):
        ipc = IPChecker()
        self.assertEqual(ipc.is_valid(".30.12.212.123"),False)
        self.assertEqual(ipc.is_valid("30.12.212.123."),False)
        self.assertEqual(ipc.is_valid(" 30.12.212.123"),True) # Trimming
        self.assertEqual(ipc.is_valid("30.12.212.123 "),True)

    def test_ip_addr(self):
        ipc = IPChecker()
        self.assertEqual(ipc.is_valid("00.12.213.243"),False)
        self.assertEqual(ipc.is_valid("10.12.212.123"),False)
        self.assertEqual(ipc.is_valid("01.12.213.243"),False)
        self.assertEqual(ipc.is_valid("256.12.212.123"),False)

        self.assertEqual(ipc.is_valid("111.312.213122"),False)
        self.assertEqual(ipc.is_valid("12.35.22.001"),False)
        self.assertEqual(ipc.is_valid("1.12.213.03"),False)
        self.assertEqual(ipc.is_valid("135.120.2.2.123"),False)

        self.assertEqual(ipc.is_valid("1.1.1"),False)
        self.assertEqual(ipc.is_valid("3.0.3.00"),False)
        self.assertEqual(ipc.is_valid("01.12.213.243"),False)
        self.assertEqual(ipc.is_valid("256.12.212.123"),False)




if __name__ == '__main__':

    unittest.main()