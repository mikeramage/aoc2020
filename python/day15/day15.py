# TODO rewrite with generators

starting_numbers = [11, 18, 0, 20, 1, 7, 16]

spoken_hist = list()
turn_last_spoken = dict()


def determine_next_number(turn_last_spoken, spoken_hist, current_index):
    next_number = 0
    if index in range(len(starting_numbers)):
        next_number = starting_numbers[index]
    else:
        last_number = spoken_hist[index - 1]
        if last_number in turn_last_spoken.keys():
            next_number = current_index - turn_last_spoken[last_number] - 1
    return next_number


last_number = 0
for index in range(30000000):
    number = determine_next_number(turn_last_spoken, spoken_hist, index)
    spoken_hist.append(number)
    if index != 0:
        turn_last_spoken[last_number] = index - 1
    last_number = number

print(f"2020th number is: {spoken_hist[2019]}")
print(f"30000000th number is: {spoken_hist[29999999]}")
