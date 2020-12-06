FILE = "day6_input.txt"


class Group:
    def __init__(self, people=list()):
        self.people = people

    def __repr__(self):
        return f"People in group: {self.people}"

    def count_unique_answers(self):
        unique_answers = set()
        for person in self.people:
            for answer in person.answers:
                if answer not in unique_answers:
                    unique_answers.add(answer)

        return len(unique_answers)

    def count_all_people_answered(self):
        all_people_answered = set()
        checked_answers = set()
        for person in self.people:
            for answer in person.answers:
                if answer not in checked_answers:
                    # not checked this answer yet.
                    checked_answers.add(answer)
                    # if not already in our list (probably redundant check) and everyone answered then add to the list
                    if answer not in all_people_answered and self.all_people_answered(
                        answer
                    ):
                        all_people_answered.add(answer)
        return len(all_people_answered)

    def all_people_answered(self, answer):
        for person in self.people:
            if answer not in person.answers:
                return False
        return True


class Person:
    def __init__(self, answers=""):
        self.answers = answers

    def __repr__(self):
        return f"Person with answers: {self.answers}"


def read_input(filename):
    groups = list()
    people = list()
    with open(filename, "r") as f:
        for line in f:
            if line.strip() == "":
                # end of group
                groups.append(Group(people=people))
                # new list of people for next group
                people = list()
            else:
                answers = line.strip()
                people.append(Person(answers))

    if len(people) != 0:
        # hit end of file and still have people we haven't added to a group.
        groups.append(Group(people=people))

    return groups


groups = read_input(FILE)

answer_count = 0
all_people_answered_count = 0
for group in groups:
    answer_count += group.count_unique_answers()
    all_people_answered_count += group.count_all_people_answered()
print(f"Part 1 unique answers count sum: {answer_count}")
print(f"Part 2 all peopled answered count sum: {all_people_answered_count}")
