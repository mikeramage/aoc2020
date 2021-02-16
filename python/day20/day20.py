from enum import Enum
import re
import itertools
import math
FILE = "day20_input.txt"

id_regex = re.compile("^Tile (?P<id>\d+):$")

class SquareGrid:
    def __init__(self, length):
        self.length = length

        #(x, y) tuple to tile object
        self.contents = dict()

        #tile Id to (x, y) tuple
        self.tile_locations = dict()
        for x in range(length):
            for y in range(length):
                self.contents[(x, y)] = None

    def add_tile(self, tile, x, y):
        self.contents[(x, y)] = tile

class Orientation(Enum):
    S = 0
    #R is rotation to right
    R1 = 1
    R2 = 2
    R3 = 3
    #F flips standard left to right
    FS = 4
    #Flip first, then rotate right
    FR1 = 5
    FR2 = 6
    FR3 = 7

class Edge(Enum):
    T = 0
    R = 1
    B = 3
    L = 4

class Tile:
    def __init__(self, id, representation):
        self.id = id
        self.full_representation = representation
        self.orientation = Orientation.S
        #TODO calculate the following from the representation
        #in standard orientation top edge read from left to right
        self.top_edge = self.full_representation[0]
        #right edge read from top to bottom
        self.right_edge = ''.join([line[-1] for line in self.full_representation])
        #bottom edge read from right to left
        self.bottom_edge = ''.join(reversed(self.full_representation[-1]))
        #left edge read from bottom to top
        self.left_edge = ''.join(reversed([line[0] for line in self.full_representation]))
        #Store the backwards strings too as optimization
        self.top_edge_back = ''.join(reversed(self.top_edge))
        self.right_edge_back =''.join(reversed(self.right_edge))
        self.bottom_edge_back = ''.join(reversed(self.bottom_edge))
        self.left_edge_back = ''.join(reversed(self.left_edge))

    def top(self):
        if self.orientation == Orientation.S:
            return self.top_edge
        if self.orientation == Orientation.R1:
            return self.left_edge
        if self.orientation == Orientation.R2:
            return self.bottom_edge
        if self.orientation == Orientation.R3:
            return self.right_edge
        if self.orientation == Orientation.FS:
            return self.top_edge_back
        if self.orientation == Orientation.FR1:
            return self.right_edge_back
        if self.orientation == Orientation.FR2:
            return self.bottom_edge_back
        if self.orientation == Orientation.FR3:
            return self.left_edge_back

    def left(self):
        if self.orientation == Orientation.S:
            return self.left_edge
        if self.orientation == Orientation.R1:
            return self.bottom_edge
        if self.orientation == Orientation.R2:
            return self.right_edge
        if self.orientation == Orientation.R3:
            return self.top_edge
        if self.orientation == Orientation.FS:
            return self.right_edge_back
        if self.orientation == Orientation.FR1:
            return self.bottom_edge_back
        if self.orientation == Orientation.FR2:
            return self.left_edge_back
        if self.orientation == Orientation.FR3:
            return self.top_edge_back

    def bottom(self):
        if self.orientation == Orientation.S:
            return self.bottom_edge
        if self.orientation == Orientation.R1:
            return self.right_edge
        if self.orientation == Orientation.R2:
            return self.top_edge
        if self.orientation == Orientation.R3:
            return self.left_edge
        if self.orientation == Orientation.FS:
            return self.bottom_edge_back
        if self.orientation == Orientation.FR1:
            return self.left_edge_back
        if self.orientation == Orientation.FR2:
            return self.top_edge_back
        if self.orientation == Orientation.FR3:
            return self.right_edge_back

    def right(self):
        if self.orientation == Orientation.S:
            return self.right_edge
        if self.orientation == Orientation.R1:
            return self.top_edge
        if self.orientation == Orientation.R2:
            return self.left_edge
        if self.orientation == Orientation.R3:
            return self.bottom_edge
        if self.orientation == Orientation.FS:
            return self.right_edge_back
        if self.orientation == Orientation.FR1:
            return self.bottom_edge_back
        if self.orientation == Orientation.FR2:
            return self.left_edge_back
        if self.orientation == Orientation.FR3:
            return self.top_edge_back

    def set_orientation(self, orientation):
        self.orientation = orientation


