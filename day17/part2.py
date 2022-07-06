import argparse
import os.path
from itertools import chain
from itertools import combinations
from itertools import groupby

import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')
# NOTE: paste test text here
INPUT_S = """\
20
15
10
5
5
"""
EXPECTED = 3


def all_combinations(lst):
    yield from chain.from_iterable(
        combinations(lst, c_len)
        for c_len in range(1, len(lst))
        )


def compute(s: str, litres: int) -> int:
    nums = [int(n) for n in s.splitlines()]

    TOTAL_VOLUME = litres

    fit = lambda cmb: sum(cmb) == TOTAL_VOLUME
    succes_combinations = filter(fit, all_combinations(nums))
    lists = [list(g) for k, g in groupby(succes_combinations, key=len)]
    return len(lists[0])


@pytest.mark.solved
@pytest.mark.parametrize(
    ('input_s', 'litres', 'expected'),
    (
            (INPUT_S, 25, EXPECTED),
            ),
    )
def test(input_s: str, litres: int, expected: int) -> None:
    assert compute(input_s, litres) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, timing():
        print(compute(f.read(), 150))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
