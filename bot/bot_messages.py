# --------------------------------------------------------------------
START_CMD = "start"
PLAY_CMD = "play"
HELP_CMD = "help"
END_CMD = "end"


# --------------------------------------------------------------------
START_MSG = "Я - бот для игры в крестики-нолики.\n" \
            "Введите /help чтобы увидеть список команд"
HELP_MSG = "/start - включить бота\n" \
           "/help - показать справку\n" \
           "/play - начать игру\n" \
           "/end - завершить игру"

PLAY_MSG = "Выберите сторонy.\nКрестики ходят первыми"
END_GAME_MSG = "Вы успешно закончили игру.\nЧтобы начать новую игру, введите команду /play"
GAME_IS_NOT_YET_START_MSG = "Игра еще не начата или уже закончена, поэтому ее невозможно закончить." \
                            "\nЧтобы начать новую игру, введите команду /play"
GAME_IS_ALREADY_EXIST_MSG = "Вы уже начали одну игру. Чтобы начать новую надо закончить предыдущую" \
                            " (закончить можно с помощью команды /end"
CHOOSE_PC_LVL_MSG = "Выберите уровень компьютера"
PRESS_PLAY_FOR_START_NEW_GAME_MSG = "\nЧтобы начать новую игру, введите команду /play"
DRAW_MSG = "Ничья!"
ERROR_MSG = "Произошла непредвиденная ошибка"
WRONG_BUTTON_PRESSED_MSG = 'Вы нажали на уже занятую клетку. Нажимать можно только на свободные клетки. ' \
                           'Это сообщение автоматически удалится через 15 секунд'


# --------------------------------------------------------------------
PC_TURN_KEY = "pc_turn"
USER_TURN_KEY = "user_turn"
turn = {USER_TURN_KEY: 1, PC_TURN_KEY: 2}
sides = {0: ' ', 1: 'X', 2: 'O'}


# --------------------------------------------------------------------
PC_LVL_HARD_BUTTON_TEXT = 'Непобедимый'
PC_LVL_MEDIUM_BUTTON_TEXT = 'Средний'
PC_LVL_EASY_BUTTON_TEXT = 'Легкий'

PC_LVL_HARD_CB = 'hard_pc_lvl'
PC_LVL_MEDIUM_CB = 'medium_pc_lvl'
PC_LVL_EASY_CB = 'easy_pc_lvl'

pc_lvl_cb = {PC_LVL_EASY_CB: 3, PC_LVL_MEDIUM_CB: 2, PC_LVL_HARD_CB: 1}
pc_lvl_text = {1: PC_LVL_HARD_BUTTON_TEXT, 2: PC_LVL_MEDIUM_BUTTON_TEXT, 3: PC_LVL_EASY_BUTTON_TEXT}


# --------------------------------------------------------------------
USER_SIDE_X_BUTTON_TEXT = 'X'
USER_SIDE_O_BUTTON_TEXT = 'O'

USER_SIDE_X_CB = 'user_side_x'
USER_SIDE_O_CB = 'user_side_o'

user_side_cb = {USER_SIDE_X_CB: USER_TURN_KEY, USER_SIDE_O_CB: PC_TURN_KEY}


# --------------------------------------------------------------------
PVP_INLINE_KB_CB = 'pvp_callback'
SOLO_INLINE_KB_CB = "solo_callback"


# --------------------------------------------------------------------
PVP_GAME_INLINE_BUTTON_ID = '1'


# --------------------------------------------------------------------
message_visible_duration = 15


# --------------------------------------------------------------------
field_and_side_user_data_key = "field_and_side"
pc_lvl_user_data_key = "pc_lvl"


# --------------------------------------------------------------------
main_color = 'black'
end_line_color = 'red'
bkg_color = 'white'


# --------------------------------------------------------------------
type_win_main_diag = 'main diag'
type_win_side_diag = 'side diag'
type_win_horizontal_line = 'horizontal line'
type_win_vertical_line = 'vertical line'


# --------------------------------------------------------------------
def solo_end_game_msg(state, user_side, pc_lvl):
    # Сообщение после окончания соло игры
    end_game_msg = ''
    if state == -1:
        end_game_msg += DRAW_MSG
    elif state != 0:
        if state == user_side:
            end_game_msg += solo_game_user_win(pc_lvl)
        else:
            end_game_msg += solo_game_pc_win(pc_lvl)
    end_game_msg += PRESS_PLAY_FOR_START_NEW_GAME_MSG
    return end_game_msg


def solo_game_user_win(pc_lvl):
    return f'Вы победили {pc_lvl_text[pc_lvl]} уровень компьютера!'


def solo_game_pc_win(pc_lvl):
    return f'Компьютер уровня {pc_lvl_text[pc_lvl]} выиграл!'


def pvp_end_game_msg(state, players):
    # Сообщение после окончания pvp игры
    if state == -1:
        return DRAW_MSG
    else:
        return player_win_msg(players[state - 1], players[2 - state])


def player_win_msg(player1, player2):
    return f'Игрок {player1} выиграл у игрока {player2}!'


def field_to_str(field):
    # Конвертим поле в строку, чтобы его можно было передать в callback
    str_field = ''
    for i in range(3):
        for j in range(3):
            str_field += str(field[i][j])
            if i + j < 4:
                str_field += ' '
    return str_field


def form_callback_data_pvp_game(i, j, field, player1, player2, turn):
    return ' '.join([PVP_INLINE_KB_CB, str(i), str(j), field_to_str(field), player1, player2, str(turn)])


def parse_pvp_game_callback_data(data):
    # Парсим callback для pvp игры
    i, j = int(data[0]), int(data[1])
    field = [[], [], []]
    for k in range(3):
        for l in range(3):
            field[k].append(int(data[k * 3 + l + 2]))

    players = [data[11], data[12]]
    turn = int(data[13])
    return i, j, field, players, turn


def parse_solo_game_callback_data(data):
    return [int(i) for i in data]


def inline_field_button_text(cell):
    return sides[cell]


def form_callback_data_solo_game(i, j):
    return ' '.join([SOLO_INLINE_KB_CB, str(i), str(j)])


def form_pvp_game_inline_result_article_title_text(player):
    return f'Вызвать на дуэль {player}?'


def form_pvp_game_message_text(player1, player2):
    return f'Играют {player1} и {player2}'


def turn_msg(pc_lvl):
    return f'Вы играете с компьютером {pc_lvl_text[pc_lvl]}'