def read_file(filename):
    tiles = list()
    with open(filename, 'r') as f:
        tile_id = 0
        representation = list()
        for l in f:
            id_match = re.match(id_regex, l.strip())
            if id_match is not None:
                tile_id = int(id_match.group('id'))
            elif l.strip() == "":
                tiles.append(Tile(tile_id, representation))
                representation = list()
            else:
                representation.append(l.strip())
    return tiles

orientations = (Orientation.S,
                Orientation.R1,
                Orientation.R2,
                Orientation.R3,
                Orientation.FS,
                Orientation.FR1,
                Orientation.FR2,
                Orientation.FR3)
tiles = read_file(FILE)
print(f"{len(tiles)}")
for tile in tiles:
    print(f"Tile, id: {tile.id}: {tile.full_representation}")

#Find all matching edges.
all_two_tile_combos = itertools.combinations(tiles, 2)
print(f"{len(list(all_two_tile_combos))}")

all_matches = dict()
for combo in itertools.combinations(tiles, 2):
    matches = list()
    for orientation in orientations:
        combo[1].set_orientation(orientation)
        if combo[0].top() == combo[1].bottom():
            matches.append((Edge.T, orientation))
        if combo[0].right() == combo[1].left():
            matches.append((Edge.R, orientation))
        if combo[0].bottom() == combo[1].top():
            matches.append((Edge.B, orientation))
        if combo[0].left() == combo[1].right():
            matches.append((Edge.L, orientation))
    #Must remember to reset orientation!
    combo[1].set_orientation(Orientation.S)
    if len(matches) > 0:
        all_matches[(combo[0].id, combo[1].id)] = matches

counts = dict()
for tile in tiles:
    for keys in all_matches.keys():
        if tile.id in keys:
            if tile.id in counts.keys():
                counts[tile.id] += 1
            else:
                counts[tile.id] = 1
product = 1
corner_ids = set()
edge_ids = set()
middle_ids = set()
for tileid, count in counts.items():
    if count == 2:
        corner_ids.add(tileid)
        product *= tileid
    if count == 3:
        edge_ids.add(tileid)
    if count == 4:
        middle_ids.add(tileid)

print(f"Part 1 answer: {product}")

for key, match in all_matches.items():
    for tileid in corner_ids:
        if tileid in key:
            print(f"{tileid} {key} {match}")

grid = SquareGrid(int(math.sqrt(len(tiles))))
assert math.sqrt(len(tiles)) == 12

def flip_edge(edge):
    if edge == Edge.T:
        return Edge.B
    if edge == Edge.B:
        return Edge.T
    if edge == Edge.R:
        return Edge.L
    if edge == Edge.L:
        return Edge.R

def flip_orientation(orientation):
    if orientation == Orientation.S:
        return Orientation.S
    if orientation == Orientation.R1:
        return Orientation.R3
    if orientation == Orientation.R2:
        return Orientation.R2
    if orientation == Orientation.R3:
        return Orientation.R1
    if orientation == Orientation.FS:
        return Orientation.FS
    if orientation == Orientation.FR1:
        return Orientation.FR1
    if orientation == Orientation.FR2:
        return Orientation.FR2
    if orientation == Orientation.FR3:
        return Orientation.FR3

