import re

FILE = "day14_input.txt"
MASK = "mask"
MEM = "mem"
V1 = "V1"
V2 = "V2"

mask_regex = re.compile("^mask = (?P<mask>[\d\w]+)$")
mem_regex = re.compile("^mem\[(?P<addr>\d+)\] = (?P<value>\d+)$")


def read_file(filename):
    instructions = list()
    with open(filename, "r") as f:
        for line in f:
            mask_match = re.match(mask_regex, line.strip())
            mem_match = re.match(mem_regex, line.strip())
            if mask_match is not None:
                assert mem_match == None
                instructions.append((MASK, mask_match.group("mask")))
            elif mem_match is not None:
                assert mask_match == None
                instructions.append(
                    (MEM, int(mem_match.group("addr")), int(mem_match.group("value")))
                )
    return instructions


def apply_mask_to_value(mask, value):
    assert len(mask) > 0
    value_as_bin_string = format(value, "0" + str(len(mask)) + "b")
    assert len(value_as_bin_string) == len(mask)
    # print(f"value  {value_as_bin_string}")
    # print(f"mask   {mask}")
    output_bits = ""
    for mask_bit, value_bit in zip(mask, value_as_bin_string):
        if mask_bit == "X":
            output_bits += value_bit
        else:
            assert mask_bit == "0" or mask_bit == "1"
            output_bits += mask_bit
    return int(output_bits, 2)
    # input_bits_as_int = int(value_as_bin_string, 2)
    # print(f"output {output_bits}")
    # print(f"output as int {output_bits_as_int}")
    # print(f"input as int {output_bits_as_int}")


def apply_mask_to_memory(mask, memory):
    assert len(mask) > 0
    memory_as_bin_string = format(memory, "0" + str(len(mask)) + "b")
    assert len(memory_as_bin_string) == len(mask)
    # print(f"memory  {memory_as_bin_string}")
    # print(f"mask   {mask}")
    new_mem_bits = ""
    for mask_bit, mem_bit in zip(mask, memory_as_bin_string):
        if mask_bit == "0":
            new_mem_bits += mem_bit
        else:
            assert mask_bit == "X" or mask_bit == "1"
            new_mem_bits += mask_bit

    floating_bits_matches = list(re.finditer("X", new_mem_bits))
    num_floating_bits = len(floating_bits_matches)
    floating_bit_indices = [bit.span()[0] for bit in floating_bits_matches]
    mem_addresses = list()
    for i in range(2 ** num_floating_bits):
        # convert integer to number of floating bits padded binary string
        mem_addr = list(new_mem_bits)
        i_as_bin_string = format(i, "0" + str(num_floating_bits) + "b")
        for floating_bit_ix, replacement in zip(floating_bit_indices, i_as_bin_string):
            mem_addr[floating_bit_ix] = replacement
        mem_addr = "".join(mem_addr)
        mem_addresses.append(int(mem_addr, 2))

    return mem_addresses


def calculate_memory_contents(instructions, version=V1):
    mem_contents = dict()
    current_mask = ""
    for instruction in instructions:
        if instruction[0] == MASK:
            assert len(instruction) == 2
            current_mask = instruction[1]
        else:
            assert instruction[0] == MEM
            assert len(instruction) == 3
            if version == V1:
                mem_contents[instruction[1]] = apply_mask_to_value(
                    current_mask, instruction[2]
                )
            elif version == V2:
                mem_keys_to_update = apply_mask_to_memory(current_mask, instruction[1])
                for key in mem_keys_to_update:
                    mem_contents[key] = instruction[2]

    return mem_contents


instructions = read_file(FILE)
# print(f"instructions: {instructions}")
mem_contents = calculate_memory_contents(instructions)
sum_of_contents = sum(mem_contents.values())
print(f"Sum = {sum_of_contents}")
mem_contents_2 = calculate_memory_contents(instructions, version=V2)
sum_of_contents_2 = sum(mem_contents_2.values())
print(f"Sum 2 = {sum_of_contents_2}")
