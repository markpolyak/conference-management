import discord
import requests
from discord.ui import Button, View, modal
from discord.ext import commands
from discord import message
import json
import datetime
from datetime import timezone
import time
import pytz
from database import *


#проверка возможности отправить заявку
def reg_check(id):
    current_date = datetime.date.today()
    registration_start_date = datetime.datetime.strptime(
        ([x["registration_start_date"] for x in conferences_json if x['conference_id'] == id])[0],
        "%d-%m-%Y").date()
    registration_end_date = datetime.datetime.strptime(
        ([x["registration_end_date"] for x in conferences_json if x['conference_id'] == id])[0], "%d-%m-%Y").date()

    return registration_start_date <= current_date <= registration_end_date


#закончилась ли конференция
def conf_check(id):
    current_date = datetime.date.today()
    conference_end_date = datetime.datetime.strptime(
        ([x["conference_end_date"] for x in conferences_json if x['conference_id'] == id])[0], "%d-%m-%Y").date()

    return current_date <= conference_end_date


#ужасный костыль
idholder = ""
new_app_holder = {
        "id": " ",
        "conference_id": " ",
        "telegram_id": " ",
        "discord_id": " ",
        "submitted_at": " ",
        "updated_at": " ",
        "email": " ",
        "phone": " ",
        "name": " ",
        "surname": " ",
        "patronymic": " ",
        "university": " ",
        "student_group": " ",
        "applicant_role": " ",
        "title": " ",
        "adviser": " ",
        "coauthors": []
    }

#можно ли отправить статью
def submission_check(id):
    current_date = datetime.date.today()
    submission_end_date = datetime.datetime.strptime(
        ([x["submission_end_date"] for x in conferences_json if x['conference_id'] == id])[0], "%d-%m-%Y").date()

    return current_date <= submission_end_date

#были ранее поданные заявки или нет
def application_check(id):
    if any([x for x in application_json if x["conference_id"] == (id) and x["discord_id"] == "1234"]):
        return True
    else:
        return False


intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)


#выбор конференции
@bot.command()
async def start(ctx):
    view = View()
    for x in conferences_json:
        label = x["conference_short_name_russian"]
        custom_id = x["conference_id"]
        emoji = ""
        if conf_check(x['conference_id']):
            style = discord.ButtonStyle.green
        else:
            style = discord.ButtonStyle.red
        if reg_check(x['conference_id']):
            emoji += "👍"
        if application_check(x['conference_id']):
            emoji += "📃"
        if emoji == "":
            emoji += "🛑"
        button = Button(label=label, style=style, custom_id=custom_id, emoji=emoji)
        view.add_item(button)
    await ctx.send("Выберите конференцию. \nКрасным отмечены конференции, которые уже прошли. \nКонференции на которые "
                   "можно подать заявку отмечены знаком 👍\n"
                   "Конференции на которые вы ранее подавали заявку отмечены знаком 📃", view=view)
    res = await bot.wait_for('interaction', check=lambda interaction: interaction.data["component_type"] == 2 and "custom_id" in interaction.data.keys())
    for item in view.children:
        if item.custom_id == res.data["custom_id"]:
            button = item
            await second_view(ctx, button.custom_id)

#страничка конференции
async def second_view(ctx, id):
    conference = [x for x in conferences_json if x['conference_id'] == id][0]
    application_list = [x for x in application_json if x['discord_id'] == "1234" and x['conference_id'] == id]
    name = conference["conference_name_russian"]
    await ctx.send(f"Вы выбрали конференцию: {name}\nСписок поданных заявок:\n")
    if not application_list:
        await ctx.send("Вы еще не подали заявку на участие")
    else:
        view1 = View()
        for x in application_list:
            title = x["title"]
            button = Button(label=title, emoji="🔍", custom_id=x["id"])
            view1.add_item(button)
        await ctx.send(view=view1)
    view = View()
    button1 = Button(label="Информация о конференции", style=discord.ButtonStyle.green)
    button2 = Button(label="Подать заявку", style=discord.ButtonStyle.green)
    button3 = Button(label="Назад", style=discord.ButtonStyle.red)
    view.add_item(button1)
    if reg_check(id):
        view.add_item(button2)
    view.add_item(button3)

    async def back_button_callback(interaction):
        await start(ctx)

    button3.callback = back_button_callback

    async def info_button_callback(interaction):
        await conference_info(ctx, id)

    button1.callback = info_button_callback

    async def add_button_callback(interaction: discord.Interaction):
        global idholder
        idholder = id
        #new_app = create_new_application(get_unique_id(application_json), id, "1234", datetime.datetime.now(pytz.timezone('Europe/Moscow')).strftime("%Y-%m-%dT%H:%M:%S.%f%z"))
        await interaction.response.send_modal(AddModal())
        await fourth_view(ctx)

    button2.callback = add_button_callback

    await ctx.send(view=view)
    if application_list:
        res = await bot.wait_for('interaction', check=lambda interaction: interaction.data["component_type"] == 2 and "custom_id" in interaction.data.keys())
        for item in view1.children:
            if item.custom_id == res.data["custom_id"]:
                button = item
                await third_view(ctx, button.custom_id)