def apply_orientation_to_edge(orientation, edge):
    if edge == Edge.T:
        if orientation == Orientation.S:
            return Edge.T
        if orientation == Orientation.R1:
            return Edge.R
        if orientation == Orientation.R2:
            return Edge.B
        if orientation == Orientation.R3:
            return Edge.L
        if orientation == Orientation.FS:
            return Edge.T
        if orientation == Orientation.FR1:
            return Edge.R
        if orientation == Orientation.FR2:
            return Edge.B
        if orientation == Orientation.FR3:
            return Edge.L
    if edge == Edge.R:
        if orientation == Orientation.S:
            return Edge.R
        if orientation == Orientation.R1:
            return Edge.B
        if orientation == Orientation.R2:
            return Edge.L
        if orientation == Orientation.R3:
            return Edge.T
        if orientation == Orientation.FS:
            return Edge.L
        if orientation == Orientation.FR1:
            return Edge.T
        if orientation == Orientation.FR2:
            return Edge.R
        if orientation == Orientation.FR3:
            return Edge.B
    if edge == Edge.B:
        if orientation == Orientation.S:
            return Edge.B
        if orientation == Orientation.R1:
            return Edge.L
        if orientation == Orientation.R2:
            return Edge.T
        if orientation == Orientation.R3:
            return Edge.R
        if orientation == Orientation.FS:
            return Edge.B
        if orientation == Orientation.FR1:
            return Edge.L
        if orientation == Orientation.FR2:
            return Edge.T
        if orientation == Orientation.FR3:
            return Edge.R
    if edge == Edge.L:
        if orientation == Orientation.S:
            return Edge.L
        if orientation == Orientation.R1:
            return Edge.T
        if orientation == Orientation.R2:
            return Edge.R
        if orientation == Orientation.R3:
            return Edge.B
        if orientation == Orientation.FS:
            return Edge.R
        if orientation == Orientation.FR1:
            return Edge.B
        if orientation == Orientation.FR2:
            return Edge.L
        if orientation == Orientation.FR3:
            return Edge.T

def apply_orientation_to_orientation(orientation, orientation2):
    if orientation == Orientation.S:
        if orientation2 == Orientation.S:
            return Orientation.S
        if orientation2 == Orientation.R1:
            return Orientation.R1
        if orientation2 == Orientation.R2:
            return Orientation.R2
        if orientation2 == Orientation.R3:
            return Orientation.R3
        if orientation2 == Orientation.FS:
            return Orientation.FS
        if orientation2 == Orientation.FR1:
            return Orientation.FR1
        if orientation2 == Orientation.FR2:
            return Orientation.FR2
        if orientation2 == Orientation.FR3:
            return Orientation.FR3
    if orientation == Orientation.R1:
        if orientation2 == Orientation.S:
            return Orientation.R1
        if orientation2 == Orientation.R1:
            return Orientation.R2
        if orientation2 == Orientation.R2:
            return Orientation.R3
        if orientation2 == Orientation.R3:
            return Orientation.S
        if orientation2 == Orientation.FS:
            return Orientation.FR3
        if orientation2 == Orientation.FR1:
            return Orientation.FS
        if orientation2 == Orientation.FR2:
            return Orientation.FR1
        if orientation2 == Orientation.FR3:
            return Orientation.FR2
    if orientation == Orientation.R2:
        if orientation2 == Orientation.S:
            return Orientation.R2
        if orientation2 == Orientation.R1:
            return Orientation.R3
        if orientation2 == Orientation.R2:
            return Orientation.S
        if orientation2 == Orientation.R3:
            return Orientation.R1
        if orientation2 == Orientation.FS:
            return Orientation.FR2
        if orientation2 == Orientation.FR1:
            return Orientation.FR3
        if orientation2 == Orientation.FR2:
            return Orientation.FS
        if orientation2 == Orientation.FR3:
            return Orientation.FR1
    if orientation == Orientation.R3:
        if orientation2 == Orientation.S:
            return Orientation.R3
        if orientation2 == Orientation.R1:
            return Orientation.S
        if orientation2 == Orientation.R2:
            return Orientation.R1
        if orientation2 == Orientation.R3:
            return Orientation.R2
        if orientation2 == Orientation.FS:
            return Orientation.FR1
        if orientation2 == Orientation.FR1:
            return Orientation.FR2
        if orientation2 == Orientation.FR2:
            return Orientation.FR3
        if orientation2 == Orientation.FR3:
            return Orientation.FS
    if orientation == Orientation.FS:
        if orientation2 == Orientation.S:
            return Orientation.FS
        if orientation2 == Orientation.R1:
            return Orientation.FR3
        if orientation2 == Orientation.R2:
            return Orientation.FR2
        if orientation2 == Orientation.R3:
            return Orientation.FR1
        if orientation2 == Orientation.FS:
            return Orientation.S
        if orientation2 == Orientation.FR1:
            return Orientation.R1
        if orientation2 == Orientation.FR2:
            return Orientation.R2
        if orientation2 == Orientation.FR3:
            return Orientation.R3
    if orientation == Orientation.FR1:
        if orientation2 == Orientation.S:
            return Orientation.FR1
        if orientation2 == Orientation.R1:
            return Orientation.FR2
        if orientation2 == Orientation.R2:
            return Orientation.FR3
        if orientation2 == Orientation.R3:
            return Orientation.FS
        if orientation2 == Orientation.FS:
            return Orientation.R3
        if orientation2 == Orientation.FR1:
            return Orientation.S
        if orientation2 == Orientation.FR2:
            return Orientation.R1
        if orientation2 == Orientation.FR3:
            return Orientation.R2
    if orientation == Orientation.FR2:
        if orientation2 == Orientation.S:
            return Orientation.FR2
        if orientation2 == Orientation.R1:
            return Orientation.FR3
        if orientation2 == Orientation.R2:
            return Orientation.FS
        if orientation2 == Orientation.R3:
            return Orientation.FR1
        if orientation2 == Orientation.FS:
            return Orientation.R2
        if orientation2 == Orientation.FR1:
            return Orientation.R3
        if orientation2 == Orientation.FR2:
            return Orientation.S
        if orientation2 == Orientation.FR3:
            return Orientation.R1
    if orientation == Orientation.FR3:
        if orientation2 == Orientation.S:
            return Orientation.FR3
        if orientation2 == Orientation.R1:
            return Orientation.FS
        if orientation2 == Orientation.R2:
            return Orientation.FR1
        if orientation2 == Orientation.R3:
            return Orientation.FR2
        if orientation2 == Orientation.FS:
            return Orientation.R1
        if orientation2 == Orientation.FR1:
            return Orientation.R2
        if orientation2 == Orientation.FR2:
            return Orientation.R3
        if orientation2 == Orientation.FR3:
            return Orientation.S

