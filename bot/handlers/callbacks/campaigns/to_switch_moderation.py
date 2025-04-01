from bot.config import bot
from bot.keyboards.keyboards import moderation_menu
from bot.texts.campaigns import switch_moderation_mode


@bot.callback_query_handler(func=lambda call: call.data == "to_switch_moderation")
def to_switch_moderation(call):
    bot.answer_callback_query(call.id)

    bot.send_message(call.message.chat.id, switch_moderation_mode, reply_markup=moderation_menu, parse_mode="Markdown")
