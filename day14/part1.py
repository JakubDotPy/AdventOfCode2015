import argparse
import os.path
import re
from itertools import chain
from itertools import cycle
from itertools import repeat

import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')
# NOTE: paste test text here
INPUT_S = """\
Comet can fly 14 km/s for 10 seconds, but then must rest for 127 seconds.
Dancer can fly 16 km/s for 11 seconds, but then must rest for 162 seconds.
"""
EXPECTED = 1120


class Deer:
    distance = 0

    def __init__(self, name, speed, duration, rest):
        self.name = name
        self.speed = int(speed)
        self.duration = int(duration)
        self.rest = int(rest)

        self.diff_gen = self.diff_generator()

    def diff_generator(self):
        yield from cycle(
            chain(
                repeat(self.speed, self.duration),
                repeat(0, self.rest)
                )
            )

    def move(self):
        self.distance += next(self.diff_gen)

    def __str__(self):
        return f'{self.name} at {self.distance}'

    __repr__ = __str__


def compute(s: str, seconds: int) -> int:
    lines = s.splitlines()
    pattern = r'(^\w+|\d+)+'
    deers = [
        Deer(*re.findall(pattern, line))
        for line in lines
        ]

    for _ in range(seconds):
        for deer in deers:
            deer.move()

    winnig_distance = max(deer.distance for deer in deers)

    return winnig_distance


@pytest.mark.parametrize(
    ('input_s', 'seconds', 'expected'),
    (
            (INPUT_S, 1_000, EXPECTED),
            ),
    )
def test(input_s: str, seconds: int, expected: int) -> None:
    assert compute(input_s, seconds) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, timing():
        print(compute(f.read(), 2503))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
