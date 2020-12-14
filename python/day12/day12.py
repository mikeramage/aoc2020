from enum import Enum
import re
import math

FILE = "day12_input.txt"

instruction_re = re.compile("(?P<instruction>\w)(?P<value>\d+)")

class Heading:
    EAST = 0
    SOUTH = 1
    WEST = 2
    NORTH = 3

class Ship:
    def __init__(self,
                 heading=Heading.EAST,
                 e_position=0,
                 n_position=0,
                 we_position = 10,
                 wn_position=1):
        self.heading = heading
        #Ship coords
        self.n_position = n_position
        self.e_position = e_position
        #Waypoint coords relative to ship
        self.wn_position = wn_position
        self.we_position = we_position

    def apply_instruction_part1(self, instruction, value):
        if instruction == 'E':
            self.e_position += value
        elif instruction == 'S':
            self.n_position -= value
        elif instruction == 'W':
            self.e_position -= value
        elif instruction == 'N':
            self.n_position += value
        elif instruction == 'L':
            if value % 90 != 0:
                raise Exception(f"Unexpected L degrees: {value}")
            self.heading = (self.heading - value/90) % 4
        elif instruction == 'R':
            if value % 90 != 0:
                raise Exception(f"Unexpected R degrees: {value}")
            self.heading = (self.heading + value/90) % 4
        elif instruction == 'F':
            if self.heading == Heading.EAST:
                self.e_position += value
            elif self.heading == Heading.SOUTH:
                self.n_position -= value
            elif self.heading == Heading.WEST:
                self.e_position -= value
            elif self.heading == Heading.NORTH:
                self.n_position += value
            else:
                raise Exception(f"Bad heading: {self.heading}!")
        else:
            raise Exception(f"Bad instruction: {self.instruction}!")

    def apply_instruction_part2(self, instruction, value):
        if instruction == 'E':
            self.we_position += value
        elif instruction == 'S':
            self.wn_position -= value
        elif instruction == 'W':
            self.we_position -= value
        elif instruction == 'N':
            self.wn_position += value
        elif instruction == 'L':
            if value % 90 != 0:
                raise Exception(f"Unexpected L degrees: {value}")
            tmp_wn_position = self.wn_position
            tmp_we_position = self.we_position
            self.wn_position = (int)(math.cos(math.radians(value)))*tmp_wn_position + (int)(math.sin(math.radians(value)))*tmp_we_position
            self.we_position = (int)(math.cos(math.radians(value)))*tmp_we_position - (int)(math.sin(math.radians(value)))*tmp_wn_position
        elif instruction == 'R':
            if value % 90 != 0:
                raise Exception(f"Unexpected R degrees: {value}")
            tmp_wn_position = self.wn_position
            tmp_we_position = self.we_position
            self.wn_position = (int)(math.cos(math.radians(value)))*tmp_wn_position - (int)(math.sin(math.radians(value)))*tmp_we_position
            self.we_position = (int)(math.cos(math.radians(value)))*tmp_we_position + (int)(math.sin(math.radians(value)))*tmp_wn_position
        elif instruction == 'F':
            self.e_position += value*self.we_position
            self.n_position += value*self.wn_position
        else:
            raise Exception(f"Bad instruction: {self.instruction}!")

    def manhattan_distance(self):
        return abs(self.e_position) + abs(self.n_position)


def read_file(filename):
    instructions = list()
    with open(filename, 'r') as f:
        for line in f:
            m = re.match(instruction_re, line.strip())
            if m is not None:
                instructions.append((m.group('instruction'), int(m.group('value'))))
    return instructions


instructions = read_file(FILE)
ship = Ship()
ship2 = Ship()

for instruction in instructions:
    ship.apply_instruction_part1(instruction[0], instruction[1])
    ship2.apply_instruction_part2(instruction[0], instruction[1])
print(f"Part 1 manhattan_distance = {ship.manhattan_distance()}")
print(f"Part 2 manhattan_distance = {ship2.manhattan_distance()}")


