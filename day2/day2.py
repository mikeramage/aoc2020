import re
import operator

FILE = "day2_passwords.txt"


class InputDataItem:
    def __init__(self, low=0, high=0, letter="", password=""):
        self.low = low
        self.high = high
        self.letter = letter
        self.password = password

    def __str__(self):
        return f"{str(self.low)}, {str(self.high)}, {self.letter}, {self.password}"


def read_input(filename):
    input_data = list()
    pwd_regex = re.compile(
        "(?P<low>\d+)-(?P<high>\d+)\s+(?P<letter>\w+):\s+(?P<password>.*)"
    )
    with open(filename, "r") as f:
        for line in f:
            match = re.match(pwd_regex, line.strip())
            if match is not None:
                data_item = InputDataItem(
                    low=int(match.group("low")),
                    high=int(match.group("high")),
                    letter=match.group("letter"),
                    password=match.group("password"),
                )
                input_data.append(data_item)
            else:
                raise RuntimeError(f"Data doesn't match regex: {line.strip()}")

    return input_data


def count_valid_passwords_policy1(input_data):
    valid_passwords = 0
    for item in input_data:
        char_count = 0
        for letter in item.password:
            if letter == item.letter:
                char_count += 1

        if char_count >= item.low and char_count <= item.high:
            valid_passwords += 1

    return valid_passwords


def count_valid_passwords_policy2(input_data):
    valid_passwords = 0
    for item in input_data:
        if operator.xor(
            item.password[item.low - 1] == item.letter,
            item.password[item.high - 1] == item.letter,
        ):
            valid_passwords += 1

    return valid_passwords


data = read_input(FILE)
valid_count_policy1 = count_valid_passwords_policy1(data)
print(f"Number of valid passwords (policy 1) is: {valid_count_policy1}")
valid_count_policy2 = count_valid_passwords_policy2(data)
print(f"Number of valid passwords (policy 2) is: {valid_count_policy2}")
