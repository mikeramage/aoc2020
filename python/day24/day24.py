FILE = "day24_input.txt"

SE = "se"
SW = "sw"
NE = "ne"
NW = "nw"
E = "e"
W = "w"

BLACK = "Black"
WHITE = "White"


def parse_input(filename):
    instruction_set = []
    with open(filename, "r") as f:
        for line in f:
            instructions = []
            in_s = False
            in_n = False
            for char in line.strip():
                if char == "s":
                    assert not in_s
                    in_s = True
                elif char == "n":
                    assert not in_n
                    in_n = True
                elif char == "e":
                    if in_s:
                        assert not in_n
                        instructions.append(SE)
                        in_s = False
                    elif in_n:
                        assert not in_s
                        instructions.append(NE)
                        in_n = False
                    else:
                        assert not in_s
                        assert not in_n
                        instructions.append(E)
                elif char == "w":
                    if in_s:
                        assert not in_n
                        instructions.append(SW)
                        in_s = False
                    elif in_n:
                        assert not in_s
                        instructions.append(NW)
                        in_n = False
                    else:
                        assert not in_s
                        assert not in_n
                        instructions.append(W)
                else:
                    raise Exception(f"Bad character in input: {char}")
            instruction_set.append(instructions)
    return instruction_set


# Coordinate system is row (where 0 is center tile's row). Increases by 1 for ne, nw
# Decreases by 1 for se, sw, no change for e or w
# Column increases by 1 for ne or e, decreases for sw or w, no change for se or
# nw
# I think this is sufficient for uniquely labelling hex grid
def get_coords(instructions):
    row = 0
    col = 0
    for instruction in instructions:
        if instruction == E:
            col += 1
        elif instruction == W:
            col -= 1
        elif instruction == NW:
            row += 1
        elif instruction == SW:
            row -= 1
            col -= 1
        elif instruction == SE:
            row -= 1
        elif instruction == NE:
            row += 1
            col += 1
        else:
            raise Exception(f"Unrecognized instruction: {instruction}")
    return (row, col)


def flip_colour(colour):
    if colour == WHITE:
        return BLACK
    elif colour == BLACK:
        return WHITE
    raise Exception(f"Unrecognized colour: {colour}")


def do_initial_flips(instruction_set):
    flipped_tiles = dict()
    for instructions in instruction_set:
        tile = get_coords(instructions)
        if tile in flipped_tiles.keys():
            flipped_tiles[tile] = flip_colour(flipped_tiles[tile])
        else:
            flipped_tiles[tile] = BLACK
    return flipped_tiles


def get_limits_of_area_to_check(flipped_tiles):
    min_x = min([location[0] for location in flipped_tiles.keys()]) - 1
    max_x = max([location[0] for location in flipped_tiles.keys()]) + 1
    min_y = min([location[1] for location in flipped_tiles.keys()]) - 1
    max_y = max([location[1] for location in flipped_tiles.keys()]) + 1
    return (min_x, max_x, min_y, max_y)


def get_neighbour_coords(x, y):
    return [
        (x + 1, y + 1),
        (x - 1, y - 1),
        (x + 1, y),
        (x - 1, y),
        (x, y + 1),
        (x, y - 1),
    ]


def get_num_adjacent_blacks(x, y, flipped_tiles):
    count = 0
    neighbours = get_neighbour_coords(x, y)
    for neighbour in neighbours:
        if neighbour in flipped_tiles.keys():
            if flipped_tiles[neighbour] == BLACK:
                count += 1
    return count


def determine_tiles_to_flip(limits, flipped_tiles):
    tiles_to_flip = set()
    for x in range(limits[0], limits[1] + 1):
        for y in range(limits[2], limits[3] + 1):
            num_blacks = get_num_adjacent_blacks(x, y, flipped_tiles)
            current_colour = WHITE
            if (x, y) in flipped_tiles.keys():
                current_colour = flipped_tiles[(x, y)]
            if current_colour == BLACK and (num_blacks == 0 or num_blacks > 2):
                tiles_to_flip.add((x, y))
            elif current_colour == WHITE and num_blacks == 2:
                tiles_to_flip.add((x, y))
    return tiles_to_flip


def flip_tiles_in_place(flipped_tiles, tiles_to_flip):
    for tile in tiles_to_flip:
        if tile in flipped_tiles.keys():
            flipped_tiles[tile] = flip_colour(flipped_tiles[tile])
        else:
            flipped_tiles[tile] = BLACK


instruction_set = parse_input(FILE)
flipped_tiles = do_initial_flips(instruction_set)

# Count the black tiles
black_count = sum([1 for tile in flipped_tiles.keys() if flipped_tiles[tile] == BLACK])
print(f"Number of black tiles is {black_count}")

# Part 2
for day in range(1, 101):
    limits = get_limits_of_area_to_check(flipped_tiles)
    tiles_to_flip = determine_tiles_to_flip(limits, flipped_tiles)
    flip_tiles_in_place(flipped_tiles, tiles_to_flip)
    black_count = sum(
        [1 for tile in flipped_tiles.keys() if flipped_tiles[tile] == BLACK]
    )
    print(f"Day {day}: {black_count}")
