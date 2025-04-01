from bot.config import bot
from bot.handlers.messages.start import start
from bot.services.campaigns import put_campaign
from bot.texts import campaigns, menus


@bot.callback_query_handler(func=lambda call: call.data == "to_put_target_campaign")
def to_put_target_campaign(call):
    bot.answer_callback_query(call.id)

    msg = bot.send_message(call.message.chat.id, campaigns.id_to_put_campaign, parse_mode="Markdown")

    bot.register_next_step_handler(msg, register_campaign_id)


def register_campaign_id(message):
    campaign_id = message.text

    msg = bot.send_message(message.chat.id, campaigns.get_campaign_advertiser_id, parse_mode="Markdown")

    bot.register_next_step_handler(msg, register_advertiser_id, campaign_id)


def register_advertiser_id(message, campaign_id):
    advertiser_id = message.text

    msg = bot.send_message(
        message.chat.id,
        campaigns.post_campaign_something_target.format(something="пола ЦА (`MALE` / `FEMALE` / `ALL`)"),
        parse_mode="Markdown",
    )

    bot.register_next_step_handler(msg, register_target_gender, campaign_id, advertiser_id)


def register_target_gender(message, campaign_id, advertiser_id):
    target_gender = message.text if message.text != "-" else None

    msg = bot.send_message(
        message.chat.id,
        campaigns.post_campaign_something_target.format(something="нижней планки возраста ЦА"),
        parse_mode="Markdown",
    )

    bot.register_next_step_handler(
        msg,
        register_target_age_from,
        campaign_id,
        advertiser_id,
        target_gender,
    )


def register_target_age_from(message, campaign_id, advertiser_id, target_gender):
    target_age_from = message.text if message.text != "-" else None

    msg = bot.send_message(
        message.chat.id,
        campaigns.post_campaign_something_target.format(something="верхней планки возраста ЦА"),
        parse_mode="Markdown",
    )

    bot.register_next_step_handler(
        msg, register_target_age_to, campaign_id, advertiser_id, target_gender, target_age_from
    )


def register_target_age_to(message, campaign_id, advertiser_id, target_gender, target_age_from):
    target_age_to = message.text if message.text != "-" else None

    msg = bot.send_message(
        message.chat.id, campaigns.post_campaign_something_target.format(something="локации ЦА"), parse_mode="Markdown"
    )

    bot.register_next_step_handler(
        msg,
        register_target_location,
        campaign_id,
        advertiser_id,
        target_gender,
        target_age_from,
        target_age_to,
    )


def register_target_location(
    message,
    campaign_id,
    advertiser_id,
    target_gender,
    target_age_from,
    target_age_to,
):
    target_location = message.text if message.text != "-" else None

    status_code, response = put_campaign(
        campaign_id, advertiser_id, target_gender, target_age_from, target_age_to, target_location
    )

    if status_code == 200:
        bot.send_message(
            message.chat.id,
            """Таргетинг успешно обновлен\n\n""" + campaigns.successful_get_campaign(response),
            parse_mode="Markdown",
        )
    else:
        bot.send_message(
            message.chat.id, menus.error_text.format(status_code=status_code, response=response), parse_mode="Markdown"
        )
    start(message)
