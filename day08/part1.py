import argparse
import os.path

import pytest
from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')
# NOTE: paste test text here
INPUT_S = r"""
""
"abc"
"aaa\"aaa"
"\x27"
"""


def compute(s: str) -> int:
    total_count = 0
    memory_count = 0

    # parse lines
    lines = s.splitlines()
    for line in lines:
        if not line:
            continue
        escaped = bytes(line, 'utf-8').decode('unicode_escape')
        total_count += len(line)
        memory_count += (len(escaped) - 2)

    return total_count - memory_count


@pytest.mark.solved
@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
            (INPUT_S, 12),
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
