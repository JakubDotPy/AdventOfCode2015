import argparse
import functools
import itertools
import operator
import os.path

import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')
# NOTE: paste test text here
INPUT_S = """\
"""


def calculate_ribbon(dimensions):
    sides = sorted(itertools.combinations(dimensions, 2))
    circs = sorted((x + y) * 2 for x, y in sides)
    ribbon_length = circs[0] + functools.reduce(operator.mul, dimensions)
    return ribbon_length


def compute(s: str) -> int:
    total_length = 0
    for line in s.splitlines():
        dimensions = list(map(int, line.split('x')))
        total_length += calculate_ribbon(dimensions)

    return total_length


@pytest.mark.solved
@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
            ('2x3x4', 34),
            ('1x1x10', 14),
            ),
    )
def test(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
