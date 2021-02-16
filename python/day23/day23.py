state = [int(x) for x in list(str(219748365))]
# state = [int(x) for x in list(str(389125467))]

# Ugly list-based implementation. See part 2 for full linked list glory
cc = state[0]
for i in range(100):
    cc_index = state.index(cc)

    # extract 3 to move
    tc = list()
    for j in range(3):
        if cc_index + 1 >= len(state):
            # wrap
            cc_index = -1
        tc.append(state.pop(cc_index + 1))

    # print(f"3 to move: {tc}")
    # print(f"State is now: {state}")

    # get destination
    dc = cc - 1
    if dc < min(state):
        dc = max(state)
    while dc in tc:
        dc -= 1
        if dc < min(state):
            dc = max(state)
    # print(f"dest cup: {dc}")

    # get the insertion index
    i_index = state.index(dc) + 1

    # print(f"Insertion index is {i_index}")
    while len(tc) > 0:
        state.insert(i_index, tc.pop())

    # print(f"After insertion, state is {state}")

    # get new current cup - need to recalculate cc index because could have
    # shifted due to insertion
    cc_index = state.index(cc) + 1
    if cc_index >= len(state):
        cc_index = 0

    cc = state[cc_index]
    # print(f"New current cup is {cc}")

print(f"Get part 1 from this: {state}")


class Cup:
    def __init__(self, label, prev, nxt):
        self._label = label
        self._prev = prev
        self._nxt = nxt

    @property
    def label(self):
        return self._label

    @property
    def prev(self):
        return self._prev

    @property
    def nxt(self):
        return self._nxt

    @prev.setter
    def prev(self, prev):
        self._prev = prev

    @nxt.setter
    def nxt(self, nxt):
        self._nxt = nxt

    def remove(self):
        assert self._nxt != None
        assert self._prev != None
        self._nxt.prev = self._prev
        self._prev.nxt = self._nxt
        self._nxt = None
        self._prev = None

    def insert_before(self, cup):
        assert self._nxt == None
        assert self._prev == None
        self._nxt = cup
        self._prev = cup.prev
        cup.prev.nxt = self
        cup.prev = self

    # remove chain of cups starting with the first one
    def remove_chain(self, length):
        assert self.prev != None
        last = self
        for i in range(length - 1):
            last = last.nxt
        assert last.nxt != None
        self.prev.nxt = last.nxt
        last.nxt.prev = self.prev
        self.prev = None
        last.nxt = None

    def insert_chain_before(self, cup):
        assert self.prev == None
        last = self
        while last.nxt is not None:
            last = last.nxt
        assert last.nxt == None
        last.nxt = cup
        self._prev = cup.prev
        cup.prev.nxt = self
        cup.prev = last

    def is_label_in_chain(self, label):
        cup = self
        while cup != None:
            if cup.label == label:
                return True
            cup = cup.nxt
        return False


def get_dest_cup(cups, current_cup, chain_start):
    dest_cup_label = current_cup.label - 1
    if dest_cup_label < 1:
        dest_cup_label = MAX_LABEL
    while chain_start.is_label_in_chain(dest_cup_label):
        dest_cup_label = dest_cup_label - 1
        if dest_cup_label < 1:
            dest_cup_label = MAX_LABEL
    return cups[dest_cup_label]


MAX_LABEL = 1000000
state = [int(x) for x in list(str(219748365))]
for i in range(max(state) + 1, 1000001):
    state.append(i)

# Just a dict of cups keyed by label - need for quick find
cups = dict()

# Now build a linked list of Cups
for label in state:
    cups[label] = Cup(label, None, None)

# Set up next and previous pointers
for index in range(len(state)):
    if index == 0:
        cups[state[index]].prev = cups[state[-1]]
    else:
        cups[state[index]].prev = cups[state[index - 1]]

    if index == len(state) - 1:
        cups[state[index]].nxt = cups[state[0]]
    else:
        cups[state[index]].nxt = cups[state[index + 1]]

current_cup = cups[state[0]]

for i in range(10000000):
    # check progress
    if i % 1000000 == 0:
        print(f"Move #: {i}")

    # Extract 3 to move
    chain_start = current_cup.nxt
    chain_start.remove_chain(3)
    destination_cup = get_dest_cup(cups, current_cup, chain_start)
    chain_start.insert_chain_before(destination_cup.nxt)
    current_cup = current_cup.nxt


result = cups[1].nxt.label * cups[1].nxt.nxt.label
print(f"{result}")
