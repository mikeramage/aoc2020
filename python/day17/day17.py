FILE = "day17_input.txt"
V1 = "V1.0"
V2 = "V2.0"
INACTIVE = "."
ACTIVE = "#"


def read_input(filename):
    grid = dict()
    x, y, z, w = (0, 0, 0, 0)
    max_coords = [0, 0, 0, 0]
    min_coords = [0, 0, 0, 0]
    with open(filename, "r") as f:
        for line in f:
            l = line.strip()
            x = 0
            for c in l:
                grid[(x, y, z, w)] = c
                x += 1
            max_coords[0] = x
            y += 1
        max_coords[1] = y
    return grid, max_coords, min_coords


def apply_rules(grid, point, version=V1):
    # Get current effective value of cube at this point
    # print(f"Apply rules to point: {point}")
    value = INACTIVE
    if point in grid.keys():
        # print(f"Point exists")
        value = grid[point]
    # print(f"Current value is: {value}")

    # count of active neighbours
    count = 0
    for x in range(point[0] - 1, point[0] + 2, 1):
        for y in range(point[1] - 1, point[1] + 2, 1):
            for z in range(point[2] - 1, point[2] + 2, 1):
                # print(f"Consider point at {(x, y, z)}")
                if version == V1:
                    w = 0
                    if x == point[0] and y == point[1] and z == point[2]:
                        pass
                    # don't consider the point itself
                    # print(f"Ignore self")
                    elif (x, y, z, w) in grid.keys() and grid[(x, y, z, w)] == ACTIVE:
                        # print(f"Cell is active")
                        count += 1
                        if count > 3:
                            # If there are more than 3 active neighbouring cubes
                            # this one becomes inactive and we can break out the
                            # loop
                            # print(f"More than 3 active cells - deactivate!")
                            return INACTIVE
                elif version == V2:
                    for w in range(point[3] - 1, point[3] + 2, 1):
                        if (
                            x == point[0]
                            and y == point[1]
                            and z == point[2]
                            and w == point[3]
                        ):
                            pass
                            # don't consider the point itself
                            # print(f"Ignore self")
                        elif (x, y, z, w) in grid.keys() and grid[
                            (x, y, z, w)
                        ] == ACTIVE:
                            # print(f"Cell is active")
                            count += 1
                            if count > 3:
                                # If there are more than 3 active neighbouring cubes
                                # this one becomes inactive and we can break out the
                                # loop
                                # print(f"More than 3 active cells - deactivate!")
                                return INACTIVE

    if value == ACTIVE and count != 2 and count != 3:
        # print(f"Active and count not 2 or 3 - deactivate")
        return INACTIVE

    if value == INACTIVE and count == 3:
        # print(f"Inactive and count 3 - activate")
        return ACTIVE

    # print(f"Stay same - {value}")
    return value


def update_grid(grid, max_coords, min_coords, version=V1):
    new_grid = dict()
    for x in range(min_coords[0] - 1, max_coords[0] + 2, 1):
        for y in range(min_coords[1] - 1, max_coords[1] + 2, 1):
            for z in range(min_coords[2] - 1, max_coords[2] + 2, 1):
                if version == V1:
                    w = 0
                    value = apply_rules(grid, (x, y, z, w))
                    new_grid[(x, y, z, w)] = value
                elif version == V2:
                    for w in range(min_coords[3] - 1, max_coords[3] + 2, 1):
                        value = apply_rules(grid, (x, y, z, w), version=V2)
                        new_grid[(x, y, z, w)] = value

    if version == V1:
        min_coords = (min_coords[0] - 1, min_coords[1] - 1, min_coords[2] - 1, 0)
        max_coords = (max_coords[0] + 1, max_coords[1] + 1, max_coords[2] + 1, 0)
    elif version == V2:
        min_coords = (
            min_coords[0] - 1,
            min_coords[1] - 1,
            min_coords[2] - 1,
            min_coords[3] - 1,
        )
        max_coords = (
            max_coords[0] + 1,
            max_coords[1] + 1,
            max_coords[2] + 1,
            max_coords[3] + 1,
        )

    return new_grid, max_coords, min_coords


def count_active_cubes(grid):
    count = 0
    for point in grid.keys():
        if grid[point] == ACTIVE:
            count += 1

    return count


grid, max_coords, min_coords = read_input(FILE)
# print(f"Starting grid: {grid}")

for i in range(6):
    grid, max_coords, min_coords = update_grid(grid, max_coords, min_coords, version=V1)

num = count_active_cubes(grid)
print(f"Number of active cubes: {num}")

grid, max_coords, min_coords = read_input(FILE)
for i in range(6):
    grid, max_coords, min_coords = update_grid(grid, max_coords, min_coords, version=V2)

num = count_active_cubes(grid)
print(f"Number of active cubes 4D: {num}")