def flip_match(match):
    flipped_edge = flip_edge(match[0])
    flipped_orientation = flip_orientation(match[1])
    flipped_edge = apply_orientation_to_edge(flipped_orientation, flipped_edge)
    return (flipped_edge, flipped_orientation)

corner_matches = dict()
edge_matches = dict()
middle_matches = dict()

for corner_id in corner_ids:
    corner_matches[corner_id] = list()
    for key, value in all_matches.items():
        if corner_id == key[0]:
            corner_matches[corner_id].append((key[1], value[0]))
        elif corner_id == key[1]:
            corner_matches[corner_id].append((key[0], [flip_match(match) for match in value][0]))

for edge_id in edge_ids:
    edge_matches[edge_id] = list()
    for key, value in all_matches.items():
        if edge_id == key[0]:
            edge_matches[edge_id].append((key[1], value[0]))
        elif edge_id == key[1]:
            edge_matches[edge_id].append((key[0], [flip_match(match) for match in value][0]))

for middle_id in middle_ids:
    middle_matches[middle_id] = list()
    for key, value in all_matches.items():
        if middle_id == key[0]:
            middle_matches[middle_id].append((key[1], value[0]))
        elif middle_id == key[1]:
            middle_matches[middle_id].append((key[0], [flip_match(match) for match in value][0]))

print(f"Corners: {corner_matches}")
print(f"Edges: {edge_matches.keys()}")
print(f"Middles: {middle_matches.keys()}")

tiles_dict = dict()
for tile in tiles:
    tiles_dict[tile.id] = tile

fixed_tiles = set()
grid.add_tile(tiles_dict[3931], 0, 0)
fixed_tiles.add(3931)
first_matches = corner_matches[3931]
print(f"{first_matches}")
next_tile_id = None
next_tile_orientation = Orientation.S
for edge in first_matches:
    if edge[1][0] == Edge.R:
        next_tile_id = edge[0]
        next_tile_orientation = edge[1][1]
        break
x = 1
y = 0
while True:
    next_tile = tiles_dict[next_tile_id]
    next_tile.set_orientation(next_orientation)
    grid.add_tile(next_tile, x, y)
    fixed_tiles.add(next_tile_id)
    matches = edge_matches[next_tile_id]





while True:








