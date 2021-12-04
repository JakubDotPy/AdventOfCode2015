import argparse
import itertools
import os.path

import pytest
from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')
# NOTE: paste test text here
INPUT_S = """\
"""


def calculate_wrapping(dimensions):
    sides = sorted(itertools.combinations(dimensions, 2))
    areas = sorted(x * y for x, y in sides)
    wrapping_size = sum(area * 2 for area in areas) + areas[0]
    return wrapping_size


def compute(s: str) -> int:
    total_area = 0

    for line in s.splitlines():
        dimensions = map(int, line.split('x'))
        total_area += calculate_wrapping(dimensions)

    return total_area


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
            ('2x3x4', 58),
            ('1x1x10', 43),
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
