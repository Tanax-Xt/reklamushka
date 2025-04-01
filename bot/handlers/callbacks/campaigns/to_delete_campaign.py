from bot.config import bot
from bot.handlers.messages.start import start
from bot.services.campaigns import delete_campaign
from bot.texts import campaigns, menus


@bot.callback_query_handler(func=lambda call: call.data == "to_delete_campaign")
def to_delete_campaign(call):
    bot.answer_callback_query(call.id)

    msg = bot.send_message(call.message.chat.id, campaigns.delete_campaign_text, parse_mode="Markdown")

    bot.register_next_step_handler(msg, register_campaign_id)


def register_campaign_id(message):
    campaign_id = message.text

    msg = bot.send_message(message.chat.id, campaigns.delete_campaign_advertiser_id, parse_mode="Markdown")

    bot.register_next_step_handler(msg, register_advertiser_id, campaign_id)


def register_advertiser_id(message, campaign_id):
    status_code, response = delete_campaign(message.text, campaign_id)

    if status_code == 204:
        bot.send_message(
            message.chat.id,
            campaigns.successful_delete_campaign.format(id=message.text),
            parse_mode="Markdown",
        )
    else:
        bot.send_message(
            message.chat.id, menus.error_text.format(status_code=status_code, response=response), parse_mode="Markdown"
        )
    start(message)
