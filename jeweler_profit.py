"""
Dynamic Programming solution for the problem described at
http://www.utdallas.edu/~rbk/teach/2018/hw/p1-6363-2018s.pdf

Author: Siddhant Sahu
"""
import os
import sys
import math
import pdb

class Item(object):
    """A class representing an item and its attributes."""

    def __init__(self, id, weight, profit, min_qty, max_qty, fine, fine_cap):
        self.id = id
        self.weight = weight
        self.profit = profit
        self.min = min_qty
        self.max = max_qty
        self.fine = fine
        self.cap = fine_cap


def max_profit(W, N, items):
    """Computes the maximum possible profit that the jeweler can make from N
    items and W units of gold.

    Args
        W: non-negative int, represents units of gold available
        N: non-negative int, represents total number of items
        items: list of `Item` objects

    Returns
        2d table whose (i, w) index represents the maximum profit that can be
        made with the first id items and w units of gold
    """
    m = [[None for j in range(W + 1)] for i in range(N + 1)]

    for i in range(N + 1):
        for w in range(W + 1):
            if i == 0:  # base case, no profit with 0 items
                m[i][w] = 0
            else:
                max_profit = -math.inf
                quantity = min(items[i - 1].max, w // items[i - 1].weight)
                for k in range(quantity + 1):
                    profit = k * items[i - 1].profit + m[i - 1][w - k * items[i - 1].weight]
                    if k < items[i - 1].min:
                        fine = min(items[i - 1].cap, items[i - 1].fine * (items[i - 1].min - k))
                        profit -= fine
                    if profit > max_profit:
                        max_profit = profit
                m[i][w] = max_profit
    return m


def get_solutions(m, items, i, w):
    """Prints all possible solutions.

    Args
        m: 2d table, returned from `max_profit()`
        items: list of `Item` objects
        i, w: i-th row and w-th column for which we want solutions

    Returns
        list of solution(s), to be read `len(items)` elements at a time
    """
    solutions = []

    # not many opportunities to use nested functions
    # recursion is very effective at finding multiple solutions
    # especially, in this case
    def reconstruct(m, items, i, w):
        """Helper recursive function to reconstruct the solution."""
        if i > 0:
            quantity = min(w // items[i - 1].weight, items[i - 1].max)
            for k in range(quantity + 1):
                val = k * items[i - 1].profit
                if k < items[i - 1].min:
                    fine = min(items[i - 1].cap, items[i - 1].fine * (items[i - 1].min - k))
                    val -= fine
                if m[i][w] - val == m[i - 1][w - k * items[i - 1].weight]:
                    solutions.append(k)
                    reconstruct(m, items, i - 1, w - k * items[i - 1].weight)

    reconstruct(m, items, i, w)
    return solutions


if __name__ == '__main__':
    # parse command line arguments
    # if command line argument is empty or '-', take input from stdin
    # otherwise, take input from file
    items = []
    if len(sys.argv) == 1 or sys.argv[1] == '-':
        W, N = [int(x) for x in input().split(' ')]
        for i in range(N):
            # variable nomenclature consistent with description
            i, w, p, n, x, f, c, *rest = [int(x) for x in input().split(' ')]
            items.append(Item(i, w, p, n, x, f, c))
    elif os.path.exists(sys.argv[1]):
        with open(sys.argv[1], 'r') as fp:
            W, N = [int(x) for x in fp.readline().strip().split(' ')]
            for i in range(N):
                i, w, p, n, x, f, c, *rest = [int(x) for x in fp.readline().strip().split(' ')]
                items.append(Item(i, w, p, n, x, f, c))
    else:
        print('Command line argument not recognized or file doesn\'t exist')

    m = max_profit(W, N, items)
    sol = get_solutions(m, items, N, W)
    number_of_solutions = int(len(sol) / N)

    # by default prints the optimal profit and the number of solutions
    print(m[N][W], number_of_solutions)

    # if there is a second command line argument, prints the list of optimal solutions
    if len(sys.argv) > 2 and sys.argv[2]:
        for i in range(number_of_solutions):
            q = []
            for j in range(N):
                q.append(sol.pop())
            print(' '.join([str(x) for x in q]))
