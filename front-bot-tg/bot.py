import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Game
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import Message
import datetime
import pytz
from datetime import timezone
from data import *
from user import *


# Инициализация бота
bot_token = '6297405813:AAF7QsOsC-LJzXDZu7LnTmA2vV48tdSNqII'
bot = Bot(token=bot_token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Инициализaция доп классов 
user_table = UserTable()
application_table = ApplicationTable()

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Define your states
class InputState(StatesGroup):
    waiting_for_input = State()
    waiting_for_coauthor_input = State()
    waiting_for_publication_input = State()


# Обработчик команды /start
@dp.message_handler(Command("start") & types.ChatType.is_private)
async def start(message: types.Message, state: FSMContext):
    user_table.add_user(message.from_user.id)
    
    await message.answer(start_message, reply_markup=InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Начать", callback_data = 'conference')]
        ],
        resize_keyboard=True,
    ))

    


@dp.callback_query_handler(lambda query: query.data == "conference")
async def conference_choise(callback_query: types.CallbackQuery, state: FSMContext):
    # Определение, можно ли подать заявку на конференцию
    def time_mark(conf_id):
        current_date = datetime.date.today()
        # Check if registration is open
        registration_start_date = datetime.datetime.strptime(([x["registration_start_date"] for x in conferences_json if x['id']==int(conf_id)])[0], "%d.%m.%Y").date()
        registration_end_date = datetime.datetime.strptime(([x["registration_end_date"] for x in conferences_json if x['id']==int(conf_id)])[0], "%d.%m.%Y").date()
        
        new_application_allowance = registration_start_date <= current_date <= registration_end_date

        if new_application_allowance: return "(Можно подать)" 
        else: return "(Нельзя подать)"

    # Определение, завершена ли конференция
    def conf_time_mark(conf_id):
        current_date = datetime.date.today()
        # Check if registration is open
        registration_end_date = datetime.datetime.strptime(([x["conf_end_date"] for x in conferences_json if x['id']==int(conf_id)])[0], "%d.%m.%Y").date()
        
        new_application_allowance =  current_date <= registration_end_date

        if new_application_allowance: return " " 
        else: return "(Конференция закончена)"

    # Определение, есть ли уже поданные заявки на конференцию от текущего пользователя
    def previous_application_mark(conf_id):
        
        if any([x for x in application_json if x["conf_id"] == (conf_id) and x["telegram_id"]==str(callback_query.from_user.id)]):
            return "(Есть заявки)"
        else: return  " "

    # Отправка сообщения с просьбой выбрать конференцию
    await callback_query.message.answer("Выберите конференцию", reply_markup=InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=x['name_rus_short'] + " (" + x["registration_start_date"] + " - " + x["registration_end_date"] + ")"
                                         + " " + time_mark(x["id"]) + " " + previous_application_mark(x["id"]) + " " + conf_time_mark(x["id"]),
                                           callback_data="id_"+str(x["id"]))] for x in conferences_json],
        resize_keyboard=True,
    ))
    


@dp.callback_query_handler(lambda query: query.data.startswith("id_"))
async def application_choise(callback_query: types.CallbackQuery, state: FSMContext):

    # Получаем идентификатор конференции из callback-запроса
    conf_id = callback_query.data.split("_")[1]

    # Находим информацию о конференции по ее идентификатору
    conference  = [x for x in conferences_json if x['id']==int(conf_id)][0]

    # Get the current date
    current_date = datetime.date.today()

    # Check if registration is open
    registration_start_date = datetime.datetime.strptime(([x["registration_start_date"] for x in conferences_json if x['id']==int(conf_id)])[0], "%d.%m.%Y").date()
    registration_end_date = datetime.datetime.strptime(([x["registration_end_date"] for x in conferences_json if x['id']==int(conf_id)])[0], "%d.%m.%Y").date()
    
    new_application_allowance = registration_start_date <= current_date <= registration_end_date

    # Получаем список заявок пользователя для данной конференции
    application_list = [x for x in application_json if x['telegram_id'] == str(callback_query.from_user.id) and x['conf_id']==int(conf_id)]
    

    inline_keyboard = [[InlineKeyboardButton(text="Выбор конференции", callback_data="conference")]]

    output_msg = f"""
  Название: {conference["name_rus"]}
  Аббревиатура: {conference["name_rus_short"]}
  Name: {conference["name_eng"]}
  Short name: {conference["name_eng_short"]}
  Дата начала регистрации: {conference["registration_start_date"]} 
  Дата конца регистрации: {conference["registration_end_date"]}
  Дата начала приема докладов: {conference["submission_start_date"]}
  Дата конца приема статей: {conference["submission_end_date"]}
  Дата начала конференции: {conference["conf_start_date"]}
  Дата конца конференции: {conference["conf_end_date"]}
  Организатор: {conference["organized_by"]}
  url: {conference["url"]}
  email: {conference["email"]}
"""
    # Добавляем кнопку "Создать заявку", если разрешено подавать новые заявки
    if new_application_allowance is True:
        inline_keyboard.append([InlineKeyboardButton(text="Создать заявку", callback_data="new_application"+"_"+str(conf_id)+"_"+str(get_unique_id()))])

    # Проверяем, есть ли у пользователя уже поданные заявки на данную конференцию
    if not application_list:
        await callback_query.message.answer("Вы еще не подали заявку на участие"+output_msg
                                            , reply_markup=InlineKeyboardMarkup(
            inline_keyboard = inline_keyboard,
            resize_keyboard = True
        ))
    else:
        # Добавляем кнопки для каждой поданной заявки пользователя
        inline_keyboard.append(InlineKeyboardButton(text = x['title'],
                                                     callback_data=('application_id_' + str(x['id']) +"_"+str(conf_id))) for x in application_list)
        
        await callback_query.message.answer(output_msg,
                                             reply_markup=InlineKeyboardMarkup(
            inline_keyboard = inline_keyboard,
            resize_keyboard = True
        ))
        

