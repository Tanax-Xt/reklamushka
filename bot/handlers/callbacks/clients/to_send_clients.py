from bot.config import bot
from bot.handlers.messages.start import start
from bot.services.client import send_client
from bot.texts import client, menus


@bot.callback_query_handler(func=lambda call: call.data == "to_send_clients")
def send_clients(call):
    bot.answer_callback_query(call.id)

    msg = bot.send_message(call.message.chat.id, client.send_client_menu, parse_mode="Markdown")

    bot.register_next_step_handler(msg, register_client_id)


def register_client_id(message):
    client_id = message.text

    msg = bot.send_message(
        message.chat.id, client.send_client_attribute.format(attribute="логин"), parse_mode="Markdown"
    )

    bot.register_next_step_handler(msg, register_client_login, client_id)


def register_client_login(message, client_id):
    login = message.text

    msg = bot.send_message(
        message.chat.id, client.send_client_attribute.format(attribute="возраст"), parse_mode="Markdown"
    )

    bot.register_next_step_handler(msg, register_client_age, client_id, login)


def register_client_age(message, client_id, login):
    age = message.text

    msg = bot.send_message(
        message.chat.id, client.send_client_attribute.format(attribute="локацию"), parse_mode="Markdown"
    )

    bot.register_next_step_handler(msg, register_client_location, client_id, login, age)


def register_client_location(message, client_id, login, age):
    location = message.text

    msg = bot.send_message(
        message.chat.id, client.send_client_attribute.format(attribute="пол (`MALE` / `FEMALE`)"), parse_mode="Markdown"
    )

    bot.register_next_step_handler(msg, register_client_gender, client_id, login, age, location)


def register_client_gender(message, client_id, login, age, location):
    gender = message.text

    status_code, response = send_client(client_id, login, age, location, gender)

    if status_code == 200:
        bot.send_message(
            message.chat.id,
            client.successful_response.format(
                action="добавлен",
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
