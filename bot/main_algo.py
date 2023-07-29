import functools


class turn:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.defeat = 0
        self.win = 0
        self.draw = 0


def is_win(field) -> int:
    # 0 - не закончена игра, -1 - ничья, 1 - победили крестики, 2 - победили нолики
    for i in range(3):
        if field[i][0] == field[i][1] and field[i][1] == field[i][2] and field[i][0] != 0:
            return field[i][0]
        if field[0][i] == field[1][i] and field[1][i] == field[2][i] and field[0][i] != 0:
            return field[0][i]
    if (field[1][1] == field[2][2] and field[2][2] == field[0][0] and field[0][0] != 0) or (
            field[0][2] == field[1][1] and field[1][1] == field[2][0] and field[1][1] != 0):
        return field[1][1]

    for i in range(3):
        for j in range(3):
            if field[i][j] == 0:
                return 0
    return -1


def fill_field(field, x, y, type: int):
    field[x][y] = type


def analyze(field, results, type: int):
    wins = is_win(field)
    if wins == -1:
        results[0] += 1
        return
    elif wins == 1 or wins == 2:
        results[wins] += 1
        return
    for i in range(3):
        for j in range(3):
            if field[i][j] == 0:
                field[i][j] = type
                analyze(field, results, 3 - type)
                field[i][j] = 0
    return


def fill_result(results, i, res, x, y, type):
    sum = res[0] + res[1] + res[2]
    results[i].x = x
    results[i].y = y
    results[i].defeat = int(res[3 - type] / sum * 10 ** 4)
    results[i].draw = int(res[0] / sum * 10 ** 4)
    results[i].win = int(res[type] / sum * 10 ** 4)


def find_best_turn(arr, size, pc_lvl) -> turn:
    # min_def = turn()
    # min_def.defeat = 10 ** 4
    copy_arr = []
    for i in range(size):
        is_item = False
        for j in range(len(copy_arr)):
            if arr[i].draw == copy_arr[j].draw and arr[i].win == copy_arr[j].win and arr[i].defeat == copy_arr[j].defeat:
                is_item = True
                break
        if not is_item:
            copy_arr.append(arr[i])

    def compare(it1, it2):
        if it1.defeat < it2.defeat:
            return -1
        elif it1.defeat == it2.defeat:
            if it1.win < it2.win:
                return 1
            else:
                return -1
        else:
            return 0

    copy_arr.sort(key=functools.cmp_to_key(compare))
    if len(copy_arr) >= pc_lvl:
        return copy_arr[pc_lvl - 1]
    else:
        return copy_arr[len(copy_arr) - 1]

    # for i in range(size):
    #     if arr[i].defeat < min_def.defeat or arr[i].defeat == min_def.defeat and arr[i].win > min_def.win:
    #         min_def = arr[i]
    # return min_def


def pc_turn(field, type: int, pc_lvl) -> (int, int):
    arr = [turn() for _ in range(9)]
    res = [0 for _ in range(3)]
    r = 0

    for i in range(3):
        for j in range(3):
            if field[i][j] == 0:
                copy_field = [field[i].copy() for i in range(3)]
                copy_field[i][j] = type

                analyze(copy_field, res, 3 - type)

                fill_result(arr, r, res, i, j, type)
                r += 1

                res = [0 for _ in range(3)]

    best_turn = find_best_turn(arr, r, pc_lvl)

    fill_field(field, best_turn.x, best_turn.y, type)
    return best_turn.x, best_turn.y
