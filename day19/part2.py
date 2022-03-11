import argparse
import os.path
from random import shuffle

import pytest
from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')
# NOTE: paste test text here
INPUT_S_1 = """\
e => H
e => O
H => HO
H => OH
O => HH

HOH
"""
EXPECTED_1 = 3
INPUT_S_2 = """\
e => H
e => O
H => HO
H => OH
O => HH

HOHOHO
"""
EXPECTED_2 = 6


def compute(s: str) -> int:
    # FIXME: NOT MY SOLUTION
    # TODO: investigate

    repl_s, mol = s.split('\n\n')
    reps = [
        tuple(line.split(' => '))
        for line in repl_s.splitlines()
        ]

    target = mol.strip()
    steps = 0

    while target != 'e':
        tmp = target
        for a, b in reps:
            if b not in target:
                continue

            target = target.replace(b, a, 1)
            steps += 1

        if tmp == target:
            target = mol
            steps = 0
            shuffle(reps)

    return steps


@pytest.mark.solved
@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
            (INPUT_S_1, EXPECTED_1),
            (INPUT_S_2, EXPECTED_2),
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
