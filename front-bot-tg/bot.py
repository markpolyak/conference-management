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
import requests
from datetime import timezone
from data import *
    

# Инициализация бота
bot_token = '6297405813:AAF7QsOsC-LJzXDZu7LnTmA2vV48tdSNqII'
bot = Bot(token=bot_token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Define your states
class InputState(StatesGroup):
    waiting_for_input = State()
    waiting_for_coauthor_input = State()
    waiting_for_publication_input = State()
    coautor = State()
    new_application_input = State()


# Обработчик команды /start
@dp.message_handler(Command("start") & types.ChatType.is_private)
async def start(message: types.Message, state: FSMContext):
    
    
    await message.answer(start_message, reply_markup=InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Начать", callback_data = 'conference')]
        ],
        resize_keyboard=True,
    ))


@dp.callback_query_handler(lambda query: query.data == "conference")
async def conference_choise(callback_query: types.CallbackQuery, state: FSMContext):

    conferences_json = requests.get(f"http://127.0.0.1:8000/conferences").json()["conferences_json"]
    application_json = requests.get(f"http://127.0.0.1:8000/application_approval").json()["application_approval"]
   


    def time_mark(conf_id):
        current_date = datetime.date.today()
        # Check if registration is open
        registration_start_date = datetime.datetime.strptime(([x["registration_start_date"] for x in conferences_json if x['id']==int(conf_id)])[0], "%d.%m.%Y").date()
        registration_end_date = datetime.datetime.strptime(([x["registration_end_date"] for x in conferences_json if x['id']==int(conf_id)])[0], "%d.%m.%Y").date()
        
        new_application_allowance = registration_start_date <= current_date <= registration_end_date

        if new_application_allowance: return "(Можно подать)" 
        else: return "(Нельзя подать)"

    def conf_time_mark(conf_id):
        current_date = datetime.date.today()
        # Check if registration is open
        registration_end_date = datetime.datetime.strptime(([x["conf_end_date"] for x in conferences_json if x['id']==int(conf_id)])[0], "%d.%m.%Y").date()
        
        new_application_allowance =  current_date <= registration_end_date

        if new_application_allowance: return " " 
        else: return "(Конференция закончена)"


    def previous_application_mark(conf_id):
        
        if any([x for x in application_json if x["conf_id"] == (conf_id) and x["telegram_id"]==str(callback_query.from_user.id)]):
            return "(Есть заявки)"
        else: return  " "



    await callback_query.message.answer("Выберите конференцию", reply_markup=InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=x['name_rus_short'] + " (" + x["registration_start_date"] + " - " + x["registration_end_date"] + ")"
                                         + " " + time_mark(x["id"]) + " " + previous_application_mark(x["id"]) + " " + conf_time_mark(x["id"]),
                                           callback_data="id_"+str(x["id"]))] for x in conferences_json],
        resize_keyboard=True,
    ))
    
@dp.callback_query_handler(lambda query: query.data.startswith("id_"))
async def application_choise(callback_query: types.CallbackQuery, state: FSMContext):
    
    conf_id = callback_query.data.split("_")[1]
    
    conferences_json = requests.get(f"http://127.0.0.1:8000/conferences").json()["conferences_json"]
    application_json = requests.get(f"http://127.0.0.1:8000/application_approval").json()["application_approval"]

    conference  = [x for x in conferences_json if x['id']==int(conf_id)][0]

    # Get the current date
    current_date = datetime.date.today()

    # Check if registration is open
    registration_start_date = datetime.datetime.strptime(([x["registration_start_date"] for x in conferences_json if x['id']==int(conf_id)])[0], "%d.%m.%Y").date()
    registration_end_date = datetime.datetime.strptime(([x["registration_end_date"] for x in conferences_json if x['id']==int(conf_id)])[0], "%d.%m.%Y").date()
    
    new_application_allowance = registration_start_date <= current_date <= registration_end_date

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

    if new_application_allowance is True:
        inline_keyboard.append([InlineKeyboardButton(text="Подать новую заявку", callback_data="new_application"+"_"+str(conf_id)+"_"+str(get_unique_id()))])
    
    if not application_list:
        await callback_query.message.answer("Вы еще не подали заявку на участие"+output_msg
                                            , reply_markup=InlineKeyboardMarkup(
            inline_keyboard = inline_keyboard,
            resize_keyboard = True
        ))
    else: 
        
        inline_keyboard.append(InlineKeyboardButton(text = x['title'],
                                                     callback_data=('application_id_' + str(x['id']) +"_"+str(conf_id))) for x in application_list)
        
        await callback_query.message.answer(output_msg,
                                             reply_markup=InlineKeyboardMarkup(
            inline_keyboard = inline_keyboard,
            resize_keyboard = True
        ))
        
