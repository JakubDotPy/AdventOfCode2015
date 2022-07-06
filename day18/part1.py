import argparse
import os.path
from itertools import product

import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')
# NOTE: paste test text here
INPUT_S = """\
.#.#.#
...##.
#....#
..#...
#.#..#
####..
"""
EXPECTED = 4


def get_surround_num(pos, grid):
    coords_diffs = product((-1, 0, 1), (-1, 0, 1))
    x, y = pos
    surround = (
        grid.get((x + dx, y + dy), '.')
        for dx, dy in coords_diffs
        if (dx, dy) != (0, 0)
        )
    return sum(c == '#' for c in surround)


def get_new(pos, grid):
    num_surr = get_surround_num(pos, grid)
    this_char = grid[pos]
    if this_char == '#':
        return '#' if num_surr in (2, 3) else '.'
    else:
        return '#' if num_surr == 3 else '.'


def draw_grid(grid):
    for y in range(6):
        for x in range(6):
            print(grid[(x, y)], end='')
        print()
    print('-' * 10)


def compute(s: str, steps: int) -> int:
    grid = {
        (x, y): c
        for y, row in enumerate(s.splitlines())
        for x, c in enumerate(row)
        }

    for _ in range(steps):
        # draw_grid(grid)
        new_grid = {}
        for pos in grid.keys():
            new_grid[pos] = get_new(pos, grid)
        grid = new_grid

    return sum(c == '#' for c in grid.values())


@pytest.mark.parametrize(
    ('input_s', 'steps', 'expected'),
    (
            (INPUT_S, 4, EXPECTED),
            ),
    )
def test(input_s: str, steps: int, expected: int) -> None:
    assert compute(input_s, steps) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, timing():
        print(compute(f.read(), 100))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
