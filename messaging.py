"""
This is a echo bot.
It echoes any incoming text messages.
"""

import logging

from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = '5889194200:AAGzo5kG_wBiXei_LWfVhdlpMnXQEAnyoC4'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
members_list = []
pairs = {}


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("Здравствуйте!\nЯ бот Тайного Санты!\nВы хотите участвовать в игре?")



@dp.message_handler()
async def add_user(message: types.Message):
    user_message = message.text
    match user_message:
        case 'Да' | 'да':
            await message.answer('УРА!!!\nВы теперь участвуете!')
            members_list.append(message.from_user.first_name)
            await message.answer(members_list)
        case 'Нет' | 'нет':
            await message.answer('Тогда нам с тобой не по пути(')
        case 'всё' | 'Всё' | 'все' | 'Все':
            await message.answer(members_list)
        case _:
            await message.answer('Сорян, я тебя не понял(')



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)