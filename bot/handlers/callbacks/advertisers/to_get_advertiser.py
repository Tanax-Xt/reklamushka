from bot.config import bot
from bot.handlers.messages.start import start
from bot.services.advertiser import get_advertiser_by_id
from bot.texts import advertiser, menus


@bot.callback_query_handler(func=lambda call: call.data == "to_get_advertiser")
def get_advertiser_menu(call):
    bot.answer_callback_query(call.id)

    msg = bot.send_message(
        call.message.chat.id, menus.get_by_id.format(model="рекламодателя", which="которого"), parse_mode="Markdown"
    )

    bot.register_next_step_handler(msg, register_advertiser_id)


def register_advertiser_id(message):
    status_code, response = get_advertiser_by_id(message.text)

    if status_code == 200:
        bot.send_message(
            message.chat.id,
            advertiser.successful_get_advertiser_response.format(
                action="получен",
                id=response["advertiser_id"],
                name=response["name"],
            ),
            parse_mode="Markdown",
        )
    else:
        bot.send_message(
            message.chat.id, menus.error_text.format(status_code=status_code, response=response), parse_mode="Markdown"
        )
    start(message)
