from bot.config import bot
from bot.keyboards.keyboards import start_menu
from bot.texts import menus


@bot.message_handler(commands=["start", "help"])
def start(message):
    bot.send_message(
        message.chat.id,
        menus.start_text.format(name=message.from_user.first_name),
        reply_markup=start_menu,
        parse_mode="Markdown",
    )
