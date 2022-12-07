import random, logging

from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = '5889194200:AAGzo5kG_wBiXei_LWfVhdlpMnXQEAnyoC4'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
members_data = {}


def shuffle_members (members_id):
    random.shuffle(members_id)
    return members_id


def set_santa(members_dict):
    members_id = list(members_dict.keys())
    n = len(members_id)
    shuffle_members(members_id)
    print(members_id)
    id_pairs = []
    for i in range(n):
        if i == n-1:
            id_pairs.append([members_id[i], members_id[0]])
        else:
            id_pairs.append([members_id[i], members_id[i+1]])
    return id_pairs


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Здравствуйте!\nЯ бот Тайного Санты!\nВы участвуете в игре!")
    members_data[message.from_user.id] = [message.from_user.id, message.from_user.first_name]
    await message.answer(members_data)



@dp.message_handler(commands=['shuffle'])
async def shuffle_func(message: types.Message):
    pairs = set_santa(members_data)
    await message.reply("Я замешал список участников")
    await message.reply(str(pairs))


@dp.message_handler(commands=['pm_all'])
async def sending_func(message: types.Message):
    incoming_list = str(message.text).split()
    del incoming_list[0]
    if len(incoming_list) == 0:
        await message.reply('Вы не ввели список участников!')
    missing_participants = []
    unexpected_participants = []
    #await message.reply(incoming_list)
    santa_pairs = {}
    arr = []
    member_is_found = False
    member_in_list = False
    member_in_array = False
    for i, j in members_data.items():
        arr.append(j[1])
    for p in incoming_list:
        for k, v in members_data.items():  # Тут в k будет лежать id-шник игрока, в v - массив с айдишником и именем
            if p in arr:
                if v[1] in incoming_list:
                    member_in_list = True
                    member_in_array = True
                else:
                    unexpected_participants.append(v[1])
                    member_in_list = True
                    member_in_array = False
                    break
            elif p not in arr:
                missing_participants.append(p)
                member_in_list = True
                member_in_array = False
                break
    if (len(missing_participants) == 0) and (len(unexpected_participants) == 0):
        # Если этот список пустой, значит все игроки, которых мы ввели в pm_all, зарегистрированы
        id_pairs = set_santa(members_data)
    elif member_in_list and (not member_in_array):
        await message.reply('Unexpected participants: ' + str(unexpected_participants))
    else:
        await message.reply('Missing participants: ' + str(missing_participants))

@dp.message_handler()
async def exception_message(message: types.Message):
    user_message = message.text
    match user_message:
        case _:
            await message.answer('Сорян, я тебя не понял(')

if __name__ == '__main__':
    executor.start_polling(dp)