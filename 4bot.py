import asyncio
from aiogram import Bot, Dispatcher, executor, filters, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import datetime


token = '1943338034:AAHGWuvQUsBfgeei0jS6D1LPCyg9hrgsy38'
chat_id = -1001340410503

bot = Bot(token)
dp = Dispatcher(bot)

url = 'https://t.me/cryptobubblle'

messages_datetime = {}
warned = []

@dp.message_handler()
async def gg(message):
    print(message)
    if (message.chat.type == 'group') or (message.chat.type == 'supergroup'):
        user_state = await bot.get_chat_member(chat_id=chat_id, user_id=message['from'].id)
        user_state = user_state['status']
        if (user_state == "member" or user_state == "creator"):
            print("YES")
        else:
            print("NO")
            if message['from'].id in warned:
                pass
            else:
                btn = InlineKeyboardButton("📩 Подписаться на канал", url = url)
                markup = InlineKeyboardMarkup()
                markup.add(btn)
                msg = await message.reply(f"Чтобы посылать сообщения в эту группу, вы должны быть подписаны на канал @cryptobubblle", reply_markup=markup)
                warned.append(message['from'].id)
                time = datetime.datetime.now()
                time = time + datetime.timedelta(seconds = 5)
                messages_datetime[msg['from'].id] = [msg, time, message['from'].id]
            await message.delete()

async def timer():
    while True:
        for carry in messages_datetime.copy().items():
            dt = carry[1][1]
            msg = carry[1][0]
            id_ = carry[1][2]
            now = datetime.datetime.now()
            if now > dt:
                warned.remove(id_)
                del messages_datetime[msg['from'].id]
                await msg.delete()
                print('Deleted!')
            await asyncio.sleep(1)
        await asyncio.sleep(1)

async def on_startup(_):
    asyncio.create_task(timer())
    pass

if __name__ == '__main__':
    while True:
        try:
            executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
        except Exception as e:
            pass