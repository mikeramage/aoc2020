from enum import Enum
import re
import itertools
import math
from functools import reduce
import numpy as np
import sys

FILE = "day20_input.txt"
GRID_SIZE = 12
HASH = "#"
DOT = "."
np.set_printoptions(threshold=sys.maxsize)

id_regex = re.compile("^Tile (?P<id>\d+):$")


class Orientation(Enum):
    I = 0
    # R is anticlockwise rotation
    R1 = 1
    R2 = 2
    R3 = 3
    # F flips I left to right
    F = 4
    # Flip first, then rotate anticlockwise
    FR1 = 5
    FR2 = 6
    FR3 = 7


class Edge(Enum):
    T = 0
    R = 1
    B = 3
    L = 4


class Tile:
    def __init__(self, id, pixels):
        self._id = id
        # ----------------------------------------------------------------------
        # pre-calculate all possible rotations.  Note - these are counter-
        # clockwise rotations and a flip about the L/R axis
        # ----------------------------------------------------------------------
        self._I = pixels
        self._orientation = Orientation.I
        self._R1 = np.rot90(self._I)
        self._R2 = np.rot90(self._R1)
        self._R3 = np.rot90(self._R2)
        self._F = np.fliplr(self._I)
        self._FR1 = np.rot90(self._F)
        self._FR2 = np.rot90(self._FR1)
        self._FR3 = np.rot90(self._FR2)

    def __repr__(self):
        return f"\nID: {self._id}\nRepresentation:\n{self.pixels()}"

    @property
    def I(self):
        return self._I

    @property
    def R1(self):
        return self._R1

    @property
    def R2(self):
        return self._R2

    @property
    def R3(self):
        return self._R3

    @property
    def F(self):
        return self._F

    @property
    def FR1(self):
        return self._FR1

    @property
    def FR2(self):
        return self._FR2

    @property
    def FR3(self):
        return self._FR3

    @property
    def id(self):
        return self._id

    @property
    def orientation(self):
        return self._orientation

    def set_orientation(self, orientation):
        self._orientation = orientation

    def get_all_orientations(self):
        return [
            self._I,
            self._R1,
            self._R2,
            self._R3,
            self._F,
            self._FR1,
            self._FR2,
            self._FR3,
        ]

    def pixels(self):
        if self._orientation == Orientation.I:
            return self._I
        elif self._orientation == Orientation.R1:
            return self._R1
        elif self._orientation == Orientation.R2:
            return self._R2
        elif self._orientation == Orientation.R3:
            return self._R3
        elif self._orientation == Orientation.F:
            return self._F
        elif self._orientation == Orientation.FR1:
            return self._FR1
        elif self._orientation == Orientation.FR2:
            return self._FR2
        elif self._orientation == Orientation.FR3:
            return self._FR3

    # This is just for exploration purposes
    def count_matching_edges(A, B):
        count = 0

        # Remember - only need to rotate one tile or we'll get double counting!
        # But also remember - test all sides of A
        for orient_b in B.get_all_orientations():
            # Test upper edge of A against bottom of B, all rotations of B
            if np.array_equal(A.I[0, :], orient_b[orient_b.shape[0] - 1, :]):
                count += 1

            # Test right edge of A against left of B, all rotations of B
            if np.array_equal(A.I[:, A.I.shape[1] - 1], orient_b[:, 0]):
                count += 1

            # Test bottom edge of A against top of B, all rotations of B
            if np.array_equal(A.I[A.I.shape[0] - 1, :], orient_b[0, :]):
                count += 1

            # Test left edge of A against right of B, all rotations of B
            if np.array_equal(A.I[:, 0], orient_b[:, orient_b.shape[1] - 1]):
                count += 1

        return count


