from bot.config import bot
from bot.handlers.callbacks.ads.to_click_ad import register_ad_id


@bot.callback_query_handler(func=lambda call: "click" in call.data)
def send__ad_menu(call):
    bot.answer_callback_query(call.id)

    ad_id = call.data.split(":")[1]

    register_ad_id(call.message, ad_id)
