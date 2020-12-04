import re

FILE = "day4_input.txt"


class Passport:

    mandatory_fields = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]
    optional_fields = ["cid"]

    year_regex = re.compile("^(?P<year>\d{4})$")
    height_regex = re.compile("^(?P<height>\d+)(?P<unit>cm|in)$")
    hair_regex = re.compile("^(?P<colour>#[0-9a-f]{6})$")
    eye_regex = re.compile("^(?P<colour>amb|blu|brn|gry|grn|hzl|oth)$")
    pid_regex = re.compile("^(?P<pid>\d{9})$")

    def __init__(self, data=dict()):
        self.data = data  # Dictionary of data

    def is_valid(self, check_field=False):
        for field in Passport.mandatory_fields:
            if (
                field not in self.data.keys()
                or check_field
                and not self.check_field(field)
            ):
                return False
        # all valid fields present and correct
        return True

    def check_field(self, field):
        if field == "byr":
            if (
                re.fullmatch(Passport.year_regex, self.data[field])
                and int(self.data[field]) >= 1920
                and int(self.data[field]) <= 2002
            ):
                return True
            else:
                return False
        elif field == "iyr":
            if (
                re.fullmatch(Passport.year_regex, self.data[field])
                and int(self.data[field]) >= 2010
                and int(self.data[field]) <= 2020
            ):
                return True
            else:
                return False
        elif field == "eyr":
            if (
                re.fullmatch(Passport.year_regex, self.data[field])
                and int(self.data[field]) >= 2020
                and int(self.data[field]) <= 2030
            ):
                return True
            else:
                return False
        elif field == "hgt":
            match = re.fullmatch(Passport.height_regex, self.data[field])
            if match:
                if match.group("unit") == "cm":
                    if (
                        int(match.group("height")) >= 150
                        and int(match.group("height")) <= 193
                    ):
                        return True
                    else:
                        return False
                else:
                    assert match.group("unit") == "in"
                    if (
                        int(match.group("height")) >= 59
                        and int(match.group("height")) <= 76
                    ):
                        return True
                    else:
                        return False
            else:
                return False
        elif field == "hcl":
            if re.fullmatch(Passport.hair_regex, self.data[field]):
                return True
            else:
                return False
        elif field == "ecl":
            if re.fullmatch(Passport.eye_regex, self.data[field]):
                return True
            else:
                return False
        elif field == "pid":
            if re.fullmatch(Passport.pid_regex, self.data[field]):
                return True
            else:
                return False
        elif field == "cid":
            return True
        else:
            return False


def read_input(filename):
    passports = list()
    with open(filename, "r") as f:
        current_entry = dict()
        for line in f:
            if line.strip() == "":
                passports.append(Passport(current_entry))
                current_entry = dict()
            else:
                fields = line.strip().split(" ")
                for field in fields:
                    key, value = field.strip().split(":")
                    if key not in current_entry:
                        current_entry[key] = value
    if len(current_entry.keys()) > 0:
        passports.append(Passport(current_entry))
    return passports


passports = read_input(FILE)
part1_count = 0
part2_count = 0
for passport in passports:
    if passport.is_valid():
        # print(f"valid passport part 1: {passport.data}")
        part1_count += 1
    if passport.is_valid(check_field=True):
        part2_count += 1
print(f"# valid passports part 1 is {part1_count}")
print(f"# valid passports part 2 is {part2_count}")
