import argparse
import os.path
from collections import defaultdict
from itertools import permutations
from itertools import repeat

import pytest
from more_itertools import sliding_window

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')
# NOTE: paste test text here
INPUT_S = """\
Alice would gain 54 happiness units by sitting next to Bob.
Alice would lose 79 happiness units by sitting next to Carol.
Alice would lose 2 happiness units by sitting next to David.
Bob would gain 83 happiness units by sitting next to Alice.
Bob would lose 7 happiness units by sitting next to Carol.
Bob would lose 63 happiness units by sitting next to David.
Carol would lose 62 happiness units by sitting next to Alice.
Carol would gain 60 happiness units by sitting next to Bob.
Carol would gain 55 happiness units by sitting next to David.
David would gain 46 happiness units by sitting next to Alice.
David would lose 7 happiness units by sitting next to Bob.
David would gain 41 happiness units by sitting next to Carol.
"""
EXPECTED = 330


def compute(s: str) -> int:
    people = defaultdict(dict)
    lines = s.splitlines()
    for line in lines:
        line = line.replace('.', '')
        line = line.replace('lose ', '-')
        line = line.replace('gain ', '')
        l = line.split()
        who, how_much, to_whom = l[0], l[2], l[-1]
        people[who][to_whom] = int(how_much)

    # add me, with relationship 0 to others, to the seating
    for relation in people.values():
        relation['me'] = 0
    people['me'] = dict(zip(people.keys(), repeat(0)))

    max_happiness = 0
    for seating in permutations(people.keys()):
        seating = list(seating)
        seating.extend(seating[0:2])  # make pairwise circular
        this_max = sum(
            people[person][left] + people[person][right]
            for left, person, right in sliding_window(seating, 3)
            )
        max_happiness = max(max_happiness, this_max)

    return max_happiness


@pytest.mark.skip  # no test input was provided for day13 part2
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
