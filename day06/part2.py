import argparse
import itertools
import os.path
import re
from collections import Counter

import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')
# NOTE: paste test text here
INPUT_S = """\
"""


def square_coords(x1, y1, x2, y2):
    return itertools.product(range(x1, x2 + 1), range(y1, y2 + 1))


def parse(line):
    pattern = r'([a-z ]+) (\d+),(\d+).*?(\d+),(\d+)'
    groups = list(re.match(pattern, line).groups())
    groups[0] = groups[0].replace(' ', '_')
    groups[1:] = list(map(int, groups[1:]))
    return groups


def compute(s: str) -> int:
    # milion lights
    decoration = Counter()
    commands = {
        'turn_on' : 1,
        'turn_off': -1,
        'toggle'  : 2,
        }

    lines = s.splitlines()
    for line in lines:
        command, x1, y1, x2, y2 = parse(line)
        for coord in square_coords(x1, y1, x2, y2):
            new_value = max(decoration[coord] + commands[command], 0)
            decoration[coord] = new_value

    return sum(v for v in decoration.values() if v >= 0)


@pytest.mark.solved
@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
            ('turn on 0,0 through 0,0', 1),
            ('turn on 0,0 through 1,1', 4),
            ('toggle 0,0 through 999,999', 2_000_000),
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
