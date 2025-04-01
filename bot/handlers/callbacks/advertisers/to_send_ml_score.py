from bot.config import bot
from bot.handlers.messages.start import start
from bot.services.advertiser import send_ml_score
from bot.texts import advertiser, menus


@bot.callback_query_handler(func=lambda call: call.data == "to_send_ml_score")
def get_advertiser_menu(call):
    bot.answer_callback_query(call.id)

    msg = bot.send_message(call.message.chat.id, advertiser.add_id.format(model="рекламодателя"), parse_mode="Markdown")

    bot.register_next_step_handler(msg, register_advertiser_id)


def register_advertiser_id(message):
    advertiser_id = message.text

    msg = bot.send_message(message.chat.id, advertiser.add_id.format(model="клиента"), parse_mode="Markdown")

    bot.register_next_step_handler(msg, register_client_id, advertiser_id)


def register_client_id(message, advertiser_id):
    client_id = message.text

    msg = bot.send_message(
        message.chat.id,
        advertiser.add_ml_score.format(advertiser_id=advertiser_id, client_id=client_id),
        parse_mode="Markdown",
    )

    bot.register_next_step_handler(msg, register_ml_score, advertiser_id, client_id)


def register_ml_score(message, advertiser_id, client_id):
    ml_score = message.text

    status_code, response = send_ml_score(advertiser_id, client_id, ml_score)

    if status_code == 200:
        bot.send_message(
            message.chat.id,
            advertiser.successful_send_ml_score_response.format(
                advertiser_id=response["advertiser_id"], client_id=response["client_id"], ml_score=response["score"]
            ),
            parse_mode="Markdown",
        )
    else:
        bot.send_message(
            message.chat.id, menus.error_text.format(status_code=status_code, response=response), parse_mode="Markdown"
        )
    start(message)
