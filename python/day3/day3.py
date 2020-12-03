TREE = "#"
OPEN = "."
FILE = "day3_input.txt"


def parse_input(filename):
    rows = list()
    with open(filename, "r") as f:
        for line in f:
            rows.append(line.strip())
    return rows


def count_trees(rows=list(), strategy=(3, 1)):
    x = 0  # index of current location
    count = 0  # count of trees
    for i in range(0, len(rows), strategy[1]):
        row = rows[i]
        if row[x] == TREE:
            count += 1
        x = (x + strategy[0]) % len(row)
    return count


hillside = parse_input(FILE)
tree_count = count_trees(rows=hillside)
print(f"There are {tree_count} trees")

# part 2
strategies = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]

product = 1
for strategy in strategies:
    product *= count_trees(rows=hillside, strategy=strategy)

print(f"Product of trees is: {product}")
