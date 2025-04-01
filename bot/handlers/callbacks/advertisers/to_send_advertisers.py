from bot.config import bot
from bot.handlers.messages.start import start
from bot.services.advertiser import send_advertiser
from bot.texts import advertiser, menus


@bot.callback_query_handler(func=lambda call: call.data == "to_send_advertisers")
def send_advertisers(call):
    bot.answer_callback_query(call.id)

    msg = bot.send_message(call.message.chat.id, advertiser.send_advertiser_menu, parse_mode="Markdown")

    bot.register_next_step_handler(msg, register_advertiser_id)


def register_advertiser_id(message):
    advertiser_id = message.text

    msg = bot.send_message(
        message.chat.id, advertiser.send_advertiser_attribute.format(attribute="название"), parse_mode="Markdown"
    )

    bot.register_next_step_handler(msg, register_advertiser_name, advertiser_id)


def register_advertiser_name(message, advertiser_id):
    name = message.text

    status_code, response = send_advertiser(advertiser_id, name)

    if status_code == 200:
        bot.send_message(
            message.chat.id,
            advertiser.successful_get_advertiser_response.format(
                action="добавлен",
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
