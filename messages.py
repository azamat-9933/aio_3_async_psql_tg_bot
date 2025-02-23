messages = {
    "message_1": f"""<b>Здравствуйте 😊
Выберите язык 🌐
Hello 😊
Please choose the language 🌐</b>""",
    "message_2": {
        "ru": f"""<b>Вы выбрали русский язык интерфейса 🇷🇺</b>""",
        "en": f"""<b>You have chase the english interface language 🇬🇧</b>"""
    },
    "message_3": {
        "ru": f"""<b>Напишите своё полное имя ⬇</b>""",
        "en": f"""<b>Enter your full name ⬇</b>"""
    },
    "message_4": {
        "ru": f"""<b>Отправьте нам контакты для обратной связи 📲</b>""",
        "en": f"""<b>Send us your phone number for feedback 📲</b>"""
    },
    "message_5": {
        "ru": f"""<b>Вы отклонили ваши данные ! Вам придется перепройти регистрацию !</b>""",
        "en": f"""<b>You have rejected your data ! You will have to re-register !</b>"""
    },
    "message_6": {
        "ru": f"""<b>Вы успешно прошли регистрацию 📋</b>""",
        "en": f"""<b>You have successfully registered 📋</b>"""
    },
    "message_7": {
        "ru": f"""<b>Чтобы пользоватся нашим телеграм ботом вам объязательно нужно пройти регистрацию 📋</b>""",
        "en": f"""<b>To use our Telegram bot you need to register 📋</b>"""
    },
    "message_8": {
        "ru": f"""<b>Основное меню ⚡
Выберите опцию ⬇</b>""",
        "en": f"""<b>Main menu ⚡
Choose option ⬇</b>"""
    },
}


async def generate_submit_message(full_name, phone_number, language):
    text = f""""""
    if language == "ru":
        text = f"""<b>Подтвердите свои данные:
Полное имя: {full_name}
Номер телефона: {phone_number}</b>"""
    elif language == "en":
        text = f"""<b>Submit your data:
Full name: {full_name}
Phone number: {phone_number}</b>"""

    return text
