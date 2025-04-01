from bot.config import bot
from bot.handlers.messages.start import start
from bot.services.stat import get_advertiser_stat
from bot.texts import menus, stat


@bot.callback_query_handler(func=lambda call: call.data == "to_advertiser_stat")
def to_advertiser_stat(call):
    bot.answer_callback_query(call.id)

    msg = bot.send_message(call.message.chat.id, stat.to_stat.format(model="рекламодателя"), parse_mode="Markdown")

    bot.register_next_step_handler(msg, register_advertiser_id)


def register_advertiser_id(message):
    status_code, response = get_advertiser_stat(message.text)

    if status_code == 200:
        bot.send_message(
            message.chat.id,
            stat.successful_get_stat.format(
                name="рекламодателя",
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