#подтверждение подачи заявки
async def fourth_view(ctx):
    view = View()
    button1 = Button(label="Продолжить заполнение заявки", style=discord.ButtonStyle.green)
    view.add_item(button1)

    async def add_button_callback(interaction: discord.Interaction):
        await interaction.response.send_modal(AddModal2())
        await fifth_view(ctx)

    button1.callback = add_button_callback
    await ctx.send(view=view)


async def fifth_view(ctx):
    view = View()
    button1 = Button(label="Отправить заявку", style=discord.ButtonStyle.green)
    button2 = Button(label="Отмена", style=discord.ButtonStyle.red)
    view.add_item(button1)
    view.add_item(button2)

    async def add_button_callback(interaction: discord.Interaction):
        global new_app_holder
        application_json.append(new_app_holder)
        global idholder
        new_app_holder = {
            "id": " ",
            "conference_id": " ",
            "telegram_id": " ",
            "discord_id": " ",
            "submitted_at": " ",
            "updated_at": " ",
            "email": " ",
            "phone": " ",
            "name": " ",
            "surname": " ",
            "patronymic": " ",
            "university": " ",
            "student_group": " ",
            "applicant_role": " ",
            "title": " ",
            "adviser": " ",
            "coauthors": []
        }
        await second_view(ctx, idholder)
        idholder = ""

    button1.callback = add_button_callback

    async def back_button_callback(interaction: discord.Interaction):
        global new_app_holder
        global idholder
        new_app_holder = {
            "id": " ",
            "conference_id": " ",
            "telegram_id": " ",
            "discord_id": " ",
            "submitted_at": " ",
            "updated_at": " ",
            "email": " ",
            "phone": " ",
            "name": " ",
            "surname": " ",
            "patronymic": " ",
            "university": " ",
            "student_group": " ",
            "applicant_role": " ",
            "title": " ",
            "adviser": " ",
            "coauthors": []
        }
        await second_view(ctx, idholder)
        idholder = ""

    button2.callback = back_button_callback
    await ctx.send(view=view)


def new_app_part1(title, name, surname, patronymic, university, id):
    new_app = create_new_application(get_unique_id(application_json), id, "1234", datetime.datetime.now(pytz.timezone('Europe/Moscow')).strftime("%Y-%m-%dT%H:%M:%S.%f%z"))
    new_app["name"] = name
    new_app["surname"] = surname
    new_app["patronymic"] = patronymic
    new_app["university"] = university
    new_app["title"] = title
    return new_app


def new_app_part2(new_app, student_group, applicant_role, adviser, email, phone):
    new_app["student_group"] = student_group
    new_app["applicant_role"] = applicant_role
    new_app["adviser"] = adviser
    new_app["email"] = email
    new_app["phone"] = phone
    return new_app


#добавить заявку
class AddModal(discord.ui.Modal, title="Добваление заявки"):
    apptitle = discord.ui.TextInput(
        style=discord.TextStyle.short,
        label="заголовок",
        required=True,
        max_length=80,
        placeholder="Заголовок вашей заявки"
    )

    name = discord.ui.TextInput(
        style=discord.TextStyle.short,
        label="Имя",
        required=True,
        max_length=30,
        placeholder="ваше имя"
    )

    surname = discord.ui.TextInput(
        style=discord.TextStyle.short,
        label="Фамилия",
        required=True,
        max_length=30,
        placeholder="ваша фамилия"
    )

    patronymic = discord.ui.TextInput(
        style=discord.TextStyle.short,
        label="Отчество",
        required=False,
        max_length=30,
        placeholder="ваше отчество (если есть)"
    )

    university = discord.ui.TextInput(
        style=discord.TextStyle.short,
        label="Университет",
        required=True,
        max_length=30,
        placeholder="ваша образовательная организация"
    )

    async def on_submit(self, interaction: discord.Interaction):
        global new_app_holder
        global idholder
        new_app_holder = new_app_part1(self.apptitle, self.name, self.surname, self.patronymic, self.university, idholder)
        await interaction.response.defer()


