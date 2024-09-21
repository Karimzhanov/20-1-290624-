from aiogram import Bot, Dispatcher,  types
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, BotCommand
from config import token 
import requests, time, asyncio, logging

bot= Bot(token=token)
dp = Dispatcher()
logging.basicConfig(level=logging.INFO)

monitoring = False
chat_id = None


async def get_btc_price():
    url = 'https://api.binance.com/api/v3/avgPrice?symbol=BTCUSDT'
    response = requests.get(url=url).json()
    price = response.get('price')
    if price:
        return f'Стоимость биткоина на {time.ctime()}, {price}'
    else:
        return f'Не удалось получить цену биткоина'


async def monitor_btc_price():
    global monitoring
    while monitoring:
        message = await get_btc_price()
        await bot.send_message(chat_id, message)
        await asyncio.sleep(10)  

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(f'Привет, {message.from_user.full_name}')

@dp.message(Command('btc'))
async def btc(message: Message):
    global chat_id, monitoring
    chat_id = message.chat.id
    if not monitoring:
        monitoring = True
        await message.answer("Начало мониторинга")
        asyncio.create_task(monitor_btc_price())  

        await message.answer("Мониторинг уже запущен!")

@dp.message(Command('stop'))
async def stop(message: Message):
    global monitoring
    if monitoring:
        monitoring = False
        await message.answer("Мониторинг цены остановлен")
    else:
        await message.answer("Мониторинг уже остановлен")

async def on_startup():
    await bot.set_my_commands([
        BotCommand(command="/start", description='Запустить бота'),
        BotCommand(command="/btc", description='Начать мониторинг BTC'),
        BotCommand(command="/stop", description='Остановить мониторинг BTC'),
    ])
    logging.info("БОТ ЗАПУЩЕН")

async def main():
    await on_startup()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
