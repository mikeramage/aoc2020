FILE = "day13_input.txt"


def read_file(filename):
    earliest_time = 0
    bus_ids = list()
    with open(filename, "r") as f:
        earliest_time = int(f.readline().strip())
        bus_ids_raw = f.readline().strip().split(",")

        # This line works because the first non-x bus id has index 0
        bus_ids = [
            (ix, int(bus_id)) for ix, bus_id in enumerate(bus_ids_raw) if bus_id != "x"
        ]

    return (earliest_time, bus_ids)


def times_to_wait(time, bus_ids):
    times = list()
    for bus_id in bus_ids:
        if time % bus_id[1] == 0:
            times.append(0)
        else:
            times.append(bus_id[1] - time % bus_id[1])

    return times


def min_time_to_wait(time, bus_ids):
    times = times_to_wait(time, bus_ids)
    min_time_to_wait = min(times)
    return (min_time_to_wait, bus_ids[times.index(min_time_to_wait)][1])


def iterate_to_p2_soln(bus_ids):
    bus_offsets = [[bus_id[1], bus_id[0] % bus_id[1]] for bus_id in bus_ids]
    # print(f"bus_offsets: {bus_offsets}")
    first_bus_id, first_bus_offset = bus_offsets.pop(0)
    cycles = list()
    first_time = True
    calc_stuff = [first_bus_id]
    while len(bus_offsets) > 0:
        # There's probably a better way that treating the first iteration as a
        # special case - probably got the data structures wrong
        for bus_id, offset in bus_offsets:
            cycle_offset = 0
            counter = 0
            i = 1
            while True:
                if first_time:
                    this_offset = bus_id - (i * first_bus_id) % bus_id
                else:
                    this_offset = i * first_bus_id % bus_id
                # print(f"0 {i} {this_offset}")
                if this_offset == offset:
                    if counter == 1:
                        # print(f"1 {i} {this_offset}")
                        cycles.append([i - cycle_offset, cycle_offset])
                        break
                    else:
                        # print(f"2 {i} {this_offset}")
                        assert counter == 0
                        cycle_offset = i
                        counter = 1
                i += 1
        first_time = False
        # reduce and reorder bus_offsets
        # print(f"cycles: {cycles}")
        bus_offsets = cycles
        min_offset_ix = 0
        min_offset = bus_offsets[0][1]
        for ix, offset in enumerate(bus_offsets):
            if offset[1] < min_offset:
                min_offset = offset[1]
                min_offset_ix = ix
        min_offset_elem = bus_offsets.pop(min_offset_ix)
        bus_offsets = [min_offset_elem] + bus_offsets
        for offset in bus_offsets:
            offset[1] -= min_offset
        # print(f"bus_offsets: {bus_offsets}")

        first_bus_id, first_bus_offset = bus_offsets.pop(0)
        calc_stuff.append(min_offset)
        if len(cycles) > 0:
            calc_stuff.append(first_bus_id)
        cycles = list()

    # print(f"calc_stuff {calc_stuff}")
    product = calc_stuff[-1]
    for ix, item in enumerate(reversed(calc_stuff)):
        if ix != 0 and ix % 2 == 0:
            product = product + item
        elif ix != 0:
            product = product * item

    return product


earliest_time, bus_ids = read_file(FILE)
# print(f"bus ids: {bus_ids}")
current_max = 0
min_time_to_wait, min_bus_id = min_time_to_wait(earliest_time, bus_ids)
print(
    f"Time to wait: {min_time_to_wait}, bus_id: {min_bus_id}, product = {min_time_to_wait * min_bus_id}"
)
product = iterate_to_p2_soln(bus_ids)
print(f"part2: {product}")
