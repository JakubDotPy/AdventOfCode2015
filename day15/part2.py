import argparse
import os.path
import re
from dataclasses import dataclass
from functools import reduce
from itertools import combinations_with_replacement
from itertools import permutations
from operator import mul

import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')
# NOTE: paste test text here
INPUT_S = """\
Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8
Cinnamon: capacity 2, durability 3, flavor -2, texture -1, calories 3
"""
EXPECTED = 57600000


@dataclass
class Ingredient:
    name: str
    capacity: int
    durability: int
    flavor: int
    texture: int
    calories: int
    ratio: int = 0


def ratios_gen(num):
    # TODO: optimize this...
    for c in combinations_with_replacement(range(1, 100), num):
        if sum(c) == 100:
            yield from permutations(c)


def compute(s: str) -> int:
    pattern = r'(^\w+|-?\d+)'
    ingredients = []
    for line in s.splitlines():
        name, *properties = re.findall(pattern, line)
        ingredients.append(
            Ingredient(name, *map(int, properties))
            )

    props = [
        'capacity',
        'durability',
        'flavor',
        'texture',
        'calories',
        ]

    max_score = 0
    rg = ratios_gen(len(ingredients))

    for ratios in rg:
        # attach ratios
        for ing, ratio_amt in zip(ingredients, ratios):
            ing.ratio = ratio_amt

        prop_scores = []
        for prop in props:
            prop_score = sum(
                ing.ratio * getattr(ing, prop)
                for ing in ingredients
                )
            prop_scores.append(max(0, prop_score))
        if prop_scores[-1] == 500:
            new_score = reduce(mul, prop_scores[:-1])
            max_score = max(max_score, new_score)

    return max_score


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
