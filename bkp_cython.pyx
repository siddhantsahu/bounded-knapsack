import sys

import numpy as np

# learning cython, so hardcoded this for the number of items
# use the appropriate test data 
DEF NITEMS = 50

# work with structs, localized data => insane speeds
cdef struct item_t:
    int idx
    long weight
    long profit
    long min_q
    long max_q
    long fine
    long cap


def test_data(filename):
    """Parses the input from a file."""
    items = []
    with open(filename, 'r') as fp:
        W, N = [int(x) for x in fp.readline().strip().split(' ')]
        for i in range(N):
            i, w, p, n, x, f, c = [int(x) for x in fp.readline().strip().split(' ')]
            items.append({'idx': i, 'weight': w, 'profit': p, 'min_q': n, 'max_q': x, 'fine': f, 'cap': c})
    return W, N, items


# this function converts list of dictionaries to c structs
cdef void make_items(list py_items, item_t *c_items):
    for i, el in enumerate(py_items):  # iterating over python list of dicts
        c_items[i].idx = el['idx']
        c_items[i].weight = el['weight']
        c_items[i].profit = el['profit']
        c_items[i].min_q = el['min_q']
        c_items[i].max_q = el['max_q']
        c_items[i].fine = el['fine']
        c_items[i].cap = el['cap']


# max profit calculator, same as in jeweler_profit.py, cython optimized
def max_profit(long W, long N, py_items):
    # m and count tables are 1-indexed, while items is 0-indexed
    cdef:
        long i, j, w, k, quantity, profit, max_profit, fine
        item_t items[NITEMS]
        item_t *cur_item    # for the current item, c pointer

    # initialize 2d arrays using numpy
    m_table = np.zeros((N + 1, W + 1), dtype=np.int64)
    count_table = np.zeros((N + 1, W + 1), dtype=np.int64)
    
    # typed memoryviews
    # removing bounds check makes these even faster but trade-off is safety
    cdef:
        long [:,:] m = m_table
        long [:,:] count = count_table

    make_items(py_items, items)

    # workhorse, most of these happen in C, ridiculuous speed-up compared to Python
    for i in range(N + 1):
        for w in range(W + 1):
            cur_item = &items[i - 1]
            if i == 1:
                count[i][w] = 1
            if i == 0:  # base case, no profit with 0 items
                m[i][w] = 0
                count[i][w] = 0
            else:
                max_profit = m[i - 1][w] - min(cur_item.cap,
                                               cur_item.fine * (cur_item.min_q - 0))  # for k = 0
                quantity = min(cur_item.max_q, w // cur_item.weight)
                for k in range(quantity + 1):
                    profit = k * cur_item.profit + m[i - 1][w - k * cur_item.weight]
                    if k < cur_item.min_q:
                        fine = min(cur_item.cap, cur_item.fine * (cur_item.min_q - k))
                        profit -= fine
                    if profit > max_profit:
                        max_profit = profit
                m[i][w] = max_profit
                for k in range(quantity + 1):
                    profit = k * cur_item.profit + m[i - 1][w - k * cur_item.weight]
                    if k < cur_item.min_q:
                        fine = min(cur_item.cap, cur_item.fine * (cur_item.min_q - k))
                        profit -= fine
                    if profit == max_profit:
                        count[i][w] += count[i - 1][w - k * cur_item.weight]
    return m, count

def run(filename):
    W, N, items = test_data(filename)
    m, count = max_profit(W, N, items)
    print(m[-1][-1], count[-1][-1])
