import re

FILE = "day16_input.txt"
YOURS = "your ticket:"
NEARBY = "nearby tickets:"

field_range_regex = re.compile(
    "^(?P<field>[\w\s]+): (?P<first_lower>\d+)-(?P<first_upper>\d+) or (?P<second_lower>\d+)-(?P<second_upper>\d+)$"
)
ticket_regex = re.compile("^[\d,]+$")
departure_regex = re.compile("^departure.*$")


def read_file(filename):
    reading_your_ticket = True
    ranges = list()
    your_ticket = None
    nearby_tickets = list()

    with open(filename, "r") as f:
        for line in f:
            l = line.strip()
            range_match = re.match(field_range_regex, l)
            ticket_match = re.match(ticket_regex, l)
            if range_match:
                ranges.append(
                    (
                        range_match.group("field"),
                        int(range_match.group("first_lower")),
                        int(range_match.group("first_upper")),
                        int(range_match.group("second_lower")),
                        int(range_match.group("second_upper")),
                    )
                )
            elif l == "":
                continue
            elif l == YOURS:
                reading_your_ticket = True
            elif l == NEARBY:
                reading_your_ticket = False
            elif ticket_match:
                if reading_your_ticket:
                    assert your_ticket is None
                    your_ticket = [int(x) for x in ticket_match.group().split(",")]
                else:
                    nearby_tickets.append(
                        [int(x) for x in ticket_match.group().split(",")]
                    )

    return (ranges, your_ticket, nearby_tickets)


def field_in_range(field, field_range):
    return (field >= field_range[1] and field <= field_range[2]) or (
        field >= field_range[3] and field <= field_range[4]
    )


# TODO fix bad design that has this function perform multiple operations
def calculate_error_scanning_rate(ranges, tickets):
    error_rate = 0
    valid_tickets = list()
    for ticket in tickets:
        all_fields_valid = True
        for field in ticket:
            field_valid = False
            for field_range in ranges:
                if field_in_range(field, field_range):
                    field_valid = True
                    break
            if not field_valid:
                error_rate += field
                all_fields_valid = False
        if all_fields_valid:
            valid_tickets.append(ticket)
    return error_rate, valid_tickets


def determine_fields(ranges, tickets):
    index_to_field_mapping = dict()
    valid_ranges_for_field = set()
    all_fields = [field_range[0] for field_range in ranges]
    for field_range in ranges:
        valid_ranges_for_field.add(field_range[0])
    for i in range(len(tickets[0])):
        valid_ranges = set(valid_ranges_for_field)
        for ticket in tickets:
            for field_range in ranges:
                if not field_in_range(ticket[i], field_range):
                    if field_range[0] in valid_ranges:
                        valid_ranges.remove(field_range[0])
        index_to_field_mapping[i] = valid_ranges
    out_index_to_field_mapping = dict()
    determined_fields = set()

    change_occurred = True
    while change_occurred:
        change_occurred = False
        determined_field = None
        # Check for "only possibility" - sufficient for this problem
        for key, val in index_to_field_mapping.items():
            if len(val) == 1:
                determined_field = val.pop()
                out_index_to_field_mapping[key] = determined_field
                determined_fields.add(determined_field)
                change_occurred = True
                break
        for val in index_to_field_mapping.values():
            if determined_field is not None:
                val.discard(determined_field)

        # #This could be necessary in the more general case
        # for field in all_fields:
        #     present_indices = set()
        #     for key, val in index_to_field_mapping.items():
        #         if field in val:
        #             present_indices.add(key)
        #     if len(present_indices) == 1:
        #         index = present_indices.pop()
        #         out_index_to_field_mapping[index] = field
        #         determined_fields.add(field)
        #         index_to_field_mapping[index] = set()

    return out_index_to_field_mapping


ranges, your_ticket, nearby_tickets = read_file(FILE)
rate, valids = calculate_error_scanning_rate(ranges, nearby_tickets)
print(f"Error rate: {rate}")
mapping = determine_fields(ranges, valids)

product = 1
for i in range(len(your_ticket)):
    if re.match(departure_regex, mapping[i]):
        product *= your_ticket[i]

print(f'Product of "departure" fields: {product}')
