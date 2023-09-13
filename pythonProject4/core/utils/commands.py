import types
from typing import List

from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_commands(bot: Bot, additive_commands: List[BotCommand] = None):
    commands = [
        BotCommand(
            command='start_bot',
            description='Начать работу',
        ),
        BotCommand(
            command='cancel_input',
            description='Прекратить заполнение',
        ),
    ]
    if additive_commands:
        commands.extend(additive_commands)
    print(additive_commands)
    await bot.delete_my_commands()
    await bot.set_my_commands(commands, BotCommandScopeDefault())
