import executor as executor
import requests
import datetime
import asyncio
from config import tg_bot_token, token_wather
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command

bot = Bot(token=tg_bot_token)
dp = Dispatcher()


@dp.message(Command("start"))
async def start_command(message: types.Message):
    await message.reply("Здравствуйте, напишите мне свой город! \n"
                        "Например: Minsk ")


@dp.message()
async def start_command2(message: types.Message):
    try:
        req = requests.get(
            f'https://api.openweathermap.org/data/2.5/forecast?q={message.text}&appid={token_wather}&units=metric'
        )
        data = req.json()
        list_data_interval_rain = [data['list'].index(check) for check in data['list'] if 'rain' in check]
        now_data = datetime.datetime.now()

        if list_data_interval_rain[0] >= 4:
            fin_data = datetime.datetime.fromtimestamp(data['list'][list_data_interval_rain[0] - 8]['dt'])
            await message.reply(f'Ближайшее время для мойки c {now_data.strftime("%Y-%m-%d %H:%M:%S")} по {fin_data}')
        else:
            for i in range(1, len(list_data_interval_rain)):
                if list_data_interval_rain[i] - list_data_interval_rain[i - 1] >= 8:
                    start_data = datetime.datetime.fromtimestamp(data["list"][list_data_interval_rain[i - 1] - 8]["dt"])
                    fin_data = datetime.datetime.fromtimestamp(data["list"][list_data_interval_rain[i] - 1]["dt"])
                    await message.reply(f'Машину можно везти на мойку с {start_data} по {fin_data}')
            else:
                await message.reply("Ближайшие 5 дней на мойку уможно не ехать")

    except:
        await message.reply("Вы некорректно ввели город :) Попробуйте еще раз: /start")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
