import random
import logging

from aiogram import Bot, Dispatcher, executor, types


API_TOKEN = '5889194200:AAGzo5kG_wBiXei_LWfVhdlpMnXQEAnyoC4'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
members_data = {215689976: [215689976, 'Stan'], 179906609: [179906609, 'David'], 306300575: [306300575, 'Valery'], 874831756: [874831756, 'Dasha'], 185280118: [185280118, 'Alexey'], 828845247: [828845247, 'Мурад'], 663764121: [663764121, 'Tatiana F'], 228786824: [228786824, 'Дмитрий']}


def shuffle_members(members_id):
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


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    members_data[message.from_user.id] = [message.from_user.id, message.from_user.first_name]
    await message.reply("Здравствуйте!\nЯ бот Тайного Санты!\nВы участвуете в игре!")


@dp.message_handler(commands=['get_all'])
async def sending_func(message: types.Message):
    await message.reply(str(members_data))


@dp.message_handler(commands=['shake_my_secret_santa'])
async def sending_func(message: types.Message):
    if message.from_user.first_name == 'David':
        incoming_list = str(message.text).split(',')
        incoming_list[0] = ' '.join(incoming_list[0].split()[1:])
        if len(incoming_list) == 0:
            await message.reply('Вы не ввели список участников!')
        members_to_sort = {}
        missing_participants = []
        for p in incoming_list:
            member_is_found = False
            for k, v in members_data.items():
                if v[1] == p:
                    member_is_found = True
                    break
            if not member_is_found:
                missing_participants.append(p)
        if len(missing_participants) == 0:

            for o in incoming_list:
                for p, m in members_data.items():
                    if m[1] == o:
                        members_to_sort[p] = m
                        break
            sorted_pairs = set_santa(members_to_sort)
            for j in sorted_pairs:
                await bot.send_message(j[0], 'Ты Тайный Санта для: ' + str(members_data[j[1]][1]))
                break
        else:
            # Если тут есть хоть один чувак, значит начинать нельзя, нужно написать в чат, кого не хватает
            await message.reply('Missing participants: ' + str(missing_participants))
        with open('dance-dancing.gif', 'rb') as gif_file:
            await bot.send_animation(215689976, gif_file)
    else:
        await message.reply('Извините, но Вы не ведущий(')


@dp.message_handler()
async def exception_message(message: types.Message):
    user_message = message.text
    match user_message:
        case _:
            await message.answer('Сорян, я тебя не понял(')

if __name__ == '__main__':
    executor.start_polling(dp)
