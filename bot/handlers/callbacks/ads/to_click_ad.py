from bot.config import bot
from bot.handlers.messages.start import start
from bot.services.ad import click_ad
from bot.texts import ad, menus


@bot.callback_query_handler(func=lambda call: call.data == "to_click_ad")
def post_ad_click(call):
    bot.answer_callback_query(call.id)

    msg = bot.send_message(call.message.chat.id, ad.click_ad_id_text, parse_mode="Markdown")

    bot.register_next_step_handler(msg, register_ad_id)


def register_ad_id(message, ad_id=None):
    ad_id = ad_id if ad_id is not None else message.text

    msg = bot.send_message(message.chat.id, ad.click_client_id_text, parse_mode="Markdown")

    bot.register_next_step_handler(msg, register_client_id, ad_id)


def register_client_id(message, ad_id):
    client_id = message.text
    status_code, response = click_ad(ad_id, client_id)

    if status_code == 204:
        bot.send_message(
            message.chat.id,
            ad.successful_click.format(ad_id=ad_id, client_id=client_id),
            parse_mode="Markdown",
        )
    else:
        bot.send_message(
            message.chat.id, menus.error_text.format(status_code=status_code, response=response), parse_mode="Markdown"
        )
    start(message)
