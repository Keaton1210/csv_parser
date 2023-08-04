Project: CSVParser.py
Author: Erik Diehl

Evaluates the target csv and processes the trade data into the following:

    - Min Price of All Trades
    - Max Price of All Trades
    - Unweighted Average Price of Trades
    - Total Volume Traded

    ...for each ticker found within the CSV.

    Optionally, you can also process the following:

    - Total Number of Trades
    - Weighted Average Price of Trades
    - Average Volume per Trade
    - Graph of each ticker's traded volume over time (hours since midnight)

The script is designed to be run from a terminal, can parse multiple csvs,
can log errors independently between csvs, and includes a basic set of unit tests,
contained within csv_parser_tests.py

I also included a set of 4 example csv documents for testing/observation.

    - Example_1.csv is the full input data from the prompt
    - Example_2.csv is the basic input data from the prompt README
    - Example_3.csv is the same as Example_2.csv, except it contains missing data
    - Example_4.csv is the same as Example_2.csv, but has more variation in trading times
      for better visualization with the graphing functionality

Key for UI:

    - (e): Evaluates a new CSV file from the inputted path
    - (g): Generates a graph from an inputted ticker. Data is pulled from the last evaluated CSV file
    - (p): Prints a more comprehensive set of data for an inputted ticker
    - (q): Quits the program
