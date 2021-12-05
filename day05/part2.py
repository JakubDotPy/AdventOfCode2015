import argparse
import os.path
import re

import pytest
from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')
# NOTE: paste test text here
INPUT_S = """\
"""


class Word:

    def __init__(self, word):
        self.word = word

    @property
    def double_letter(self):
        pattern = re.compile(r'(\w{2}).*\1')
        return bool(re.findall(pattern, self.word))

    @property
    def letter_between(self):
        pattern = re.compile(r'(\w).\1')
        return bool(re.findall(pattern, self.word))

    @property
    def is_nice(self):
        return all((
            self.double_letter,
            self.letter_between,
            ))

    def __repr__(self):
        return f'Word({self.word})'


def compute(s: str) -> int:
    words = [Word(line) for line in s.splitlines()]
    return sum(w.is_nice for w in words)


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
            (INPUT_S, 0),
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
