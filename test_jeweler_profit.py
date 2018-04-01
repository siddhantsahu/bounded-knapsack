import glob

import pytest

from jeweler_profit import Item, max_profit, get_solutions

TEST_FILES = glob.glob('test_data/in*.txt')


@pytest.fixture(scope='module', params=TEST_FILES)
def test_data(request):
    """Parses the input and output from a file."""
    items = []
    solutions = set()
    with open(request.param, 'r') as fp:
        W, N = [int(x) for x in fp.readline().strip().split(' ')]
        for i in range(N):
            i, w, p, n, x, f, c = [int(x) for x in fp.readline().strip().split(' ')]
            items.append(Item(i, w, p, n, x, f, c))
        fp.readline()  # caption for output
        max_profit, number_of_solutions = [int(x) for x in fp.readline().strip().split(' ')]
        fp.readline()  # caption for list of optimal solutions
        for i in range(number_of_solutions):
            solutions.add(tuple([int(x) for x in fp.readline().strip().split(' ')]))
    return {'input': (W, N, items),
            'output': (max_profit, number_of_solutions, solutions)}


@pytest.fixture(scope='module')
def test_max_profit(test_data):
    W, N, items = test_data['input']
    max_value, number_of_solutions, _ = test_data['output']
    m, sol = max_profit(W, N, items)
    assert m[N][W] == max_value
    assert sol[N][W] == number_of_solutions
    return m


def test_solutions(test_data, test_max_profit):
    W, N, items = test_data['input']
    _, _, solutions = test_data['output']
    m = test_max_profit
    items = get_solutions(m, items, N, W)
    items = set([s.get_items() for s in items])
    assert items == solutions
