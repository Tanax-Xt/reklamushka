from telebot import types

from bot.keyboards import buttons

start_menu = types.InlineKeyboardMarkup()
start_menu.add(buttons.to_clients_menu)
start_menu.add(buttons.to_advisers_menu)
start_menu.add(buttons.to_campaigns_menu)
start_menu.add(buttons.to_ad_menu)
start_menu.add(buttons.to_stat_menu)
start_menu.add(buttons.to_date_menu)

date_menu = types.InlineKeyboardMarkup()
date_menu.add(buttons.send_new_date)
date_menu.add(buttons.to_start_menu)

clients_menu = types.InlineKeyboardMarkup()
clients_menu.add(buttons.to_get_client)
clients_menu.add(buttons.to_send_clients)
clients_menu.add(buttons.to_start_menu)

advertisers_menu = types.InlineKeyboardMarkup()
advertisers_menu.add(buttons.to_get_advertiser)
advertisers_menu.add(buttons.to_send_advertisers)
advertisers_menu.add(buttons.to_send_ml_score)
advertisers_menu.add(buttons.to_start_menu)

campaign_menu = types.InlineKeyboardMarkup()
campaign_menu.add(buttons.to_switch_moderation)
campaign_menu.add(buttons.generate_ai_text)
campaign_menu.add(buttons.to_post_campaign)
campaign_menu.add(buttons.to_get_campaigns)
campaign_menu.add(buttons.to_get_campaign)
campaign_menu.add(buttons.to_put_target_campaign)
campaign_menu.add(buttons.to_patch_image_campaign)
campaign_menu.add(buttons.to_delete_campaign)
campaign_menu.add(buttons.to_start_menu)

moderation_menu = types.InlineKeyboardMarkup()
moderation_menu.add(buttons.on_moderation)
moderation_menu.add(buttons.off_moderation)
moderation_menu.add(buttons.to_start_menu)

stat_menu = types.InlineKeyboardMarkup()
stat_menu.add(buttons.to_campaign_stat)
stat_menu.add(buttons.to_campaign_stat_daily)
stat_menu.add(buttons.to_advertiser_stat)
stat_menu.add(buttons.to_advertiser_stat_daily)
stat_menu.add(buttons.to_start_menu)

ad_menu = types.InlineKeyboardMarkup()
ad_menu.add(buttons.to_get_ad)
ad_menu.add(buttons.to_click_ad)
ad_menu.add(buttons.to_start_menu)
