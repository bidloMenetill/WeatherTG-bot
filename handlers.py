from aiogram import Bot, Dispatcher, F, Router
from aiogram.types import Message
from aiogram.filters import CommandStart
import keyboards as kb
import os
from dotenv import load_dotenv
import requests
from datetime import datetime
import locale
load_dotenv()

locale.setlocale(locale.LC_TIME, 'en_US.UTF-8')

router = Router()
user_city_selection = {}
WEATHER_TOKEN = os.getenv("WEATHER_TOKEN")
API_URL = os.getenv("API_URL")

@router.message(CommandStart())
async def cmd_start(message: Message):
    last_name = message.from_user.last_name if message.from_user.last_name else ""
    await message.reply(
        f'Привет {message.from_user.first_name} {last_name}, я приветствую тебя! Выберите город:',
        reply_markup=kb.main
    )

@router.message(F.text)
async def handle_text(message: Message):
    if message.text in ["Бишкек", "Нарын", "Чуй", "Ош", "Джалал-Абад", "Иссык-куль", "Талас"]:
        user_city_selection[message.from_user.id] = message.text
        await message.reply(
            f"Вы выбрали город {message.text}. Теперь выберите временной промежуток:",
            reply_markup=kb.second_step
        )
    elif message.text in ["Текущие сутки", "3 дня", "7 дней", "Назад"]:
        city = user_city_selection.get(message.from_user.id)
        if not city:
            await message.reply("Сначала выберите город.")
            return
        if message.text == "Текущие сутки":
            await get_hourly_weather(message, city)
        elif message.text == "3 дня":
            await get_daily_weather(message, city, days=3)
        elif message.text == "7 дней":
            await get_daily_weather(message, city, days=7)
        elif message.text == "Назад" or message.text == "назад":
            await message.reply("Вы вернулись в главное меню.", reply_markup=kb.main)
    else:
        await message.reply("Пожалуйста, выберите город или временной промежуток из предложенного списка.")

async def get_hourly_weather(message: Message, city: str):
    params = {
        "q": f"{city},KG",
        "appid": WEATHER_TOKEN,
        "units": "metric",
        "lang": "ru"
    }
    response = requests.get(API_URL, params=params)

    if response.status_code == 200:
        forecast_data = response.json()
        forecasts = forecast_data["list"][:8]

        weather_message = f"🌤️ Прогноз погоды в городе {city} на текущие сутки:\n"
        for forecast in forecasts:
            time = forecast["dt_txt"]
            dt = datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
            formatted_date = dt.strftime("%A, %d %B %Y")
            formatted_time = dt.strftime("%H:%M")
            temp = forecast["main"]["temp"]
            description = forecast["weather"][0]["description"]
            feels_like = forecast["main"]["feels_like"]
            humidity = forecast["main"]["humidity"]
            
            emoji = "🌡️"
            if temp < 0:
                emoji = "❄️"
            elif temp > 30:
                emoji = "☀️"
            elif temp > 20:
                emoji = "🌤️"
            elif temp > 10:
                emoji = "🌥️"

            weather_message += (
                f"\n📅 Дата: {formatted_date}, 🕒 Время: {formatted_time}\n"
                f"{emoji} Температура: {temp}°C \n"
                f"🧊 Ощущается как: {feels_like}°C\n"
                f"📝 Описание: {description.capitalize()}\n"
                f"💧 Влажность: {humidity}%\n"
            )
        await message.reply(weather_message)
    else:
        await message.reply("🚫 Не удалось получить данные о погоде. Попробуйте позже.")

async def get_daily_weather(message: Message, city: str, days: int):
    params = {
        "q": f"{city},KG",
        "appid": WEATHER_TOKEN,
        "units": "metric",
        "lang": "ru"
    }
    response = requests.get(API_URL, params=params)

    if response.status_code == 200:
        forecast_data = response.json()
        forecasts = forecast_data["list"]

        daily_data = {}
        for forecast in forecasts:
            date = forecast["dt_txt"].split(" ")[0]
            temp = forecast["main"]["temp"]
            if date not in daily_data:
                daily_data[date] = []
            daily_data[date].append(temp)

        weather_message = f"🌤️ Прогноз погоды в городе {city} на {days} дня(ей):\n"
        for i, (date, temps) in enumerate(daily_data.items()):
            if i >= days:
                break
            dt = datetime.strptime(date, "%Y-%m-%d")
            formatted_date = dt.strftime("%A, %d %B %Y")
            avg_temp = sum(temps) / len(temps)
            emoji = "🌡️"
            if avg_temp < 0:
                emoji = "❄️"
            elif avg_temp > 30:
                emoji = "☀️"
            elif avg_temp > 20:
                emoji = "🌤️"
            elif avg_temp > 10:
                emoji = "🌥️"
            weather_message += f"\n📅 Дата: {formatted_date}\n{emoji} Средняя температура: {avg_temp:.1f}°C\n"

        await message.reply(weather_message)
    else:
        await message.reply("🚫 Не удалось получить данные о погоде. Попробуйте позже.")
