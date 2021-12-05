import argparse
import itertools
import os.path
import re

import pytest
from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')
# NOTE: paste test text here
INPUT_S = """\
"""


class Light:
    def __init__(self):
        self.power = False

    def turn_on(self):
        self.power = True

    def turn_off(self):
        self.power = False

    def toggle(self):
        self.power = not self.power

    @property
    def on(self):
        return self.power

    @property
    def off(self):
        return not self.on


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
    decoration = {
        coord: Light()
        for coord in itertools.product(range(1_000), range(1_000))
        }

    lines = s.splitlines()
    for line in lines:
        command, x1, y1, x2, y2 = parse(line)
        for coord in square_coords(x1, y1, x2, y2):
            getattr(decoration[coord], command)()

    return sum(l.on for l in decoration.values())


@pytest.mark.template
@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
            (INPUT_S, 0),
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
