#!/usr/bin/env python3
from collections import Counter


with open('./input.txt') as input_file:
    box_ids = input_file.read().split('\n')

two_count = 0
three_count = 0
correct_boxes = None

for box_id in box_ids:

    counts = Counter(box_id).values()

    two_count += 2 in counts
    three_count += 3 in counts

    # If we already found our matching boxes, continue to finish the checksum.
    if correct_boxes:
        continue

    # For a given box ID, compare it to all other IDs to find a matching one.
    # (This for-loop could be replaced by a clever use of `difflib`.)
    for other_box_id in box_ids:

        # Skip comparing the current box.
        if box_id == other_box_id:
            continue

        # If we found the correct box, skip comparing the rest of them.
        if correct_boxes:
            break

        mismatch_found = False
        for idx, char in enumerate(box_id):
            # Compare IDs character by character. If we find a mismatch, record it. If a mismatch
            # was found the second time, exit since two or more mismatches indicates non-matching
            # boxes.
            if char == other_box_id[idx]:
                continue
            else:
                if mismatch_found:
                    break
                else:
                    mismatch_found = True
        else:
            # If we looped through all characters and only found one mismatch (otherwise we would
            # have exited already. Record the two boxes as the correct ones.
            correct_boxes = (box_id, other_box_id)

mismatched_char = (set(correct_boxes[0]) - set(correct_boxes[1])).pop()
common_letters = ''.join(correct_boxes[0].split(mismatched_char))

print(f'Part #1: checksum of all box IDs is {two_count * three_count}.\n'
      f'Part #2: boxes "{correct_boxes[0]}" and "{correct_boxes[1]}" differ in letter '
      f'"{mismatched_char}" and have common letters "{common_letters}".')
