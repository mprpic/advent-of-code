#!/usr/bin/env python3
import re
from collections import defaultdict
from dataclasses import dataclass


@dataclass
class Claim:
    id: str
    offset_left: int
    offset_top: int
    width: int
    height: int

    def claimed_positions(self):
        # Can also use itertools.product() on both ranges but looks less readable.
        for x in range(self.offset_left, self.width + self.offset_left):
            for y in range(self.offset_top, self.height + self.offset_top):
                yield (x, y)


def print_fabric(fabric):
    """Helper function to print fabrics with 9 or less claims. Does not print leftover areas."""
    height = max(claim[0] for claim in fabric.keys())
    width = max(claim[1] for claim in fabric.keys())

    for y in range(height + 1):
        for x in range(width + 1):
            claims = fabric.get((x, y))
            if not claims:
                print('.', end='')
            elif len(claims) > 1:
                print('X', end='')
            else:
                print(claims[0], end='')
        print()


claims = []

with open('./input.txt') as input_file:
    for line in input_file:
        # Process e.g. #1 @ 896,863: 29x19
        values = map(int, re.findall(r'\d+', line))
        claims.append(Claim(*values))

fabric = defaultdict(list)

for claim in claims:
    for position in claim.claimed_positions():
        fabric[position].append(claim.id)

overlapping_positions = sum(len(claim) > 1 for claim in fabric.values())

non_overlapping_claim = None
for claim in claims:
    if non_overlapping_claim:
        break

    for position in claim.claimed_positions():
        if len(fabric.get(position, [])) > 1:
            break
    else:
        non_overlapping_claim = claim

print(f'Part #1: number of overlapping positions (two or more claims) is {overlapping_positions}\n'
      f'Part #2: the only non-overlapping claim is #{non_overlapping_claim.id}')
