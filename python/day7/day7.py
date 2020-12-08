import re

FILE = "day7_input.txt"
rule_regex = re.compile("(?P<name>[\w\s]+) bags contain\s+(?P<content>[\w\d\s,]+).*")
content_regex = re.compile("(?P<number>\d+)\s+(?P<bag>[\w\s]+)\s+(bag|bags)")


def read_input(filename):
    bags = dict()

    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            rule_match = re.match(rule_regex, line)
            if rule_match:
                name = rule_match.group("name")
                content = rule_match.group("content")
                items = []
                for item in content.split(","):
                    item_match = re.match(content_regex, item.strip())
                    if item_match:
                        items.append(
                            (item_match.group("number"), item_match.group("bag"))
                        )
                    else:
                        assert item.strip() == "no other bags"
                assert name not in bags.keys()
                bags[name] = items

    return bags


bags = read_input(FILE)
# print(f"{bags}")
count = 0


def is_in_bag(bags, bag_contents, name):

    if not bag_contents:
        # print(f"no contents!")
        return False

    for sub_bag in bag_contents:
        # print(f"checking sub_bag {sub_bag}")
        if name == sub_bag[1]:
            return True

    for sub_bag in bag_contents:
        new_contents = bags[sub_bag[1]]
        # print(f"Bag: {new_contents}")
        if is_in_bag(bags, new_contents, name):
            return True

    return False


for bag_name, contents in bags.items():
    print(f"Checking bag {bag_name} with contents {contents}")
    if is_in_bag(bags, contents, "shiny gold"):
        print(f"Found shiny gold bag in bag {bag_name}")
        count += 1


def number_of_bags(bags, name):
    count = 0
    for sub_bag in bags[name]:
        count += int(sub_bag[0])
        count += int(sub_bag[0]) * number_of_bags(bags, sub_bag[1])

    return count


bag_count = number_of_bags(bags, "shiny gold")
print(f"{count} bags ultimately contain a shiny gold bag")
print(f"{bag_count} bags needed in a shiny gold bag")
