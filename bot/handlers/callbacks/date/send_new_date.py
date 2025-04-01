from bot.config import bot
from bot.handlers.messages.start import start
from bot.services.date import send_new_date
from bot.texts import date, menus


@bot.callback_query_handler(func=lambda call: call.data == "send_new_date")
def new_date_menu(call):
    bot.answer_callback_query(call.id)

    msg = bot.send_message(call.message.chat.id, date.new_date_text, parse_mode="Markdown")

    bot.register_next_step_handler(msg, register_new_date)


def register_new_date(message):
    status_code, response = send_new_date(message.text)

    if status_code == 200:
        bot.send_message(message.chat.id, date.date_changed.format(date=response), parse_mode="Markdown")
    else:
        bot.send_message(
            message.chat.id, menus.error_text.format(status_code=status_code, response=response), parse_mode="Markdown"
        )
    start(message)
