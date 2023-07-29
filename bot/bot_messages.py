START_CMD = "start"
PLAY_CMD = "play"
HELP_CMD = "help"
END_CMD = "end"

START_MSG = "Я - бот для игры в крестики-нолики.\n" \
            "Введите /help чтобы увидеть список команд"
HELP_MSG = "/start - включить бота\n" \
           "/help - показать справку\n" \
           "/play - начать игру за крестиков (право первого хода) или за ноликов " \
           "(право второго хода)\n" \
           "/end - завершить игру"
WRONG_BUTTON_PRESSED_MSG = "Нажмите на кнопку, на которой нарисован символ, за который вы играете" \
                           " (крестик или нолик).\nОстальные поля уже заняты"
TURN_MSG = "Ваш ход.\nНажмите на кнопку. Вы сходите на соответствующую клетку на поле."
PLAY_MSG = "Выберите сторонy.\nКрестики ходят первыми"
END_GAME_MSG = "Вы успешно закончили игру.\nЧтобы начать новую игрую введите команду /play"
GAME_IS_NOT_YET_START_MSG = "Игра еще не начата или уже закончена, поэтому ее невозможно закончить." \
                            "\nЧтобы начать новую игрую введите команду /play"
GAME_IS_ALREADY_EXIST_MSG = "Вы уже начали одну игру. Чтобы начать новую надо закончить предыдущую" \
                            " (закончить можно с помощью команды /end"
CHOOSE_PC_LVL_MSG = "Выберите уровень компьютера\n3 - самый легкий, 2 - средний, 1 - непобедимый"
PRESS_PLAY_FOR_START_NEW_GAME_MSG = "\nЧтобы начать новую игру, введите команду /play"
CURRENT_FIELD_STATE_MSG = "Текущее состояние поля\n"
DRAW_MSG = "\nНичья!"
USER_WIN_MSG = "\nВы победили!"
PC_WIN_MSG = "\nЯ победил!"
ERROR_MSG = "Произошла непредвиденная ошибка"


# def field_in_str(field):
#     field_str = ''
#     for i in range(3):
#         for j in range(3):
#             if field[i][j] == 0:
#                 field_str += "  "
#             elif field[i][j] == 1:
#                 field_str += "X"
#             elif field[i][j] == 2:
#                 field_str += "O"
#
#             if j != 2:
#                 field_str += "|"
#         field_str += "\n"
#         if i != 2:
#             field_str += "-+-+-\n"
#     field_str += "\n"
#     return field_str


def before_user_turn_msg(field):
    return TURN_MSG + '\n'


def game_state_msg(field, state, user_side):
    end_game_msg = CURRENT_FIELD_STATE_MSG
    if state == -1:
        end_game_msg += DRAW_MSG
    elif state != 0:
        if state == user_side:
            end_game_msg += USER_WIN_MSG
        else:
            end_game_msg += PC_WIN_MSG
    end_game_msg += PRESS_PLAY_FOR_START_NEW_GAME_MSG
    return end_game_msg
