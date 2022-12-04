import random, logging

from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = '5889194200:AAGzo5kG_wBiXei_LWfVhdlpMnXQEAnyoC4'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
members_list = []
members_id = []
pairs = {}

def shuffle_members (members_list):
    random.shuffle(members_list)
    return members_list

def set_santa (members_list):
    n = len(members_list)
    for i in range(n):
        if i == n-1:
            pairs[members_list[n-1]] = members_list[0]
        else:
            pairs[members_list[i]] = members_list[i+1]
    return pairs

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Здравствуйте!\nЯ бот Тайного Санты!\nВы хотите участвовать в игре?")

@dp.message_handler(commands=['shuffle'])
async def shuffle_func(message: types.Message):
    shuffle_members(members_list)
    await message.reply("Я замешал список участников")

"""@dp.message_handler(commands=['i_am_santa_for'])
async def dispatch_func(message: types.Message):
    santa_pairs = set_santa(members_list)
    i=0
    while message.from_user.first_name != santa_pairs[i]:
        i=i+1
    await message.reply("Ты Тайный санта для: ", {gifted_one[message.from_user.name]})"""

@dp.message_handler(commands=['pm_all'])
async def sending_func(message: types.Message):
    """for i in range(len(members_id)):
        howdi_str = 'Дарова, ' + members_list[i]
        await bot.send_message(members_id[i], howdi_str)"""

    for i in range(len(members_id)):
       howdi_str = 'Ты Тайный Санта для: ' + str(pairs[members_list[i]])
       await bot.send_message(members_id[i], howdi_str)

@dp.message_handler()
async def add_user(message: types.Message):
    user_message = message.text
    match user_message:
        case 'Да' | 'да':
            await message.answer('УРА!!!\nВы теперь участвуете!')
            members_list.append(message.from_user.first_name)
            members_id.append(message.from_user.id)
            await message.answer(members_list)
            await message.answer(members_id)
        case 'Нет' | 'нет':
            await message.answer('Тогда нам с тобой не по пути(')
        case 'всё' | 'Всё' | 'все' | 'Все':
            await message.answer(members_list)
        case _:
            await message.answer('Сорян, я тебя не понял(')

if __name__ == '__main__':
    executor.start_polling(dp)