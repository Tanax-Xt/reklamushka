from telebot import types

to_start_menu = types.InlineKeyboardButton(text="В главное меню", callback_data="to_start_menu")

to_clients_menu = types.InlineKeyboardButton(text="Управление клиентами", callback_data="to_clients_menu")
to_advisers_menu = types.InlineKeyboardButton(text="Управление рекламодателями", callback_data="to_advertiser_menu")
to_campaigns_menu = types.InlineKeyboardButton(
    text="Управление рекламными кампаниями", callback_data="to_campaigns_menu"
)
to_ad_menu = types.InlineKeyboardButton(text="Рекламные объявления", callback_data="to_ad_menu")
to_stat_menu = types.InlineKeyboardButton(text="Получить статистику", callback_data="to_stat_menu")
to_date_menu = types.InlineKeyboardButton(text="Управление датой", callback_data="to_date_menu")

send_new_date = types.InlineKeyboardButton(text="Установить новую дату", callback_data="send_new_date")

to_get_client = types.InlineKeyboardButton(text="Получить клиента по ID", callback_data="to_get_client")
to_send_clients = types.InlineKeyboardButton(text="Добавить или обновить клиента", callback_data="to_send_clients")

to_get_advertiser = types.InlineKeyboardButton(text="Получить рекламодателя по ID", callback_data="to_get_advertiser")
to_send_advertisers = types.InlineKeyboardButton(
    text="Добавить или обновить рекламодателя", callback_data="to_send_advertisers"
)
to_send_ml_score = types.InlineKeyboardButton(text="Добавить ML-score", callback_data="to_send_ml_score")

to_post_campaign = types.InlineKeyboardButton(text="Добавить рекламную кампанию", callback_data="to_post_campaign")
to_get_campaigns = types.InlineKeyboardButton(
    text="Получить все рекламные кампании рекламодателя", callback_data="to_get_campaigns"
)
to_switch_moderation = types.InlineKeyboardButton(
    text="Переключить режим модерации", callback_data="to_switch_moderation"
)
on_moderation = types.InlineKeyboardButton(text="Включить модерацию", callback_data="on_moderation")
off_moderation = types.InlineKeyboardButton(text="Выключить модерацию", callback_data="off_moderation")
generate_ai_text = types.InlineKeyboardButton(
    text="Сгенерировать текст для рекламной кампании", callback_data="generate_ai_text"
)
to_get_campaign = types.InlineKeyboardButton(text="Получить рекламную кампанию", callback_data="to_get_campaign")
to_put_target_campaign = types.InlineKeyboardButton(
    text="Обновить таргет рекламной кампании", callback_data="to_put_target_campaign"
)
to_patch_image_campaign = types.InlineKeyboardButton(
    text="Обновить изображение рекламной кампании", callback_data="to_patch_image_campaign"
)
to_delete_campaign = types.InlineKeyboardButton(text="Удалить рекламную кампанию", callback_data="to_delete_campaign")

to_campaign_stat = types.InlineKeyboardButton(
    text="Получить статистику по рекламной кампании", callback_data="to_campaign_stat"
)
to_campaign_stat_daily = types.InlineKeyboardButton(
    text="Получить статистику по рекламной кампании по дням", callback_data="to_campaign_stat_daily"
)
to_advertiser_stat = types.InlineKeyboardButton(
    text="Получить статистику по рекламодателю", callback_data="to_advertiser_stat"
)
to_advertiser_stat_daily = types.InlineKeyboardButton(
    text="Получить статистику по рекламодателю по дням", callback_data="to_advertiser_stat_daily"
)

to_get_ad = types.InlineKeyboardButton(text="Получить рекламное объявление", callback_data="to_get_ad")
to_click_ad = types.InlineKeyboardButton(text="Клинкуть по рекламному объявления", callback_data="to_click_ad")
