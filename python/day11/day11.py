from collections import Counter
from enum import Enum

FILE = "day11_input.txt"


class Strategy(Enum):
    ADJACENT = 1
    VISIBLE = 2


def read_file(filename):
    plan = list()
    with open(filename, "r") as f:
        i = 0
        for line in f:
            plan.append(list(line.strip()))
    return plan


def determine_neighbours(i, j, max_i, max_j, data, strategy):
    neighbours = list()

    if strategy == Strategy.ADJACENT:
        for i_step in range(-1, 2):
            for j_step in range(-1, 2):
                if (
                    (i + i_step) >= 0
                    and (i + i_step) <= max_i
                    and (j + j_step) >= 0
                    and (j + j_step) <= max_j
                    and not (i_step == 0 and j_step == 0)
                ):
                    neighbours.append(data[i + i_step][j + j_step])
    if strategy == Strategy.VISIBLE:
        posi = False
        posj = False
        negi = False
        negj = False
        posiposj = False
        posinegj = False
        negiposj = False
        neginegj = False
        for step in range(1, max((len(data) - i), (len(data[i]) - j), i, j)):
            if (
                posi
                and posj
                and negi
                and negj
                and posiposj
                and posinegj
                and negiposj
                and neginegj
            ):
                break
            if not posi:
                posi = check_and_fill_position(
                    i + step, j, max_i, max_j, neighbours, data
                )
            if not negi:
                negi = check_and_fill_position(
                    i - step, j, max_i, max_j, neighbours, data
                )
            if not posj:
                posj = check_and_fill_position(
                    i, j + step, max_i, max_j, neighbours, data
                )
            if not negj:
                negj = check_and_fill_position(
                    i, j - step, max_i, max_j, neighbours, data
                )
            if not posiposj:
                posiposj = check_and_fill_position(
                    i + step, j + step, max_i, max_j, neighbours, data
                )
            if not posinegj:
                posinegj = check_and_fill_position(
                    i + step, j - step, max_i, max_j, neighbours, data
                )
            if not negiposj:
                negiposj = check_and_fill_position(
                    i - step, j + step, max_i, max_j, neighbours, data
                )
            if not neginegj:
                neginegj = check_and_fill_position(
                    i - step, j - step, max_i, max_j, neighbours, data
                )

    # print(f"Neighbours = {neighbours}")
    return neighbours


def check_and_fill_position(i, j, max_i, max_j, neighbours, data):
    if i < 0 or i > max_i or j < 0 or j > max_j:
        return True
    if data[i][j] in ("L", "#"):
        neighbours.append(data[i][j])
        return True
    return False


def apply_rules(state, neighbours, strategy):
    changed = False
    new_state = state
    counter = Counter(neighbours)

    if strategy == Strategy.ADJACENT:
        if state == "L" and "#" not in neighbours:
            new_state = "#"
            changed = True
        elif state == "#" and counter["#"] >= 4:
            new_state = "L"
            changed = True
    elif strategy == Strategy.VISIBLE:
        if state == "L" and "#" not in neighbours:
            new_state = "#"
            changed = True
        elif state == "#" and counter["#"] >= 5:
            new_state = "L"
            changed = True

    return (changed, new_state)


def apply_one_step(data, strategy):
    changed = False
    new_data = list()
    for i, row in enumerate(data):
        new_row = list()
        for j, item in enumerate(row):
            neighbours = determine_neighbours(
                i, j, len(data) - 1, len(row) - 1, data, strategy
            )
            ij_changed, state = apply_rules(data[i][j], neighbours, strategy)
            new_row.append(state)
            changed = changed or ij_changed
        new_data.append(new_row)
    # print(f"New data = {new_data}")
    return changed, new_data


def iterate(data, strategy):
    current_data = data
    while True:
        changed, new_data = apply_one_step(current_data, strategy)
        current_data = new_data
        if not changed:
            break
    return current_data


def num_occupied_seats(data):
    data_list = list()
    for row in data:
        for item in row:
            data_list.append(item)
    counter = Counter(data_list)
    return counter["#"]


data = read_file(FILE)
new_data = iterate(data, Strategy.ADJACENT)
num = num_occupied_seats(new_data)
print(f"Number of occupied seats (adjacent) = {num}")
new_data = iterate(data, Strategy.VISIBLE)
num = num_occupied_seats(new_data)
print(f"Number of occupied seats (visible) = {num}")
