import random, logging

from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = '5889194200:AAGzo5kG_wBiXei_LWfVhdlpMnXQEAnyoC4'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
member_data = {'member_id': [['member_id'], ['member_name']]}
pairs = {}

def shuffle_members (members_id):
    random.shuffle(members_id)
    return members_id

def set_santa (member_data):
    members_id = dict.keys(member_data)
    n = len(members_id)
    print(members_id)
    shuffle_members(members_id)
    """for i in range(n):
        if i == n-1:
            pairs[members_id[n-1]] = members_id[0]
        else:
            pairs[members_id[i]] = members_id[i+1]
    return pairs"""

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Здравствуйте!\nЯ бот Тайного Санты!\nВы участвуете в игре!")
    member_data['member_id'].append(message.from_user.id)
    member_data[message.from_user.id] = [[message.from_user.id], [message.from_user.first_name]]
    await message.answer(member_data)

@dp.message_handler(commands=['shuffle'])
async def shuffle_func(message: types.Message):
    set_santa(member_data)
    await message.reply("Я замешал список участников")
    await message.reply(pairs)

"""@dp.message_handler(commands=['i_am_santa_for'])
async def dispatch_func(message: types.Message):
    santa_pairs = set_santa(members_list)
    i=0
    while message.from_user.first_name != santa_pairs[i]:
        i=i+1
    await message.reply("Ты Тайный санта для: ", {gifted_one[message.from_user.name]})"""

@dp.message_handler(commands=['pm_all'])
async def sending_func(message: types.Message):
    pairs = set_santa(members_list)
    """for i in range(len(members_id)):
        howdi_str = 'Дарова, ' + members_list[i]
        await bot.send_message(members_id[i], howdi_str)"""
    for i in range(len(members_list)):
        member_argument = str(members_list[i])
        howdi_str = 'Ты Тайный Санта для: ' + str(pairs[member_argument])
        await bot.send_message(members_id[i], howdi_str)

@dp.message_handler()
async def exception_message(message: types.Message):
    user_message = message.text
    match user_message:
        case _:
            await message.answer('Сорян, я тебя не понял(')

if __name__ == '__main__':
    executor.start_polling(dp)