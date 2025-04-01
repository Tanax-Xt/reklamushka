from telebot import types


def generate_click_ad_keyboard(ad_id):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Кликнуть по рекламе", callback_data=f"click:{ad_id}"))

    return keyboard
