import argparse
import json
import os.path

import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')
# NOTE: paste test text here
INPUT_S = """\
"""
EXPECTED = 0


def sum_no_red(obj):
    if isinstance(obj, int):
        return obj
    elif isinstance(obj, list):
        return sum(sum_no_red(x) for x in obj)
    elif isinstance(obj, dict):
        vals = obj.values()
        if "red" in vals:
            return 0
        else:
            return sum(sum_no_red(v) for v in vals)
    else:  # for None
        return 0


def compute(s: str) -> int:
    return sum_no_red(json.loads(s))


@pytest.mark.solved
@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
            ('[1,2,3]', 6),
            ('[1,{"c":"red","b":2},3]', 4),
            ('{"d":"red","e":[1,2,3,4],"f":5}', 0),
            ('[1,"red",5]', 6),
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
