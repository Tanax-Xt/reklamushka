from bot.config import bot
from bot.handlers.messages.start import start
from bot.services.campaigns import patch_image_campaign
from bot.texts import campaigns, menus
from bot.texts.campaigns import successful_get_campaign


@bot.callback_query_handler(func=lambda call: call.data == "to_patch_image_campaign")
def to_patch_image_campaign(call):
    bot.answer_callback_query(call.id)

    msg = bot.send_message(
        call.message.chat.id, campaigns.patch_campaign_text.format(target="изображение"), parse_mode="Markdown"
    )

    bot.register_next_step_handler(msg, register_campaign_id)


def register_campaign_id(message):
    campaign_id = message.text

    msg = bot.send_message(message.chat.id, campaigns.get_campaign_advertiser_id, parse_mode="Markdown")

    bot.register_next_step_handler(msg, register_advertiser_id, campaign_id)


def register_advertiser_id(message, campaign_id):
    advertiser_id = message.text

    msg = bot.send_message(message.chat.id, campaigns.get_image, parse_mode="Markdown")

    bot.register_next_step_handler(msg, register_image, campaign_id, advertiser_id)


def register_image(message, campaign_id, advertiser_id):
    try:
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        status_code, response = patch_image_campaign(campaign_id, advertiser_id, downloaded_file)

        if status_code == 200:
            bot.send_message(
                message.chat.id,
                f"{campaigns.successful_patch_image_campaign.format(id=campaign_id)}\n\n{successful_get_campaign(response)}",
                parse_mode="Markdown",
            )
        else:
            bot.send_message(
                message.chat.id,
                menus.error_text.format(status_code=status_code, response=response),
                parse_mode="Markdown",
            )
    except:
        bot.send_message(message.chat.id, campaigns.incorrect_image, parse_mode="Markdown")
    start(message)
