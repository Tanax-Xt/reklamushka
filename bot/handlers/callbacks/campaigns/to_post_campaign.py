from bot.config import bot
from bot.handlers.messages.start import start
from bot.services.campaigns import post_campaign
from bot.texts import campaigns, menus


@bot.callback_query_handler(func=lambda call: call.data == "to_post_campaign")
def to_post_campaign(call):
    bot.answer_callback_query(call.id)

    msg = bot.send_message(call.message.chat.id, campaigns.get_advertiser_id_to_post_campaign, parse_mode="Markdown")

    bot.register_next_step_handler(msg, register_advertiser_id)


def register_advertiser_id(message):
    advertiser_id = message.text

    msg = bot.send_message(
        message.chat.id, campaigns.post_campaign_something.format(something="лимита показов"), parse_mode="Markdown"
    )

    bot.register_next_step_handler(msg, register_impressions_limit, advertiser_id)


def register_impressions_limit(message, advertiser_id):
    impressions_limit = message.text

    msg = bot.send_message(
        message.chat.id, campaigns.post_campaign_something.format(something="лимита кликов"), parse_mode="Markdown"
    )

    bot.register_next_step_handler(msg, register_clicks_limit, advertiser_id, impressions_limit)


def register_clicks_limit(message, advertiser_id, impressions_limit):
    clicks_limit = message.text

    msg = bot.send_message(
        message.chat.id, campaigns.post_campaign_something.format(something="стоимоси показа"), parse_mode="Markdown"
    )

    bot.register_next_step_handler(msg, register_cost_per_impression, advertiser_id, impressions_limit, clicks_limit)


def register_cost_per_impression(message, advertiser_id, impressions_limit, clicks_limit):
    cost_per_impression = message.text

    msg = bot.send_message(
        message.chat.id, campaigns.post_campaign_something.format(something="стоимости клика"), parse_mode="Markdown"
    )

    bot.register_next_step_handler(
        msg, register_cost_per_click, advertiser_id, impressions_limit, clicks_limit, cost_per_impression
    )


def register_cost_per_click(message, advertiser_id, impressions_limit, clicks_limit, cost_per_impression):
    cost_per_click = message.text

    msg = bot.send_message(
        message.chat.id, campaigns.post_campaign_something.format(something="названия"), parse_mode="Markdown"
    )

    bot.register_next_step_handler(
        msg, register_campaign_name, advertiser_id, impressions_limit, clicks_limit, cost_per_impression, cost_per_click
    )


def register_campaign_name(
    message, advertiser_id, impressions_limit, clicks_limit, cost_per_impression, cost_per_click
):
    campaign_name = message.text

    msg = bot.send_message(
        message.chat.id, campaigns.post_campaign_something.format(something="описания"), parse_mode="Markdown"
    )

    bot.register_next_step_handler(
        msg,
        register_campaign_text,
        advertiser_id,
        impressions_limit,
        clicks_limit,
        cost_per_impression,
        cost_per_click,
        campaign_name,
    )


def register_campaign_text(
    message, advertiser_id, impressions_limit, clicks_limit, cost_per_impression, cost_per_click, campaign_name
):
    campaign_text = message.text

    msg = bot.send_message(
        message.chat.id, campaigns.post_campaign_something.format(something="даты начала"), parse_mode="Markdown"
    )

    bot.register_next_step_handler(
        msg,
        register_campaign_start_date,
        advertiser_id,
        impressions_limit,
        clicks_limit,
        cost_per_impression,
        cost_per_click,
        campaign_name,
        campaign_text,
    )


def register_campaign_start_date(
    message,
    advertiser_id,
    impressions_limit,
    clicks_limit,
    cost_per_impression,
    cost_per_click,
    campaign_name,
    campaign_text,
):
    campaign_start_date = message.text

    msg = bot.send_message(
        message.chat.id, campaigns.post_campaign_something.format(something="даты окончания"), parse_mode="Markdown"
    )

    bot.register_next_step_handler(
        msg,
        register_campaign_end_date,
        advertiser_id,
        impressions_limit,
        clicks_limit,
        cost_per_impression,
        cost_per_click,
        campaign_name,
        campaign_text,
        campaign_start_date,
    )