class AddModal2(discord.ui.Modal, title="Добваление заявки"):
    student_group = discord.ui.TextInput(
        style=discord.TextStyle.short,
        label="Группа",
        required=False,
        max_length=30,
        placeholder="ваша группа"
    )

    applicant_role = discord.ui.TextInput(
        style=discord.TextStyle.short,
        label="Должность",
        required=True,
        max_length=30,
        placeholder="ваша должность (например студент)"
    )

    adviser = discord.ui.TextInput(
        style=discord.TextStyle.short,
        label="Научный руководитель",
        required=True,
        max_length=80,
        placeholder="ФИО и должность научрука"
    )

    email = discord.ui.TextInput(
        style=discord.TextStyle.short,
        label="email",
        required=False,
        max_length=30,
        placeholder="example@example.com"
    )

    phone = discord.ui.TextInput(
        style=discord.TextStyle.short,
        label="Телефон для свзяи",
        required=False,
        max_length=30,
        placeholder="+79001234567"
    )

    async def on_submit(self, interaction: discord.Interaction):
        global new_app_holder
        new_app_holder = new_app_part2(new_app_holder, self.student_group, self.applicant_role, self.adviser, self.email, self.phone)
        conf_id = new_app_holder["conference_id"]
        discord_id = new_app_holder["discord_id"]
        title = new_app_holder["title"]
        submitted_at = new_app_holder["submitted_at"]
        name = new_app_holder["name"]
        surname = new_app_holder["surname"]
        patronymic = new_app_holder["patronymic"]
        university = new_app_holder["university"]
        student_group = new_app_holder["student_group"]
        applicant_role = new_app_holder["applicant_role"]
        adviser = new_app_holder["adviser"]
        email = new_app_holder["email"]
        phone = new_app_holder["phone"]
        await interaction.response.send_message(f"Информация о заявке:\nconference_id: {conf_id}\ndiscord_id: {discord_id}\n"
                                                f"Заголовок: {title}\nОтправлена: {submitted_at}\n"
                   f"Электронная почта: {email}\nТелефон: {phone}\n"
                   f"Имя: {name}\nФамилия: {surname}\nОтчество: {patronymic}\nУниверситет: {university}\n"
                   f"Группа: {student_group}\nДолжность: {applicant_role}\nРуководитель: {adviser}\n")



#страничка заявки
async def third_view(ctx, id):
    application = [x for x in application_json if x['id'] == id][0]
    conference_id = application["conference_id"]
    title = application["title"]
    submitted_at = application["submitted_at"]
    updated_at = application["updated_at"]
    email = application["email"]
    phone = application["phone"]
    name = application["name"]
    surname = application["surname"]
    patronymic = application["patronymic"]
    university = application["university"]
    student_group = application["student_group"]
    applicant_role = application["applicant_role"]
    adviser = application["adviser"]
    coauthors = ", ".join([x['name']+" "+x["surname"]+ " "+ x["patronymic"] for x in application['coauthors']])
    view = View()
    button1 = Button(label="Назад", style=discord.ButtonStyle.red)
    button2 = Button(label="Добавить публикацию", style=discord.ButtonStyle.green)
    view.add_item(button1)
    view.add_item(button2)

    async def back_button_callback(interaction):
        await second_view(ctx, conference_id)

    button1.callback = back_button_callback

    async def add_button_callback(interaction: discord.Interaction):
        attachment_url = ctx.message.attachments[0].url
        file_request = requests.get(attachment_url)
        print(file_request.content)
        await interaction.response.defer()

    button1.callback = add_button_callback
    await ctx.send(f"Информация о заявке:\nЗаголовок: {title}\nОтправлена: {submitted_at}\n"
                   f"Обновлена: {updated_at}\nЭлектронная почта: {email}\nТелефон: {phone}\n"
                   f"Имя: {name}\nФамилия: {surname}\nОтчество: {patronymic}\nУниверситет: {university}\n"
                   f"Группа: {student_group}\nДолжность: {applicant_role}\nРуководитель: {adviser}\n"
                   f"Соавторы: {coauthors}", view=view)


#информация о конференции
async def conference_info(ctx, id):
    conference = [x for x in conferences_json if x['conference_id'] == id][0]
    name = conference["conference_name_russian"]
    short_name = conference["conference_short_name_russian"]
    conference_name_english = conference["conference_name_english"]
    conference_short_name_english = conference["conference_short_name_english"]
    organizing_organization = conference["organizing_organization"]
    registration_dates = conference["registration_start_date"] + " - " +conference["registration_end_date"]
    submission_dates = conference["submission_start_date"] + " - " + conference["submission_end_date"]
    conference_dates = conference["conference_start_date"] + " - " + conference["conference_end_date"]
    site = conference["conference_website_url"]
    email = conference["contact_email"]
    if not reg_check(id):
        registration_dates += " (закончилось)"
    if not submission_check(id):
        submission_dates += " (закончилось)"
    if not conf_check(id):
        conference_dates += " (закончилось)"
    view = View()
    button1 = Button(label="Назад", style=discord.ButtonStyle.red)
    view.add_item(button1)

    async def back_button_callback(interaction):
        await second_view(ctx, id)

    button1.callback = back_button_callback
    await ctx.send(f"Информация о конференции:\nНазвание: {name}\nАббревиатура: {short_name}\n"
                   f"Название на английском: {conference_name_english}\n"
                   f"Аббревиатура на английском: {conference_short_name_english}\n"
                   f"Организатор: {organizing_organization}\nДаты регистрации: {registration_dates}\n"
                   f"Прием статей: {submission_dates}\nДаты проведения: {conference_dates}\n"
                   f"Вебсайт: {site}\nЭлектронная почта: {email}\n", view=view)

# Запускаем бота
bot.run('MTE0ODk1NTM2OTg0Mjk1NDI2MA.GT-dIu.Qjzmo7uEIrqYqa5ZuW-_yFOshCDJIRRe3g5gLg')