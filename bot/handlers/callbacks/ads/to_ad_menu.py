from bot.config import bot
from bot.keyboards.keyboards import ad_menu
from bot.texts import menus


@bot.callback_query_handler(func=lambda call: call.data == "to_ad_menu")
def send__ad_menu(call):
    bot.send_message(call.message.chat.id, menus.universal_text, reply_markup=ad_menu, parse_mode="Markdown")

    bot.answer_callback_query(call.id)
