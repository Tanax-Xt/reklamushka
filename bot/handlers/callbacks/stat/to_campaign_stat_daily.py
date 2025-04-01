from bot.config import bot
from bot.handlers.messages.start import start
from bot.services.stat import get_campaign_stat_daily
from bot.texts import menus, stat
from bot.texts.stat import generate_daily_stat_text


@bot.callback_query_handler(func=lambda call: call.data == "to_campaign_stat_daily")
def to_campaign_stat_daily(call):
    bot.answer_callback_query(call.id)

    msg = bot.send_message(
        call.message.chat.id, stat.to_stat_daily.format(model="рекламной кампании"), parse_mode="Markdown"
    )

    bot.register_next_step_handler(msg, register_campaign_id)


def register_campaign_id(message):
    status_code, response = get_campaign_stat_daily(message.text)

    if status_code == 200:
        bot.send_message(
            message.chat.id,
            generate_daily_stat_text(name="рекламной кампании", id=message.text, response=response),
            parse_mode="Markdown",
        )
    else:
        bot.send_message(
            message.chat.id, menus.error_text.format(status_code=status_code, response=response), parse_mode="Markdown"
        )
    start(message)
