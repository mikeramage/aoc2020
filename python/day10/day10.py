import numpy as np

FILE = "day10_input.txt"


def read_file(filename):
    joltages = list()
    joltages.append(0)
    with open(filename, "r") as f:
        for line in f:
            joltages.append(int(line.strip()))
    return sorted(joltages)


def count_differences_all_adaptors(joltages):
    differences = dict()
    current_input = 0
    for joltage in joltages[1:]:
        diff = joltage - current_input
        if diff <= 3 and diff >= 1:
            if diff not in differences.keys():
                differences[diff] = 1
            else:
                differences[diff] += 1
        else:
            raise Exception(f"No possible adaptors: {joltage}!")
        current_input = joltage

    return differences


def count_arrangements_of_adaptors(joltages):
    # need branch factors
    # branch factor is 3 for next 3 differences = 1,1,1
    # branch factor is 2 for 2,1,X or 1,2,X, or 1,1,(X!=1)
    # branch factor is 1 for 3,X,X, 2,2,X, 2,3,X, 1,3,X
    # numpy arrays would make this really fast so let's do it
    # print(f"Joltages {joltages}")
    jlts = np.array(joltages)
    diffs = np.ediff1d(jlts)
    # print(f"{diffs}")
    branch_factors = list()
    for ix in range(diffs.shape[0]):
        diffs_slice = diffs[ix : min(diffs.shape[0], ix + 3)]
        current_sum = 0
        local_branch_factor = 0
        for jx in range(diffs_slice.shape[0]):
            if current_sum + diffs_slice[jx] > 3:
                break
            current_sum += diffs_slice[jx]
            local_branch_factor += 1
        assert local_branch_factor != 0
        # print(f"{local_branch_factor}")
        branch_factors.append(local_branch_factor)
    # print(f"{branch_factors}")
    # print(f"{len(branch_factors)}")

    indexset = dict()
    indexset[0] = 1
    count = 0
    while len(indexset) > 0:
        new_indexset = dict()
        for ix in indexset.keys():
            for j in range(1, branch_factors[ix] + 1):
                if ix + j < len(branch_factors):
                    if ix + j in new_indexset.keys():
                        new_indexset[ix + j] += indexset[ix]
                    else:
                        new_indexset[ix + j] = indexset[ix]
                else:
                    count += indexset[ix]
        indexset = new_indexset
        # print(f"Length of indexset {len(indexset)}, {indexset}")

    return count


joltages = read_file(FILE)
# append our device
joltages.append(max(joltages) + 3)
differences = count_differences_all_adaptors(joltages)
print(f"Joltages: {joltages}")
print(f"{differences[1]*differences[3]}")
print(f"{count_arrangements_of_adaptors(joltages)}")
