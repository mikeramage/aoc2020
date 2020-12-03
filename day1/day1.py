entries = list()
with open("day1_expenses.txt", "r") as f:
    for line in f:
        entries.append(int(line.strip()))

for i in range(len(entries)):
    for j in range(i + 1, len(entries)):
        if entries[i] + entries[j] == 2020:
            print(f"{entries[i]}, {entries[j]}: {entries[i] * entries[j]}")

for i in range(len(entries)):
    for j in range(i + 1, len(entries)):
        for k in range(j + 1, len(entries)):
            if entries[i] + entries[j] + entries[k] == 2020:
                print(
                    f"{entries[i]}, {entries[j]}, {entries[k]}: {entries[i] * entries[j] * entries[k]}"
                )
