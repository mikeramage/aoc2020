FILE = "day5_input.txt"


def read_input(filename):
    boarding_passes = list()
    with open(filename, "r") as f:
        for line in f:
            boarding_passes.append(line.strip())

    return boarding_passes


def boarding_pass_to_id(boarding_pass):
    row = boarding_pass[:7]
    col = boarding_pass[7:]

    row_number = 0
    row_factor = 64
    for x in row:
        if x == "B":
            row_number = row_number + row_factor
        row_factor /= 2

    col_number = 0
    col_factor = 4
    for x in col:
        if x == "R":
            col_number = col_number + col_factor
        col_factor /= 2

    seat_id = row_number * 8 + col_number

    return seat_id


boarding_passes = read_input(FILE)

max_id = 0
seat_ids = list()
for boarding_pass in boarding_passes:
    current_id = boarding_pass_to_id(boarding_pass)
    seat_ids.append(current_id)
    max_id = max(max_id, current_id)

sorted_ids = sorted(seat_ids)

previous_id = sorted_ids[0]
my_seat_id = 0
for seat_id in sorted_ids[1:]:
    print(f"{seat_id}")
    if seat_id - previous_id > 1:
        assert seat_id - previous_id == 2
        my_seat_id = seat_id - 1
        break
    previous_id = seat_id

print(f"max_id: {max_id}")
print(f"my seat: {my_seat_id}")