def read_input(filename):
    tiles = dict()
    with open(filename, "r") as f:
        tile_id = 0
        pixel_array = list()
        for l in f:
            id_match = re.match(id_regex, l.strip())
            if id_match is not None:
                tile_id = int(id_match.group("id"))
            elif l.strip() == "":
                tiles[tile_id] = Tile(tile_id, np.array(pixel_array, dtype=np.int64))
                pixel_array = list()
            else:
                # append the row of pixels
                pixel_row = list()
                for c in l.strip():
                    if c == HASH:
                        pixel_row.append(1)
                    elif c == DOT:
                        pixel_row.append(0)
                    else:
                        raise Exception(f"Unrecognized character: {c}")
                pixel_array.append(pixel_row)
    return tiles


# finds all the matching pairs
def find_matching_pairs(tiles):
    all_matches = dict()

    # Test all pairs of tiles to see if they have a matching edge.
    for combination in itertools.combinations(tiles, 2):
        # Remember - only need to rotate one tile or we'll get double counting!
        # But also remember - test all sides of A
        A = combination[0]
        B = combination[1]
        for orient_b in B.get_all_orientations():
            # Test edges of A against matching edge of B, all rotations of B
            # Respectively, top A, bottom B; right A, left B; bottom A, top B; left A, right B
            if (
                np.array_equal(A.I[0, :], orient_b[orient_b.shape[0] - 1, :])
                or np.array_equal(A.I[:, A.I.shape[1] - 1], orient_b[:, 0])
                or np.array_equal(A.I[A.I.shape[0] - 1, :], orient_b[0, :])
                or np.array_equal(A.I[:, 0], orient_b[:, orient_b.shape[1] - 1])
            ):
                # Add both A and B to the dictionary - don't know which we're going to want to look up.
                if A.id in all_matches.keys():
                    all_matches[A.id].append(B.id)
                else:
                    all_matches[A.id] = [B.id]

                if B.id in all_matches.keys():
                    all_matches[B.id].append(A.id)
                else:
                    all_matches[B.id] = [A.id]

    return all_matches


# ------------------------------------------------------------------------------
# This function and create_picture make use of the assumptions in the big
# comment below
# ------------------------------------------------------------------------------
def find_corner_tiles(matches):
    corners = list()
    for key in matches.keys():
        if len(matches[key]) == 2:
            corners.append(key)
    return corners


