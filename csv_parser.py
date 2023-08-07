"""
Author: Erik Keaton Diehl
Project: Test CSV Reader
"""

# Imports
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import logging


# Hybrid container/data-processing class for data per ticker
class Instrument:

    def __init__(self, ticker_name, curr_frame, origin_path) -> None:

        self.ticker_name = ticker_name
        self.frame = curr_frame
        self.origin_path = origin_path

        self.val_collection = []
        self.volume_collection = []
        self.time_collection = []

        # For each row associated with a ticker, track the trade price and the quantity
        for row in self.frame.itertuples():
            self.val_collection.append(row[3])
            self.volume_collection.append(row[2])
            self.time_collection.append(row[1])

        # Find the total number of trades for the ticker
        self.num_trades = self.frame.shape[0]

        # Find the total volume traded for the ticker
        self.tot_volume = sum(self.volume_collection)

        # Find the maximum price across all trades for the ticker (index 2)
        max_series: pd.Series = self.frame.max()
        self.max_price = max_series.tolist()[2]

        # Find the minimum price across all trades for the ticker (index 2)
        min_series: pd.Series = self.frame.min()
        self.min_price = min_series.tolist()[2]

        # Find the unweighted and weighted averages of the price for the ticker
        self.avg_price = np.mean(self.val_collection)
        self.wavg_price = np.average(self.val_collection, weights=self.volume_collection)

        # Find the average volume traded per trade for the ticker
        self.avg_volume_per_trade = np.mean(self.volume_collection)

    def gen_trade_plot(self) -> None:

        fig, ax = plt.subplots()

        x_ax = np.divide(self.time_collection, 3600000000)
        y_ax = self.volume_collection

        ax.stem(x_ax, y_ax)

        ax.set_ylabel('Volume Traded')
        ax.set_xlabel('Time of Trade (hours since Midnight)')
        ax.set_title(f'[{self.ticker_name}] Trades Over Time')

        plt.xticks(range(0, 25))

        logging.info(f'INFO | Generated graph for [{self.ticker_name}] from {self.origin_path}')

        plt.show()

    def print_summary(self, to_print=False) -> str:

        msg = f'[{self.ticker_name}] 'f'Max Price: {self.max_price}, '\
            f'Min Price: {self.min_price}, Unweighted Average Price: {self.avg_price}, '\
            f'Total Volume Traded: {self.tot_volume}\n'

        if to_print:
            print(msg)

        return msg

    def print_summary_ext(self, to_print=False) -> str:

        msg = (f'[{self.ticker_name}] \nTotal # of Trades: {self.num_trades}, '
               f'\nMax Price: {self.max_price}, \nMin Price: {self.min_price}, '
               f'\nUnweighted Average Price: {self.avg_price}, '
               f'\nWeighted Average Price: {self.wavg_price}, '
               f'\nTotal Volume Traded: {self.tot_volume}, '
               f'\nAvg Volume per Trade: {self.avg_volume_per_trade} \n')

        if to_print:
            print(f'[{self.ticker_name}] \n'
                  f'    Total # of Trades: {self.num_trades}, \n'
                  f'    Max Price: {self.max_price}, \n'
                  f'    Min Price: {self.min_price}, \n'
                  f'    Unweighted Average Price: {self.avg_price}, \n'
                  f'    Weighted Average Price: {self.wavg_price}, \n'
                  f'    Total Volume Traded: {self.tot_volume}, \n'
                  f'    Avg Volume per Trade: {self.avg_volume_per_trade} \n')

        return msg


def evaluate_csv(path: str) -> dict:

    ticker_data = {}

    logging.info(f'INFO | Attempting to parse {path}...')

    test = pd.read_csv(path, header=None)

    # Checks whether there is missing data anywhere in the csv and aborts if any is found
    if test.isnull().values.any():
        logging.error('ERROR | Target CSV is missing data. Please fix target csv before parsing. Aborting...')
        print('Target CSV is missing data. Please fix target csv before parsing. Aborting...')
        return {}

    # Archaic method of finding unique tickers
    # unique_tickers = np.unique(test.loc[:, 'ticker'].tolist())

    # Find the unique tickers substantially faster than np.unique (according to pandas)
    unique_tickers = pd.unique(test.iloc[:, 1])
    unique_tickers.sort()

    # print(f'{unique_tickers}\n')

    """
    Allow indexing of the rows by ticker

    Ex. df =   value   ticker
            0   12      'a'
            1   24      'b'

    Rather than indexing by row number (0), setting the
    indexing to the 'ticker' column transforms the dataframe into...

    --> df =     
                      value
             ticker 
              'a'      12
              'b'      24

    where we can access certain rows of data by indexing the ticker
    name 'a' instead
    """

    tick_index_frame: pd.DataFrame = test.set_index(list(test.columns[[1]]))

    # Open a new file to write the data to
    f = open(f'{os.getcwd()}/ticker_data.txt', 'w')

    for ticker in unique_tickers:

        # Collect all rows of data associated with current ticker
        curr_frame = tick_index_frame.loc[[ticker]]

        # Generate a new ticker object and automatically calculate params
        ticker_data[ticker] = Instrument(ticker, curr_frame, path)

    for key in ticker_data.keys():
        data = ticker_data[key].print_summary()
        # data = ticker_data[key].print_summary_ext()
        f.write(data)

    logging.info(f'INFO | Successfully parsed {path}.')
    f.close()
    return ticker_data


if __name__ == '__main__':

    logging.basicConfig(filename='csv_parser.log',
                        filemode='w',
                        format='%(asctime)s | %(message)s',
                        level=logging.INFO)

    ticker_data = {}

    try:

        path = input('Enter Path to Target CSV: \n')
        try:
            ticker_data = evaluate_csv(path)
        except FileNotFoundError:
            print("Target file not found")
            logging.info(f'INFO | Target CSV not found at {path}')

        while True:

            response = input("(e)valuate another sheet, "
                             "(g)enerate trade graph, "
                             "(p)rint ticker data, "
                             "(q)uit \n")

            if response == 'e':
                path = input("Enter Path: ")
                try:
                    ticker_data = evaluate_csv(path)
                except FileNotFoundError:
                    print("Target file not found")
                    logging.info(f'INFO | Target CSV not found at {path}')
            elif response == 'g':
                ticker = input("Enter Ticker: ")
                try:
                    ticker_data[ticker].gen_trade_plot()
                except KeyError:
                    print("Ticker does not exist within the data")
                except TypeError:
                    print("No CSV Evaluated")
            elif response == 'p':
                ticker = input("Enter Ticker: ")
                try:
                    ticker_data[ticker].print_summary_ext(to_print=True)
                except KeyError:
                    print("Ticker does not exist within the data")
                except TypeError:
                    print("No CSV Evaluated")
            elif response == 'q':
                logging.info("INFO | Quitting.")
                exit(0)
    except KeyboardInterrupt:
        logging.info("INFO | Program Terminated Externally.")
        exit(0)

