import copy
import logging

from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

red_keyboard = InlineKeyboardMarkup(resize_keyboard=True, selective=True, inline_keyboard=[
    [InlineKeyboardButton(text="Изменить discord_id", callback_data="red_discord_id"),
     InlineKeyboardButton(text="Изменить email", callback_data="red_email")],
     [InlineKeyboardButton(text="Изменить phone", callback_data="red_phone"),
     InlineKeyboardButton(text="Изменить name", callback_data="red_name")],
     [InlineKeyboardButton(text="Изменить surname", callback_data="red_surname"),
     InlineKeyboardButton(text="Изменить patronymic", callback_data="red_patronymic")
     ],

    [InlineKeyboardButton(text="Изменить student_group", callback_data="red_student_group"),
     InlineKeyboardButton(text="Изменить applicant_role", callback_data="red_applicant_role")],
     [InlineKeyboardButton(text="Изменить title", callback_data="red_title"),
    InlineKeyboardButton(text="Изменить научного руководителя", callback_data="red_adviser")],
     [InlineKeyboardButton(text="Изменить университет", callback_data="red_university"),
     ],
    [InlineKeyboardButton(text="Посмотреть заявку", callback_data="show_app")],
     [InlineKeyboardButton(text="Отменить редактирование", callback_data="cancel")],
    [InlineKeyboardButton(text="Готово", callback_data="ready")]
])
