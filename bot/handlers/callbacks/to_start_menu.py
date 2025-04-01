from bot.config import bot
from bot.keyboards.keyboards import start_menu
from bot.texts import menus


@bot.callback_query_handler(func=lambda call: call.data == "to_start_menu")
def call_start(call):
    bot.send_message(
        call.message.chat.id,
        menus.start_text.format(name=call.from_user.first_name),
        reply_markup=start_menu,
        parse_mode="Markdown",
    )

    bot.answer_callback_query(call.id)
