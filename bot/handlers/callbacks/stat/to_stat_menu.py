from bot.config import bot
from bot.keyboards.keyboards import stat_menu
from bot.texts import menus
from bot.texts.stat import where_get_grafana


@bot.callback_query_handler(func=lambda call: call.data == "to_stat_menu")
def to_stat_menu(call):
    bot.send_message(
        call.message.chat.id,
        f"{where_get_grafana}\n\n{menus.universal_text}",
        reply_markup=stat_menu,
        parse_mode="Markdown",
    )

    bot.answer_callback_query(call.id)
