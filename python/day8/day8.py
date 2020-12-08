file = "day8_input.txt"


def read_file(filename):
    instructions = []
    with open(filename, "r") as f:
        for line in f:
            instructions.append(line.strip().split(" "))
    return instructions


def run_instructions_to_infinite_loop_or_success(instructions):
    accumulator = 0
    seen_before = set()
    instruction = instructions[0][0]
    number = int(instructions[0][1])
    current_index = 0

    # Loop till we get a repeat or hit the end of the input
    while True:
        # Bail if we've seen this index before - it's an infinite loop.
        # Otherwise, just remember we've seen it
        if current_index not in seen_before:
            seen_before.add(current_index)
        else:
            break

        # Implement the instruction
        if instruction == "acc":
            accumulator += number
            current_index += 1
        elif instruction == "jmp":
            current_index += number
        else:
            current_index += 1

        # If we've got to the end, break out
        if current_index >= len(instructions):
            break

        # Get the next instruction
        instruction = instructions[current_index][0]
        number = int(instructions[current_index][1])

    return (accumulator, current_index)


def modify_instructions_till_success(instructions):
    for mod_index in range(len(instructions)):

        # Make a modification (storing previous val so we can restore)
        old_instruction = instructions[mod_index][0]
        if old_instruction == "nop":
            instructions[mod_index][0] = "jmp"
        elif old_instruction == "jmp":
            instructions[mod_index][0] = "nop"
        elif old_instruction == "acc":
            continue
        (acc, ix) = run_instructions_to_infinite_loop_or_success(instructions)

        # if we got to the end, bail
        if ix >= len(instructions):
            return (acc, mod_index)

        # restore old value
        instructions[mod_index][0] = old_instruction

    # Fail
    raise RuntimeException("No successful solution found")


instructions = read_file(file)
accumulator = run_instructions_to_infinite_loop_or_success(instructions)[0]

print(f"Last accumulator value {accumulator}")

accumulator, changed_index = modify_instructions_till_success(instructions)
print(f"Accumulator value on success: {accumulator}")
print(f"Index of changed instruction: {changed_index}")
