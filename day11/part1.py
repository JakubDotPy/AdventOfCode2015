import argparse
import collections
import os.path
import re
from itertools import islice

import pytest
from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')
# NOTE: paste test text here
INPUT_S = """\
"""
EXPECTED = 0


def next_password(s):
    """Increment a string"""
    if s[-1] == "z":
        return next_password(s[:-1]) + "a"
    else:
        return s[:-1] + chr(ord(s[-1]) + 1)


def sliding_window(iterable, n):
    # sliding_window('ABCDEFG', 4) -> ABCD BCDE CDEF DEFG
    it = iter(iterable)
    window = collections.deque(islice(it, n), maxlen=n)
    if len(window) == n:
        yield tuple(window)
    for x in it:
        window.append(x)
        yield tuple(window)


def has_two_pairs(password):
    return len(re.findall(r'(\w)\1', password)) >= 2


def has_consecutive_triple(password):
    def is_consecutive(triplet):
        a, b, c = triplet
        return ord(a) + 2 == ord(b) + 1 == ord(c)

    return any(
        is_consecutive(triplet)
        for triplet in sliding_window(password, 3)
        )


def has_blacklist_char(password):
    char_blacklist = 'ilo'
    return any(c in password for c in char_blacklist)


def is_valid(password):
    return all((
        not (has_blacklist_char(password)),
        has_two_pairs(password),
        has_consecutive_triple(password),
        ))


def compute(s: str) -> int:
    s = s.strip()
    password = next_password(s)
    while not is_valid(password):
        password = next_password(password)

    return password


@pytest.mark.complete
@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
            ('abcdefgh', 'abcdffaa'),
            ('ghijklmn', 'ghjaabcc'),
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