@dp.callback_query_handler(lambda query: query.data.startswith("application_id_"))
async def application_processing(callback_query: types.CallbackQuery, state: FSMContext):
    # Получение идентификатора заявки и конференции из callback-запроса
    application_id = callback_query.data.split("_")[2]
    conf_id = callback_query.data.split("_")[3]

    # Находим информацию о заявке на основе идентификаторов
    application = [x for x in application_json if x['telegram_id'] == str(callback_query.from_user.id) and x['conf_id']==int(conf_id) and x['id']==int(application_id)]
    
    


    inline_keyboard = [[InlineKeyboardButton(text="Выбор конференции", callback_data="conference")],
                       [InlineKeyboardButton(text="Все заявки", callback_data="id_"+str(conf_id))],
                       [InlineKeyboardButton(text="Подача статьи", callback_data="article_submission_"+application_id)],
                       [InlineKeyboardButton(text="Обновить заявку", callback_data="update_data_"+conf_id+"_"+application_id)],
                       ]


    qwe = [x['name']+" "+x["surname"]+ " "+ x["patronymic"] for x in application[0]['coauthors']]

    aplication_info = f"""
Дискорд id: {application[0]['discord_id']}
Подано: {application[0]['submitted_at']}
Обновлено: {application[0]['updated_at']}
email: {application[0]['email']}
Номер телефона: {application[0]['phone']}
Имя: {application[0]['name']}
Фамилия: {application[0]['patronymic']}
Отчество: {application[0]['surname']}
Университет: {application[0]['university']}
Группа: {application[0]['student_group']}
Должность: {application[0]['applicant_role']}
Название работы: {application[0]['title']}
Научный руководитель: {application[0]['adviser']}
Соавторы: {", ".join([x['name']+" "+x["surname"]+ " "+ x["patronymic"] for x in application[0]['coauthors']])}
"""

    info_message = f"Ваша заявка: {aplication_info} для конференции: {([x['name_rus'] for x in conferences_json if x['id']==int(conf_id)])[0]}"

    # Отправляем сообщение с информацией и кнопками для управления заявкой
    await callback_query.message.answer(info_message, reply_markup=InlineKeyboardMarkup(
        inline_keyboard=inline_keyboard,
        resize_keyboard=True,
    ))

@dp.callback_query_handler(lambda query: query.data.startswith("article_submission"))
async def application_processing(callback_query: types.CallbackQuery, state: FSMContext):
    application_id = callback_query.data.split("_")[-1]

    # Добавление новой публикации в список publications_json
    publications_json.append(create_new_publication(int(application_id),datetime.datetime.now(pytz.timezone('Europe/Moscow')).strftime("%Y-%m-%dT%H:%M:%S.%f%z")))

    # Отправка сообщения о создании публикации и кнопок для управления публикацией
    await callback_query.message.answer("Публикация создана", reply_markup=InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="Выбор конференции", callback_data="conference")],
                       [InlineKeyboardButton(text="Обновить данные по публикации", callback_data="update_publication_data_"+application_id)]],
        resize_keyboard=True
    ))

