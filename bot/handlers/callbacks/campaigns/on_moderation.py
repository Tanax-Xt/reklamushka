from bot.config import bot
from bot.handlers.callbacks.to_start_menu import call_start
from bot.services.campaigns import post_moderation_mode
from bot.texts import menus
from bot.texts.campaigns import moderation_mode_switch_success


@bot.callback_query_handler(func=lambda call: call.data == "on_moderation")
def on_moderation(call):
    bot.answer_callback_query(call.id)

    status_code, response = post_moderation_mode(True)

    if status_code == 200:
        bot.send_message(
            call.message.chat.id,
            moderation_mode_switch_success.format(mode="включена"),
            parse_mode="Markdown",
        )
    else:
        bot.send_message(
            call.message.chat.id,
            menus.error_text.format(status_code=status_code, response=response),
            parse_mode="Markdown",
        )
    call_start(call)
