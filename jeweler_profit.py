"""
Dynamic Programming solution for the problem described at
http://www.utdallas.edu/~rbk/teach/2018/hw/p1-6363-2018s.pdf

Author: Siddhant Sahu
"""
from __future__ import print_function

import os
import sys


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

    def __str__(self):
        return 'Wt = {}, profit = {}, min = {}, max = {}, fine = {}, cap = {}'.format(
            self.weight, self.profit, self.min, self.max, self.fine, self.cap
        )


class Solution(object):
    """Class representing the item and its quantity in the solution."""

    def __init__(self, id, quantity):
        self.id = id
        self.quantity = quantity
        self.parent = None

    def __str__(self):
        return 'id = {}, quantity = {}, parent = ({})'.format(self.id, self.quantity, self.parent)

    def get_items(self):
        sol = []
        while self:
            sol.append(self.quantity)
            self = self.parent
        return tuple(sol)


def max_profit(W, N, items):
    """Computes the maximum possible profit that the jeweler can make from N
    items and W units of gold.

    Args
        W: non-negative int, represents units of gold available
        N: non-negative int, represents total number of items
        items: list of `Item` objects

    Returns
        2d table whose (i, w) index represents the maximum profit that can be
        made with the first i items and w units of gold
    """
    m = [[None for j in range(W + 1)] for i in range(N + 1)]
    sol = [[0 for j in range(W + 1)] for i in range(N + 1)]

    for i in range(N + 1):
        for w in range(W + 1):
            if i == 0:  # base case, no profit with 0 items
                m[i][w] = 0
            else:
                max_profit = m[i - 1][w] - min(items[i - 1].cap,
                                               items[i - 1].fine * (items[i - 1].min - 0))  # for k = 0
                quantity = min(items[i - 1].max, w // items[i - 1].weight)
                for k in range(1, quantity + 1):
                    profit = k * items[i - 1].profit + m[i - 1][w - k * items[i - 1].weight]
                    if k < items[i - 1].min:
                        fine = min(items[i - 1].cap, items[i - 1].fine * (items[i - 1].min - k))
                        profit -= fine
                    if profit > max_profit:
                        max_profit = profit
                m[i][w] = max_profit
                for k in range(1, quantity + 1):
                    profit = k * items[i - 1].profit + m[i - 1][w - k * items[i - 1].weight]
                    if k < items[i - 1].min:
                        fine = min(items[i - 1].cap, items[i - 1].fine * (items[i - 1].min - k))
                        profit -= fine
                    if profit == max_profit:
                        sol[i][w] += 1
    return m, sol


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

    def reconstruct(m, items, i, w, parent=None, node=None):
        """Helper recursive function to reconstruct the solution."""
        if i > 0:
            quantity = min(items[i - 1].max, w // items[i - 1].weight)
            for k in range(quantity + 1):
                val = k * items[i - 1].profit
                if k < items[i - 1].min:
                    fine = min(items[i - 1].cap, items[i - 1].fine * (items[i - 1].min - k))
                    val -= fine
                if (m[i][w] - val) == m[i - 1][w - k * items[i - 1].weight]:
                    node = Solution(i, k)
                    node.parent = parent
                    reconstruct(m, items, i - 1, w - k * items[i - 1].weight, parent=node, node=node)
        else:
            solutions.append(node)

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
            i, w, p, n, x, f, c = [int(x) for x in input().split(' ')]
            items.append(Item(i, w, p, n, x, f, c))
    elif os.path.exists(sys.argv[1]):
        with open(sys.argv[1], 'r') as fp:
            W, N = [int(x) for x in fp.readline().strip().split(' ')]
            for i in range(N):
                i, w, p, n, x, f, c = [int(x) for x in fp.readline().strip().split(' ')]
                items.append(Item(i, w, p, n, x, f, c))
    else:
        raise ValueError('Command line argument not recognized or file doesn\'t exist')

    m, sol = max_profit(W, N, items)
    number_of_solutions = sol[-1][-1]

    # by default prints the optimal profit and the number of solutions
    print(m[N][W], number_of_solutions)

    # if there is a second command line argument, prints the list of optimal solutions
    if len(sys.argv) > 2 and int(sys.argv[2]) > 0:
        solutions = get_solutions(m, items, N, W)
        for sol in solutions:
            print(' '.join(str(i) for i in sol.get_items()))
