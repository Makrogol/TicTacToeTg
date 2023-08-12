from telegram import InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardMarkup, InlineKeyboardButton

from bot import bot_messages as bm


def form_inline_query_result(field, player1, player2, turn):
    # Формируем инлайн ответ на инлайн вызов бота
    return [InlineQueryResultArticle(id=bm.PVP_GAME_INLINE_BUTTON_ID,
                                     title=bm.form_pvp_game_inline_result_article_title_text(player2),
                                     input_message_content=InputTextMessageContent(
                                         bm.form_pvp_game_message_text(player1, player2)),
                                     reply_markup=form_inline_pvp_game_kb(field, player1, player2, turn))]


def form_inline_pvp_game_kb(field, player1, player2, turn):
    # Формируем инлайн клавиатуру для pvp игры
    inline_kb = []

    for i in range(3):
        inline_kb.append([])
        for j in range(3):
            inline_kb[i].append(InlineKeyboardButton(text=bm.inline_field_button_text(field[i][j]),
                                                     callback_data=bm.form_callback_data_pvp_game(i, j, field, player1,
                                                                                                  player2, turn)))
    return InlineKeyboardMarkup(inline_kb)


def form_inline_solo_game_kb(field):
    # Формируем инлайн клавиатуру для соло игры
    inline_kb = []

    for i in range(3):
        inline_kb.append([])
        for j in range(3):
            inline_kb[i].append(InlineKeyboardButton(text=bm.inline_field_button_text(field[i][j]),
                                                     callback_data=bm.form_callback_data_solo_game(i, j)))
    return InlineKeyboardMarkup(inline_kb)
