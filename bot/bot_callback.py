import asyncio
import os

from telegram import Update
from telegram.ext import ContextTypes

from bot import main_algo, bot_inline_methods as bim, bot_messages as bm, bot_main


async def pvp_inline_callback(data, update: Update):
    # Получаем распарсенный callback
    i, j, field, players, turn = bm.parse_pvp_game_callback_data(data)

    # Проверяем, что нужный пользователь нажал на кнопку (если кто-то другой, то ничего не произойдет)
    if update.effective_user.name == players[turn - 1]:
        # Проверяем, что пользователь нажал на пустую клетку (если нажал не на пустую, то ничего не происходит)
        if field[i][j] == 0:
            # Записываем ход пользователя на поле
            main_algo.fill_field(field, i, j, turn)

            # Проверка поля на "закончилась игра или нет"
            current_state = main_algo.is_win(field)
            if current_state == 0:
                # Если не закончилась, то отрисовываем поле с новым ходом
                await update.callback_query.edit_message_reply_markup(
                    reply_markup=bim.form_inline_pvp_game_kb(field, players[0], players[1], 3 - turn))
            else:
                # Если закончилась, сообщаем об этом и убираем поле
                await update.callback_query.edit_message_reply_markup()
                await update.callback_query.edit_message_text(bm.pvp_end_game_msg(current_state, players))


async def choose_pc_lvl_inline_kb_callback(self, data, update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.edit_message_reply_markup()
    await update.callback_query.delete_message()
    # Записываем в контекст уровень компьютера, выбранного пользователем
    context.user_data[bm.pc_lvl_user_data_key] = bm.pc_lvl_cb[data[0]]
    # Дальше начинаем игру (для первого хода отдельная функция,
    # потому что там отправляется сообщение с отрисованным полем, а дальше это сообщение редактируется)
    await bot_main.Bot.first_turn(self, context.user_data[bm.field_and_side_user_data_key][1], update, context)


async def user_side_inline_kb_callback(data, update: Update, context: ContextTypes.DEFAULT_TYPE):
    # 1 - крестики, 2 - нолики
    await update.callback_query.edit_message_reply_markup()
    await update.callback_query.delete_message()
    # Генерируем пустое поле и записываем в контекст его и сторону, которую выбрал пользователь
    field = [[0] * 3 for _ in range(3)]
    context.user_data[bm.field_and_side_user_data_key] = [field, bm.user_side_cb[data[0]]]
    # Дальше даем пользователю выбрать уровень компьютера
    await bot_main.Bot.choose_pc_lvl(update, context)


async def user_turn_inline_kb_callback(self, data, update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Проверяем, что у нас в контексте пользователя есть поле для игры, то есть, что игра была начата.
    # Это для непредвиденных случаев
    if not context.user_data.get(bm.field_and_side_user_data_key):
        return

    field = context.user_data[bm.field_and_side_user_data_key][0]
    data = bm.parse_solo_game_callback_data(data)
    # Проверяем, что пользователь нажал на пустую клетку на поле
    if field[data[0]][data[1]] == 0:
        main_algo.fill_field(field, data[0], data[1], bm.turn[context.user_data[bm.field_and_side_user_data_key][1]])
        context.user_data[bm.field_and_side_user_data_key][0] = field

        # Проверка поля на "закончилась игра или нет"
        current_state = main_algo.is_win(field)
        if current_state == 0:  # Если не закончилась, то вызываем ход компьютера
            await bot_main.Bot.pc_turn(self, update, context)
            await update.callback_query.edit_message_reply_markup(bim.form_inline_solo_game_kb(field))
        else:  # Если закончилась, сообщаем об этом
            await update.callback_query.edit_message_reply_markup()
            await update.callback_query.delete_message()
            await bot_main.Bot.end_game_send_message(current_state, update, context)
    # Если пользователь нажал на уже занятую клетку, то отправляем сообщение, которое удалится через несколько секунд
    else:
        asyncio.create_task(bot_main.Bot.delete_wrong_button_press_message(
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text=bm.WRONG_BUTTON_PRESSED_MSG),
            bm.message_visible_duration))