@dp.callback_query_handler(lambda query: query.data.startswith("update_publication_data_"))
async def application_processing(callback_query: types.CallbackQuery, state: FSMContext):

    application_id = callback_query.data.split("_")[-1]

    publication = [x for x in publications_json if x['id']==int(application_id)][0]

    inline_keyboard = [[InlineKeyboardButton(text="Выбор конференции", callback_data="conference")],
                        [InlineKeyboardButton(text="Название публикации", callback_data="publication_input&publication_title&"+application_id)],
                        [InlineKeyboardButton(text="Ссылка", callback_data="publication_input&download_url&"+application_id)],
                       [InlineKeyboardButton(text="Ключевые слова", callback_data="publication_input&keywords&"+application_id)],
                       [InlineKeyboardButton(text="Аннотация", callback_data="publication_input&abstract&"+application_id)]
                       ]

    

    info_message = f"""
Данные обновлены:
Название статьи: {publication["publication_title"]}
Дата обновления: {publication["upload_date"]}
Статус ревью: {publication["review_status"]}
Ссылка для скачивания: {publication["download_url"]}
Ключевые слова: {publication["keywords"]}
Аннотация: {publication["abstract"]}
"""

    # Отправляем сообщение с информацией и кнопками для управления публикацией
    await callback_query.message.answer(info_message, reply_markup=InlineKeyboardMarkup(
        inline_keyboard=inline_keyboard,
        resize_keyboard=True,
    ))

@dp.callback_query_handler(lambda query: query.data.startswith("publication_input"))
async def application_processing(callback_query: types.CallbackQuery, state: FSMContext):
    # Получение типа данных и идентификатора заявки из callback-запроса
    data_type = callback_query.data.split("&")[1]
    application_id = callback_query.data.split("&")[-1]

    # Инициализация состояния и сохранение типа данных в FSMContext
    await state.update_data(data_type=data_type, application_id=application_id)

    
    await InputState.waiting_for_publication_input.set()
    # Отправка сообщения с запросом ввода данных
    await callback_query.message.answer(f"Введите "+json_to_name(data_type))
    
    
    

@dp.message_handler(state=InputState.waiting_for_publication_input, content_types=types.ContentTypes.TEXT)
async def process_input(message: types.Message, state: FSMContext):
    # Получение данных из состояния FSM
    data = await state.get_data()
    data_type = data.get("data_type")
    application_id = data.get("application_id")
    user_input = message.text
    # Обработка введенных данных пользователя
    publication = [x for x in publications_json if x['id']==int(application_id)][0]
    publication[data_type]=user_input
    publication["upload_date"]=datetime.datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f%z")
    if data_type == "download_url":
        addictive_msg = " , пожалуйста, перепроверьте ссылку"
        url_flag = False
    else:
        addictive_msg = " "
        url_flag = True
    # Отправка подтверждения введенных данных
    if url_flag:
        await message.answer(f"Вы ввели: {user_input}"+addictive_msg, reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Выбор конференции", callback_data="conference")],
                [types.InlineKeyboardButton(text="Вернуться к заполнению заявки", callback_data="update_publication_data_"+"_"+str(application_id))],
            ],
            resize_keyboard=True,
        ))
    else:
        await message.answer(f"Вы ввели: {user_input}"+addictive_msg, reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Выбор конференции", callback_data="conference")],
                [types.InlineKeyboardButton(text="Подтвердить", callback_data="update_publication_data_"+"_"+str(application_id))],
                [types.InlineKeyboardButton(text="Неверно", callback_data="publication_input&download_url&"+application_id)]
            ],
            resize_keyboard=True,
        ))

    # Сброс состояния после чтения ввода
    await state.finish()


   
@dp.callback_query_handler(lambda query: query.data.startswith("new_application_"))
async def application_processing(callback_query: types.CallbackQuery, state: FSMContext):
    
    conf_id = callback_query.data.split("_")[2]
    application_id = callback_query.data.split("_")[3]
    application_json.append(create_new_application(int(application_id),int(conf_id),str(callback_query.from_user.id),
                                                   datetime.datetime.now(pytz.timezone('Europe/Moscow')).strftime("%Y-%m-%dT%H:%M:%S.%f%z")
))
   
    #application_json.append(new_application)

    await callback_query.message.answer("Заявка принята", reply_markup=InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="Выбор конференции", callback_data="conference")],
                       [InlineKeyboardButton(text="Обновить данные по заявке", callback_data="update_data_"+conf_id+"_"+application_id)]],
        resize_keyboard=True
    ))

