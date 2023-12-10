def get_range(tree, row):
    if tree > max(row):
        return len(row)

    for n, t in enumerate(row):
        if tree <= t:
            return n + 1


def num_visible(trees, puzzle_type):
    assert puzzle_type in ('visible', 'score')

    result = 0

    for row_num, tree_row in enumerate(trees[1:-1]):
        for tree_num, tree in enumerate(tree_row[1:-1]):
            abs_row_num = row_num + 1
            abs_tree_num = tree_num + 1

            left = trees[abs_row_num][:abs_tree_num]
            right = trees[abs_row_num][abs_tree_num+1:]
            top = [t[abs_tree_num] for t in trees[:abs_row_num]]
            bottom = [t[abs_tree_num] for t in trees[abs_row_num+1:]]
            
            if puzzle_type == 'visible':
                if tree > max(left) or tree > max(right) or tree > max(top) or tree > max(bottom):
                    result += 1
            elif puzzle_type == 'score':
                range_left = get_range(tree, left[::-1])
                range_right = get_range(tree, right)
                range_top = get_range(tree, top[::-1])
                range_bottom = get_range(tree, bottom)

                score = range_left * range_right * range_top * range_bottom
                result = max(score, result)

    if puzzle_type == 'visible':
        x = len(trees[0])
        y = len(trees)
        result += 2 * x + 2 * y - 4

    return result


def solver(input_path, puzzle_type: str):

    trees = []

    with open(input_path, 'r') as puzzle:
        for line in puzzle.readlines():
            trees.append(line.strip())
    
    return num_visible(trees, puzzle_type)


if __name__ == '__main__':
    expected1 = 21
    result1 = solver('test_input', 'visible')
    assert result1 == expected1, f'Example 1 failed: {result1}'

    expected2 = 8
    result2 = solver('test_input', 'score')
    assert result2 == expected2, f'Example 2 failed: {result2}'

    print("Examples passed")
    print("Puzzle 1 answer:", solver('input', 'visible'))
    print("Puzzle 2 answer:", solver('input', 'score'))

