import argparse
import os.path
import re
from itertools import permutations

import pytest
from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')
# NOTE: paste test text here
INPUT_S = """\
London to Dublin = 464
London to Belfast = 518
Dublin to Belfast = 141
"""
EXPECTED = 982


def compute(s: str) -> int:
    line_pattern = r'(\w+) to (\w+) = (\d+)'

    distances = {}
    places = set()
    for line in s.splitlines():
        *from_to, distance = re.match(line_pattern, line).groups()
        distances[tuple(from_to)] = int(distance)
        distances[tuple(reversed(list(from_to)))] = int(distance)
        places.update(set(from_to))

    path_lengths = []
    for each in permutations(places):
        sum = 0
        for x, y in zip(each, each[1:]):
            sum += distances[(x, y)]
        path_lengths.append(sum)

    return max(path_lengths)


@pytest.mark.solved
@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
            (INPUT_S, EXPECTED),
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