@dp.callback_query_handler(lambda query: query.data.startswith("application_id_"))
async def application_processing(callback_query: types.CallbackQuery, state: FSMContext):
    conferences_json = requests.get(f"http://127.0.0.1:8000/conferences").json()["conferences_json"]
    application_json = requests.get(f"http://127.0.0.1:8000/application_approval").json()["application_approval"]
    application_id = callback_query.data.split("_")[2]
    conf_id = callback_query.data.split("_")[3]

    application = [x for x in application_json if x['telegram_id'] == str(callback_query.from_user.id) and x['conf_id']==int(conf_id) and x['id']==int(application_id)]
    
    


    inline_keyboard = [[InlineKeyboardButton(text="Выбор конференции", callback_data="conference")],
                       [InlineKeyboardButton(text="Все заявки", callback_data="id_"+str(conf_id))],
                       [InlineKeyboardButton(text="Подача статьи", callback_data="article_submission_"+application_id)],
                       [InlineKeyboardButton(text="Обновить заявку", callback_data="update_data_"+conf_id+"_"+application_id)],
                       ]


    qwe = [x['name']+" "+x["surname"]+ " "+ x["patronymic"] for x in application[0]['coauthors']]

    aplication_info = f"""
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

    


    publications_json = requests.get(f"http://127.0.0.1:8000/publication").json()["publication_json"]

    

    publication = [x for x in publications_json if x["id"]==application[0]["id"]]


    if publication:
        
        publication_info = f"""
Данные обновлены:
Название статьи: {publication[0]["publication_title"]}
Дата обновления: {publication[0]["upload_date"]}
Статус ревью: {publication[0]["review_status"]}
Ссылка для скачивания: {publication[0]["download_url"]}
Ключевые слова: {publication[0]["keywords"]}
Аннотация: {publication[0]["abstract"]}
"""
    else:
        publication_info = "У вас нет статьи"


    info_message = f"Ваша заявка: {aplication_info} для конференции: {([x['name_rus'] for x in conferences_json if x['id']==int(conf_id)])[0]} {publication_info}"

    await callback_query.message.answer(info_message, reply_markup=InlineKeyboardMarkup(
        inline_keyboard=inline_keyboard,
        resize_keyboard=True,
    ))

@dp.callback_query_handler(lambda query: query.data.startswith("article_submission"))
async def application_processing(callback_query: types.CallbackQuery, state: FSMContext):
    application_id = callback_query.data.split("_")[-1]
    publications_json = requests.get(f"http://127.0.0.1:8000/publication").json()["publication_json"]
    
    publication = [x for x in publications_json if x['id']==int(application_id)]
    
    if publication:
        pass
        publication_info = f"""
