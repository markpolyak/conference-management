import logging
from aiogram import types, Dispatcher
from aiogram.fsm.context import FSMContext
from aiogram import F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from core.data.test_data import application_json, authors_json
from core.utils.statesforms import AppInput, AuthorInput


async def cancel_input(message: types.Message, state: FSMContext):
    if await state.get_state():
        state_data = await state.get_data()
        logging.info(state_data)
        await message.answer("Возврат", reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [types.InlineKeyboardButton(text='Назад', callback_data=f"conference_{state_data['conf_id']}")]]))
        await state.clear()


field_state = {
    'university': AppInput.waiting_for_university,
    'discord_id': AppInput.waiting_for_discord_id,
    'email': AppInput.waiting_for_email,
    'phone': AppInput.waiting_for_phone,
    'name': AppInput.waiting_for_name,
    'surname': AppInput.waiting_for_surname,
    'patronymic': AppInput.waiting_for_patronymic,
    'student_group': AppInput.waiting_for_student_group,
    'applicant_role': AppInput.waiting_for_applicant_role,
    "title": AppInput.waiting_for_title,
}

invalid_answers = {
    'pure_string': 'строка должна содержать только буквы в нижнем или верхнем регистре!',
    'pure_numbers': 'строка должна содержать только цифры!',
    'student_group': 'строка должна содержать только цифры и может содержать букву в конце!',
    'email': 'email должен быть в формате: dycjh@example.com.',
    'phone': 'номер телефона должен выглядеть так: 89528545563,+79528545563',
    'string_with_space': 'строка должна содержать только буквы в нижнем или верхнем регистре и может содержать пробелы!',
    'discord_id': 'строка должна содержать только цифры! (5)',
    'adviser': 'строка в таком формате проф.Аа А.В. (вместо проф.может быть что угодно)'
}

pattern = r'^.+ [A-ZА-Я][a-zа-я]+\s[A-ZА-Я]\.[A-ZА-Я]\.$'
async def reduction_enter(callback_query: types.CallbackQuery, state: FSMContext):
    await state.update_data(mode='reduction', input='application')
    field = callback_query.data.split("_", 1)[1]
    state_to_stand = field_state[field]
    data = format_dict[state_to_stand]
    await callback_query.message.answer(data['text'])
    await state.set_state(state_to_stand)


format_dict = {
    AppInput.waiting_for_university: {
        'field': 'university',
        'text': 'Введите университет',
        'next_text': 'Введите discord_id',
        'next_state': AppInput.waiting_for_discord_id,
        'filter': F.text.regexp(r'^[a-zA-Zа-яА-Я]*$'),
        'invalid_answer': invalid_answers['pure_string']
    },

    AppInput.waiting_for_discord_id: {
        'field': 'discord_id',
        'text': 'Введите discord_id',
        'next_text': 'Введите email',
        'next_state': AppInput.waiting_for_email,
        'filter': F.text.regexp(r'^\d{5}$'),
        'invalid_answer': invalid_answers['discord_id']
    },

    AppInput.waiting_for_email: {
        'field': 'email',
        'text': 'Введите email',
        'next_text': 'Введите номер телефона',
        'next_state': AppInput.waiting_for_phone,
        'filter': F.text.regexp(r'^[\w\.-]+@[\w\.-]+\.\w+$'),
        'invalid_answer': invalid_answers['email']
    },

    AppInput.waiting_for_phone: {
        'field': 'phone',
        'text': 'Введите номер телефона',
        'next_text': 'Введите имя',
        'next_state': AppInput.waiting_for_name,
        'filter': F.text.regexp(r'^\+?\d{11}$'),
        'invalid_answer': invalid_answers['phone']
    },

    AppInput.waiting_for_name: {
        'field': 'name',
        'text': 'Введите имя',
        'next_text': 'Введите фамилию',
        'next_state': AppInput.waiting_for_surname,
        'filter': F.text.regexp(r'^[a-zA-Zа-яА-Я]*$'),
        'invalid_answer': invalid_answers['pure_string']
    },

    AppInput.waiting_for_surname: {
        'field': 'surname',
        'text': 'Введите фамилию',
        'next_text': 'Введите отчество',
        'next_state': AppInput.waiting_for_patronymic,
        'filter': F.text.regexp(r'^[a-zA-Zа-яА-Я]*$'),
        'invalid_answer': invalid_answers['pure_string']
    },

    AppInput.waiting_for_patronymic: {
        'field': 'patronymic',
        'text': 'Введите отчество',
        'next_text': 'Введите группу',
        'next_state': AppInput.waiting_for_student_group,
        'filter': F.text.regexp(r'^[a-zA-Zа-яА-Я]*$'),
        'invalid_answer': invalid_answers['pure_string']
    },

    AppInput.waiting_for_student_group: {
        'field': 'student_group',
        'text': 'Введите группу',
        'next_text': 'Введите роль',
        'next_state': AppInput.waiting_for_applicant_role,
        'filter': F.text.regexp(r'^\d+[a-zA-Zа-яА-Я]?$'),
        'invalid_answer': invalid_answers['student_group']
    },

    AppInput.waiting_for_applicant_role: {
        'field': 'applicant_role',
        'text': 'Введите роль',
        'next_text': 'Введите название',
        'next_state': AppInput.waiting_for_title,
        'filter': F.text.regexp(r'^[a-zA-Zа-яА-Я\s]+$'),
        'invalid_answer': invalid_answers['string_with_space']
    },

    AppInput.waiting_for_title: {
        'field': 'title',
        'text': 'Введите название',
        'next_text': 'Введите советника',  # You can set this to an appropriate value if needed
        'next_state': AppInput.waiting_for_adviser,
        'filter': F.text.regexp(r'^[a-zA-Zа-яА-Я\s]+$'),
        'invalid_answer': invalid_answers['pure_string']
    },

    AppInput.waiting_for_adviser: {'field': 'adviser', 'next_text': '',
                                 'next_state': AppInput.waiting_for_coauthors,
                                  'filter': F.text.regexp(r'^[A-ZА-Я][a-zа-я]+\s[A-ZА-Я]\.?\s?[A-ZА-Я]\.$'),
                                  'invalid_answer': invalid_answers['adviser']},
}

