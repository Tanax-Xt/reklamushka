from bot.config import bot
from bot.handlers.messages.start import start
from bot.services.campaigns import get_campaigns
from bot.texts import campaigns, menus


@bot.callback_query_handler(func=lambda call: call.data == "to_get_campaigns")
def to_get_campaigns(call):
    bot.answer_callback_query(call.id)

    msg = bot.send_message(call.message.chat.id, campaigns.get_advertiser_id_to_get_campaigns, parse_mode="Markdown")

    bot.register_next_step_handler(msg, register_advertiser_id)


def register_advertiser_id(message):
    status_code, response = get_campaigns(message.text)

    if status_code == 200:
        bot.send_message(
            message.chat.id,
            "\n\n".join([campaigns.successful_get_campaign(data) for data in response]),
            parse_mode="Markdown",
        )
    else:
        bot.send_message(
            message.chat.id, menus.error_text.format(status_code=status_code, response=response), parse_mode="Markdown"
        )
    start(message)