Ваша статья:
Название статьи: {publication[0]["publication_title"]}
Дата обновления: {publication[0]["upload_date"]}
Статус ревью: {publication[0]["review_status"]}
Ссылка для скачивания: {publication[0]["download_url"]}
Ключевые слова: {publication[0]["keywords"]}
Аннотация: {publication[0]["abstract"]}
"""



        await callback_query.message.answer(f"У вас есть статья: {publication_info}", reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[[InlineKeyboardButton(text="Выбор конференции", callback_data="conference")],
                            [InlineKeyboardButton(text="Обновить данные по публикации", callback_data="update_publication_data_"+application_id)]],
                resize_keyboard=True
            ))


    else:

        publications_json = (create_new_publication(int(application_id),datetime.datetime.now(pytz.timezone('Europe/Moscow')).strftime("%Y-%m-%dT%H:%M:%S.%f%z")))
        response = requests.post("http://127.0.0.1:8000/new_publication", json=publications_json)
        await callback_query.message.answer("Публикация создана", reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text="Выбор конференции", callback_data="conference")],
                        [InlineKeyboardButton(text="Обновить данные по публикации", callback_data="update_publication_data_"+application_id)]],
            resize_keyboard=True
        ))

@dp.callback_query_handler(lambda query: query.data.startswith("update_publication_data_"))
async def application_processing(callback_query: types.CallbackQuery, state: FSMContext):
    publications_json = requests.get(f"http://127.0.0.1:8000/publication").json()["publication_json"]
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

    await callback_query.message.answer(info_message, reply_markup=InlineKeyboardMarkup(
        inline_keyboard=inline_keyboard,
        resize_keyboard=True,
    ))

@dp.callback_query_handler(lambda query: query.data.startswith("publication_input"))
async def application_processing(callback_query: types.CallbackQuery, state: FSMContext):
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
    publications_json = requests.get(f"http://127.0.0.1:8000/publication").json()["publication_json"]
    data = await state.get_data()
    data_type = data.get("data_type")
    application_id = data.get("application_id")
    user_input = message.text
    # Обработка введенных данных пользователя
    publication = [x for x in publications_json if x['id']==int(application_id)][0]

    publication[data_type]=user_input
    publication["upload_date"]=datetime.datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f%z")


    response = requests.post("http://127.0.0.1:8000/new_publication", json=publication)

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
                [types.InlineKeyboardButton(text="Подтвердить", callback_data="update_publication_data_"+"_"+str(application_id))],
                [types.InlineKeyboardButton(text="Неверно", callback_data="publication_input&download_url&"+application_id)]
            ],
            resize_keyboard=True,
        ))

    # Сброс состояния после чтения ввода
    await state.finish()
   
@dp.callback_query_handler(lambda query: query.data.startswith("new_application_"))
async def application_processing(callback_query: types.CallbackQuery, state: FSMContext):

    conf_id = callback_query.data.split("_")[-2]
    application_id = callback_query.data.split("_")[-1]
    application_data = (create_new_application(int(application_id),int(conf_id),str(callback_query.from_user.id),
                                                   datetime.datetime.now(pytz.timezone('Europe/Moscow')).strftime("%Y-%m-%dT%H:%M:%S.%f%z")))
    
    
    response = requests.post("http://127.0.0.1:8000/new_application", json=application_data)
    
   
    #application_json.append(new_application)

    await callback_query.message.answer("Введите данные:", reply_markup=InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="Выбор конференции", callback_data="conference")],
                       [InlineKeyboardButton(text="Заполнить данные по заявке", callback_data="save_application_"+conf_id+"_"+application_id)]],
        resize_keyboard=True
    ))

@dp.callback_query_handler(lambda query: query.data.startswith("update_data_"))
async def application_processing(callback_query: types.CallbackQuery, state: FSMContext):
    application_json = requests.get(f"http://127.0.0.1:8000/application_approval").json()["application_approval"]+requests.get(f"http://127.0.0.1:8000/application").json()["application_json"]
    conf_id = callback_query.data.split("_")[-2]
    application_id = callback_query.data.split("_")[-1]
    application = [x for x in application_json if x['id']==int(application_id)]
    
    info_message = f"""
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
                       [InlineKeyboardButton(text="Соавторы", callback_data="coauthors_input"+"_"+application_id)],
                       [InlineKeyboardButton(text="Сохранить заявку", callback_data="save_application"+"_"+application_id)]
                       ]

    

    await callback_query.message.answer(info_message, reply_markup=InlineKeyboardMarkup(
        inline_keyboard=inline_keyboard,
        resize_keyboard=True,
    ))

