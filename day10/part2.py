import argparse
import os.path
from itertools import chain
from itertools import groupby

import pytest
from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')
# NOTE: paste test text here
INPUT_S = """\
1
"""
EXPECTED = 6


def expand(num):
    num_s = str(num)
    nums = [(str(sum(1 for _ in g)), k) for k, g in groupby(num_s)]
    return ''.join(chain.from_iterable(nums))


def compute(s: str) -> int:
    s = s.strip()
    for _ in range(50):
        s = expand(s)
    return len(s)


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
