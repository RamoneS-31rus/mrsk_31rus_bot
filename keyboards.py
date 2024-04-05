from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


buttons = [
        [
            KeyboardButton(text='/плановые'),            
            KeyboardButton(text='/аварийные')
        ],
        [
            KeyboardButton(text='/внерегламентные'),
            KeyboardButton(text='/информация')
        ],
    ]

keyboard_main = ReplyKeyboardMarkup(
    keyboard=buttons,
    resize_keyboard=True,
    input_field_placeholder='Введите название улицы'
)