@dp.callback_query_handler(lambda query: query.data.startswith("save_application"))
async def application_processing(callback_query: types.CallbackQuery):
    application_json = requests.get(f"http://127.0.0.1:8000/application").json()["application_json"]
    application_id = callback_query.data.split("_")[-1]
    
    application = [x for x in application_json if x['id']==int(application_id)]
    conf_id = application[0]["conf_id"]
    
    
    info_message = f"""
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
    check = lambda x: False if x=="" else True

    approval = check(application[0]['email']) and check(application[0]['phone']) and check(application[0]['name']) and check(application[0]['patronymic'])and\
    check(application[0]['surname']) and check(application[0]['university']) and check(application[0]['student_group']) and\
    check(application[0]['applicant_role']) and check(application[0]['title']) and check(application[0]['adviser'])
                
    if approval:
        response = requests.post("http://127.0.0.1:8000/new_approval_application", json=application[0])
        

        await callback_query.message.answer(info_message, reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Выбор конференции", callback_data="conference")],
                [InlineKeyboardButton(text="Проверить данные по заявке", callback_data="update_data_"+str(conf_id)+"_"+application_id)],
            ],
            resize_keyboard=True
        ))
    else:
        await callback_query.message.answer(info_message, reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Заполнить данные по заявке", callback_data="update_data_"+str(conf_id)+"_"+application_id)],
            ],
            resize_keyboard=True
        ))

@dp.callback_query_handler(lambda query: query.data.startswith("coauthors_input"))
async def application_processing(callback_query: types.CallbackQuery):
    application_json = requests.get(f"http://127.0.0.1:8000/application_approval").json()["application_approval"]+requests.get(f"http://127.0.0.1:8000/application").json()["application_json"]
    application_id = callback_query.data.split("_")[-1]
    application = [x for x in application_json if x['id']==int(application_id)][0]
    conf_id = application["conf_id"]
    if application['coauthors']:
        msg = f"Ваши соавторы: { ', '.join([x['name']+' '+x['surname']+ ' '+ x['patronymic'] for x in application['coauthors']])}"
        await callback_query.message.answer(msg, reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text="Выбор конференции", callback_data="conference")],
                        [InlineKeyboardButton(text="Обновить данные по заявке", callback_data="update_data_"+str(conf_id)+"_"+str(application_id))],
                        [InlineKeyboardButton(text="Добавить", callback_data="add_coauthor_"+application_id)],
                        [InlineKeyboardButton(text="Удалить", callback_data="del_coauthor_"+application_id)]],
            resize_keyboard=True
        ))
    else:
        msg = f"Ваши соавторы: { ', '.join([x['name']+' '+x['surname']+ ' '+ x['patronymic'] for x in application['coauthors']])}"
        await callback_query.message.answer(msg, reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text="Выбор конференции", callback_data="conference")],
                        [InlineKeyboardButton(text="Обновить данные по заявке", callback_data="update_data_"+str(conf_id)+"_"+str(application_id))],
                        [InlineKeyboardButton(text="Добавить", callback_data="add_coauthor_"+application_id)]],
            resize_keyboard=True
        ))

@dp.callback_query_handler(lambda query: query.data.startswith("add_coauthor"))
async def application_processing(callback_query: types.CallbackQuery,state: FSMContext):
    application_id = callback_query.data.split("_")[-1]
   
    application_json = requests.get(f"http://127.0.0.1:8000/application_approval").json()["application_approval"]+requests.get(f"http://127.0.0.1:8000/application").json()["application_json"]

    
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
    application_json = requests.get(f"http://127.0.0.1:8000/application_approval").json()["application_approval"]+requests.get(f"http://127.0.0.1:8000/application").json()["application_json"]

    application = [x for x in application_json if x['id']==int(application_id)][0]
    conf_id = application["conf_id"]
    coauthors = [x['name']+' '+x['surname']+ ' '+ x['patronymic'] for x in application['coauthors']]
    if coauthors:
        inline_keyboard = [[InlineKeyboardButton(text=x[1], callback_data=f"del_this_coauthor_"+str(x[0])+"_"+str(application_id))] for x in enumerate(coauthors)]
        await callback_query.message.answer("Выберите соавтора для удаления", reply_markup=InlineKeyboardMarkup(
            inline_keyboard=inline_keyboard,
            resize_keyboard=True
        ))
    else:
        inline_keyboard =[[InlineKeyboardButton(text="Заполнить данные по заявке", callback_data="save_application_"+conf_id+"_"+application_id)]]
        await callback_query.message.answer("Продолжить", reply_markup=InlineKeyboardMarkup(
            inline_keyboard=inline_keyboard,
            resize_keyboard=True
        ))

@dp.callback_query_handler(lambda query: query.data.startswith("del_this_coauthor"))
async def application_processing(callback_query: types.CallbackQuery):
    application_id = callback_query.data.split("_")[-1]
    coautor = callback_query.data.split("_")[-2]
    application_json = requests.get(f"http://127.0.0.1:8000/application_approval").json()["application_approval"]+requests.get(f"http://127.0.0.1:8000/application").json()["application_json"]
    application = [x for x in application_json if x['id']==int(application_id)][0]
    conf_id = application["conf_id"]

    application["coauthors"].pop(int(coautor))
    
    response = requests.post("http://127.0.0.1:8000/new_application", json=application)

    await callback_query.message.answer("Продолжить", reply_markup=InlineKeyboardMarkup(
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
    application_json = requests.get(f"http://127.0.0.1:8000/application_approval").json()["application_approval"]+requests.get(f"http://127.0.0.1:8000/application").json()["application_json"]
    application = [x for x in application_json if x['id']==int(application_id)][0]
    application["coauthors"].append(coauthor)
    response = requests.post("http://127.0.0.1:8000/new_application", json=application)
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
    if data_type == "studentgroup":
        data_type = "student_group"
    if data_type == "applicantrole":
        data_type = "applicant_role"
    # Отправка сообщения с запросом ввода данных
    await callback_query.message.answer(f"Введите "+json_to_name(data_type))
    
@dp.message_handler(state=InputState.waiting_for_input, content_types=types.ContentTypes.TEXT)
async def process_input(message: types.Message, state: FSMContext):
    # Получение данных из состояния FSM
    data = await state.get_data()
    data_type = data.get("data_type")

    if data_type == "studentgroup":
        data_type = "student_group"
    if data_type == "applicantrole":
        data_type = "applicant_role"
    application_id = data.get("application_id")
    user_input = message.text
    # Обработка введенных данных пользователя
    application_json = requests.get(f"http://127.0.0.1:8000/application_approval").json()["application_approval"]+requests.get(f"http://127.0.0.1:8000/application").json()["application_json"]
    application = [x for x in application_json if x['id']==int(application_id)][0]
    application[data_type]=user_input
    application["updated_at"]=datetime.datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f%z")
    
    response = requests.post("http://127.0.0.1:8000/new_application", json=application)

    conf_id = application["conf_id"]
    # Отправка подтверждения введенных данных
    await message.answer(f"Не забудьте сохранить изменения!, "+json_to_name(data_type)+": " + user_input, reply_markup=types.InlineKeyboardMarkup(
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
    
