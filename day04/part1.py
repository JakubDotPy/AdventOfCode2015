import argparse
import hashlib
import itertools
import os.path

import pytest
from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')
# NOTE: paste test text here
INPUT_S = """\
"""


def compute(s: str) -> int:
    numbers = itertools.count(start=1)

    while True:
        num = next(numbers)
        md5 = hashlib.md5(f'{s}{num}'.encode('utf-8')).hexdigest()
        if md5.startswith('00000'):
            return num


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
            ('abcdef', 609043),
            ('pqrstuv', 1048970),
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
