import argparse
import itertools
import os.path
from collections import Counter

import pytest
from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')
# NOTE: paste test text here
INPUT_S = """\
"""


class Messenger:
    pos_change = {
        '^': (0, 1),
        '>': (1, 0),
        '<': (-1, 0),
        'v': (0, -1),
        }

    def __init__(self, name):
        self.name = name
        self.position = (0, 0)
        self.visited = Counter({self.position: 1})

    def move(self, direction):
        x, y = self.position
        dx, dy = Messenger.pos_change[direction]
        self.position = (x + dx, y + dy)
        self.visited[self.position] += 1

    def __repr__(self):
        return f'Messenger({self.name})'


def compute(s: str) -> int:
    messengers = [
        Messenger('santa'),
        Messenger('robo_santa'),
        ]

    order = itertools.cycle(messengers)

    for direction in s:
        messenger = next(order)
        messenger.move(direction)

    combined_counter = next(order).visited + next(order).visited

    return len(combined_counter)


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
            ('^v', 3),
            ('^>v<', 3),
            ('^v^v^v^v^v', 11),
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
