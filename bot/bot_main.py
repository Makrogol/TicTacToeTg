import asyncio
import os

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, Message
from telegram.ext import Application, ContextTypes, CommandHandler, CallbackQueryHandler, InlineQueryHandler

from bot import bot_messages as bm, main_algo, bot_inline_methods as bim, bot_callback as bc, draw


class Bot:

    def __init__(self):
        self.bot = Application.builder() \
            .token(os.getenv("BOT_TOKEN")) \
            .build()
        self.bot.add_handler(CommandHandler(bm.START_CMD, self.start))
        self.bot.add_handler(CommandHandler(bm.PLAY_CMD, self.play))
        self.bot.add_handler(CommandHandler(bm.HELP_CMD, self.help))
        self.bot.add_handler(CommandHandler(bm.END_CMD, self.end))
        self.bot.add_handler(CallbackQueryHandler(self.call_back))
        self.bot.add_handler(InlineQueryHandler(self.inline_pvp_game))

    @staticmethod
    async def inline_pvp_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
        field = [[0] * 3 for _ in range(3)]
        # user1 - тот, который начал игру (вызвал бота) и он же будет первым ходить (за крестиков играть).
        # user2 - тот, кого вызвали на игру, он будет ходить вторым (играть за ноликов)
        user1 = update.effective_user.name
        user2 = update.inline_query.query.split()[0]

        await context.bot.answer_inline_query(update.inline_query.id,
                                              bim.form_inline_query_result(field, user1, user2, 1))

    async def call_back(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.callback_query.answer()
        data = update.callback_query.data.split()

        if data[0] == bm.PVP_INLINE_KB_CB:
            # Обработка нажатий на инлайн клавиатуре во время pvp игры
            await bc.pvp_inline_callback(data[1:], update)
            return

        if data[0] in list(bm.pc_lvl_cb.keys()):
            # Обработка нажатий на инлайн клавиатуру для выбора уровня бота
            await bc.choose_pc_lvl_inline_kb_callback(self, data, update, context)
            return

        if data[0] in list(bm.user_side_cb.keys()):
            # Обработка нажатий на инлайн клавиатуру для выбора стороны пользователя
            await bc.user_side_inline_kb_callback(data, update, context)
            return

        if data[0] == bm.SOLO_INLINE_KB_CB:
            # Обработка нажатий на инлайн клавиатуру для хода пользователя
            await bc.user_turn_inline_kb_callback(self, data[1:], update, context)
            return

        else:
            # Дефолт на случай чего-то непредвиденного (убирается инлайн клавиатура и выводится сообщение об ошибке)
            await update.callback_query.edit_message_reply_markup()
            await context.bot.send_message(update.effective_chat.id, text=bm.ERROR_MSG)
            return

    @staticmethod
    async def end_game_send_message(current_state: int, update: Update, context: ContextTypes.DEFAULT_TYPE):
        # Если игра закончилась, то выводим соответствующее сообщение
        # Отрисовываем конечное поле картинкой, для хроников
        draw.paint_field(context.user_data[bm.field_and_side_user_data_key][0], current_state)
        pc_lvl = context.user_data[bm.pc_lvl_user_data_key]
        user_side = bm.turn[context.user_data[bm.field_and_side_user_data_key][1]]
        await context.bot.send_photo(chat_id=update.effective_chat.id,
                                     caption=bm.solo_end_game_msg(current_state, user_side, pc_lvl),
                                     photo='field.jpg')
        os.remove(path="field.jpg")
        context.user_data.pop(bm.field_and_side_user_data_key)

    @staticmethod
    async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await context.bot.send_message(chat_id=update.effective_chat.id, text=bm.START_MSG)

    @staticmethod
    async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await context.bot.send_message(chat_id=update.effective_chat.id, text=bm.HELP_MSG)

    @staticmethod
    async def end(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if context.user_data.get(bm.field_and_side_user_data_key):
            # Если игра была начата, то заканчиваем ее
            context.user_data.pop(bm.field_and_side_user_data_key)
            await context.bot.send_message(chat_id=update.effective_chat.id, text=bm.END_GAME_MSG)
        else:
            # Если игра еще не была начата
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text=bm.GAME_IS_NOT_YET_START_MSG)

    @staticmethod
    async def play(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if context.user_data.get(bm.field_and_side_user_data_key):
            # Если игра уже была начата, то сообщаем об этом
            await context.bot.send_message(update.effective_chat.id, text=bm.GAME_IS_ALREADY_EXIST_MSG)
            return

        # Иначе начинаем новую игру и даем пользователю выбрать сторону
        inline_kb_user_play_side = InlineKeyboardMarkup(
            [[
                InlineKeyboardButton(text=bm.USER_SIDE_X_BUTTON_TEXT, callback_data=bm.USER_SIDE_X_CB),
                InlineKeyboardButton(text=bm.USER_SIDE_O_BUTTON_TEXT, callback_data=bm.USER_SIDE_O_CB)
            ]]
        )
        await context.bot.send_message(update.effective_chat.id, text=bm.PLAY_MSG,
                                       reply_markup=inline_kb_user_play_side)

    @staticmethod
    async def choose_pc_lvl(update: Update, context: ContextTypes.DEFAULT_TYPE):
        # Даем пользователю выбрать уровень бота
        inline_kb_choose_pc_lvl = InlineKeyboardMarkup(
            [[
                InlineKeyboardButton(text=bm.PC_LVL_EASY_BUTTON_TEXT, callback_data=bm.PC_LVL_EASY_CB),
                InlineKeyboardButton(text=bm.PC_LVL_MEDIUM_BUTTON_TEXT, callback_data=bm.PC_LVL_MEDIUM_CB),
                InlineKeyboardButton(text=bm.PC_LVL_HARD_BUTTON_TEXT, callback_data=bm.PC_LVL_HARD_CB)
            ]]
        )

        await context.bot.send_message(update.effective_chat.id, text=bm.CHOOSE_PC_LVL_MSG,
                                       reply_markup=inline_kb_choose_pc_lvl)

    async def first_turn(self, turn: str, update: Update, context: ContextTypes.DEFAULT_TYPE):
        # Если ход компьютера, то компьютер делает ход
        if turn == bm.PC_TURN_KEY:
            await self.pc_turn(update, context)

        # Отрисовываем поле и даем пользователю сделать ход (если компьютер уже сделал ход,
        # то отрисовываем поле, учитывая этот ход. Иначе отрисовываем пустое поле)
        field = context.user_data[bm.field_and_side_user_data_key][0]
        pc_lvl = context.user_data[bm.pc_lvl_user_data_key]
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text=bm.turn_msg(pc_lvl),
                                       reply_markup=bim.form_inline_solo_game_kb(field))

    async def pc_turn(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        field = context.user_data[bm.field_and_side_user_data_key][0]
        pc_lvl = context.user_data[bm.pc_lvl_user_data_key]
        user_side = bm.turn[context.user_data[bm.field_and_side_user_data_key][1]]
        pc_side = 3 - user_side
        # Вызываем ход компьютера от 3 - user_side потому что компьютер играет за противоположную
        # относительно пользователя сторону (либо 1, либо 2. поскольку в сумме они дают 3,
        # то сделав 3 - "сторона пользователя" получим сторону компьютера)

        main_algo.pc_turn(field, pc_side, pc_lvl)
        context.user_data[bm.field_and_side_user_data_key][0] = field
        current_state = main_algo.is_win(field)

        # Проверяем игру на конец
        if current_state != 0:
            await self.end_game_send_message(current_state, update, context)

    @staticmethod
    async def delete_wrong_button_press_message(message: Message, delay: int):
        await asyncio.sleep(delay)
        await message.delete()