def create_picture(tiles, corners, matching_pairs):
    used_tiles = set()
    picture = list()

    # Just grab the first corner
    first_tile = tiles[corners[0]]
    picture.append([first_tile])

    # Get the orientation correct so that this is the top-left piece. That means
    # matching tiles must connect to the right and bottom edges of the first tile.
    connecting_tiles = [tiles[x] for x in matching_pairs[first_tile.id]]
    assert len(connecting_tiles) == 2
    all_rotations = [Orientation.I, Orientation.R1, Orientation.R2, Orientation.R3]
    for rotation in all_rotations:
        first_tile.set_orientation(rotation)
        right_match = None
        bottom_match = None

        for orientation in Orientation:
            connecting_tiles[0].set_orientation(orientation)
            # Check if top/left edge matches bottom/right edge of first tile
            if np.array_equal(
                first_tile.pixels()[:, first_tile.pixels().shape[1] - 1],
                connecting_tiles[0].pixels()[:, 0],
            ):
                right_match = connecting_tiles[0]
                break
            elif np.array_equal(
                first_tile.pixels()[first_tile.pixels().shape[0] - 1, :],
                connecting_tiles[0].pixels()[0, :],
            ):
                bottom_match = connecting_tiles[0]
                break

        if (right_match is not None) or (bottom_match is not None):
            for orientation in Orientation:
                connecting_tiles[1].set_orientation(orientation)
                if (bottom_match is not None) and np.array_equal(
                    first_tile.pixels()[:, first_tile.pixels().shape[1] - 1],
                    connecting_tiles[1].pixels()[:, 0],
                ):
                    right_match = connecting_tiles[1]
                    break
                elif (right_match is not None) and np.array_equal(
                    first_tile.pixels()[first_tile.pixels().shape[0] - 1, :],
                    connecting_tiles[1].pixels()[0, :],
                ):
                    bottom_match = connecting_tiles[1]
                    break

        if (right_match is not None) and (bottom_match is not None):
            picture[0].append(right_match)
            picture.append([bottom_match])
            used_tiles.add(right_match.id)
            used_tiles.add(bottom_match.id)
            used_tiles.add(first_tile.id)
            break

    # print(f"First tile: {first_tile.id}, {first_tile.orientation}\n{first_tile.pixels()}")
    # print(f"Bottom tile: {bottom_match.id}, {bottom_match.orientation}\n{bottom_match.pixels()}")
    # print(f"Right tile: {right_match.id}, {right_match.orientation}\n{right_match.pixels()}")
    # print(f"{picture}")

    # Phew - that's the first tile and its neighbours sorted. Now do the rest of the first row
    for col_ix in range(1, GRID_SIZE - 1):
        # print(f"Picture now: {picture}")
        # print(f"Column index {col_ix}")
        current_tile = picture[0][col_ix]
        # print(f"Current tile: {current_tile}")
        for tile_id in matching_pairs[current_tile.id]:
            # print(f"checking tile {tile_id}")
            if tile_id not in used_tiles:
                # print(f"not used this yet {tile_id}")
                tile = tiles[tile_id]
                for orientation in Orientation:
                    # Right/Left match only
                    # print(f"Checking orientation {orientation}")
                    tile.set_orientation(orientation)
                    if np.array_equal(
                        current_tile.pixels()[:, current_tile.pixels().shape[1] - 1],
                        tile.pixels()[:, 0],
                    ):
                        # Got match
                        # print(f"Matches")
                        picture[0].append(tile)
                        # print(f"Picture updated: {picture}\n\n")
                        used_tiles.add(tile.id)
                        break

    # And the rest (similar code to the above but can't be bothered to commonalize)
    for row_ix in range(1, GRID_SIZE):
        for col_ix in range(0, GRID_SIZE - 1):
            current_tile = picture[row_ix][col_ix]
            for tile_id in matching_pairs[current_tile.id]:
                if tile_id not in used_tiles:
                    tile = tiles[tile_id]
                    for orientation in Orientation:
                        # Right/Left match only
                        tile.set_orientation(orientation)
                        if np.array_equal(
                            current_tile.pixels()[
                                :, current_tile.pixels().shape[1] - 1
                            ],
                            tile.pixels()[:, 0],
                        ):
                            # Got match
                            picture[row_ix].append(tile)
                            used_tiles.add(tile.id)
                            break

        # End of the row - add one below unless it's the last row
        if row_ix != GRID_SIZE - 1:
            current_tile = picture[row_ix][0]
            for tile_id in matching_pairs[current_tile.id]:
                if tile_id not in used_tiles:
                    tile = tiles[tile_id]
                    for orientation in Orientation:
                        # Bottom/Top match only
                        tile.set_orientation(orientation)
                        if np.array_equal(
                            current_tile.pixels()[
                                current_tile.pixels().shape[1] - 1, :
                            ],
                            tile.pixels()[0, :],
                        ):
                            # Got match
                            picture.append([tile])
                            used_tiles.add(tile.id)
                            break

    # I think - fingers crossed, that's it. Now to strip out the excess bits and pieces.
    new_picture = None
    for row_ix in range(GRID_SIZE):
        this_row = None
        for col_ix in range(GRID_SIZE):
            if col_ix == 0:
                # First tile in row
                this_row = picture[row_ix][col_ix].pixels()[1:-1, 1:-1]
            else:
                this_row = np.hstack(
                    (this_row, picture[row_ix][col_ix].pixels()[1:-1, 1:-1])
                )
        if row_ix == 0:
            # First row in picture
            new_picture = this_row
        else:
            new_picture = np.vstack((new_picture, this_row))

    # print(f"Picture: {picture}")
    # print(f"New picture: {new_picture}")
    return new_picture


