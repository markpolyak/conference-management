import asyncio
from aiogram import Dispatcher, Bot
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from core.handlers.basic import *
from aiogram import F
from core.handlers.input_handlers import register_input_handlers, cancel_input, reduction_enter, reduction_end


async def stop_bot(message:types.Message, bot: Bot):
    await message.answer(text="Бот остановлен!")
    loop =  asyncio.get_event_loop()
    loop.close()



async def start():
    logging.basicConfig(level=logging.INFO)
    storage = MemoryStorage()
    bot = Bot(token=settings.bots.bot_token, parse_mode='HTML')
    dp = Dispatcher(storage=storage)
    await set_commands(bot)
    dp.message.register(start_bot, Command('start_bot'))
    #dp.message.register(stop_bot, Command('stop_bot'))
    dp.message.register(cancel_input, Command('cancel_input'))
    await register_input_handlers(dp)
    dp.callback_query.register(reduction_keyboard, F.data == "reduction_keyboard")
    dp.callback_query.register(conference, F.data == "conference")
    dp.callback_query.register(reduction_end, F.data == "ready")
    dp.callback_query.register(reduction_enter, F.data.startswith("red"))
    dp.callback_query.register(app_list, F.data.startswith("conference_"))
    dp.callback_query.register(add_author, F.data.startswith("add_author"))

    dp.callback_query.register(app_detail, F.data.startswith("app_"))

    dp.callback_query.register(publication, F.data.startswith("publication"))
    dp.callback_query.register(show_app, F.data == "show_app")
    dp.message.register(load_file, F.document, PublicationInput.waiting_for_file)

    dp.callback_query.register(confirm, F.data.startswith("confirm_"))
    dp.callback_query.register(authors_info, F.data.startswith("coauthors_"))

    dp.callback_query.register(new_application, F.data.startswith("new_app_"))

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(start())

