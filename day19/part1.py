import argparse
import os.path
import re
from collections import defaultdict
from itertools import product

import pytest
from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')
# NOTE: paste test text here
INPUT_S_1 = """\
H => HO
H => OH
O => HH

HOH
"""
EXPECTED_1 = 4
INPUT_S_2 = """\
H => HO
H => OH
O => HH

HOHOHO
"""
EXPECTED_2 = 7


def parse(s):
    replacements_s, molecule = s.split('\n\n')
    replacements = defaultdict(list)
    for line in replacements_s.splitlines():
        from_, to = line.split(' => ')
        replacements[from_].append(to)
    return replacements, molecule.strip()


def sub_in_str(string, span, sub):
    pos, endpos = span
    return string[:pos] + sub + string[endpos:]


def get_all_replaced_strings(string, matches, to_list):
    yield from (
        sub_in_str(string, m.span(), sub)
        for m, sub in product(matches, to_list)
        )


def compute(s: str) -> int:
    replacements, molecule = parse(s)

    results = set()
    for from_, to_list in replacements.items():
        matches = re.finditer(from_, molecule)
        results.update(get_all_replaced_strings(molecule, matches, to_list))

    return len(results)


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