def count_sea_monsters(picture, sea_monster):
    size_picture = picture.pixels().shape[0]
    # print(f"{size_picture}")
    length_sea_monster = sea_monster.shape[1]
    height_sea_monster = sea_monster.shape[0]
    # print(f"l = {length_sea_monster}, h= {height_sea_monster}")
    count = 0
    for orientation in Orientation:
        picture.set_orientation(orientation)
        for row_ix in range(size_picture - height_sea_monster):
            for col_ix in range(size_picture - length_sea_monster):
                # print(f"{row_ix}, {col_ix}")
                # print(f"{picture.pixels()[row_ix:row_ix+height_sea_monster, col_ix:col_ix+length_sea_monster].shape}")
                if np.array_equal(
                    picture.pixels()[
                        row_ix : row_ix + height_sea_monster,
                        col_ix : col_ix + length_sea_monster,
                    ]
                    & sea_monster,
                    sea_monster,
                ):
                    count += 1
        if count > 0:
            # print(f"Orientation: {orientation}")
            break

    return count


tiles = read_input(FILE)

# ------------------------------------------------------------------------------
# The following code checks all possible combinations of 2 tiles and all
# possible edge matches for a given tile pair.  Result is there are loads of
# pairs with no edge matches, 264 with one edge match, and none with any more
# than one edge match 264 is 2*n*(n-1) for n=12, which is the number of unique
# internal matching edges in a 12x12 puzzle.  This means we can simplify a lot
# - the corners will be uniquely defined as those tiles only appearing in 2
# combinations, edges will appear in only 3, all others in 4.  All we need to
# do is just grab any old corner and stick it at 0,0 in the 12x12 grid, then
# just fill in the rest of the grid by brute force - we know we only have to
# check a single edge per tile and know the rest must match up if there's any
# solution to this problem.
# ------------------------------------------------------------------------------
# matches = dict()
# for combination in itertools.combinations(tiles, 2):
#     matches[(combination[0].id, combination[1].id)] = Tile.count_matching_edges(combination[0], combination[1])

# # print(matches)
# count0 = 0
# count1 = 0
# count2 = 0
# count3 = 0
# countother = 0
# for key in matches.keys():
#     if matches[key] == 0:
#         count0 += 1
#     elif matches[key] == 1:
#         count1 += 1
#     elif matches[key] == 2:
#         count2 += 1
#     elif matches[key] == 3:
#         count3 += 1
#     else:
#         countother += 1

# #Suggests there's a simple unique solution - edges, corners, others.
# print(f"0: {count0}\n1: {count1}\n2: {count2}\n3: {count3}\nother: {countother}")

# Let's get on with it!
matching_pairs = find_matching_pairs(tiles.values())
corners = find_corner_tiles(matching_pairs)
part1_answ = reduce(lambda x, y: x * y, corners)
print(f"{corners}, {part1_answ}")

# Part 2
picture = create_picture(tiles, corners, matching_pairs)
super_tile = Tile(1, picture)
sea_monster_strings = [
    "                  # ",
    "#    ##    ##    ###",
    " #  #  #  #  #  #   ",
]
sea_monster_array = list()
for line in sea_monster_strings:
    line_data = list()
    for c in line:
        if c == " ":
            line_data.append(0)
        elif c == HASH:
            line_data.append(1)
    sea_monster_array.append(line_data)

sea_monster = np.array(sea_monster_array)
num_hash_in_picture = np.sum(picture)
num_hash_in_sea_monster = np.sum(sea_monster)
num_sea_monsters_in_picture = count_sea_monsters(super_tile, sea_monster)
print(
    f"{num_hash_in_picture}, {num_hash_in_sea_monster}, {num_sea_monsters_in_picture}"
)
print(
    f"{num_hash_in_picture - (num_hash_in_sea_monster * num_sea_monsters_in_picture)}"
)
