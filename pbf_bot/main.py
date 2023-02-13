from aiogram import Bot, Dispatcher, executor, types
from utils.config import BOT_TOKEN
import utils.api_utils as au

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
utils = au.Utils()


@dp.message_handler(commands=['start'])
async def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("ввести код")
    btn2 = types.KeyboardButton("Инструкция")
    markup.add(btn1, btn2)
    await bot.send_message(message.chat.id,
                           text="Привет, {0.first_name}!".format(
                               message.from_user), reply_markup=markup)


@dp.message_handler(content_types=['text'])
async def func(message):
    if message.text == "ввести код":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        back = types.KeyboardButton("Вернуться в главное меню")
        markup.add(back)

        await bot.send_message(message.chat.id, text="Введите серию и код через пробел", reply_markup=markup)

        check = None
        # Wait for user to input code
        while not check:
            try:
                check = (await dp.wait_for_message(chat_id=message.from_user.id, timeout=60)).text

            except:
                pass

        await check_code(check, message)

    elif message.text == "Инструкция":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        back = types.KeyboardButton("Вернуться в главное меню")
        markup.add(back)
        await bot.send_message(message.chat.id, text="вава", reply_markup=markup)

    elif message.text == "Вернуться в главное меню":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton("ввести код")
        button2 = types.KeyboardButton("Инструкция")
        markup.add(button1, button2)
        await bot.send_message(message.chat.id, text="Вы вернулись в главное меню", reply_markup=markup)
    else:
        await bot.send_message(message.chat.id, text="где-то произошла ошибка")


async def check_code(check, message):
        pbf_data = utils.check_code(series=check.split()[0], number=check.split()[1])
        if pbf_data and 'items' in pbf_data:

            pbf_data = pbf_data['items'][0]
            await bot.send_message(message.chat.id, f"""
                                    "series": {pbf_data['series']},
                                    "number": {pbf_data['number']},
                                    "regionName": {pbf_data['regionName']},
                                    "organization": {pbf_data['organization']},
                                    "productGroup": {pbf_data['productGroup']},
                                    "productName": {pbf_data['productName']},
                                    "volume": {pbf_data['volume']},
                                    "degree": {pbf_data['degree']},...""")
        else:
            await bot.send_message(message.chat.id, "Invalid code")


if __name__ == '__main__':
    executor.start_polling(dp)
