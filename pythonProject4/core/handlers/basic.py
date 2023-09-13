import datetime
import logging
from aiogram import types, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, BotCommand
from aiogram.utils.keyboard import InlineKeyboardBuilder
from core.data.test_data import conferences_json, publications_json, application_json, authors_json
from core.keyboards.inline import red_keyboard
from core.settings import settings
from core.utils.commands import set_commands
from core.utils.functions import get_conference_status, applications, get_conference_view, findPublicationIndex, \
    get_last_id
from core.utils.statesforms import AppInput, PublicationInput, AuthorInput




async def start_bot(message: types.Message, bot: Bot):
    await set_commands(bot)
    await bot.send_message(
        settings.bots.admin_id, text="Бот запущен!"
    )
    await bot.send_message(settings.bots.admin_id, 'Приложение для подачи заявок на конференции',
                           reply_markup=InlineKeyboardMarkup(
                               inline_keyboard=[
                                   [InlineKeyboardButton(text="Начать", callback_data='conference')]
                               ],
                               resize_keyboard=True, disable_notification=True
                           ))


async def conference(callback_query: types.CallbackQuery, state: FSMContext):
    keyboard = InlineKeyboardBuilder()

    for conf in conferences_json:
        button_text = f"{conf['name_rus_short']}"
        status = get_conference_status(conf)
        if status == "Появится":
            button_text += ' (Появится)'
        elif status == "Доступна":
            button_text += ' (Доступна)'
        elif status == "Закончена":
            button_text += ' (Закончена)'
            if any(applications(conf['id'], callback_query.from_user.id)):
                button_text += ' (Заявка была добавлена)'
        else:
            button_text += ' (Неизвестно)'

        keyboard.button(text=button_text, callback_data=f"conference_{conf['id']}")
    keyboard.adjust(1, repeat=True)
    await callback_query.message.answer("Список конференций", reply_markup=keyboard.as_markup(resize_keyboard=True))


async def app_list(callback_query: types.CallbackQuery):
    answer = "Список ваших заявок:"
    conference_id = int(callback_query.data.split("_")[1])
    conference = next(conf for conf in conferences_json if conf['id'] == conference_id)  # поиск конференции по id
    keyboard = InlineKeyboardBuilder()
    option_keyboard = InlineKeyboardBuilder().button(text="Выбор конференции", callback_data="conference")
    conf_inf = get_conference_view(conference)

    apps = applications(conference_id, callback_query.from_user.id)
    logging.info(apps)
    if not apps:
        answer = "Вы еще не подали заявку на участие"
    else:
        for app in apps:
            keyboard.button(text=f'{app["title"]}', callback_data=f"app_{app['id']}_{conference_id}")

    if get_conference_status(conference) == 'Доступна':
        option_keyboard.button(text='Подать заявку', callback_data=f'new_app_{conference_id}')
    keyboard.adjust(2, repeat=True)
    option_keyboard.adjust(2, repeat=True)
    await callback_query.message.answer(f"Информация о конференции:\n {conf_inf}")
    await callback_query.message.answer(answer, reply_markup=keyboard.as_markup(resize_keyboard=True))
    await callback_query.message.answer("Опции:", reply_markup=option_keyboard.as_markup(resize_keyboard=True))


async def app_detail(callback_query: types.CallbackQuery, state: FSMContext):
    app_id = int(callback_query.data.split("_")[1])
    conf_id = int(callback_query.data.split("_")[2])
    app = next(
        app for app in application_json if app['id'] == app_id and conf_id == app['conf_id'])  # поиск заявки по id
    coauthors = [author for author in authors_json if author['application_id'] == app_id]
    coauthors_list = [{"name": author["name"], "surname": author["surname"], "patronymic": author["patronymic"]} for
                      author in coauthors]
    await state.set_data(data= \
 \
        {
            'id': app['id'],
            'conf_id': app['conf_id'],
            'telegram_id': app['telegram_id'],
            'submitted_at': app['submitted_at'],
            'updated_at': app['updated_at'],
            'university': app['university'],
            'discord_id': app['discord_id'],
            'email': app['email'],
            'phone': app['phone'],
            'name': app['name'],
            'surname': app['surname'],
            'patronymic': app['patronymic'],
            'student_group': app['student_group'],
            'applicant_role': app['applicant_role'],
            'title': app['title'],
            'adviser': app['adviser'],
            'coauthors': coauthors_list

        }
    )

    new_data = 'show_app'
    new_callback_query = callback_query.model_copy(update={'data': new_data})
    await show_app(new_callback_query, state)
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True, selective=True, inline_keyboard=[
        [InlineKeyboardButton(text="Редактировать", callback_data='reduction_keyboard')],
        [InlineKeyboardButton(text="Подача статьи", callback_data=f'publication_{app_id}_{conf_id}')],
        [InlineKeyboardButton(text="Сведенья об авторах", callback_data=f'coauthors_{app_id}_{conf_id}')],
        [InlineKeyboardButton(text="Возврат на экран выбора заявки", callback_data=f'conference_{conf_id}')]])

    await callback_query.message.answer(text="Опции", reply_markup=keyboard)


async def reduction_keyboard(callback_query: types.CallbackQuery):
    await callback_query.message.answer("Опции", reply_markup=red_keyboard)


