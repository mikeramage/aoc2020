from collections import deque

FILE = "day22_input.txt"
PLAYER1 = "Player 1"
PLAYER2 = "Player 2"


def read_input(filename):
    player1_cards = deque()
    player2_cards = deque()
    in_player1 = False
    in_player2 = False

    with open(filename, "r") as f:
        for l in f:
            cards = None
            if in_player1:
                cards = player1_cards
            elif in_player2:
                cards = player2_cards

            if l.strip() == "Player 1:":
                in_player1 = True
            elif l.strip() == "Player 2:":
                in_player1 = False
                in_player2 = True
            elif l.strip().isdigit():
                if cards == None:
                    raise Exception("No cards where there should be cards")
                cards.appendleft(int(l.strip()))
            elif l.strip() == "":
                pass
            else:
                raise Exception("Unexpected nonsense found")

    return player1_cards, player2_cards


def play_round(player1, player2, recursive=False):

    card1 = player1.pop()
    card2 = player2.pop()

    if recursive and (len(player1) >= card1) and (len(player2) >= card2):
        winner, score = play_game(
            deque(list(player1.copy())[-card1:]),
            deque(list(player2.copy())[-card2:]),
            recursive,
        )
    else:
        # No rule for if cards equal so better not be!
        assert card1 != card2
        if card1 > card2:
            # player1 wins
            winner = PLAYER1
        else:
            winner = PLAYER2

    if winner == PLAYER1:
        player1.appendleft(card1)
        player1.appendleft(card2)
    else:
        assert winner == PLAYER2
        player2.appendleft(card2)
        player2.appendleft(card1)

    return


def calc_set_key(player1, player2):
    player1_str = [str(x) for x in player1]
    player2_str = [str(x) for x in player2]
    return ",".join(player1_str) + "P" + ",".join(player2_str)


def play_game(player1, player2, recursive=False):

    seen_configurations = set()
    while len(player1) > 0 and len(player2) > 0:
        if recursive:
            set_key = calc_set_key(player1, player2)
            if set_key in seen_configurations:
                winner = player1
                winner_name = PLAYER1
                score = 0
                for i, card in enumerate(winner):
                    score += (i + 1) * card
                return winner_name, score
            seen_configurations.add(set_key)
        play_round(player1, player2, recursive)

    if len(player1) > 0:
        winner = player1
        winner_name = PLAYER1
    else:
        winner = player2
        winner_name = PLAYER2

    score = 0
    for i, card in enumerate(winner):
        score += (i + 1) * card

    return winner_name, score


player1, player2 = read_input(FILE)
print(f"Player 1: {player1}")
print(f"Player 2: {player2}")

name, score = play_game(player1, player2)
print(f"Winner is {name} with {score} points")

player1, player2 = read_input(FILE)
name, score = play_game(player1, player2, recursive=True)
print(f"Winner of recursive game is {name} with {score} points")
