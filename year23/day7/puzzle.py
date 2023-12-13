CARDS = {
    'A': 12,
    'K': 11,
    'Q': 10,
    'J': 9,
    'T': 8,
    '9': 7,
    '8': 6,
    '7': 5,
    '6': 4,
    '5': 3,
    '4': 2,
    '3': 1,
    '2': 0,
}

TYPE = {
    (5,):            6,  # Five of a kind
    (1, 4):          5,  # Four of a kind
    (2, 3):          4,  # Full house
    (1, 1, 3):       3,  # Three of a kind
    (1, 2, 2):       2,  # Two pair
    (1, 1, 1, 2):    1,  # One pair
    (1, 1, 1, 1, 1): 0,  # High card
}


def get_strength(hand: str, use_wildcards: bool = False):
    count = dict.fromkeys(CARDS, 0)
    wildcards = 0

    for card in hand:
        if use_wildcards and card == 'J':
            wildcards += 1
            continue
        count[card] += 1

    card_count = sorted(filter(lambda x: x > 0, count.values()))

    if use_wildcards:
        if card_count == []:  # in case of 5 wildcards
            card_count = [0]
        card_count[-1] += wildcards  # more of the same card type is always better

    return TYPE[tuple(card_count)]


def solver(input_path: str, puzzle_type: str):
    assert puzzle_type in ('winnings', 'wildcard')

    puzzle_answer = 0
    games = []
    use_wildcards = puzzle_type == 'wildcard'

    strengths = CARDS.copy()
    if use_wildcards:
        strengths['J'] = -1  # modifying a 'const'

    with open(input_path, 'r') as puzzle:
        for line in puzzle.readlines():
            hand, bid = line.split()
            hand_strength = get_strength(hand, use_wildcards)
            card_strength = [strengths[c] for c in hand]
            games.append({
                'strength': [hand_strength] + card_strength,
                'bid': int(bid)
            })

    games.sort(key=lambda x: x['strength'])

    for rank, game in enumerate(games):
        puzzle_answer += (rank + 1) * game['bid']

    return puzzle_answer


def run_examples():
    examples = (
        ('test_input', 'winnings', 6440),
        ('test_input', 'wildcard', 5905),
    )

    for path, puzzle_type, expected in examples:
        result = solver(path, puzzle_type)
        assert result == expected, f'Example {path} failed: {result}'

    print('Examples passed')


def main():
    import time
    start_time = time.time()

    part1 = solver('input', 'winnings')
    part2 = solver('input', 'wildcard')

    took = time.time() - start_time

    print('Puzzle 1 answer:', part1)
    print('Puzzle 2 answer:', part2)
    print(f'Both solutions found in {took:.3f}s')  # 4ms

    # Regression test
    assert part1 == 248812215
    assert part2 == 250057090


if __name__ == '__main__':
    run_examples()
    main()