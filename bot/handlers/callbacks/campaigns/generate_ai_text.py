from bot.config import bot
from bot.handlers.messages.start import start
from bot.services.campaigns import get_generate_ai_text
from bot.texts import campaigns, menus


@bot.callback_query_handler(func=lambda call: call.data == "generate_ai_text")
def generate_ai_text(call):
    bot.answer_callback_query(call.id)

    msg = bot.send_message(call.message.chat.id, campaigns.generate_ai_text, parse_mode="Markdown")

    bot.register_next_step_handler(msg, register_advertiser_name)


def register_advertiser_name(message):
    advertiser_name = message.text
    msg = bot.send_message(message.chat.id, campaigns.generate_ai_text_get_product, parse_mode="Markdown")

    bot.register_next_step_handler(msg, register_product, advertiser_name)


def register_product(message, advertiser_name):
    status_code, response = get_generate_ai_text(advertiser_name, message.text)

    if status_code == 200:
        bot.send_message(
            message.chat.id,
            campaigns.successful_generate_ai_text.format(
                title=response["title"],
                text=response["text"],
            ),
            parse_mode="Markdown",
        )
    else:
        bot.send_message(
            message.chat.id, menus.error_text.format(status_code=status_code, response=response), parse_mode="Markdown"
        )
    start(message)
