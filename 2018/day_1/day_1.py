#!/usr/bin/env python3
import itertools


with open('./input.txt') as input_file:
    freq_changes = list(map(int, input_file.readlines()))

frequency = 0
seen_freqs = {0}
num_of_changes = len(freq_changes)

repeated_freq = None
final_freq = None

# Keep looping over frequency changes but ensure we loop over all of them at least once.
for idx, change in enumerate(itertools.cycle(freq_changes)):
    frequency += change

    if idx == num_of_changes - 1:
        final_freq = frequency

    if frequency in seen_freqs and not repeated_freq:
        repeated_freq = frequency
        if idx > num_of_changes:
            break
    else:
        seen_freqs.add(frequency)


print(f'Part #1: resulting frequency is {final_freq}\n'
      f'Part #2: first frequency reached twice is {repeated_freq}')