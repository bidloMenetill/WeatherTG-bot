from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Бишкек")],
    {KeyboardButton(text="Нарын")},
    [KeyboardButton(text="Чуй")],
    {KeyboardButton(text="Ош")},
    [KeyboardButton(text="Джалал-Абад")],
    {KeyboardButton(text="Иссык-куль")},
    [KeyboardButton(text="Талас")],
   
    
], resize_keyboard=True, input_field_placeholder="Выбери город, чтобы узнать погоду.")


second_step = ReplyKeyboardMarkup(keyboard=[
    [
   
    KeyboardButton(text="Текущие сутки"),
    KeyboardButton(text="3 дня"),
    KeyboardButton(text="7 дней")],
    [ KeyboardButton(text="Назад"),],
], resize_keyboard=True,  input_field_placeholder="Узнай прогноз погоды.")
