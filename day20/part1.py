import argparse
import os.path
from itertools import chain
from math import sqrt

import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')
# NOTE: paste test text here
INPUT_S = """\
"""
EXPECTED = 0


def divisors(n):
    yield from set(chain.from_iterable(
        (i, n // i)
        for i in range(1, int(sqrt(n)) + 1)
        if n % i == 0
        ))


def compute(n: int) -> int:
    i = 1
    while sum(map(lambda x: x * 10, divisors(i))) < n:
        i += 1
    return i


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
            (140, 8),
            ),
    )
def test(input_s: int, expected: int) -> None:
    assert compute(input_s) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, timing():
        print(compute(33_100_000))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
