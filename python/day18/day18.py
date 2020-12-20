FILE = "day18_input.txt"


def read_file(filename):
    lines = list()
    with open(filename, "r") as f:
        for line in f:
            lines.append(line.strip())
    return lines


def evaluate_line(line):
    # print(f"Enter evaluate_line")
    operator = None
    lhs = None
    rhs = None
    i = 0
    while i < len(line):
        # This assumes all single-digit numbers
        # print(f"i, line(i): {i}, {line[i]}")
        if line[i].isdigit():
            if lhs is not None:
                assert operator is not None
                rhs = line[i]
                lhs = str(eval(f"{lhs}{operator}{rhs}"))
                operator = None
                rhs = None
            else:
                lhs = line[i]
        elif line[i] == " ":
            pass
        elif line[i] == "+" or line[i] == "*":
            operator = line[i]
        elif line[i] == "(":
            # print(f"Got opening paren")
            close_ix = find_matching_paren_index(i + 1, line[i + 1 :])
            if lhs is not None:
                assert operator is not None
                rhs = str(evaluate_line(line[i + 1 : close_ix]))
                lhs = str(eval(f"{lhs}{operator}{rhs}"))
                operator = None
                rhs = None
            else:
                lhs = str(evaluate_line(line[i + 1 : close_ix]))
            # set i to closing paren - we'll increment by 1 before going round
            # the loop again in the general increment by 1 step, skipping the
            # closing paren - this means we should never hit a closing paren
            # in this loop - exception raised below will catch this if I'm wrong
            i = close_ix
        else:
            raise Exception(f"Unexpected character: {line[i]} at index {i}")

        i += 1

    # print(f"Returning: {lhs}")
    return int(lhs)


def add_parens_for_plus_precedence(line):
    # print(f"Entering add_parens_for_predence")
    new_line = ""
    opened_parens = False
    i = 0
    start_index = i
    while i < len(line):
        # This assumes all single-digit numbers
        if line[i].isdigit():
            new_line += line[i]
        elif line[i] == " ":
            new_line += line[i]
        elif line[i] == "+":
            opened_parens = True
            new_line += line[i]
        elif line[i] == "*":
            if opened_parens:
                opened_parens = False
                prefix = new_line[:start_index]
                new_line = prefix + "(" + new_line[start_index:-1] + ") " + line[i]
            else:
                new_line += line[i]
            start_index = len(new_line)
        elif line[i] == "(":
            # print(f"Got opening paren")
            close_ix = find_matching_paren_index(i + 1, line[i + 1 :])
            new_line += (
                "(" + add_parens_for_plus_precedence(line[i + 1 : close_ix]) + ")"
            )
            i = close_ix
        else:
            raise Exception(f"Unexpected character: {line[i]} at index {i}")

        i += 1
        # print(f"New line: {new_line}")

    if opened_parens:
        prefix = new_line[:start_index]
        new_line = prefix + "(" + new_line[start_index:] + ")"

    # print(f"Returning: {new_line}")
    return new_line


def find_matching_paren_index(start_index, line):
    # print(f"Enter find_matching_paren_index")
    counter = 1
    for i, c in enumerate(line):
        if c == "(":
            counter += 1
        if c == ")":
            counter -= 1
            if counter == 0:
                # print(f"Closing paren at index {i}")
                return i + start_index
    raise Exception("Oy! Mismatched parentheses")


lines = read_file(FILE)
total = 0
for line in lines:
    # print(f"Line: {line}")
    total += evaluate_line(line)

print(f"Part1 total: {total}")

part2_total = 0
for line in lines:
    # print(f"Line: {line}")
    new_line = add_parens_for_plus_precedence(line)
    part2_total += evaluate_line(new_line)

print(f"Part2 total: {part2_total}")
