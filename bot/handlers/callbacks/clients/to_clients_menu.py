from bot.config import bot
from bot.keyboards.keyboards import clients_menu
from bot.texts import menus


@bot.callback_query_handler(func=lambda call: call.data == "to_clients_menu")
def client_menu(call):
    bot.send_message(call.message.chat.id, menus.universal_text, reply_markup=clients_menu, parse_mode="Markdown")

    bot.answer_callback_query(call.id)
