from bot.config import bot
from bot.handlers.messages.start import start
from bot.services.stat import get_campaign_stat
from bot.texts import menus, stat


@bot.callback_query_handler(func=lambda call: call.data == "to_campaign_stat")
def to_campaign_stat(call):
    bot.answer_callback_query(call.id)

    msg = bot.send_message(call.message.chat.id, stat.to_stat.format(model="рекламной кампании"), parse_mode="Markdown")

    bot.register_next_step_handler(msg, register_campaign_id)


def register_campaign_id(message):
    status_code, response = get_campaign_stat(message.text)

    if status_code == 200:
        bot.send_message(
            message.chat.id,
            stat.successful_get_stat.format(
                name="рекламной кампании",
                id=message.text,
                impressions_count=response["impressions_count"],
                clicks_count=response["clicks_count"],
                conversion=response["conversion"],
                spent_impressions=response["spent_impressions"],
                spent_clicks=response["spent_clicks"],
                spent_total=response["spent_total"],
            ),
            parse_mode="Markdown",
        )
    else:
        bot.send_message(
            message.chat.id, menus.error_text.format(status_code=status_code, response=response), parse_mode="Markdown"
        )
    start(message)
