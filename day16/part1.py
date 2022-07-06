import argparse
import os.path
import re

import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')
# NOTE: paste test text here
INPUT_S = """\
"""
EXPECTED = 0


class Sue:
    def __init__(self, a_id):
        self.a_id = a_id

    def __str__(self):
        return f'Sue {self.a_id}'

    @property
    def prop_set(self):
        return set(
            (k, v) for k, v in self.__dict__.items()
            if k != 'a_id'
            )

    __repr__ = __str__


TICKER = {
    'children'   : 3,
    'cats'       : 7,
    'samoyeds'   : 2,
    'pomeranians': 3,
    'akitas'     : 0,
    'vizslas'    : 0,
    'goldfish'   : 5,
    'trees'      : 3,
    'cars'       : 2,
    'perfumes'   : 1,
    }

TICKER_SET = set(TICKER.items())


def compute(s: str) -> int:
    # parse lines
    lines = s.splitlines()

    pattern = r'(\w+): (\d+)'

    aunts = []
    for a_id, line in enumerate(lines, start=1):
        s = Sue(a_id)
        for name, count in re.findall(pattern, line):
            setattr(s, name, int(count))
        aunts.append(s)

    for sue in aunts:
        if sue.prop_set.issubset(TICKER_SET):
            return sue.a_id

    return 0


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
