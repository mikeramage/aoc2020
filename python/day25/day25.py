card_public_key = 3248366
door_public_key  = 4738476
# card_public_key = 5764801
# door_public_key  = 17807724
subject_number = 7
divisor = 20201227

def find_loop_size(public_key):
    loop_size = 1
    value = 1
    while True:
        # print(f"Loop size: {loop_size}")
        value = (value * subject_number) % divisor
        if value == public_key:
            return loop_size
        loop_size += 1

def calc_encryption_key(loop_size, public_key):
    value = 1
    for step in range(loop_size):
        value = (value * public_key) % divisor
    return value

card_loop_size = find_loop_size(card_public_key)
print(f"Card loop size = {card_loop_size}")
door_loop_size = find_loop_size(door_public_key)
print(f"Door loop size = {door_loop_size}")
encryption_key = calc_encryption_key(card_loop_size, door_public_key)
print(f"Encryption key = {encryption_key}")
check_encryption_key = calc_encryption_key(door_loop_size, card_public_key)
print(f"Check encryption key = {check_encryption_key}")



