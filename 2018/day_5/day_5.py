#!/usr/bin/env python3
import re
from string import ascii_letters, ascii_lowercase


def react_re(polymer, ignored_unit):
    """Naive solution using regexes.

    Terrible performance since it has to do many passes over the string each time using the same
    regex to filter out reacting units:

    real    0m55.194s
    user    0m55.086s
    sys     0m0.012s
    """
    reactive_unit_pairs = []
    for x, y in zip(ascii_letters[:26], ascii_letters[26:]):
        if x == ignored_unit:
            continue
        reactive_unit_pairs.append(x + y)
        reactive_unit_pairs.append(y + x)

    unit_re = re.compile('(' + '|'.join(reactive_unit_pairs) + ')')

    while True:
        old_len = len(polymer)
        polymer = unit_re.sub('', polymer)

        if old_len == len(polymer):
            break

    return polymer


def react_iter(polymer):
    """Single pass solution.

    Much faster than regex solution:

    real    0m0.031s
    user    0m0.023s
    sys     0m0.008s
    """
    reacted_polymer = ['']

    for unit in polymer:
        if unit == reacted_polymer[-1].swapcase():
            reacted_polymer.pop()
        else:
            reacted_polymer.append(unit)

    return ''.join(reacted_polymer)


with open('./input.txt') as input_file:
    polymer = input_file.read().strip()

reactions = {}
for removed_unit in ' ' + ascii_lowercase:
    polymer_to_react = polymer.replace(removed_unit, '').replace(removed_unit.upper(), '')

    reactions[removed_unit] = react_iter(polymer_to_react)
    # reactions[removed_unit] = react_re(polymer_to_react, removed_unit)

removed_unit, shortest_polymer = min(reactions.items(), key=lambda x: len(x[1]))

print(f'Part #1: Polymer length after all unit reactions is {len(reactions[" "])}')
print(f'Part #2: Shortest polymer after removing unit "{removed_unit}" has length '
      f'{len(shortest_polymer)}')