#!/usr/bin/env python3
import operator
import re
from collections import defaultdict

entry_re = re.compile(r'\[(?P<timestamp>[^\]]+)\] '
                      r'(?:(?P<wakes_up>wakes up)|'
                      r'(?P<falls_asleep>falls asleep)|'
                      r'(?:Guard #(?P<guard_id>\d+) .*))')
events = []

with open('./input.txt') as input_file:
    for line in input_file:
        events.append(entry_re.match(line).groupdict())

guard_sleepiness = defaultdict(list)
started_sleeping, current_guard_id = None, None

# This loop assumes entries start with a "Guard begins shift" entry, and all "falls asleep"
# entries are followed by "wakes up" entries.
for event in sorted(events, key=operator.itemgetter('timestamp')):
    if event['guard_id']:
        current_guard_id = int(event['guard_id'])

    else:
        minute = int(event['timestamp'].split(':')[1])

        if event['falls_asleep']:
            started_sleeping = minute

        elif event['wakes_up']:
            guard_sleepiness[current_guard_id].append((started_sleeping, minute))

guard_minute_counts = {}

# Create counters of all minutes asleep for each guard.
for guard_id, sleep_times in guard_sleepiness.items():
    minute_counter = defaultdict(int)
    for minute in range(60):
        for time in sleep_times:
            if time[0] <= minute <= time[1]:
                minute_counter[minute] += 1
        guard_minute_counts[guard_id] = minute_counter

sleepiest_guard, _ = max(guard_sleepiness.items(),
                         key=lambda times: sum(time[1] - time[0] for time in times[1]))
sleepiest_minute = max(guard_minute_counts[sleepiest_guard].items(), key=operator.itemgetter(1))[0]

print(f'Part #1: Sleepiest guard {sleepiest_guard} slept most in minute {sleepiest_minute}; '
      f'result is {sleepiest_guard * sleepiest_minute}')

most_asleep_minutes = []
for guard_id, minute_counter in guard_minute_counts.items():
    sleepiest_minute = max(minute_counter.items(), key=operator.itemgetter(1))
    most_asleep_minutes.append((guard_id, sleepiest_minute))

guard_id, most_asleep_minute = max(most_asleep_minutes, key=lambda x: x[1][1])

print(f'Part #2: Guard {guard_id} slept the most in minute {most_asleep_minute[0]}; '
      f'results is {guard_id * most_asleep_minute[0]}')
