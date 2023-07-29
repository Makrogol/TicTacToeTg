import os

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, ContextTypes, CommandHandler, CallbackQueryHandler

from bot import bot_messages, main_algo, draw


class Bot:
    def __init__(self):
        self.bot = Application.builder() \
            .token(os.getenv("BOT_TOKEN")) \
            .build()
        self.bot.add_handler(CommandHandler(bot_messages.START_CMD, self.start))
        self.bot.add_handler(CommandHandler(bot_messages.PLAY_CMD, self.play))
        self.bot.add_handler(CommandHandler(bot_messages.HELP_CMD, self.help))
        self.bot.add_handler(CommandHandler(bot_messages.END_CMD, self.end))
        self.bot.add_handler(CallbackQueryHandler(self.turn_call_back))

    async def turn_call_back(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.callback_query.answer()
        await update.callback_query.edit_message_reply_markup()

        if len(update.callback_query.data) == 1:
            # Обработка нажатий на инлайн клавиатуру для выбора уровня бота
            context.user_data["pc_lvl"] = int(update.callback_query.data)
            await self.game(context.user_data["field_and_side"][1], update, context)
            return

        if len(update.callback_query.data) == 2:
            # Обработка нажатий на инлайн клавиатуру для выбора стороны пользователя
            field = [[0] * 3 for _ in range(3)]
            # 1 - крестики, 2 - нолики
            if update.callback_query.data == 'XX':
                user_side = 1
            elif update.callback_query.data == 'OO':
                user_side = 2
            else:
                await context.bot.send_message(update.effective_chat.id, text=bot_messages.ERROR_MSG)
            context.user_data["field_and_side"] = [field, user_side]
            await self.choose_pc_lvl(update, context)
            return

        if len(update.callback_query.data) == 5:
            # Обработка нажатий на инлайн клавиатуру для хода пользователя
            data = [int(i) for i in update.callback_query.data.split()]
            if data[2] != context.user_data["field_and_side"][1]:
                # Если пользователь нажал на кнопку, на которой не было текста (просто пустая, она нужна для структуры)
                await context.bot.send_message(update.effective_chat.id, text=bot_messages.WRONG_BUTTON_PRESSED_MSG)
                await self.game(1, update, context)
            else:
                field = context.user_data["field_and_side"][0]
                main_algo.fill_field(field, data[0], data[1], context.user_data["field_and_side"][1])
                # await context.bot.send_message(update.effective_chat.id,
                #                                text=bot_messages.user_turn_msg(field, data[0], data[1]))
                context.user_data["field_and_side"][0] = field
                current_state = main_algo.is_win(field)
                # Проверка поля на "закончилась игра или нет"
                if current_state == 0:
                    # Если не закончилась, то вызываем ход компьютера
                    await self.game(2, update, context)
                else:
                    # Если закончилась, сообщаем об этом
                    await self.end_game_send_message(current_state, update, context)
        else:
            await context.bot.send_message(update.effective_chat.id, text=bot_messages.ERROR_MSG)

    @staticmethod
    async def end_game_send_message(current_state: int, update: Update, context: ContextTypes.DEFAULT_TYPE):
        # Если игра закончилась, то выводим соответствующее сообщение
        field = context.user_data["field_and_side"][0]
        draw.paint_field(field)
        await context.bot.send_photo(chat_id=update.effective_chat.id,
                                     caption=bot_messages.game_state_msg(field, current_state,
                                                                         context.user_data["field_and_side"][
                                                                             1]), photo='field.jpg')
        os.remove(path="field.jpg")
        context.user_data.pop("field_and_side")

    @staticmethod
    async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await context.bot.send_message(chat_id=update.effective_chat.id, text=bot_messages.START_MSG)

    @staticmethod
    async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await context.bot.send_message(chat_id=update.effective_chat.id, text=bot_messages.HELP_MSG)

    @staticmethod
    async def end(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if context.user_data.get("field_and_side"):
            context.user_data.pop("field_and_side")
            await context.bot.send_message(chat_id=update.effective_chat.id, text=bot_messages.END_GAME_MSG)
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text=bot_messages.GAME_IS_NOT_YET_START_MSG)

    @staticmethod
    async def play(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if context.user_data.get("field_and_side"):
            # Если игра уже была начата, то сообщаем об этом
            await context.bot.send_message(update.effective_chat.id, text=bot_messages.GAME_IS_ALREADY_EXIST_MSG)
            return

        # Иначе начинаем новую игру и даем пользователю выбрать сторону
        inline_kb_user_play_side = InlineKeyboardMarkup(
            [[InlineKeyboardButton(text='X', callback_data='XX'),
              InlineKeyboardButton(text='O', callback_data='OO')]])
        await context.bot.send_message(update.effective_chat.id, text=bot_messages.PLAY_MSG,
                                       reply_markup=inline_kb_user_play_side)

    @staticmethod
    async def choose_pc_lvl(update: Update, context: ContextTypes.DEFAULT_TYPE):
        # Даем пользователю выбрать уровень бота
        inline_kb_choose_pc_lvl = InlineKeyboardMarkup(
            [[InlineKeyboardButton(text='3', callback_data='3'),
              InlineKeyboardButton(text='2', callback_data='2'),
              InlineKeyboardButton(text='1', callback_data='1')]])
        await context.bot.send_message(update.effective_chat.id, text=bot_messages.CHOOSE_PC_LVL_MSG,
                                       reply_markup=inline_kb_choose_pc_lvl)

    async def game(self, turn: int, update: Update, context: ContextTypes.DEFAULT_TYPE):
        dict = {1: "user_turn", 2: "pc_turn"}
        if dict[turn] == "user_turn":
            # Если ход пользователя, то выводим поле и даем ему сделать ход
            field = context.user_data["field_and_side"][0]
            user_side = context.user_data["field_and_side"][1]
            sides = {0: ' ', 1: 'X', 2: 'O'}
            # inline_kb = [[InlineKeyboardButton(text=sides[user_side * int(field[i][j] == 0)],
            #                                    callback_data=[i * 3 + j, user_side * int(field[i][j] == 0)]) for j in
            #               field[i]] for i in range(3)]

            inline_kb = [[], [], []]
            for i in range(3):
                for j in range(3):
                    inline_kb[i].append(InlineKeyboardButton(text=sides[user_side * int(field[i][j] == 0)],
                                                             callback_data=f'{i} {j} '
                                                                           f'{user_side * int(field[i][j] == 0)}'))
            draw.paint_field(field)
            await context.bot.send_photo(chat_id=update.effective_chat.id,
                                         caption=bot_messages.before_user_turn_msg(field),
                                         reply_markup=InlineKeyboardMarkup(inline_kb), photo="field.jpg")
            os.remove(path="field.jpg")
        elif dict[turn] == "pc_turn":
            # Если ход компьютера, то компьютер делает ход
            await self.pc_turn(update, context)
        else:
            await context.bot.send_message(update.effective_chat.id, text=bot_messages.ERROR_MSG)

    async def pc_turn(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        field = context.user_data["field_and_side"][0]
        # Вызываем ход компьютера от 3 - context.user_data... потому что компьютер играет за противоположную
        # относительно пользователя сторону (либо 1, либо 2. поскольку в сумме они дают 3,
        # то сделав 3 - "сторона пользователя" получим сторону компьютера)
        main_algo.pc_turn(field, 3 - context.user_data["field_and_side"][1], context.user_data["pc_lvl"])
        # await context.bot.send_message(chat_id=update.effective_chat.id,
        #                                text=bot_messages.pc_turn_msg(field,
        #                                                              pc_turn_x, pc_turn_y))
        context.user_data["field_and_side"][0] = field
        current_state = main_algo.is_win(field)

        # Проверяем игру на конец
        if current_state != 0:
            await self.end_game_send_message(current_state, update, context)
        else:
            await self.game(1, update, context)
