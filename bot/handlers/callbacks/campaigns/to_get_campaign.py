from bot.config import bot
from bot.handlers.messages.start import start
from bot.services.campaigns import get_campaign
from bot.texts import campaigns, menus


@bot.callback_query_handler(func=lambda call: call.data == "to_get_campaign")
def to_get_campaign(call):
    bot.answer_callback_query(call.id)

    msg = bot.send_message(
        call.message.chat.id, menus.get_by_id.format(model="рекламной кампании", which="которую"), parse_mode="Markdown"
    )

    bot.register_next_step_handler(msg, register_campaign_id)


def register_campaign_id(message):
    campaign_id = message.text

    msg = bot.send_message(message.chat.id, campaigns.get_campaign_advertiser_id, parse_mode="Markdown")

    bot.register_next_step_handler(msg, register_advertiser_id, campaign_id)


def register_advertiser_id(message, campaign_id):
    status_code, response = get_campaign(message.text, campaign_id)

    if status_code == 200:
        bot.send_message(
            message.chat.id,
            campaigns.successful_get_campaign(response),
            parse_mode="Markdown",
        )
    else:
        bot.send_message(
            message.chat.id, menus.error_text.format(status_code=status_code, response=response), parse_mode="Markdown"
        )
    start(message)
