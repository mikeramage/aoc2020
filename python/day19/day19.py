import re, itertools
from timeit import default_timer

FILE = "day19_input.txt"

rule_regex = re.compile("^(?P<index>\d+): (?P<rule>.+)$")
base_regex = re.compile('^"([a-z])"$')


class Rule:
    def __init__(self, base, sub_rules):
        self.base = base
        self.sub_rules = sub_rules
        self.rule_set = None
        self.contributing_rules = set()

    def __repr__(self):
        if self.base is not None:
            return f"{self.base}"
        elif self.sub_rules is not None:
            return f"{self.sub_rules}"
        else:
            return "Null rule"

    def construct_alternatives(self, all_rules):
        if self.rule_set is not None:
            return list(self.rule_set), set(self.contributing_rules)

        self.rule_set = list()
        if self.base is not None:
            self.rule_set.append(self.base)
        else:
            assert self.sub_rules is not None
            for alternative in self.sub_rules:
                expanded_sub_rules = list()
                for rule_index in alternative:
                    self.contributing_rules.add(rule_index)
                    expanded_rule, contributing_sub_rules = all_rules[
                        rule_index
                    ].construct_alternatives(all_rules)
                    expanded_sub_rules.append(expanded_rule)
                    self.contributing_rules = (
                        self.contributing_rules | contributing_sub_rules
                    )
                combined_sub_rules = itertools.product(*expanded_sub_rules)
                for rule in combined_sub_rules:
                    self.rule_set.append("".join(rule))
        return (list(self.rule_set), set(self.contributing_rules))

    # Returns True if message matches rule, False otherwise
    # Can only be called after construct_alternatives
    def apply_rule_to_message(self, message):
        for rule in self.rule_set:
            if rule == message:
                return True
        return False


def read_file(filename):
    rules = dict()
    messages = list()
    parsing_rules = True
    with open(filename, "r") as f:
        for l in f:
            if l.strip() == "":
                parsing_rules = False
            elif parsing_rules:
                rule_match = re.match(rule_regex, l.strip())
                assert rule_match is not None
                base_match = re.match(base_regex, rule_match.group("rule"))
                base = None
                sub_rules = None
                if base_match:
                    base = base_match.group(1)
                else:
                    sub_rules = [
                        x.strip().split(" ")
                        for x in rule_match.group("rule").split("|")
                    ]
                rules[rule_match.group("index")] = Rule(base, sub_rules)
            else:
                messages.append(l.strip())
    return rules, messages


# OK Part 2 - so 0 is made from 8 11, 8 is an arbitrary number of 42s,
# 11 is N 42s followed by N 31s, where N is some integer. 42s and 31s are
# strings of length 8. That means to find the messages that match 0, they must
# start with 2 42s, then each 8 bytes further must match either a 42 or a 31
# (if a 42, then next 8 chars can match a 42 or a 31, but after a 31, next 8
# chars can only match a 31). finally, the last 8 chars need to be in the 31
# set. There also have to be more 42s than 31s by the pattern
def apply_part2_to_message(message, rules):
    # print(f"Message: {message}")
    rule42_set = set(rules["42"].rule_set)
    rule31_set = set(rules["31"].rule_set)

    length = len(rules["42"].rule_set[0])
    if (len(message) % length != 0) or (len(message) < (3 * length)):
        # print(f"Message too short: {len(message)}")
        return False

    if message[0:length] not in rule42_set:
        # print(f"First {length} chars don't match rule42: {message[0:length]}")
        return False

    if message[length : (2 * length)] not in rule42_set:
        # print(f"Second {length} chars don't match rule42: {message[length:2*length]}")
        return False

    if message[-length:] not in rule31_set:
        # print(f"Last {length} chars don't match rule31: {message[-length:]}")
        return False

    count31 = 0
    count42 = 2

    i = 2 * length
    hit_31s = False
    while (i + length) <= len(message):
        # print(f"i = {i} checking: {message[i:i+length]}")
        if not hit_31s:
            # print(f"Not hit 31s yet")
            if message[i : i + length] not in rule42_set:
                # print(f"Not in rule 42 set")
                if message[i : i + length] not in rule31_set:
                    # print(f"Not in rule 31 set")
                    return False
                else:
                    # print(f"In rule 31 set")
                    count31 += 1
                    hit_31s = True
            else:
                count42 += 1
        else:
            # print(f"On the 31s")
            if message[i : i + length] not in rule31_set:
                # print(f"Not in rule 31 set (2)")
                return False
            count31 += 1
        i += length

    if count42 > count31:
        # print(f"Message checks out")
        return True
    # else:
    # print(f"Too many 31s - impossible pattern: {count31} 31s vs {count42} 42s")


rules, messages = read_file(FILE)
# print(f"Rules: {rules}")
# print(f"Messages: {messages}")

# Finish initialization of the rules
for rule in rules.values():
    rule.construct_alternatives(rules)

count = 0
for message in messages:
    if rules["0"].apply_rule_to_message(message):
        count += 1
print(f"Part 1 count: {count}")

# print(f"Rule 8 expanded: length {len(rules['8'].rule_set)}: {rules['8'].rule_set[:20]}")
# print(f"Rule 8 contributing rules: {rules['8'].contributing_rules}")
# print(f"Rule 11 expanded: length {len(rules['11'].rule_set)}: {rules['11'].rule_set[:20]}")
# print(f"Rule 11 contributing rules: {rules['11'].contributing_rules}")
# print(f"Rule 31 expanded: length {len(rules['31'].rule_set)}: {rules['31'].rule_set}")
# print(f"Rule 31 contributing rules: {rules['31'].contributing_rules}")
# print(f"Rule 42 expanded: length {len(rules['42'].rule_set)}: {rules['42'].rule_set}")
# print(f"Rule 42 contributing rules: {rules['42'].contributing_rules}")
# print(f"Rule 0 expanded: length {len(rules['0'].rule_set)}: {rules['0'].rule_set[:20]}")
# print(f"Rule 0 contributing rules: {rules['0'].contributing_rules}")
# print(f"Max message len: {max([len(x) for x in messages])}")
start = default_timer()
count2 = 0
for message in messages:
    if apply_part2_to_message(message, rules):
        count2 += 1
stop = default_timer()
print(f"Part 2 count: {count2}")
print(f"Part 2 took: {stop-start}")
