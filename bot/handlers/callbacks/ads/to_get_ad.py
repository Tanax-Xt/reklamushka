from bot.config import bot
from bot.handlers.messages.start import start
from bot.keyboards.services import generate_click_ad_keyboard
from bot.services.ad import get_ad, get_ad_image
from bot.services.advertiser import get_advertiser_by_id
from bot.texts import ad, menus


@bot.callback_query_handler(func=lambda call: call.data == "to_get_ad")
def to_get_ad(call):
    bot.answer_callback_query(call.id)

    msg = bot.send_message(call.message.chat.id, ad.get_ad_client_id_text, parse_mode="Markdown")

    bot.register_next_step_handler(msg, register_client_id)


def register_client_id(message):
    client_id = message.text
    status_code, response = get_ad(client_id)

    if status_code == 200:
        send_ad_to_client(message, response)
    else:
        bot.send_message(
            message.chat.id, menus.error_text.format(status_code=status_code, response=response), parse_mode="Markdown"
        )
    start(message)


def send_ad_to_client(message, data_response):
    advertiser_status_code, advertiser_response = get_advertiser_by_id(data_response["advertiser_id"])

    is_message_send = False

    if "image_url" in data_response and data_response["image_url"] is not None:
        status_code, image_response = get_ad_image(data_response["advertiser_id"], data_response["ad_id"])

        if status_code == 200:
            bot.send_photo(
                message.chat.id,
                image_response,
                caption=ad.send_ad_to_client.format(
                    title=data_response["ad_title"],
                    text=data_response["ad_text"],
                    advertiser_name=advertiser_response["name"],
                    advertiser_id=data_response["advertiser_id"],
                    ad_id=data_response["ad_id"],
                ),
                reply_markup=generate_click_ad_keyboard(data_response["ad_id"]),
                parse_mode="Markdown",
            )
            is_message_send = True

    if not is_message_send:
        bot.send_message(
            message.chat.id,
            ad.send_ad_to_client.format(
                title=data_response["ad_title"],
                text=data_response["ad_text"],
                advertiser_name=advertiser_response["name"],
                advertiser_id=data_response["advertiser_id"],
                ad_id=data_response["ad_id"],
            ),
            reply_markup=generate_click_ad_keyboard(data_response["ad_id"]),
            parse_mode="Markdown",
        )