author_dict = {
    AuthorInput.waiting_for_name: {'field': 'name',
                                   'next_text': 'Введите фамилию',  # You can set this to an appropriate value if needed
                                   'next_state': AuthorInput.waiting_for_surname,
                                   'filter': lambda name: name is not None,
                                   'invalid_answer': invalid_answers['pure_string']},

    AuthorInput.waiting_for_surname: {'field': 'surname',
                                      'next_text': 'Введите отчество',
                                      # You can set this to an appropriate value if needed
                                      'next_state': AuthorInput.waiting_for_patronymic,
                                      'filter': lambda surname: surname is not None,
                                      'invalid_answer': invalid_answers['pure_string']},

    AuthorInput.waiting_for_patronymic: {'field': 'patronymic',
                                         'next_text': 'Введите email',
                                         # You can set this to an appropriate value if needed
                                         'next_state': AuthorInput.waiting_for_email,
                                         'filter': lambda patronymic: patronymic is not None,
                                         'invalid_answer': invalid_answers['pure_string']},

    AuthorInput.waiting_for_email: {'field': 'email',
                                    'next_text': 'Введите phone',  # You can set this to an appropriate value if needed
                                    'next_state': AuthorInput.waiting_for_phone,
                                    'filter': lambda email: email is not None,
                                    'invalid_answer': invalid_answers['email']},

    AuthorInput.waiting_for_phone: {'field': 'phone',
                                    'next_text': 'Введите биографию',
                                    # You can set this to an appropriate value if needed
                                    'next_state': AuthorInput.waiting_for_bio,
                                    'filter': lambda phone: phone is not None,
                                    'invalid_answer': invalid_answers['phone']},

    AuthorInput.waiting_for_bio: {'field': 'bio',
                                  'next_text': 'Введите организацию',
                                  # You can set this to an appropriate value if needed
                                  'next_state': AuthorInput.waiting_for_organization,
                                  'filter': lambda bio: bio is not None,
                                  'invalid_answer': invalid_answers['string_with_space']},

    AuthorInput.waiting_for_organization: {'field': 'organization',
                                           'next_text': 'Введите роль',
                                           # You can set this to an appropriate value if needed
                                           'next_state': AuthorInput.waiting_for_role,
                                           'filter': lambda organization: organization is not None,
                                           'invalid_answer': invalid_answers['pure_string']},

    AuthorInput.waiting_for_role: {'field': 'role',
                                   'next_text': '',  # You can set this to an appropriate value if needed
                                   'next_state': AppInput.waiting_for_surname,
                                   'filter': lambda role: role is not None,
                                   'invalid_answer': invalid_answers['string_with_space']}

}



async def app_input(message: types.Message, state: FSMContext):

    state_value = await state.get_state()
    state_data = await state.get_data()
    logging.info(state_data['conf_id'])
    if state_data['input'] == 'application':
        data = format_dict[state_value]
    else:
        data = author_dict[state_value]
    if state_data.get('mode') == 'reduction':
        await state.update_data({data['field']: message.text})
        await message.answer(text="Отредактировано!")
        return

    logging.info(message.text)

    await state.update_data({data['field']: message.text})

    try:
        await message.answer(text=data['next_text'])
        await state.set_state(data['next_state'])
    except:
        data = await state.get_data()
        if data.get('input') == 'application':
            logging.info(data)
            application_json.append(data)
            logging.info(application_json)
            await state.clear()
            await message.answer("Завершено!", reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[[InlineKeyboardButton(text='Назад', callback_data=f'conference_{data["conf_id"]}')]]))
        else:
            authors_json.append(data)
            logging.info(authors_json)
            await state.clear()
            await message.answer("Завершено!", reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[[InlineKeyboardButton(text='Назад',
                                                       callback_data=f'app_{data["application_id"]}_{data["conference_id"]}')],
                                 [
                                     InlineKeyboardButton(
                                         text="Добавить",
                                         callback_data=f'add_author_{data["application_id"]}_{data["conference_id"]}')]
                                 ]))


async def app_invalid(message: types.Message, state: FSMContext):
    state_value = await state.get_state()
    logging.info(str(message.text))
    data = format_dict[state_value]
    await message.answer(f"Неверный ввод. Повторите еще раз в формате: {data['invalid_answer']}")


async def register_input_handlers(dp: Dispatcher):
    for state in format_dict.keys():
        dp.message.register(app_input, format_dict[state]['filter'], state)
        # dp.callback_query.register(app_input, format_dict[state]['filter'])
        dp.message.register(app_invalid, F.text.not_contains('/'), state)
    for state in author_dict.keys():
        dp.message.register(app_input, author_dict[state]['filter'], state)
        # dp.callback_query.register(app_input, author_dict[state]['filter'])
        dp.message.register(app_invalid, F.text.not_contains('/'), state)


async def reduction_end(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    index = next((i for i, item in enumerate(application_json) if
                  item['conf_id'] == data['conf_id'] and item['id'] == data['id']), None)
    if index is not None:
        application_json[index] = data
        logging.info(application_json)
        # await state.clear()
        await callback.message.answer("Редактирование завершено", reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text='Назад', callback_data=f'conference_{data["conf_id"]}')]]))
