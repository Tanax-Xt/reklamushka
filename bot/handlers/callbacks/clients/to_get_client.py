from bot.config import bot
from bot.handlers.messages.start import start
from bot.services.client import get_client_by_id
from bot.texts import client, menus


@bot.callback_query_handler(func=lambda call: call.data == "to_get_client")
def get_client_menu(call):
    bot.answer_callback_query(call.id)

    msg = bot.send_message(
        call.message.chat.id, menus.get_by_id.format(model="клиента", which="которого"), parse_mode="Markdown"
    )

    bot.register_next_step_handler(msg, register_client_id)


def register_client_id(message):
    status_code, response = get_client_by_id(message.text)

    if status_code == 200:
        bot.send_message(
            message.chat.id,
            client.successful_response.format(
                action="получен",
                id=response["client_id"],
                login=response["login"],
                age=response["age"],
                location=response["location"],
                gender=response["gender"],
            ),
            parse_mode="Markdown",
        )
    else:
        bot.send_message(
            message.chat.id, menus.error_text.format(status_code=status_code, response=response), parse_mode="Markdown"
        )
    start(message)
