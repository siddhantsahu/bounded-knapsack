### Algorithms Project: Jeweler Profit Optimization Problem

#### Included Files

- `jeweler_profit.py`, the python code containing the solution
- `test_jeweler_profit.py`, a python file to test the solution
- `test_data`, a folder containing all the sample test cases provided
- `report.pdf`, explains the recurrences, proof of correctness and pseudocode



#### Usage Guide

`jeweler_profit.py` can be run from the command line as follows:

- `python jeweler_profit.py - 1`, this takes user input from the command line
- `python jeweler_profit.py filename 1`, reads input from file



Alternatively, we can also use `pytest` to test if everything works.

- Install `pytest` package using `pip install -U pytest`.
- Place test files in `test_data` folder. Either rename all test files to the form `in*.txt` or choose test files by changing the 7th line in `test_jeweler_profit.py`. For example, to test the code against a file `test_data/test_sample.txt`, change the 7th line to the following:
  `TEST_FILES = ['test_data/test_sample.txt']`
- Then, navigate to the root directory and run `pytest`.