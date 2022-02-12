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


def compute(s: str) -> int:
    return sum(map(int, re.findall(r'-?\d+', s.strip())))


@pytest.mark.solved
@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
            ('[1,2,3]', 6),
            ('{"a":2,"b":4}', 6),
            ('[[[3]]]', 3),
            ('{"a":{"b":4},"c":-1}', 3),
            ('[]', 0),
            ('[-1,{"a":1}]', 0),
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