@dp.callback_query_handler(lambda query: query.data.startswith("update_data_"))
async def application_processing(callback_query: types.CallbackQuery, state: FSMContext):

    conf_id = callback_query.data.split("_")[2]
    application_id = callback_query.data.split("_")[3]
    application = [x for x in application_json if x['id']==int(application_id)]
    # application_table.add_application(fields,conf_id)
    info_message = f"""
Дискорд id: {application[0]['discord_id']}
Подано: {application[0]['submitted_at']}
Обновлено: {application[0]['updated_at']}
email: {application[0]['email']}
Номер телефона: {application[0]['phone']}
Имя: {application[0]['name']}
Фамилия: {application[0]['patronymic']}
Отчество: {application[0]['surname']}
Университет: {application[0]['university']}
Группа: {application[0]['student_group']}
Должность: {application[0]['applicant_role']}
Название работы: {application[0]['title']}
Научный руководитель: {application[0]['adviser']}
Соавторы: {", ".join([x['name']+" "+x["surname"]+ " "+ x["patronymic"] for x in application[0]['coauthors']])}
"""

    
    inline_keyboard = [[InlineKeyboardButton(text="Выбор конференции", callback_data="conference")],
                        [InlineKeyboardButton(text="Дискорд", callback_data="input_discordid"+"_"+application_id)],
                       [InlineKeyboardButton(text="email", callback_data="input_email"+"_"+application_id)],
                       [InlineKeyboardButton(text="Номер телефона", callback_data="input_phone"+"_"+application_id)],
                       [InlineKeyboardButton(text="Имя", callback_data="input_name"+"_"+application_id)],
                       [InlineKeyboardButton(text="Фамилия", callback_data="input_surname"+"_"+application_id)],
                       [InlineKeyboardButton(text="Отчество", callback_data="input_patronymic"+"_"+application_id)],
                       [InlineKeyboardButton(text="Университет", callback_data="input_university"+"_"+application_id)],
                       [InlineKeyboardButton(text="Группа", callback_data="input_studentgroup"+"_"+application_id)],
                       [InlineKeyboardButton(text="Должность", callback_data="input_applicantrole"+"_"+application_id)],
                       [InlineKeyboardButton(text="Название работы", callback_data="input_title"+"_"+application_id)],
                       [InlineKeyboardButton(text="Научный руководитель", callback_data="input_adviser"+"_"+application_id)],
                       [InlineKeyboardButton(text="Соавторы", callback_data="coauthors_input"+"_"+application_id)]
                       ]

    

    await callback_query.message.answer(info_message, reply_markup=InlineKeyboardMarkup(
        inline_keyboard=inline_keyboard,
        resize_keyboard=True,
    ))

@dp.callback_query_handler(lambda query: query.data.startswith("coauthors_input"))
async def application_processing(callback_query: types.CallbackQuery):
    application_id = callback_query.data.split("_")[-1]
    application = [x for x in application_json if x['id']==int(application_id)][0]
    conf_id = application["conf_id"]
    msg = f"Ваши соавторы: { ', '.join([x['name']+' '+x['surname']+ ' '+ x['patronymic'] for x in application['coauthors']])}"
    await callback_query.message.answer(msg, reply_markup=InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="Выбор конференции", callback_data="conference")],
                       [InlineKeyboardButton(text="Обновить данные по заявке", callback_data="update_data_"+str(conf_id)+"_"+str(application_id))],
                       [InlineKeyboardButton(text="Добавить", callback_data="add_coauthor_"+application_id)],
                       [InlineKeyboardButton(text="Удалить", callback_data="del_coauthor_"+application_id)]],
        resize_keyboard=True
    ))

@dp.callback_query_handler(lambda query: query.data.startswith("add_coauthor"))
async def application_processing(callback_query: types.CallbackQuery,state: FSMContext):
    application_id = callback_query.data.split("_")[-1]
    application = [x for x in application_json if x['id']==int(application_id)][0]
    conf_id = application["conf_id"]
    

    coauthors = [x['name']+' '+x['surname']+ ' '+ x['patronymic'] for x in application['coauthors']]

    

    await InputState.waiting_for_coauthor_input.set()
    await state.update_data(application_id=application_id)
    # Отправка сообщения с запросом ввода данных
    await callback_query.message.answer(f"Ваши соавторы: ({' '.join(coauthors)})"+" Введите имя фамилию отчество добавляемого соавтора")


@dp.callback_query_handler(lambda query: query.data.startswith("del_coauthor"))
async def application_processing(callback_query: types.CallbackQuery):
    application_id = callback_query.data.split("_")[-1]
    application = [x for x in application_json if x['id']==int(application_id)][0]
    conf_id = application["conf_id"]
    coauthors = [x['name']+' '+x['surname']+ ' '+ x['patronymic'] for x in application['coauthors']]
    inline_keyboard = [[InlineKeyboardButton(text=x, callback_data=f"del_this_coauthor_"+str(application_id))] for x in coauthors]
    await callback_query.message.answer("Выберите соавтора для удаления", reply_markup=InlineKeyboardMarkup(
        inline_keyboard=inline_keyboard,
        resize_keyboard=True
    ))

