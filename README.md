## Algorithms: Jeweler Profit Optimization (Bounded Knapsack)

Problem statementFor recurrence equations and proof of correctness, see `report.pdf`.

### Usage Guide (Python)
***Not recommended**. Python version is for verifying correctness of algorithm and testing on small inputs.*

`jeweler_profit.py` can be run from the command line as follows:

- `python jeweler_profit.py - 1`, this takes user input from the command line
- `python jeweler_profit.py filename 1`, reads input from file

Alternatively, we can also use `pytest` to test if everything works.

- Install `pytest` package using `pip install -U pytest`.
- Place test files in `test_data` folder. Either rename all test files to the form `in*.txt` or choose test files by changing the 7th line in `test_jeweler_profit.py`. For example, to test the code against a file `test_data/test_sample.txt`, change the 7th line to the following:
  `TEST_FILES = ['test_data/test_sample.txt']`

**Note:** I took this as an opportunity to learn [Cython](http://docs.cython.org/en/latest/). Although I do not have the benchmark now and am too lazy to recreate it, I remember Cython beating the same code in Java (for this particular problem) by about 5-10%.

**TODO:** Add time benchmarks for Cython, Numba and Java.

### Usage Guide (Cython)
- [Install](http://docs.cython.org/en/latest/src/quickstart/install.html) Cython: `pip install cython`.
- As mentioned [here](http://docs.cython.org/en/latest/src/quickstart/build.html#building-a-cython-module-using-distutils), run `python setup.py build_ext --inplace` to build the `.pyx` file containing cython code.
- Use `run_bkp.py` like `jeweler_profit.py`. Read the python usage guide above.