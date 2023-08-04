import os.path
import unittest
from CSVParser import evaluate_csv


class ParserTests(unittest.TestCase):

    # Example_3.csv contains missing data in two of the columns
    # The program should recognize the missing data, log an error, and return an empty dict
    def test_missing_data(self):

        self.assertEqual({}, evaluate_csv('Example_3.csv'))

    # Basic test to ensure the correctness of processed data
    # Example_2.csv and correct values were pulled from the assignment's README
    def test_correct_data(self):

        data = evaluate_csv('Example_2.csv')

        self.assertEqual(1222, data['aaa'].max_price)
        self.assertEqual(1077, data['aaa'].min_price)
        self.assertEqual(1145.0, data['aaa'].avg_price)
        self.assertEqual(40, data['aaa'].tot_volume)

        self.assertEqual(907, data['aab'].max_price)
        self.assertEqual(724, data['aab'].min_price)
        self.assertEqual(795.6666666666666, data['aab'].avg_price)
        self.assertEqual(69, data['aab'].tot_volume)

        self.assertEqual(638, data['aac'].max_price)
        self.assertEqual(477, data['aac'].min_price)
        self.assertEqual(557.5, data['aac'].avg_price)
        self.assertEqual(41, data['aac'].tot_volume)

    # Basic tests to ensure the correctness of the optional processed data
    # The correct values were manually calculated from Example_2.csv
    def test_correct_data_extension(self):

        data = evaluate_csv('Example_2.csv')

        self.assertEqual(3, data['aaa'].num_trades)
        self.assertEqual(1161.425, data['aaa'].wavg_price)
        self.assertEqual(13.333333333333334, data['aaa'].avg_volume_per_trade)



if __name__ == '__main__':

    unittest.main()
