#!/usr/bin/env python3
from collections import defaultdict


def manhattan_distance(a, b):
    """Compute Manhattan distance between points 'a' and point 'b'."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


with open('./input.txt') as input_file:
    coordinates = []
    for line in input_file:
        x, y = line.strip().split(', ')
        coordinates.append((int(x), int(y)))

x_coordinates = [x for x, y in coordinates]
max_x, min_x = max(x_coordinates), min(x_coordinates)

y_coordinates = [y for x, y in coordinates]
max_y, min_y = max(y_coordinates), min(y_coordinates)

coordinate_counts = defaultdict(int)
infinite_coordinates = set()
safe_coordinates_count = 0

# Walk through the entire grid as defined by the border coordinates.
for y in range(min_y, max_y + 1):
    for x in range(min_x, max_x + 1):

        # Compute distances from the current coordinate (x, y) to every other coordinate from our
        # input. Save both the distance and the coordinate to which this distance belong. When
        # sorting a list of tuples, the default key sorts by the first element (distance here).
        distances = sorted((manhattan_distance((x, y), (coor_x, coor_y)), (coor_x, coor_y))
                           for coor_x, coor_y in coordinates)

        # If the sum of all distances from this coordinate is less than 10,000, count this
        # coordinate as a safe one.
        if sum(dist[0] for dist in distances) < 10_000:
            safe_coordinates_count += 1

        # If the first two closest distances to this point match, we can ignore this coordinate
        # as being equally far from two (or more) coordinates from our input.
        if distances[0][0] == distances[1][0]:
            continue

        # The closest coordinate from our input is the one with the shortest distance.
        closest_location = distances[0][1]

        # Bump the count of coordinates that are reachable from this input coordinate.
        coordinate_counts[closest_location] += 1

        # If we're at the border, note it as an infinitely expanding coordinate.
        if y == min_y or y == max_y or x == min_x or x == max_x:
            infinite_coordinates.add(closest_location)

# Remove all infinitely expanding coordinates
for coor in infinite_coordinates:
    coordinate_counts.pop(coor)

print(f'Part #1: the size of the largest area is {max(coordinate_counts.values())}')
print(f'Part #2: the size of the area with safe coordinates is {safe_coordinates_count}')