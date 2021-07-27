import unittest
import time
import main


class MainTestCase(unittest.TestCase):

    def test_calc_days_passed(self):
        # Test the Day Calculator
        yesterday = int(round(time.time())) - 86400
        main_result = main.calculate_days_since(yesterday)
        self.assertEqual(main_result, 1, 'Error: day calculator')

    def test_clean_string_lower(self):
        # Testing the lower part of the function
        main_result_low = main.clean_lower_user_input('THIS IS A TEST')
        expected_result_low = 'this is a test'
        self.assertEqual(main_result_low, expected_result_low, 'Error: Lower part of function not working')
        # Testing the stripping part of the function
        main_result_str = main.clean_lower_user_input('THIS is a   ')
        expected_result_str = 'this is a'
        self.assertEqual(main_result_str, expected_result_str, 'Error: Strip part of function not working')

    def test_clean_string_upper(self):
        # Testing the upper part of the function
        main_result_up = main.clean_upper_user_input('this IS a test')
        expected_result_up = 'THIS IS A TEST'
        self.assertEqual(main_result_up, expected_result_up, 'Error: Upper part of function not working')
        # Testing the stripping part of the function
        main_result_str = main.clean_upper_user_input('THIS is a   ')
        expected_result_str = 'THIS IS A'
        self.assertEqual(main_result_str, expected_result_str, 'Error: Strip part of function not working')

    def test_crypto_uuid(self):
        # Testing the Crypto API Getting correct UUID
        crypto = main.CryptoData()
        crypto.get_uuid('BTC')
        uuid = crypto.crypto_uuid
        self.assertEqual('Qwsogvtv82FCd', uuid, 'Error: Crypto - Getting UUID')

    def test_crypto_raw_data(self):
        # Testing the Crypto API Getting correct raw data
        crypto = main.CryptoData()
        crypto.get_uuid('BTC')
        crypto.get_raw_data()
        raw_data = crypto.raw_data
        len_raw_data = len(raw_data)
        # If there is an error in getting the data it will return a dict with a len of 0
        self.assertGreater(len_raw_data, 0, "Error: Crypto - Getting Raw Data")


if __name__ == '__main__':
    unittest.main()
