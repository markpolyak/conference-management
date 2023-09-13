import asyncio  #подключение
import time
import disnake
from disnake import ui
from disnake.ext import commands
from config import *
import json
import datetime
from disnake import TextInputStyle
import uuid
from disnake.interactions import Interaction

'''Подключаем привелегии, префикс, интенты и т.д.'''
intents = disnake.Intents().all()
bot = commands.Bot(command_prefix=PREFIX, intents=intents)
message_id = ''
conference_names = ""
keyin = None

'''Загружаем json файлы'''
with open('conferences.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

with open('conferences_full.json', 'r', encoding='utf-8') as file:
    data_full = json.load(file)

with open('publications.json', 'r', encoding='utf-8') as file:
    data_pub = json.load(file)

with open('authors.json', 'r', encoding='utf-8') as file:
    data_auto = json.load(file)


'''Обработка при начале бота'''
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

'''Список всех конференций'''
@bot.command()
async def conferences(ctx):
    global name
    count = 1
    # Создаем эмбед с информацией о доступных и завершенных конференциях
    embed = disnake.Embed(title='Список конференций', description='Выберите конференцию для просмотра заявок:',
                          color=disnake.Color.blue()) #Создаём Embed сообщение для отображения конференций

    if isinstance(data, list):
        for item in data:
            if 'name_rus_short' in item:
                name = item['name_rus_short']
                embed.add_field(name="", value=f"{count}. {name}\n", inline=False)
                count += 1
                # Перебираем каждое значение из data.json и добавляем строку с названием конференции
    embed.set_footer(text='Введите название конференции после команды ">select [название конференции]"')

    await ctx.send(embed=embed)


'''Полная информация о определённой конференции по названию'''
@bot.command()
async def select(ctx, * ,conference_name: str):
    global conference, status, MyView, view
    if isinstance(data, list):
        for item in data:
            if 'name_rus_short' in item:
                names = item['name_rus_short']
                if names == conference_name:
                    embed = disnake.Embed(title=f'Конференция: {conference_name}',
                                          description='',
                                          color=disnake.Color.blue()) #Создаём Embed сообщение для отображения выбранной конференции

                    for conference in data_full:
                        # проверяем, завершена ли конференция (сравниваем текущую дату с датой окончания) - пока что не используется
                        if conference['conf_end_date'] < datetime.datetime.today().strftime('%Y-%m-%d'):
                            status = 'Завершена'
                        else:
                            status = 'Открыта'

                    embed.add_field(name="", value=f"**{conference['name_rus']}** ({conference['name_eng']})\n"
                                                   f"Статус: {status}\n"
                                                   f"Дата начала: {conference['conf_start_date']}\n"
                                                   f"Дата окончания: {conference['conf_end_date']}\n"
                                                   f"Дата начала регистрации заявок: {conference['registration_start_date']}\n"
                                                   f"Дата окончания регистрации заявок: {conference['registration_end_date']}\n"
                                                   f"Дата начала приёма докладов: {conference['submission_start_date']}\n"
                                                   f"Дата окончания приёма докладов: {conference['submission_end_date']}\n"
                                                   f"Организаторы: {conference['organized_by']}\n"
                                                   f"URL: {conference['url']}\n"
                                                   f"Email: {conference['email']}\n\n", inline=False) #Выводим полную информацию о выбранной конференции, нужно будет привязать conferences.json и conferences_full.json
                    if status == "Открыта":
                        view = ui.View()
                        button = ui.Button(label=f"Оставить заявку", style=disnake.ButtonStyle.gray, custom_id="one")
                        view.add_item(button) #Создаём кнопку если статус заявки 'открыта'
                        conference_names = conference_name #используется для того

                        '''Функция обработка кнопки'''
                        @bot.event
                        async def on_button_click(ctx):
                            await ctx.send("Введите ваш Telegram ID:")
                            tg_msg = await bot.wait_for('message', check=lambda m: m.author == ctx.author)
                            tg = tg_msg.content
                            if tg == "Отмена":
                                await ctx.send("Отменено")
                                return
                            #Обрабатываем сообщения пользователя
                            await ctx.send("Введите ваш Discord ID:")
                            discord_msg = await bot.wait_for('message', check=lambda m: m.author == ctx.author)
                            discord = discord_msg.content
                            if discord == "Отмена":
                                await ctx.send("Отменено")
                                return
                            # Обрабатываем сообщения пользователя
                            await ctx.send("Введите ваш email:")
                            email_msg = await bot.wait_for('message', check=lambda m: m.author == ctx.author)
                            email = email_msg.content
                            if email == "Отмена":
                                await ctx.send("Отменено")
                                return
                            # Обрабатываем сообщения пользователя
                            await ctx.send("Введите ваш номер телефона:")
                            phone_msg = await bot.wait_for('message', check=lambda m: m.author == ctx.author)
                            phone = phone_msg.content
                            if phone == "Отмена":
                                await ctx.send("Отменено")
                                return
                            # Обрабатываем сообщения пользователя
                            await ctx.send("Введите ваше имя:")
                            name_msg = await bot.wait_for('message', check=lambda m: m.author == ctx.author)
                            name = name_msg.content
                            if name == "Отмена":
                                await ctx.send("Отменено")
                                return
                            # Обрабатываем сообщения пользователя
                            await ctx.send("Введите вашу фамилию:")
                            surname_msg = await bot.wait_for('message', check=lambda m: m.author == ctx.author)
                            surname = surname_msg.content
                            if surname == "Отмена":
                                await ctx.send("Отменено")
                                return
                            # Обрабатываем сообщения пользователя
                            await ctx.send("Введите ваше отчество:")
                            patronymic_msg = await bot.wait_for('message', check=lambda m: m.author == ctx.author)
                            patronymic = patronymic_msg.content
                            if patronymic == "Отмена":
                                await ctx.send("Отменено")
                                return
                            # Обрабатываем сообщения пользователя
                            await ctx.send("Введите ваш университет:")
                            university_msg = await bot.wait_for('message', check=lambda m: m.author == ctx.author)
                            university = university_msg.content
                            if university == "Отмена":
                                await ctx.send("Отменено")
                                return
                            # Обрабатываем сообщения пользователя
                            await ctx.send("Введите вашу студенческую группу:")
                            student_group_msg = await bot.wait_for('message', check=lambda m: m.author == ctx.author)
                            student_group = student_group_msg.content
                            if student_group == "Отмена":
                                await ctx.send("Отменено")
                                return
                            # Обрабатываем сообщения пользователя
                            await ctx.send("Введите вашу роль:")
                            applicant_role_msg = await bot.wait_for('message', check=lambda m: m.author == ctx.author)
                            applicant_role = applicant_role_msg.content
                            submitted_at = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
                            if applicant_role == "Отмена":
                                await ctx.send("Отменено")
                                return
                            # Обрабатываем сообщения пользователя
                            await ctx.send("Введите название работы:")
                            title_msg = await bot.wait_for('message', check=lambda m: m.author == ctx.author)
                            title = title_msg.content
                            updated_at = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
                            if title == "Отмена":
                                await ctx.send("Отменено")
                                return
                            # Обрабатываем сообщения пользователя
                            await ctx.send("Введите инициалы вашего советника:")
                            adviser_msg = await bot.wait_for('message', check=lambda m: m.author == ctx.author)
                            adviser = adviser_msg.content
                            if adviser == "Отмена":
                                await ctx.send("Отменено")
                                return
                            # Обрабатываем сообщения пользователя


                            with open('data.json', 'r') as file:
                                existing_data = json.load(file) #Открываем json файл

                            new_id = 1
                            if existing_data:
                                ids = existing_data.keys()
                                existing_ids = [int(i) for i in ids]
                                new_id = max(existing_ids) + 1
                                # Обработка ID каждой заявки

                            # Добавление новой публикации в существующие данные
                            existing_data[str(new_id)] = {
                                "id": str(new_id),
                                "telegram_id": tg,
                                "discord_id": discord,
                                "submitted_at": submitted_at,
                                "updated_at": updated_at,
                                "email": email,
                                "phone": phone,
                                "name": str(name),
                                "surname": str(surname),
                                "patronymic": str(patronymic),
                                "university": university,
                                "student_group": student_group,
                                "applicant_role": applicant_role,
                                "title": title,
                                "adviser": adviser,
                                "conference": conference_name,
                                "coauthors": [{}]
                            }

                            # Запись данных в JSON-файл с отступами
                            with open('data.json', 'w') as file:
                                json.dump(existing_data, file, ensure_ascii=False, indent=4)

                            await ctx.send(f"Заявка успешно отправлена, вот её данные:\n"
                                           f"ID: {new_id}\n"
                                           f"Telegram ID: {tg}\n"
                                           f"Discord ID:{discord}\n"
                                           f"Загружено в: {submitted_at}\n"
                                           f"Обновлено в: {updated_at}\n"
                                           f"Email: {email}\n"
                                           f"Телефон: {phone}\n"
                                           f"Имя: {name}\n"
                                           f"Фамилия: {surname}\n"
                                           f"Отчество: {patronymic}\n"
                                           f"Университет: {university}\n"
                                           f"Группа: {student_group}\n"
                                           f"Роль: {applicant_role}\n"
                                           f"Название работы: {title}\n"
                                           f"Советник: {adviser}\n"
                                           f"Соавторы: Не указаны.")




                        await ctx.send(embed=embed, view=view)
                    else:
                        await ctx.send(embed=embed)



'''Функция редактирования'''

'''Функция редактирования публикации'''
@bot.command()
async def edit_pub(ctx, id:int):
        # Загрузка существующих данных из JSON
        with open('publications.json', 'r') as file:
            existing_data = json.load(file)

        if str(id) not in existing_data:
            await ctx.send("Публикация с указанным ID не существует.")
            return

        # Вопрос 1: Новое название публикации
        await ctx.send("Введите новое название публикации:")
        title_msg = await bot.wait_for('message', check=lambda m: m.author == ctx.author)
        new_title = title_msg.content

        # Вопрос 2: Новый URL
        await ctx.send("Введите новый URL:")
        url_msg = await bot.wait_for('message', check=lambda m: m.author == ctx.author)
        new_url = url_msg.content

        upload_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
        existing_data[str(id)] = {
            "title": new_title,
            "url": new_url,
            "upload_date": upload_date
        }
        with open('publications.json', 'w') as file:
            json.dump(existing_data, file, ensure_ascii=False, indent=4)

        await ctx.send("Публикация успешно изменена!")



'''Функция добавления автора'''
async def author(ctx):

    await ctx.send("Введите ваше имя:")
    name_msg = await bot.wait_for('message', check=lambda m: m.author == ctx.author)
    name = name_msg.content

    await ctx.send("Введите вашу фамилию:")
    surname_msg = await bot.wait_for('message', check=lambda m: m.author == ctx.author)
    surname = surname_msg.content

    # Вопрос 3: Отчество
    await ctx.send("Введите ваше отчество:")
    patronymic_msg = await bot.wait_for('message', check=lambda m: m.author == ctx.author)
    patronymic = patronymic_msg.content

    # Вопрос 4: Email
    await ctx.send("Введите ваш email:")
    email_msg = await bot.wait_for('message', check=lambda m: m.author == ctx.author)
    email = email_msg.content

    # Вопрос 5: Номер телефона
    await ctx.send("Введите ваш номер телефона:")
    phone_msg = await bot.wait_for('message', check=lambda m: m.author == ctx.author)
    phone = phone_msg.content

    # Вопрос 6: Биография
    await ctx.send("Введите вашу биографию:")
    bio_msg = await bot.wait_for('message', check=lambda m: m.author == ctx.author)
    bio = bio_msg.content

    # Вопрос 7: Название организации
    await ctx.send("Введите название вашей организации:")
    organization_msg = await bot.wait_for('message', check=lambda m: m.author == ctx.author)
    organization = organization_msg.content

    # Вопрос 8: Роль
    await ctx.send("Введите вашу роль:")
    role_msg = await bot.wait_for('message', check=lambda m: m.author == ctx.author)
    role = role_msg.content

    with open('authors.json', 'r') as file:
        existing_data = json.load(file) # Открываем JSON файл для считывания информации

    new_id = 1
    if existing_data:
        ids = existing_data.keys()
        existing_ids = [int(i) for i in ids]
        new_id = max(existing_ids) + 1
    #Релизация ID публикации

    existing_data[str(new_id)] = {
        "name": name,
        "surname": surname,
        "patronymic": patronymic,
        "email": email,
        "phone": phone,
        "bio": bio,
        "organization": organization,
        "role": role
    }

    with open('authors.json', 'w') as file:
        json.dump(existing_data, file, ensure_ascii=False, indent=4)
    # Запись публикации в JSON файл

    await ctx.send("Информация об авторе успешно добавлена!")


'''Функция выбора заявки по её ID'''
@bot.command()
async def select_app(ctx, id: int):
    global tg, discord, submitted_at, updated_at, email, phone, name, surname, patronymic, university, student_group, applicant_role, adviser, conferense, key
    with open("data.json", 'r') as file:
        datatwo = json.load(file)  # Загружаем JSON файл

    key = str(id)  # Определяем key
    keyin = key
    if key in datatwo:
        request = datatwo[key]
        new_id = key
        tg = request['telegram_id']
        discord = request['discord_id']
        submitted_at = request['submitted_at']
        updated_at = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
        email = request['email']
        phone = request['phone']
        name = request['name']
        surname = request['surname']
        patronymic = request['patronymic']
        university = request['university']
        student_group = request['student_group']
        applicant_role = request['applicant_role']
        title = request['title']
        adviser = request['adviser']
        conferense = request['conference']  # Через переменную request считываем всю информацию из json файла по определённому ключу

    embed = disnake.Embed(title="Информация о заявке",
                          description=
                          f"ID: {key}\n"
                          f"Telegram ID: {tg}\n"
                          f"Discord ID:{discord}\n"
                          f"Загружено в: {submitted_at}\n"
                          f"Обновлено в: {updated_at}\n"
                          f"Email: {email}\n"
                          f"Телефон: {phone}\n"
                          f"Имя: {name}\n"
                          f"Фамилия: {surname}\n"
                          f"Отчество: {patronymic}\n"
                          f"Университет: {university}\n"
                          f"Группа: {student_group}\n"
                          f"Роль: {applicant_role}\n"
                          f"Название работы: {title}\n"
                          f"Советник: {adviser}\n"
                          f"Соавторы: Не указаны.\n"
                          f"Заявка подана на конференцию: {conferense}",
                          color=disnake.Color.yellow())

    edit_button = ui.Button(custom_id='edit', label='Редактировать', style=disnake.ButtonStyle.secondary)
    add_author_button = ui.Button(custom_id='add_author', label='Добавить автора',
                                       style=disnake.ButtonStyle.secondary)
    add_coauthor_button = ui.Button(custom_id='add_coauthor', label='Добавить со-автора',
                                         style=disnake.ButtonStyle.secondary)
    add_publication_button = ui.Button(custom_id='add_publication', label='Добавить публикацию',
                                            style=disnake.ButtonStyle.secondary)
    exit_button = ui.Button(custom_id='exit_btn', label='Отмена',
                                            style=disnake.ButtonStyle.secondary)

    action_row = disnake.ui.ActionRow(edit_button, add_author_button, add_coauthor_button, add_publication_button, exit_button)
    await ctx.send(embed=embed, components=[action_row])

    async def so_author(ctx):
        main = "Да"
        # Вопрос 1: Имя
        await ctx.send("Введите имя:")
        name_msg = await bot.wait_for('message', check=lambda m: m.author == ctx.author)
        soname = name_msg.content
        # Вопрос 2: Фамилия
        await ctx.send("Введите фамилию:")
        surname_msg = await bot.wait_for('message', check=lambda m: m.author == ctx.author)
        sosurname = surname_msg.content

        # Вопрос 3: Отчество
        await ctx.send("Введите отчество:")
        patronymic_msg = await bot.wait_for('message', check=lambda m: m.author == ctx.author)
        sopatronymic = patronymic_msg.content

        with open('data.json', 'r') as file:
            existing_data = json.load(file)
            request = existing_data[key]
            new_id = key
            tg = request['telegram_id']
            discord = request['discord_id']
            submitted_at = request['submitted_at']
            updated_at = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
            email = request['email']
            phone = request['phone']
            name = request['name']
            surname = request['surname']
            patronymic = request['patronymic']
            university = request['university']
            student_group = request['student_group']
            applicant_role = request['applicant_role']
            title = request['title']
            adviser = request['adviser']
            conferense = request['conference']  # Считываем всю информацию с json файла по ключу

        existing_data[str(key)] = {
            "id": str(key),
            "telegram_id": tg,
            "discord_id": discord,
            "submitted_at": submitted_at,
            "updated_at": updated_at,
            "email": email,
            "phone": phone,
            "name": str(name),
            "surname": str(surname),
            "patronymic": str(patronymic),
            "university": university,
            "student_group": student_group,
            "applicant_role": applicant_role,
            "title": title,
            "adviser": adviser,
            "conference": conferense,
            "coauthors": {
                "name": soname,
                "surname": sosurname,
                "patronymic": sopatronymic,
            }
        }  # Записываем новую информацию в доп.список

        with open('data.json', 'w') as file:
            json.dump(existing_data, file, ensure_ascii=False, indent=4)  # Записываем изменения

        await ctx.send("Информация об со-авторе успешно добавлена!")

    async def edit(ctx):
        with open('data.json', 'r') as file:
            existing_data = json.load(file)  # Открываем JSON файл

        if key in existing_data:
            request = existing_data[key]
            new_id = key
            tg = request['telegram_id']
            discord = request['discord_id']
            submitted_at = request['submitted_at']
            updated_at = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
            email = request['email']
            phone = request['phone']
            name = request['name']
            surname = request['surname']
            patronymic = request['patronymic']
            university = request['university']
            student_group = request['student_group']
            applicant_role = request['applicant_role']
            title = request['title']
            adviser = request['adviser']
            conferense = request['conference']
            # Обрабатываем определённые строчки по ID указанным пользователем
        await asyncio.sleep(0.3)

            # Обрабатываем сообщения пользователя
        await ctx.send("Введите ваш Telegram ID:")
        tg_msg = await bot.wait_for('message', check=lambda m: m.author == ctx.author)
        tg = tg_msg.content
        if tg == "Отмена":
            await ctx.send("Отменено")
            return
            # Обрабатываем сообщения пользователя
        await ctx.send("Введите ваш Discord ID:")
        discord_msg = await bot.wait_for('message', check=lambda m: m.author == ctx.author)
        discord = discord_msg.content
        if discord == "Отмена":
            await ctx.send("Отменено")
            return
                # Обрабатываем сообщения пользователя
        await ctx.send("Введите ваш email:")
        email_msg = await bot.wait_for('message', check=lambda m: m.author == ctx.author)
        email = email_msg.content
        if email == "Отмена":
            await ctx.send("Отменено")
            return
                # Обрабатываем сообщения пользователя
        await ctx.send("Введите ваш номер телефона:")
        phone_msg = await bot.wait_for('message', check=lambda m: m.author == ctx.author)
        phone = phone_msg.content
        if phone == "Отмена":
            await ctx.send("Отменено")
            return
                # Обрабатываем сообщения пользователя
        await ctx.send("Введите ваше имя:")
        name_msg = await bot.wait_for('message', check=lambda m: m.author == ctx.author)
        name = name_msg.content
        if name == "Отмена":
            await ctx.send("Отменено")
            return
                # Обрабатываем сообщения пользователя
        await ctx.send("Введите вашу фамилию:")
        surname_msg = await bot.wait_for('message', check=lambda m: m.author == ctx.author)
        surname = surname_msg.content
        if surname == "Отмена":
            await ctx.send("Отменено")
            return
                # Обрабатываем сообщения пользователя
        await ctx.send("Введите ваше отчество:")
        patronymic_msg = await bot.wait_for('message', check=lambda m: m.author == ctx.author)
        patronymic = patronymic_msg.content
        if patronymic == "Отмена":
            await ctx.send("Отменено")
            return
                # Обрабатываем сообщения пользователя
        await ctx.send("Введите ваш университет:")
        university_msg = await bot.wait_for('message', check=lambda m: m.author == ctx.author)
        university = university_msg.content
        if university == "Отмена":
            await ctx.send("Отменено")
            return
                # Обрабатываем сообщения пользователя
        await ctx.send("Введите вашу студенческую группу:")
        student_group_msg = await bot.wait_for('message', check=lambda m: m.author == ctx.author)
        student_group = student_group_msg.content
        if student_group == "Отмена":
            await ctx.send("Отменено")
            return
                # Обрабатываем сообщения пользователя
        await ctx.send("Введите вашу роль:")
        applicant_role_msg = await bot.wait_for('message', check=lambda m: m.author == ctx.author)
        applicant_role = applicant_role_msg.content
        submitted_at = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
        if applicant_role == "Отмена":
            await ctx.send("Отменено")
            return
                # Обрабатываем сообщения пользователя
        await ctx.send("Введите название работы:")
        title_msg = await bot.wait_for('message', check=lambda m: m.author == ctx.author)
        title = title_msg.content
        updated_at = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
        if title == "Отмена":
            await ctx.send("Отменено")
            return
                # Обрабатываем сообщения пользователя
        await ctx.send("Введите инициалы вашего советника:")
        adviser_msg = await bot.wait_for('message', check=lambda m: m.author == ctx.author)
        adviser = adviser_msg.content
        if adviser == "Отмена":
            await ctx.send("Отменено")
            return
                # Обрабатываем сообщения пользователя
        new_data = {}  # Создаём список
        new_data[str(key)] = {
                "id": str(key),
                "telegram_id": tg,
                "discord_id": discord,
                "submitted_at": submitted_at,
                "updated_at": updated_at,
                "email": email,
                "phone": phone,
                "name": str(name),
                "surname": str(surname),
                "patronymic": str(patronymic),
                "university": university,
                "student_group": student_group,
                "applicant_role": applicant_role,
                "title": title,
                "adviser": adviser,
                "conference": conferense,
                "coauthors": [{}]
            }  # Добавляем нужную информацию после обработки сообщений пользователя
        with open('data.json', 'w') as file:
            json.dump(new_data, file, ensure_ascii=False, indent=4)  # Открываем JSON файл

        await ctx.send(f"Успешно заменено! Ваши новые данные:\n"
                           f"ID: {key}\n"
                           f"Telegram ID: {tg}\n"
                           f"Discord ID:{discord}\n"
                           f"Загружено в: {submitted_at}\n"
                           f"Обновлено в: {updated_at}\n"
                           f"Email: {email}\n"
                           f"Телефон: {phone}\n"
                           f"Имя: {name}\n"
                           f"Фамилия: {surname}\n"
                           f"Отчество: {patronymic}\n"
                           f"Университет: {university}\n"
                           f"Группа: {student_group}\n"
                           f"Роль: {applicant_role}\n"
                           f"Название работы: {title}\n"
                           f"Советник: {adviser}\n"
                           f"Соавторы: Не указаны."
                           )

    async def author(ctx):
        await ctx.send("Введите ваше имя:")
        name_msg = await bot.wait_for('message', check=lambda m: m.author == ctx.author)
        name = name_msg.content

        await ctx.send("Введите вашу фамилию:")
        surname_msg = await bot.wait_for('message', check=lambda m: m.author == ctx.author)
        surname = surname_msg.content

        # Вопрос 3: Отчество
        await ctx.send("Введите ваше отчество:")
        patronymic_msg = await bot.wait_for('message', check=lambda m: m.author == ctx.author)
        patronymic = patronymic_msg.content

        # Вопрос 4: Email
        await ctx.send("Введите ваш email:")
        email_msg = await bot.wait_for('message', check=lambda m: m.author == ctx.author)
        email = email_msg.content

        # Вопрос 5: Номер телефона
        await ctx.send("Введите ваш номер телефона:")
        phone_msg = await bot.wait_for('message', check=lambda m: m.author == ctx.author)
        phone = phone_msg.content

        # Вопрос 6: Биография
        await ctx.send("Введите вашу биографию:")
        bio_msg = await bot.wait_for('message', check=lambda m: m.author == ctx.author)
        bio = bio_msg.content

        # Вопрос 7: Название организации
        await ctx.send("Введите название вашей организации:")
        organization_msg = await bot.wait_for('message', check=lambda m: m.author == ctx.author)
        organization = organization_msg.content

        # Вопрос 8: Роль
        await ctx.send("Введите вашу роль:")
        role_msg = await bot.wait_for('message', check=lambda m: m.author == ctx.author)
        role = role_msg.content

        with open('authors.json', 'r') as file:
            existing_data = json.load(file)  # Открываем JSON файл для считывания информации

        new_id = 1
        if existing_data:
            ids = existing_data.keys()
            existing_ids = [int(i) for i in ids]
            new_id = max(existing_ids) + 1
        # Релизация ID публикации

        existing_data[str(new_id)] = {
            "id": new_id,
            "name": name,
            "surname": surname,
            "patronymic": patronymic,
            "email": email,
            "phone": phone,
            "bio": bio,
            "organization": organization,
            "role": role
        }

        with open('authors.json', 'w') as file:
            json.dump(existing_data, file, ensure_ascii=False, indent=4)
        # Запись публикации в JSON файл

        await ctx.send("Информация об авторе успешно добавлена!")

    async def new_pub(ctx):
        with open('data.json', 'r') as file:
            existing_data = json.load(file)

        await ctx.send("Введите название публикации:")
        title_msg = await bot.wait_for('message', check=lambda m: m.author == ctx.author)
        title = title_msg.content
        # Запись временной метки
        upload_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')

        await ctx.send("Введите статус рецензирования:")
        review_msg = await bot.wait_for('message', check=lambda m: m.author == ctx.author)
        review_status = review_msg.content

        await ctx.send("Введите URL:")
        url_msg = await bot.wait_for('message', check=lambda m: m.author == ctx.author)
        url = url_msg.content

        await ctx.send("Введите ключевые слова:")
        keywords_msg = await bot.wait_for('message', check=lambda m: m.author == ctx.author)
        keywords = keywords_msg.content

        await ctx.send("Введите аннотацию:")
        abstract_msg = await bot.wait_for('message', check=lambda m: m.author == ctx.author)
        abstract = abstract_msg.content

        # Загрузка существующих данных из JSON
        with open('publications.json', 'r') as file:
            existing_data = json.load(file)

        new_id = keyin

        # Добавление новой публикации в существующие данные
        existing_data[str(new_id)] = {
            "id": new_id,
            "title": title,
            "upload_date": upload_date,
            "review_status": review_status,
            "url": url,
            "keywords": keywords,
            "abstract": abstract
        }

        # Запись данных в JSON-файл
        with open('publications.json', 'w') as file:
            json.dump(existing_data, file, ensure_ascii=False, indent=4)

        await ctx.send("Публикация успешно добавлена!")
    @bot.event
    async def on_button_click(interaction: disnake.Interaction):
        if interaction.component.custom_id == 'edit':
            await edit(interaction)
        elif interaction.component.custom_id == 'add_author':
            await author(interaction)
        elif interaction.component.custom_id == 'add_coauthor':
            await so_author(interaction)
        elif interaction.component.custom_id == 'add_publication':
            await new_pub(interaction)
        elif interaction.component.custom_id == "exit_btn":
            await interaction.response.send_message("Отменено.")
            return



@bot.command()
async def helps(ctx):
    embed = disnake.Embed(title="", description="",color=disnake.Color.green())
    embed.add_field(
        name="Список команд:",
        value=f">conferences (аругментов не требуется)"
              f">select (выбрать конференцию по названию, входной аргумент: название!)"
              f">edit_pub (внести изменения в существующую публикацию, входной аргумент: ID)"
              f">select_app (посмотреть информацию о заявке, входной аргумент: ID заявки!"
    )
    await ctx.send(embed=embed)
bot.run(TOKEN)