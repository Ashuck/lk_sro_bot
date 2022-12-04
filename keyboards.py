from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton



HELO_BOARD = ReplyKeyboardMarkup(True)
HELO_BOARD.add(
    KeyboardButton("Поиск организации")
)
HELO_BOARD.add(
    KeyboardButton("Личный кабинет")
)





# reg_board.add(
#     KeyboardButton(SRO_TYPES[1])
# )

# abort_kbr = InlineKeyboardMarkup()
# abort_kbr.add(
#     InlineKeyboardButton("Продолжить", callback_data="resume")
# )
# abort_kbr.add(
#     InlineKeyboardButton("Отменить", callback_data="cancel")
# )

# succes_kbr = InlineKeyboardMarkup()
# succes_kbr.add(
#     InlineKeyboardButton("Подтвержаю", callback_data="success")
# )
# succes_kbr.add(
#     InlineKeyboardButton("Нет", callback_data="drop")
# )

# city_kbr = ReplyKeyboardMarkup(True)
# for cities_list in CITIES:
#     city_kbr.add(*[KeyboardButton(city) for city in cities_list])