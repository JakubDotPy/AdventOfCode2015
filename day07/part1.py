import argparse
import os.path
from operator import and_
from operator import inv
from operator import lshift
from operator import or_
from operator import rshift

import pytest
from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')
# NOTE: paste test text here
INPUT_S = """\
123 -> x
456 -> y
x AND y -> d
x OR y -> e
x LSHIFT 2 -> f
y RSHIFT 2 -> g
NOT x -> h
NOT y -> i
"""


def parse(s):
    wires = {}
    for row in s.splitlines():
        in_, out = row.split(' -> ')
        wires[out] = in_.split()
    return wires


def compute(s: str) -> int:
    wires = parse(s)

    def get_value(wire):
        operations = {
            'RSHIFT': rshift,
            'LSHIFT': lshift,
            'AND'   : and_,
            'OR'    : or_,
            'NOT'   : inv,
            }

        if isinstance(wire, int):
            return wire

        op = wires[wire]

        if isinstance(op, int):
            return op

        if len(op) == 1:
            try:
                return int(op[0])
            except ValueError:
                wires[wire] = get_value(op[0])
                return wires[wire]

        if len(op) == 2:
            wires[wire] = operations[op[0]](get_value(op[1])) & 0xFFFF
            return wires[wire]

        if len(op) == 3:

            if op[0].isnumeric():
                a = int(op[0])
            else:
                a = get_value(op[0])

            cmd = operations[op[1]]
            if cmd in (rshift, lshift):
                b = int(op[2])
            else:
                b = get_value(op[2])

            wires[wire] = cmd(a, b)
            return wires[wire]

    return get_value('a')


@pytest.mark.solved
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
