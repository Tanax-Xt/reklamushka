from bot.config import bot
from bot.keyboards import keyboards
from bot.services.date import get_current_date
from bot.texts import date


@bot.callback_query_handler(func=lambda call: call.data == "to_date_menu")
def date_menu(call):
    bot.send_message(
        call.message.chat.id,
        date.date_text.format(date=get_current_date()),
        reply_markup=keyboards.date_menu,
        parse_mode="Markdown",
    )

    bot.answer_callback_query(call.id)
