"""
Author: Erik Keaton Diehl
Project: Test CSV Reader (temporary hard-coded dataframe)

Evaluates the target csv (WIP) and processes the trade data into the following:

    -

"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import logging


def evaluate_csv():
    test = pd.DataFrame([
        [1, 400, 'aaa'],
        [50, 200, 'bbb'],
        [11, 100, 'cbh'],
        [12, 50, 'axi'],
        [23, 100, 'bbb'],
        [3, 125, 'bbb'],
        [1, 180, 'aa'],
        [24, 200, 'bbb'],
        [15, 50, 'cbh'],
        [126, 50, 'axi'],
        [83, 25, 'bbb'],
        [37, 125, 'bbb'],
        [37, 125, 'axi']],
        columns=['val', 'quantity', 'ticker'])

    # Archaic method of finding unique tickers
    # unique_tickers = np.unique(test.loc[:, 'ticker'].tolist())

    # Find the unique tickers substantially faster than np.unique (according to pandas)
    unique_tickers = pd.unique(test.loc[:, 'ticker'])

    print(f'{unique_tickers}\n')

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
    tick_index_frame: pd.DataFrame = test.set_index('ticker')

    for ticker in unique_tickers:

        val_collection = []
        quant_collection = []

        # Collect all rows of data associated with current ticker
        curr_frame = tick_index_frame.loc[[ticker]]

        # For each row associated with a ticker, track the trade price and the quantity
        for row in curr_frame.itertuples():
            val_collection.append(row[1])
            quant_collection.append(row[2])

        # Find the total number of trades for the ticker
        total_trades = curr_frame.shape[0]
        print(f'[{ticker}] Total Trades: {total_trades}')

        # Find the maximum trade value across all trades for the ticker
        max_series: pd.Series = curr_frame.max()
        max_list = max_series.tolist()
        print(f'[{ticker}] Max Trade Value: {max_list[0]}')

        # Find the unweighted and weighted averages of the trade value for the ticker
        unw_avg = np.mean(val_collection)
        w_avg = np.average(val_collection, weights=quant_collection)
        print(f'[{ticker}] Unweighted Trade Value Avg: {unw_avg}')
        print(f'[{ticker}] Weighted Trade Value Avg: {w_avg}')

        # Find the average quantity traded for the ticker
        quant_trd_avg = np.mean(quant_collection)
        print(f'[{ticker}] Avg Quantity Traded: {quant_trd_avg}\n')

        fig, ax = plt.subplots()

        x_ax = unique_tickers
        y_ax = total_trades

        ax.bar(x_ax, y_ax)

        ax.set_ylabel('Volume Traded')
        ax.set_title('Volume Traded by Ticker')

        plt.show()


if __name__ == '__main__':

    logging.basicConfig(format='%(asctime)s | %(message)s', level=logging.INFO)
    # logging.info('INFO | test 1')
    # logging.warning('WARNING | test 2')

    evaluate_csv()



