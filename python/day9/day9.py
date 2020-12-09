import itertools

FILE = "day9_input.txt"


def read_file(filename):
    data = list()
    with open(filename, "r") as f:
        for line in f:
            data.append(int(line.strip()))
    return data


def find_first_invalid_number(data, preamble_size=25):

    test_index = preamble_size

    while test_index < len(data):
        low_index = test_index - preamble_size
        test_number = data[test_index]
        data_slice = data[low_index:test_index]
        if not is_number_valid(test_number, data_slice):
            return test_number, test_index

        test_index += 1

    raise RuntimeException(f"No invalid numbers!")


def is_number_valid(test_number, data_slice):

    for combo in itertools.combinations(data_slice, 2):
        if sum(combo) == test_number:
            return True

    return False


def find_encryption_weakness(data, preamble_size=25):
    invalid_number, invalid_index = find_first_invalid_number(data, preamble_size)
    data_slice = data[:invalid_index]
    for r in range(2, invalid_index):
        min_index = 0
        max_index = min_index + r
        while max_index < len(data_slice):
            sub_slice = data_slice[min_index:max_index]
            if sum(sub_slice) == invalid_number:
                return min(sub_slice) + max(sub_slice)
            min_index += 1
            max_index += 1

    raise RuntimeException(f"No encryption_weakness")


data = read_file(FILE)
first_invalid_number = find_first_invalid_number(data)[0]
encryption_weakness = find_encryption_weakness(data)
print(f"first_invalid_number: {first_invalid_number}")
print(f"encryption weakness: {encryption_weakness}")
