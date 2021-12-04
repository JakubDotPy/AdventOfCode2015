import argparse
import os.path
from collections import Counter

import pytest
from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')
# NOTE: paste test text here
INPUT_S = """\
"""

pos_change = {
    '^': (0, 1),
    '>': (1, 0),
    '<': (-1, 0),
    'v': (0, -1),
    }


def compute(s: str) -> int:
    position = (0, 0)
    visited = Counter()
    visited[position] += 1
    for direction in s:
        x, y = position
        dx, dy = pos_change[direction]
        position = (x + dx, y + dy)
        visited[position] += 1

    counts = Counter(visited)

    return len(counts)


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
            ('^>v<', 4),
            ('^>v<^>v<', 4),
            ('^v^v^v^v^v', 2),
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
