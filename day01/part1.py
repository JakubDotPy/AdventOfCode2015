import argparse
import os.path
import re

import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')
# NOTE: paste test text here
INPUT_S = """\
"""


def compute(s: str) -> int:
    # parse numbers
    while '()' in s:
        s = re.sub(r'\(\)', '', s)

    return s.count('(') - s.count(')')


@pytest.mark.solved
@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
            ('(())', 0),
            ('()()', 0),
            ('))(((((', 3),
            ('())', -1),
            ('))(', -1),
            (')))', -3),
            (')))', -3),
            (')())())', -3),
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