@dp.callback_query_handler(lambda query: query.data.startswith("del_this_coauthor"))
async def application_processing(callback_query: types.CallbackQuery):
    application_id = callback_query.data.split("_")[-1]
    button_text = callback_query.message.reply_markup.inline_keyboard[0][0].text
    mass = button_text.split(" ")
    application = [x for x in application_json if x['id']==int(application_id)][0]
    conf_id = application["conf_id"]

    application["coauthors"] = [coauthor for coauthor in application["coauthors"] if 
                                        coauthor["name"] != mass[0]
                                        and coauthor['surname'] != mass[1] and 
                                        coauthor['patronymic'] != mass[2]]
    
    await callback_query.message.answer("Выберите соавтора для удаления", reply_markup=InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="Выбор конференции", callback_data="conference")],
            [types.InlineKeyboardButton(text="Вернуться к заполнению заявки", callback_data="update_data_"+str(conf_id)+"_"+str(application_id))]],
        resize_keyboard=True
    ))




    # coauthors = [x['name']+' '+x['surname']+ ' '+ x['patronymic'] for x in application['coauthors']]
    # inline_keyboard = [[InlineKeyboardButton(text=x, callback_data=f"del_this_coauthor")] for x in coauthors]
    # await callback_query.message.answer("Выберите соавтора для удаления", reply_markup=InlineKeyboardMarkup(
    #     inline_keyboard=inline_keyboard,
    #     resize_keyboard=True
    # ))

    

@dp.message_handler(state=InputState.waiting_for_coauthor_input, content_types=types.ContentTypes.TEXT)
async def process_input(message: types.Message, state: FSMContext):

    data = await state.get_data()
    coauthor = {"name": message.text.split(" ")[0], "surname": message.text.split(" ")[1], "patronymic": message.text.split(" ")[2]}
    
    application_id = data.get("application_id")
    application = [x for x in application_json if x['id']==int(application_id)][0]
    application["coauthors"].append(coauthor)
    
    conf_id = application["conf_id"]
    # Отправка подтверждения введенных данных
    await message.answer(f"Вы ввели: {message.text}", reply_markup=types.InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Выбор конференции", callback_data="conference")],
            [types.InlineKeyboardButton(text="Вернуться к заполнению заявки", callback_data="update_data_"+str(conf_id)+"_"+str(application_id))],
        ],
        resize_keyboard=True,
    ))
    await state.finish()


@dp.callback_query_handler(lambda query: query.data.startswith("input_"))
async def application_processing(callback_query: types.CallbackQuery, state: FSMContext):
    data_type = callback_query.data.split("_")[1]
    application_id = callback_query.data.split("_")[-1]
    # Инициализация состояния и сохранение типа данных в FSMContext
    await state.update_data(data_type=data_type, application_id=application_id)

    
    await InputState.waiting_for_input.set()
    # Отправка сообщения с запросом ввода данных
    await callback_query.message.answer(f"Введите "+json_to_name(data_type))
    
    
    

@dp.message_handler(state=InputState.waiting_for_input, content_types=types.ContentTypes.TEXT)
async def process_input(message: types.Message, state: FSMContext):
    # Получение данных из состояния FSM
    data = await state.get_data()
    data_type = data.get("data_type")
    if data_type == "discordid":
        data_type = "discord_id"
    if data_type == "studentgroup":
        data_type = "student_group"
    if data_type == "applicantrole":
        data_type = "applicant_role"
    application_id = data.get("application_id")
    user_input = message.text
    # Обработка введенных данных пользователя
    application = [x for x in application_json if x['id']==int(application_id)][0]
    application[data_type]=user_input
    application["updated_at"]=datetime.datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f%z")
    
    conf_id = application["conf_id"]
    # Отправка подтверждения введенных данных
    await message.answer(f"Заявка обновлена, "+json_to_name(data_type)+": " + user_input, reply_markup=types.InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Выбор конференции", callback_data="conference")],
            [types.InlineKeyboardButton(text="Вернуться к заполнению заявки", callback_data="update_data_"+str(conf_id)+"_"+str(application_id))],
        ],
        resize_keyboard=True,
    ))

    # Сброс состояния после чтения ввода
    await state.finish()
    


# Запуск бота
if __name__ == '__main__':
    from aiogram import executor


    # Запуск бота
    executor.start_polling(dp, skip_updates=True)
    