def register_campaign_end_date(
    message,
    advertiser_id,
    impressions_limit,
    clicks_limit,
    cost_per_impression,
    cost_per_click,
    campaign_name,
    campaign_text,
    campaign_start_date,
):
    campaign_end_date = message.text

    msg = bot.send_message(
        message.chat.id,
        campaigns.post_campaign_something_target.format(something="пола ЦА (`MALE` / `FEMALE` / `ALL`)"),
        parse_mode="Markdown",
    )

    bot.register_next_step_handler(
        msg,
        register_target_gender,
        advertiser_id,
        impressions_limit,
        clicks_limit,
        cost_per_impression,
        cost_per_click,
        campaign_name,
        campaign_text,
        campaign_start_date,
        campaign_end_date,
    )


def register_target_gender(
    message,
    advertiser_id,
    impressions_limit,
    clicks_limit,
    cost_per_impression,
    cost_per_click,
    campaign_name,
    campaign_text,
    campaign_start_date,
    campaign_end_date,
):
    target_gender = message.text if message.text != "-" else None

    msg = bot.send_message(
        message.chat.id,
        campaigns.post_campaign_something_target.format(something="нижней планки возраста ЦА"),
        parse_mode="Markdown",
    )

    bot.register_next_step_handler(
        msg,
        register_target_age_from,
        advertiser_id,
        impressions_limit,
        clicks_limit,
        cost_per_impression,
        cost_per_click,
        campaign_name,
        campaign_text,
        campaign_start_date,
        campaign_end_date,
        target_gender,
    )


def register_target_age_from(
    message,
    advertiser_id,
    impressions_limit,
    clicks_limit,
    cost_per_impression,
    cost_per_click,
    campaign_name,
    campaign_text,
    campaign_start_date,
    campaign_end_date,
    target_gender,
):
    target_age_from = message.text if message.text != "-" else None

    msg = bot.send_message(
        message.chat.id,
        campaigns.post_campaign_something_target.format(something="верхней планки возраста ЦА"),
        parse_mode="Markdown",
    )

    bot.register_next_step_handler(
        msg,
        register_target_age_to,
        advertiser_id,
        impressions_limit,
        clicks_limit,
        cost_per_impression,
        cost_per_click,
        campaign_name,
        campaign_text,
        campaign_start_date,
        campaign_end_date,
        target_gender,
        target_age_from,
    )


def register_target_age_to(
    message,
    advertiser_id,
    impressions_limit,
    clicks_limit,
    cost_per_impression,
    cost_per_click,
    campaign_name,
    campaign_text,
    campaign_start_date,
    campaign_end_date,
    target_gender,
    target_age_from,
):
    target_age_to = message.text if message.text != "-" else None

    msg = bot.send_message(
        message.chat.id, campaigns.post_campaign_something_target.format(something="локации ЦА"), parse_mode="Markdown"
    )

    bot.register_next_step_handler(
        msg,
        register_target_location,
        advertiser_id,
        impressions_limit,
        clicks_limit,
        cost_per_impression,
        cost_per_click,
        campaign_name,
        campaign_text,
        campaign_start_date,
        campaign_end_date,
        target_gender,
        target_age_from,
        target_age_to,
    )


def register_target_location(
    message,
    advertiser_id,
    impressions_limit,
    clicks_limit,
    cost_per_impression,
    cost_per_click,
    campaign_name,
    campaign_text,
    campaign_start_date,
    campaign_end_date,
    target_gender,
    target_age_from,
    target_age_to,
):
    target_location = message.text if message.text != "-" else None

    status_code, response = post_campaign(
        advertiser_id,
        impressions_limit,
        clicks_limit,
        cost_per_impression,
        cost_per_click,
        campaign_name,
        campaign_text,
        campaign_start_date,
        campaign_end_date,
        target_gender,
        target_age_from,
        target_age_to,
        target_location,
    )

    if status_code == 200:
        bot.send_message(
            message.chat.id,
            """Компания успешно создана\n\n""" + campaigns.successful_get_campaign(response),
            parse_mode="Markdown",
        )
    else:
        bot.send_message(
            message.chat.id, menus.error_text.format(status_code=status_code, response=response), parse_mode="Markdown"
        )
    start(message)