async def publication(callback_query: types.CallbackQuery, state: FSMContext):
    app_id = int(callback_query.data.split("_")[1])
    conf_id = int(callback_query.data.split("_")[2])
    out_str = "Статья еще не была подана"
    publication_index = findPublicationIndex(app_id)
    data = await state.get_data()
    data["app_id"] = app_id
    data["conf_id"] = conf_id
    data['index'] = publication_index
    if publication_index:
        publication = publications_json[publication_index]

        out_str = \
            f""""id": {publication['id']},
            "publication_title": {publication['publication_title']},
            "upload_date": {publication['upload_date']},
            "review_status": {publication['review_status']},
            "download_url": {publication['download_url']},
            "keywords": {publication['keywords']},
            "abstract": {publication['abstract']},
        """

        data['publication'] = publication

    await state.set_data(data=data)
    await callback_query.message.answer(text=out_str)
    await callback_query.message.answer("Добавьте файл")
    await state.set_state(PublicationInput.waiting_for_file)


async def load_file(message: types.Message, state: FSMContext):
    document = message.document
    data = await state.get_data()
    data['document'] = document
    await state.set_data(data=data)
    if data.get('publication'):
        await message.answer("Вы уверены в перезаписи?", reply_markup=InlineKeyboardMarkup(resize_keyboard=True,
                                                                                           inline_keyboard=[[
                                                                                               InlineKeyboardButton(
                                                                                                   text="Да",
                                                                                                   callback_data=f'confirm_{data["app_id"]}_{data["conf_id"]}')],
                                                                                               [
                                                                                                   InlineKeyboardButton(
                                                                                                       text="Нет",
                                                                                                       callback_data=f'app_{data["app_id"]}_{data["conf_id"]}')]]))
    else:
        id = get_last_id(publications_json)
        data['id'] = id
        data['upload_date'] = message.date
        data['publication_title'] = document.file_name
        data['review_status'] = "Подготовлено"
        data['download_url'] = f"ПРИМЕР"
        data['keywords'] = "ПРИМЕР"
        data['abstract'] = "ПРИМЕР"
        publications_json.append(data)
        logging.info(publications_json)
        await state.clear()
        await message.answer(text="Файл добавлен!")


async def confirm(callback_query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    logging.info(data['document'])
    index = data['index']
    data['publication']['upload_date'] = callback_query.message.date
    data['publication']['publication_title'] = data['document'].file_name
    publications_json[index] = data['publication']
    await state.clear()
    logging.info(publications_json)

    await callback_query.message.answer(text="Файл добавлен!")


async def authors_info(callback: types.CallbackQuery, state: FSMContext, bot: Bot):
    app_id = int(callback.data.split("_")[1])
    conf_id = int(callback.data.split("_")[2])
    authors = [author for author in authors_json if author.get('application_id') == app_id]
    if not authors:
        out_str = "Пока авторов нет"
    else:
        out_str = ""
        for author in authors:
            out_str += \
                f"""
                    "id": {author['id']},
                    "application_id": {author['application_id']},
                    "name": {author['name']},
                    "surname": {author['surname']},
                    "patronymic": {author['patronymic']},
                    "email": {author['email']},
                    "phone": {author['phone']},
                    "bio": {author['bio']},
                    "organization": {author['organization']},
                    "role": {author['role']},
                """
    await callback.message.answer(text=out_str, reply_markup=InlineKeyboardMarkup(resize_keyboard=True, selective=True,
                                                                                  inline_keyboard=[[
                                                                                      InlineKeyboardButton(
                                                                                          text="Добавить",
                                                                                          callback_data=f'add_author_{app_id}_{conf_id}')],
                                                                                      [
                                                                                          InlineKeyboardButton(
                                                                                              text="Назад",
                                                                                              callback_data=f"app_{app_id}_{conf_id}")]]))


async def add_author(callback_query: types.CallbackQuery, state: FSMContext):
    id = get_last_id(authors_json)
    app_id = int(callback_query.data.split("_")[2])
    conf_id = int(callback_query.data.split("_")[3])
    await state.set_data(data= \
        {
            'input': 'author',
            'id': id,
            'application_id': app_id,
            'conference_id': conf_id
        })
    await callback_query.message.answer("Введите имя автора")
    await state.set_state(AuthorInput.waiting_for_name)


async def new_application(callback_query: types.CallbackQuery, state: FSMContext, bot: Bot):
    logging.info(application_json)
    user_id = int(callback_query.from_user.id)
    conf_id = int(callback_query.data.split("_")[2])
    application_id = get_last_id(applications(conf_id, user_id))
    await state.set_data(
        data= \
            {
                'id': application_id,
                'conf_id': conf_id,
                'telegram_id': str(user_id),
                'submitted_at': datetime.datetime.now().astimezone().isoformat(),
                'updated_at': datetime.datetime.now().astimezone().isoformat(),
                'university': '',
                'discord_id': '',
                'email': '',
                'phone': '',
                'name': '',
                'surname': '',
                'patronymic': '',
                'student_group': '',
                'applicant_role': '',
                'title': 'Новая заявка',
                'adviser': '',
                'coauthors': []
            }
    )

    logging.info(conf_id)
    await state.update_data(input='application')
    await callback_query.message.answer(text="Введите ваш университет:")
    await state.set_state(AppInput.waiting_for_university)


async def show_app(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()

    out_str = f"""
            "id": {data['id']},
            "conf_id": {data['conf_id']},
            "telegram_id": {data['telegram_id']},
            "discord_id": {data['discord_id']},
            "submitted_at": {data['submitted_at']},
            "updated_at": {data['updated_at']},
            "email": {data['email']},
            "phone": {data['phone']},
            "name": {data['name']},
            "surname": {data['surname']},
            "patronymic": {data['patronymic']},
            "university": {data['university']},
            "student_group": {data['student_group']},
            "applicant_role": {data['applicant_role']},
            "title": {data['title']},
            "adviser": {data['adviser']},
            "coauthors": {data['coauthors']}
        """

    await callback.message.answer(text=out_str)
