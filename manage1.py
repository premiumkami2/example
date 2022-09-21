import threading

import re

from itertools import islice
from datetime import datetime
from datetime import date
from random import choice
from random import sample
from os import listdir
import os
from time import sleep
import time
from datetime import datetime

from SQL import Account
from SQL import DateTime
from SQL import Username
from SQL import AdminsBot
from SQL import Groups
from SQL import SettingAddmember
from SQL import AddStatistics

from pyrogram import Client
from pyrogram import filters
from pyrogram import idle
from pyrogram import errors

from pyrogram.types import InlineKeyboardButton as button
from pyrogram.types import InlineKeyboardMarkup as markup
from pyrogram.types import ForceReply as reply

from pyrogram.raw import functions

api_id, api_hash = 13360888, "f9f13233c4bff84f6ee3423f58f796a8"
token = "5311584364:AAEYSw6-QcWnNoYzuriGp8tYK82j0pfG2No"
app = Client("bot", api_id, api_hash, bot_token=token)

numbers = list()
for fil in listdir('sessions'):
    numbers.append(fil.split("phone")[-1].split(".")[0])

global step
global phone_code_hashs
global sessions
global y
step = 'None'
phone_code_hashs = dict()
sessions = dict()
global Client_two_step
y = 0
Message = None


@app.on_message(filters.command(['start']))
def start(client, message):
    chat_id = message.chat.id
    print("Start id ->", chat_id)
    message_id = message.message_id
    Menu(chat_id, message_id)


@app.on_callback_query()
def querys(_, query):
    chat_id = query.message.chat.id
    message_id = query.message.message_id
    data = query.data

    db = AdminsBot("Model.db")
    db.create_table()
    listadmins = db.get_list_admins()
    DeleteAdmin = [Id[1] for Id in listadmins]
    db.close()

    db = Groups("Model.db")
    db.create_table()
    List_groups = db.get_list_groups()
    DeleteGroup = [Id[1] for Id in List_groups]
    AddToGroup = [Id[1]for Id in List_groups]
    db.close()

    if data == "StartLogin":
        StartLogin(chat_id, message_id)
    if data == "YesAgainAddNewLogIn":
        StartLogin(chat_id, message_id)
    if data == "NoFinishAddNewLogIn":
        Menu2(chat_id, message_id)
    if data == "ComebackToMenu":
        Menu2(chat_id, message_id)
    if data == "StartUAR":
        StartUAR(chat_id, message_id)
    if data == "StarCollect":
        StarCollect(chat_id, message_id, query)
    if data == "StartSet":
        StartSet(chat_id, message_id)
    if data == "EditAccount":
        EditAccount(chat_id, message_id)
    if data == "RemoveAccount":
        RemoveAccount(chat_id, message_id, query)
    if data == "EditAdmins":
        EditAdmins(chat_id, message_id)
    if data == "ComebackSettings":
        StartSet(chat_id, message_id)
    if data == "AddAdmin":
        AddAdmin(chat_id, message_id, query)
    if data == "RemoveAdmin":
        RemoveAdmin(chat_id, message_id, query)
    if data == "ShowAdmins":
        ShowAdmins(chat_id, message_id, query)
    if data == "StartStat":
        Statistics(chat_id, message_id)
    if data == "Accounts":
        Accounts(chat_id, message_id, query)
    if data == "Activity":
        Activityy(chat_id, message_id, query)
    if data == "EditGroups":
        EditGroups(chat_id, message_id)
    if data == "AddGroup":
        AddGroup(chat_id, message_id)
    if data == "SettingAdd":
        SettingAdd(chat_id, message_id)
    if data == "RemoveGroup":
        RemoveGroup(chat_id, message_id, query)
    if data == "ShowGroup":
        ShowGroup(chat_id, message_id, query)
    if data == "ShowSettings":
        ShowSettings(chat_id, message_id, query)
    if data == "StartAdd":
        StartAdd(chat_id, message_id, query)
    if data == "EditSettings":
        EditSettings(chat_id, message_id)
    if data == "IDeas":
        IDeas(chat_id, message_id, query)
    if data == "StartClear":
        StartClear(chat_id, message_id, query)
    if data == "start_add_users_file":
        start_add_users_file(chat_id, message_id, query)
    if data == "start_get_users_file":
        start_get_users_file(chat_id, message_id, query)
    if data == "None":
        MessageNone(chat_id, message_id, query)
    if data[:2] == "re" and data[2:] in DeleteAdmin:
        DeleteAdmins(chat_id, message_id, query, data)
    if data[:2] == "re" and data[2:] in DeleteGroup:
        DeleteGroups(chat_id, message_id, query, data)
    if data[:2] == "ad" and data[2:] in AddToGroup:
        AddToGroups(chat_id, message_id, query, data)


@app.on_message()
def Updates(app, message):
    global step
    chat_id = message.chat.id
    message_id = message.message_id
    text = message.text
    media = message.media

    if step == "GetPhone":
        GetPhone(chat_id, message_id, text)
    elif step.split(" ")[0] == "LoginCode":
        LoginCode(chat_id, message_id, text)
    elif step.split(" ")[0] == "GetTwo-step":
        LoginCodeTwoStep(chat_id, message_id, text)
    elif step.split(" ")[0] == "GetCodeliginInvalid":
        code = text
        LoginCode(chat_id, message_id, code)
    elif step == "GetUsername":
        GetUsername(chat_id, message_id, text)
    elif step == "SaveAdmin":
        SaveAdmin(chat_id, message_id, text, message)
    elif step == "SaveGroup":
        SaveGroup(chat_id, message_id, text, message)
    elif step == "GetActivityRange":
        GetActivityRange(chat_id, message_id, text, message)
    elif step == "DeleteAccount":
        DeleteAccount(chat_id, message_id, text, message)
    elif step == "add_users_file":
        add_users_file(chat_id, message_id, media, message)
    elif step[:11] == "GetAddRange":
        GetAddRange(chat_id, message_id, text, message)
    elif step[:18] == "GettActivityNumber":
        GettActivityNumber(chat_id, message_id, text, message)


# Menu------------------------------------------------------------------------------------------------------------
def Menu(chat_id, message_id):
    modir = 80031118
    modir2 = 861812214
    db = AdminsBot("Model.db")
    db.create_table()
    list_admin = db.get_list_admins()
    db.close()
    list_a = [i[1] for i in list_admin]
    if chat_id == modir or chat_id == modir2 or str(chat_id) in list_a:

        app.send_message(chat_id,
                         " 🖐🏻👽 Hi Admin. \nSelect Your Fav",
                         reply_to_message_id=message_id,
                         reply_markup=markup([[button("Login New Account 🔐", callback_data="StartLogin")],
                                              [button("Add 👤 to Group 👥",
                                                      callback_data="StartAdd")],
                                              [button("Collect Usernames 🆔", callback_data="StarCollect"), button(
                                                  "Clear Usernames 🆑", callback_data="StartClear")], [button(
                                                      "Add Users File 📁", callback_data="start_add_users_file"), button(
                                                      "Get Users File 📁", callback_data="start_get_users_file")],
                                              [button("Statistics 📊", callback_data="StartStat"), button(
                                                  "👽 Bot Settings ⚙️", callback_data="StartSet")],
                                              [button("Update Account Reports 🔄",
                                                      callback_data="StartUAR")]
                                              ]))
    else:
        app.send_message(
            chat_id, f"⭕️ <code>You do not have access to the robot. Buy license @irnaji</code>", parse_mode='html')


def Menu2(chat_id, message_id):

    app.edit_message_text(chat_id, message_id,
                          " 🖐🏻👽 Hi Admin. \nSelect Your Fav",
                          reply_markup=markup([[button("Login New Account 🔐", callback_data="StartLogin")],
                                               [button("Add 👤 to Group 👥",
                                                       callback_data="StartAdd")],
                                               [button("Collect Usernames 🆔", callback_data="StarCollect"), button(
                                                   "Clear Usernames 🆑", callback_data="StartClear")], [button(
                                                       "Add Users File 📁", callback_data="start_add_users_file"), button(
                                                       "Get Users File 📁", callback_data="start_get_users_file")],
                                               [button("Statistics 📊", callback_data="StartStat"), button(
                                                   "👽 Bot Settings ⚙️", callback_data="StartSet")],
                                               [button("Update Account Reports 🔄",
                                                       callback_data="StartUAR")]
                                               ]))
# /----------------------------------------------------------------------------------------------------------------

# MessageNone------------------------------------------------------------------------------------------------------


def MessageNone(chat_id, message_id, query):
    query.answer(f"فقط جهت نمایش")
# /----------------------------------------------------------------------------------------------------------------

# MessageTree-------------------------------------------------------------------------------------------------------


def MessageThree(chat_id, message_id):
    app.send_message(
        chat_id, "The number of accounts you request is more than the existing accounts")
# /----------------------------------------------------------------------------------------------------------------


# log in-----------------------------------------------------------------------------------------------------------
def StartLogin(chat_id, message_id):
    global step
    app.edit_message_text(
        chat_id, message_id, "<code>Send Your Number</code>\n<i>For example:</i> <b>+989381754806</b>", parse_mode="html")
    step = "GetPhone"


def GetPhone(chat_id, message_id, text):
    global step
    if not text[1:].isdigit() or text[0] != "+":
        app.send_message(chat_id, f"<code>Your Number Is Wrong</code>❌",
                         parse_mode="html", reply_to_message_id=message_id)
        step = "GetPhone"
        return

    Send_Code_Request(chat_id, message_id, text.replace(" ", ""))


def Send_Code_Request(chat_id, message_id, number):
    global step
    global phone_code_hashs
    global sessions
    session = f'sessions/phone{number}'
    api_id, api_hash = 13360888, "f9f13233c4bff84f6ee3423f58f796a8"
    client = Client(session, api_id, api_hash)
    client.connect()

    try:

        phone_code_hash = client.send_code(number).phone_code_hash
        app.send_message(
            chat_id, f"<code>Code Sended To</code> <b>{number}</b> <code>\nPlease Enter 5 digit Login Code!</code>", parse_mode="html", reply_to_message_id=message_id)
        sessions[number] = client
        phone_code_hashs[number] = phone_code_hash
        step = f"LoginCode {number}"

    except errors.PhoneNumberInvalid as error:
        print(f"Error({Send_Code_Request})-> {error}")
        app.send_message(chat_id, "<b>The phone number is invalid!</b>\nPlease correct the number or send another number",
                         parse_mode="html", reply_to_message_id=message_id)
        step = 'GetPhone'


def LoginCode(chat_id, message_id, code):
    global step
    global phone_code_hashs
    global sessions
    global Client_two_step

    if not code.isdigit() or len(code) != 5:
        app.send_message(chat_id, "<code>Your Login Code Is Wrong</code>",
                         parse_mode='html', reply_to_message_id=message_id)
        return

    number = step.split(" ")[1]
    client = sessions[number]
    #Register and Login
    try:

        client.sign_in(phone_number=number,
                       phone_code_hash=phone_code_hashs[number], phone_code=code)

    except errors.PhoneNumberUnoccupied as error:
        print(f"Error({LoginCode})-> {error}")
        client.sign_up(phone_number=number, phone_code_hash=phone_code_hash,
                       first_name="aryn", last_name="kaviani")
        app.send_message(chat_id, "<b>Register and Login Successfull!</b>",
                         parse_mode="html", reply_to_message_id=message_id)
        step = 'None'
        return

    except errors.SessionPasswordNeeded as error:
        print(f"Error({LoginCode})-> {error}")
        app.send_message(chat_id, "<b>Two-step verification password required!</b>",
                         parse_mode="html", reply_to_message_id=message_id)
        app.send_message(chat_id, f"Send the two-step password:",
                         parse_mode="html", reply_markup=reply(selective=True))
        step = f'GetTwo-step {number}'
        Client_two_step = client
        return

    except errors.PhoneCodeExpired as error:
        print(f"Error({LoginCode})-> {error}")
        app.send_message(chat_id, "<b>The confirmation code has expired!</b>",
                         parse_mode="html", reply_to_message_id=message_id)
        step = 'None'
        return

    except errors.PhoneCodeInvalid as error:
        print(f"Error({LoginCode})-> {error}")
        app.send_message(chat_id, "<b>The confirmation code is invalid!</b>",
                         parse_mode="html", reply_to_message_id=message_id)
        app.send_message(chat_id, f"Send the login code:",
                         parse_mode="html", reply_markup=reply(selective=True))
        step = f'GetCodeliginInvalid {number}'
        return
    except Exception as error:
        print(f"Error({LoginCode})-> {error}")

    else:
        app.send_message(chat_id, "<code>Login Successfull.</code>",
                         parse_mode="html", reply_to_message_id=message_id)
        SpamBot(chat_id, message_id, number)


def LoginCodeTwoStep(chat_id, message_id, text):
    global step, Client_two_step
    number = step.split(" ")[1]
    try:
        client = Client_two_step.check_password(text)
    except Exception as e:
        print(f"Error({LoginCode})-> {error}")
    else:
        print("Log in(two_step)")
        SpamBot(chat_id, message_id, number)


def SpamBot(chat_id, message_id, number, c=None):
    api_id, api_hash = 13360888, "f9f13233c4bff84f6ee3423f58f796a8"
    try:
        with Client(f'sessions/phone{number}', api_id, api_hash)as app:

            app.send_message("@SpamBot", "/start")
            count = 1
            for message in app.iter_history("SpamBot"):
                if count == 1:
                    text = message.text
                    count += 1
                    if re.search(r"^Good news", text) or re.search(r"^مژده", text):
                        report = False

                    elif re.search(r"Unfortunately", text):
                        report = "Permanent"

                    elif re.search(r"limited until(.*)\.", text):
                        reep = re.findall(r"limited until(.*)\.", text)
                        report = reep[0]
                    else:
                        report = "temporary"

                else:
                    pass
    except errors.SessionRevoked as error:
        print(f"Error 1 SpamBot {error} Phone: {number}")
        DeleteSessionRevoked(chat_id, message_id, number)

    except errors.UserDeactivated as error:
        print(f"Error 2 SpamBot {error} Phone: {number}")
        UpdateDeleteAccount(chat_id, message_id, number)
        DeleteSessionRevoked(chat_id, message_id, number)

    except errors.AuthKeyUnregistered as error:
        print(f"Error 3 SpamBot {error} Phone: {number}")
        DeleteSessionRevoked(chat_id, message_id, number)

    except errors.UserDeactivatedBan as error:
        print(f"Error 4 SpamBot {error} Phone: {number}")
        UpdateDeleteAccount(chat_id, message_id, number)
        DeleteSessionRevoked(chat_id, message_id, number)

    except errors.Unauthorized as error:
        print(f"Error 5 SpamBot {error} Phone: {number}")
        UpdateDeleteAccount(chat_id, message_id, number)
        DeleteSessionRevoked(chat_id, message_id, number)

    except Exception as error:
        print(f"Error({SpamBot})-> {error}")
    else:
        db = Account("Model.db")
        db.create_table()

        all_phone_number = db.get_list_phone()
        if str(number) not in all_phone_number:
            SaveAccountNew(chat_id, number, api_id, api_hash, report)

        elif str(number) in all_phone_number:
            UpdatesReportAccount(report, number, c, chat_id, message_id)
        db.close()


def SaveAccountNew(chat_id, number, api_id, api_hash, report):
    global step
    date = DateTime().d
    time = DateTime().t

    try:

        db = Account("Model.db")
        db.insert_data((f"{number}", f"{api_id}", f"{api_hash}", f"{report}",
                       f"False", f"{date}", f"01-01-2020", f"{time}", f"{0}", f"{0}", f"{0}"))
        db.close()
    except Exception as error:
        print(f"Error({SaveAccountNew})-> {error}")
    else:
        print(f"insert data phone number {number} to database")
        app.send_message(
            chat_id, f"✅ <code>Insert Data Phone Number</code> <b>{number}</b> <code>To Database</code>")
        app.send_message(chat_id, "<b>Enter another new account?</b>", parse_mode="html",
                         reply_markup=markup([
                             [button("Yes, again ☑️", callback_data="YesAgainAddNewLogIn"),
                              button("No, finish 🔘", callback_data="NoFinishAddNewLogIn")]
                         ]))
        step = "None"


def UpdatesReportAccount(report, number, c, chat_id, message_id):
    global y, Message
    db = Account("Model.db")
    reports = (f"{report}", f"{number}")

    db.update_report(reports)
    list_account = db.get_list_phone()
    db.close()

    l = len(list_account)
    print(f"({number}) -> report:{report}")
    if y <= 0:
        Message = app.send_message(
            chat_id, f"<code>({number})</code> -> <b>report:</b><code>{report}</code>", parse_mode='html')
        y += 1
    else:
        app.edit_message_text(chat_id, Message.message_id,
                              f"<code>({number})</code>\n<b>report:</b><code>{report}</code>", parse_mode='html')

    if c == l:
        sleep(1)
        app.send_message(chat_id, f"<code>✅ The report status of your accounts has been updated</code>",
                         parse_mode='html', reply_to_message_id=message_id)
    else:
        pass
# /-----------------------------------------------------------------------------------------------------------------


# get username------------------------------------------------------------------------------------------------------
def StarCollect(chat_id, message_id, query):
    global step
    app.edit_message_text(chat_id, message_id, "<b>Send username or hash group path</b>\n<i>For example(public):</i> <b>@tarfandnaji</b>\n<i>For example(Private):</i> <b>IfXSL8tpjCvMt6uL</b>",
                          parse_mode="html", reply_markup=markup([[button("Comeback To Menu 🔙 ", callback_data="ComebackToMenu")]]))
    step = "GetUsername"


def GetUsername(chat_id, message_id, text):
    Chats_id = None
    api_id, api_hash = 13360888, "f9f13233c4bff84f6ee3423f58f796a8"
    try:

        Cli = Client('session_me', api_id, api_hash)
        Cli.connect()
        count = 0
        try:
            if text[0] == "@":
                Join = Cli.join_chat(text)
                Chats_id = Join.id
                print("join")
            else:
                Join = Cli.send(
                    functions.messages.ImportChatInvite(hash=text)
                )
                print("join")
                TitleGroup = Join.chats[0]["title"]
        except errors.UserAlreadyParticipant as error:
            print(f"Error 1({GetUsername})-> {error}")
            Cli.disconnect()
            app.send_message(chat_id, "<code>Remove the account from the group</code>",
                             parse_mode="html", reply_to_message_id=message_id)
            step = "None"

        except errors.ChatIdInvalid as error:
            print(f"Error 2({GetUsername})-> {error}")
            Cli.disconnect()
            app.send_message(chat_id, "<code>Cannot be extracted from this group</code>",
                             parse_mode="html", reply_to_message_id=message_id)
            step = "None"

        except errors.InviteHashExpired as error:
            print(f"Error 3({GetUsername})-> {error}")
            Cli.disconnect()
            app.send_message(chat_id, "Your submitted hash has expired")
            step = "None"
        except Exception as error:
            print(f"Error 4({GetUsername})-> {error}")
            Cli.disconnect()
            step = "None"

        else:

            try:
                sleep(3)
                app.send_message(
                    chat_id, "<b>Start extracting chat ideas</b>", parse_mode="html")
                if text[0] != "@":
                    for dialog in Cli.iter_dialogs():
                        Type = dialog.chat.type
                        Title = dialog.chat.title
                        if Type == "supergroup" or Type == 'group':
                            if Title == TitleGroup:
                                Chats_id = dialog.chat.id
                            else:
                                pass
                    print(f"Group:{Chats_id} | {Title}")
                else:
                    pass

                for member in Cli.iter_chat_members(Chats_id):
                    if member.user.username and member.user.is_self != True and member.user.is_bot != True and member.status not in ["creator", "administrator"]:
                        status = member.user.status
                        if status == "offline":
                            last_online_date_user = datetime.strptime(time.ctime(
                                member.user.last_online_date), '%a %b %d %H:%M:%S %Y')
                            date_now = datetime.now()
                            c = (date_now - last_online_date_user).days
                        elif status == "within_month" or status == "long_time_ago" or status == "within_week":
                            continue
                        else:
                            c = 0

                        if c < 7:
                            user_username = member.user.username
                            user_id = member.user.id
                            try:
                                db = Username("Model.db")
                                db.create_table()
                                all_list_username = db.get_list_username()
                                db.close()
                            except Exception as error:
                                print(f"Error 5({GetUsername})-> {error}")
                            else:
                                if user_username not in all_list_username:
                                    db = Username("Model.db")
                                    db.create_table()
                                    db.insert_data(
                                        (f"{user_username}", f"{user_id}"))
                                    print(
                                        f"({count}) Save Username: {user_username}")
                                    db.close()
                                    count += 1
                                else:
                                    continue
            except errors.ChatIdInvalid as error:
                print(f"Error 6({GetUsername})-> {error}")
                Cli.disconnect()
                app.send_message(chat_id, "<code>Cannot be extracted from this group</code>",
                                 parse_mode="html", reply_to_message_id=message_id)
                step = "None"
            except Exception as error:
                print(f"Error 6({GetUsername})-> {error}")
                Cli.disconnect()
                step = "None"
            else:

                try:
                    Cli.leave_chat(Chats_id)
                except Exception as error:
                    print(f"Error 7({GetUsername})-> {error}")
                    Cli.disconnect()
                else:
                    Cli.disconnect()
                    if count > 0:
                        print("end Save username")
                        app.send_message(
                            chat_id, f"<b>[ {count} ]</b> <b>Chat ID from group <code>{text}</code> were added to the database</b>", parse_mode="html")
                        step = "None"
                    else:
                        app.send_message(
                            chat_id, f"<b>No Chat ID were added to the database</b>", parse_mode="html")
                        step = "None"
    except Exception as error:
        print(f"Error 6({GetUsername})-> {error}")


# /-----------------------------------------------------------------------------------------------------------------

# clear username----------------------------------------------------------------------------------------------------
def StartClear(chat_id, message_id, query):
    global step
    # get_list_All
    try:

        db = Username("Model.db")
        db.create_table()
        getAll = db.get_list_All()
        db.close()
    except Exception as error:
        print(f"Error({GetUsername})-> {error}")
    else:
        if len(getAll) > 1:
            try:
                db = Username("Model.db")
                db.create_table()
                db.delete_all_username()
                db.close()
            except Exception as error:
                print(f"Error({GetUsername})-> {error}")
            else:
                app.send_message(chat_id, "Deleting ideas succeeded",
                                 reply_to_message_id=message_id)
        else:
            query.answer("The basket of ideas is empty")


def start_add_users_file(chat_id, message_id, query):
    global step
    print("start_add_users_file")
    app.edit_message_text(chat_id, message_id, "<b>فایل کاربران را آپلود کنید</b>",
                          parse_mode="html", reply_markup=markup([[button("Comeback To Menu 🔙 ", callback_data="ComebackToMenu")]]))
    step = "add_users_file"


def start_get_users_file(chat_id, message_id, query):
    global step
    db = Username("Model.db")
    db.create_table()
    all_users = db.get_list_All()
    db.close()
    if len(all_users) != 0:
        with open("users_file.txt", 'wt', encoding='utf-8') as f:
            for user in all_users:
                f.write(user + '\n')
        app.send_document(chat_id, 'users_file.txt',
                          reply_to_message_id=message_id)
    else:
        app.send_message(chat_id, "❌ خطا: کاربری ذخیره نشده است",
                         reply_to_message_id=message_id)

# /-----------------------------------------------------------------------------------------------------------------


# settings-----------------------------------------------------------------------------------------------------------
def StartSet(chat_id, message_id):  # setting -> Edit Admins - Edit Groups - Setting Addmember
    global step
    app.edit_message_text(chat_id, message_id, "Click the desired button to set and edit",
                          reply_markup=markup([[button("Admins 🛠", callback_data="EditAdmins"), button("Groups 🛠", callback_data="EditGroups")],
                                               [button("Settings Addmember 🛠", callback_data="SettingAdd"), button(
                                                   "Account 🛠", callback_data="EditAccount")],
                                               [button("Comeback To Menu 🔙 ", callback_data="ComebackToMenu")]]))
    step = 'None'


def EditAdmins(chat_id, message_id):  # edit admins -> AddAdmin - RemoveAdmin - ShowAdmins
    global step
    modir = 80031118
    modir2 = 861812214
    if chat_id == modir or chat_id == modir2:
        app.edit_message_text(chat_id, message_id, "Edit Admins",
                              reply_markup=markup([[button("Remove Admin ➖", callback_data="RemoveAdmin"), button("Add Admin ➕", callback_data="AddAdmin")],
                                                   [button(
                                                       "Show Admins", callback_data="ShowAdmins")],
                                                   [button("Comeback To Menu 🔙 ", callback_data="ComebackToMenu"), button("Comeback 🔙", callback_data="ComebackSettings")]]))
        step = 'None'


def AddAdmin(chat_id, message_id, query):
    global step
    app.edit_message_text(
        chat_id, message_id, "<code>Send us the New Admin Username</code>\n<i>For example:  </i>@username", parse_mode="html")
    step = "SaveAdmin"


def SaveAdmin(chat_id, message_id, text, message):
    global step
    api_id, api_hash = 13360888, "f9f13233c4bff84f6ee3423f58f796a8"
    try:
        Cli = Client('session_me', api_id, api_hash)
        Cli.connect()

        try:
            chat = app.get_chat(f"{text[1:]}")
            Id = chat.id
            name = chat.first_name
            username = chat.username

        except Exception as error:
            print(f"Error({SaveAdmin})-> {error}")
            Cli.disconnect()
        else:
            Cli.disconnect()
            db = AdminsBot("Model.db")
            db.create_table()
            db.insert_data((f"{name}", f"{Id}", f"{username}"))
            print("save admin in admins")
            db.close()
            app.send_message(
                chat_id, f"<code>Save {text} in Admins</code>", reply_to_message_id=message_id)

    except Exception as error:
        print(f"Error({SaveAdmin})-> {error}")


def RemoveAdmin(chat_id, message_id, query):
    try:

        db = AdminsBot("Model.db")
        db.create_table()
        listadmins = db.get_list_admins()
        db.close()
        if len(listadmins) > 0:

            keyboard = [button(f"{admin[0]}", callback_data=f"re{admin[1]}")
                        for admin in listadmins]
            key = iter(keyboard)
            Output = [list(islice(key, elem))
                      for elem in [2 for n in range(len(keyboard))]]

            Output.insert(-1, [button(text="Comeback To Menu 🔙 ", callback_data="ComebackToMenu"),
                               button("Comeback 🔙", callback_data="EditAdmins")])

            app.edit_message_text(
                chat_id, message_id, "Remove\nClick on admin name to remove", reply_markup=markup(Output))

        else:
            query.answer(f"not admin")
            StartSet(chat_id, message_id)
    except Exception as error:
        print(f"Error({RemoveAdmin})-> {error}")


def DeleteAdmins(chat_id, message_id, query, data):
    try:

        ID = (f"{data[2:]}",)
        db = AdminsBot("Model.db")
        db.create_table()
        db.delete_admin(ID)
        db.close()
        query.answer(f"delete admin")
        RemoveAdmin(chat_id, message_id, query)
    except Exception as error:
        print(error)


def ShowAdmins(chat_id, message_id, query):
    try:

        db = AdminsBot("Model.db")
        db.create_table()
        listadmins = db.get_list_admins()

        if len(listadmins) > 0:

            keyboard = [
                button(f"{admin[0]}", url=f"https://t.me/{admin[2]}")for admin in listadmins]
            key = iter(keyboard)
            Output = [list(islice(key, elem))
                      for elem in [2 for n in range(len(keyboard))]]
            Output.append([button(text="Comeback To Menu 🔙 ", callback_data="ComebackToMenu"),
                           button("Comeback 🔙", callback_data="EditAdmins")])
            app.edit_message_text(
                chat_id, message_id, "Admins AddMemberBot", reply_markup=markup(Output))

        else:
            query.answer(f"not admin")
            StartSet(chat_id, message_id)
    except Exception as error:
        print(error)


def EditGroups(chat_id, message_id):  # edit groups -> AddGroup - RemoveGroup - ShowGroups
    app.edit_message_text(chat_id, message_id, "Edit Groups",
                          reply_markup=markup([[button("Remove Group ➖", callback_data="RemoveGroup"), button("Add Group ➕", callback_data="AddGroup")],
                                               [button(
                                                   "Show Group", callback_data="ShowGroup")],
                                               [button("Comeback To Menu 🔙 ", callback_data="ComebackToMenu"), button("Comeback 🔙", callback_data="ComebackSettings")]]))
    step = 'None'


def AddGroup(chat_id, message_id):
    global step
    app.edit_message_text(
        chat_id, message_id, "<code>Send us the new Group Username</code>\n<i>For example:</i>  @username", parse_mode="html")
    step = "SaveGroup"


def SaveGroup(chat_id, message_id, text, message):
    api_id, api_hash = 13360888, "f9f13233c4bff84f6ee3423f58f796a8"
    Cli = Client('session_me', api_id, api_hash)
    Cli.connect()

    try:
        chat = app.get_chat(f"{text[1:]}")
        Id = chat.id
        name = chat.title
        username = chat.username

    except Exception as error:
        print(error)

    AllData = (f"{name}", f"{Id}", f"{username}")
    db = Groups("Model.db")
    db.create_table()
    db.insert_data(AllData)
    db.close()
    print("save group in groups")
    app.send_message(
        chat_id, f"save {text} in Groups", reply_to_message_id=message_id)


def RemoveGroup(chat_id, message_id, query):
    try:

        db = Groups("Model.db")
        db.create_table()
        listgroups = db.get_list_groups()
        if len(listgroups) > 0:

            keyboard = [button(f"{group[0]}", callback_data=f"re{group[1]}")
                        for group in listgroups]
            key = iter(keyboard)
            Output = [list(islice(key, elem))
                      for elem in [2 for n in range(len(keyboard))]]

            app.edit_message_text(chat_id, message_id, "Remove\nClick on group name to remove",
                                  reply_markup=markup(Output))

        else:
            query.answer(f"not group")
            StartSet(chat_id, message_id)
    except Exception as error:
        print(error)


def DeleteGroups(chat_id, message_id, query, data):
    try:

        ID = (f"{data[2:]}",)
        db = Groups("Model.db")
        db.create_table()
        db.delete_group(ID)
        db.close()
        query.answer(f"delete Group")
        RemoveGroup(chat_id, message_id, query)

    except Exception as error:
        print(error)


def ShowGroup(chat_id, message_id, query):

    db = Groups("Model.db")
    db.create_table()
    listgroups = db.get_list_groups()
    print(len(listgroups))

    if len(listgroups) > 0:

        keyboard = [button(f"{group[0]}", url=f"https://t.me/{group[2]}")
                    for group in listgroups]
        key = iter(keyboard)
        Output = [list(islice(key, elem))
                  for elem in [2 for n in range(len(keyboard))]]
        app.edit_message_text(
            chat_id, message_id, "Groups AddMemberBot", reply_markup=markup(Output))

    else:
        query.answer(f"Not Group! ❌")
        StartSet(chat_id, message_id)


def EditAccount(chat_id, message_id):
    global step
    app.edit_message_text(chat_id, message_id, "Edit Account",
                          reply_markup=markup([[button("Remove Account ❌", callback_data="RemoveAccount")],
                                               [button("Comeback To Menu 🔙 ", callback_data="ComebackToMenu"), button("Comeback 🔙", callback_data="ComebackSettings")]]))
    step = 'None'


def RemoveAccount(chat_id, message_id, query):
    global step
    app.edit_message_text(chat_id, message_id, "Send Number")
    step = "DeleteAccount"


def DeleteAccount(chat_id, message_id, text, message):
    global step

    try:
        phone = (f"{text}",)
        db = Account("Model.db")
        db.create_table()
        db.delete_account(phone)
        db.close()
        app.send_message(chat_id, f"The account with the number {text} was removed from the list of database accounts", parse_mode='html',
                         reply_to_message_id=message_id)
        print(f"delete account {text}")
        step = 'None'
    except Exception as error:
        print(error)


def add_users_file(chat_id, message_id, media, message):
    global step
    print(media)
    if media:
        try:
            app.download_media(message=message, file_name='users.txt')
            with open('./downloads/users.txt') as f:
                tmp = f.read().split()
                # print(tmp.split())
                db = Username("Model.db")
                db.create_table()
                for user in tmp:
                    if user[0] == '@':
                        user = user[1:]
                    db.insert_data((user, 0))
                db.close()
                app.send_message(chat_id, "✅ کاربران با موفقیت ذخیره شدند", parse_mode='html',
                                 reply_to_message_id=message_id)
        except Exception as e:
            print(e)
            app.send_message(chat_id, "❌ خطا در ذخیره کاربران", parse_mode='html',
                             reply_to_message_id=message_id)
    else:
        app.send_message(chat_id, "❌ خطا در دریافت فایل کاربران", parse_mode='html',
                         reply_to_message_id=message_id)
    step = 'None'


def SettingAdd(chat_id, message_id):  # SettingAdd

    app.edit_message_text(chat_id, message_id, "SettingAdd",
                          reply_markup=markup([[button("Set Settings 🔩", callback_data="EditSettings"), button("Show Setting", callback_data="ShowSettings")],
                                               [button("Comeback To Menu 🔙 ", callback_data="ComebackToMenu"), button("Comeback 🔙", callback_data="ComebackSettings")]]))


def ShowSettings(chat_id, message_id, query):

    db = SettingAddmember("Model.db")
    db.create_table()
    list_Settingss = db.get_list_Setting()

    print(list_Settingss)
    if len(list_Settingss) >= 1:

        keyboard = [

            [button("تعداد دعوت", callback_data="None"), button(
                "استراحت اکانت ها ", callback_data="None")],
            [button(f"{list_Settingss[0][2]} ممبر", callback_data="None"), button(
                f"روز {list_Settingss[0][1]}", callback_data="None")],
            [button("Comeback To Menu 🔙 ", callback_data="ComebackToMenu"), button(
                "Comeback 🔙", callback_data="StartSet")]
        ]

        app.edit_message_text(
            chat_id, message_id, "Settings\nSettings Add Member", reply_markup=markup(keyboard))
    else:
        query.answer(f"Not Settings")
        StartSet(chat_id, message_id)


def EditSettings(chat_id, message_id):
    global step
    app.send_message(chat_id, "<code>Send ActivityRange</code>\n<i>For example(Daily rest):</i>  <b>d=1</b>\n<i>For example(Hourly rest rest):</i>  <b>t=12</b>",
                     parse_mode='html', reply_markup=reply(selective=True))
    step = "GetActivityRange"


def GetActivityRange(chat_id, message_id, text, message):
    global step
    try:
        if text[0] == "t":
            if int(text[2:]) < 24:
                app.send_message(chat_id, "<code>Send AddRange</code>\n<i>For example:</i>  <b>10 or 20 or 30 or..</b>",
                                 parse_mode='html', reply_markup=reply(selective=True))
                step = f"GetAddRange{text}"
            else:
                app.send_message(chat_id, "<b>Rest time should be between 1 and 23</b>\n<b>Resend..</b>",
                                 reply_markup=reply(selective=True))
                step = "GetActivityRange"
        elif text[0] == "d":
            if int(text[2:]) >= 1:
                app.send_message(chat_id, "<code>Send AddRange</code>\n<i>For example:</i>  <b>10 or 20 or 30 or..</b>",
                                 parse_mode='html', reply_markup=reply(selective=True))
                step = f"GetAddRange{text}"
            else:
                app.send_message(chat_id, "<b>Must be 1 day or more</b>\n<b>Resend..</b>",
                                 reply_markup=reply(selective=True))
                step = "GetActivityRange"
        else:
            app.send_message(chat_id, "<b>Your submission format is incorrect</b>\n<b>Resend..</b>",
                             parse_mode='html', reply_markup=reply(selective=True))

    except Exception as error:
        print(error)


def GetAddRange(chat_id, message_id, text, message):
    global step
    print(text)
    db = SettingAddmember("Model.db")
    db.create_table()
    list_setting = db.get_list_Setting()
    db.close()

    if len(list_setting) < 1:
        db = SettingAddmember("Model.db")
        db.create_table()
        db.insert_data((1, f"{step[11:]}", f"{text}"))
        db.close()
        app.send_message(chat_id, f"<code>✅ Your settings have been applied</code>",
                         parse_mode='html', reply_to_message_id=message_id)
        print(f"Add settings recorded")
        step = 'None'

    elif len(list_setting) >= 1:
        db = SettingAddmember("Model.db")
        db.create_table()
        db.update_data((f"{step[11:]}", f"{text}"))
        db.close()
        app.send_message(
            chat_id, f"<code>✅ Your settings have been applied</code>", reply_to_message_id=message_id)
        print(f"Add settings updated")
        step = 'None'
    else:
        print(f"list_setting:{len(list_setting)}")
# /-----------------------------------------------------------------------------------------------------------


# Statistics--------------------------------------------------------------------------------------------------
def Statistics(chat_id, message_id):
    global step
    if step == "reStatistics":
        app.delete_messages(chat_id, message_id)
        app.send_message(chat_id, "Activity statistics and accounts",
                         reply_markup=markup([[button("Activity", callback_data="Activity"), button("Accounts", callback_data="Accounts"), button("IDeas", callback_data="IDeas")],
                                              [button("Comeback To Menu 🔙 ", callback_data="ComebackToMenu")]]))
    else:
        app.edit_message_text(chat_id, message_id, "Activity statistics and accounts",
                              reply_markup=markup([[button("Activity", callback_data="Activity"), button("Accounts", callback_data="Accounts"), button("IDeas", callback_data="IDeas")],
                                                   [button("Comeback To Menu 🔙 ", callback_data="ComebackToMenu")]]))


def Accounts(chat_id, message_id, query):
    global step
    db = Account("Model.db")
    db.create_table()
    list_phone = db.get_list_phone()
    len_phone = len(list_phone)
    list_healthy_account = db.get_list_healthy_account()
    len_healthy = len(list_healthy_account)
    list_Temporary_report = db.get_list_Temporary_report()
    len_Temporary = len(list_Temporary_report)
    list_Permanent_report = db.get_list_Permanent_report()
    len_Permanent = len(list_Permanent_report)
    list_Deleted = db.get_list_deleted_account()
    len_delete = len(list_Deleted)
    list_phone_Activity = db.get_list_phone_Activity()
    db.close()
    list_accounts_add = list()
    stdelta = None
    setting = None

    db = SettingAddmember("Model.db")
    db.create_table()
    get_list_Setting = db.get_list_Setting()
    print(get_list_Setting)
    db.close()

    # check len settings addmember
    if len(get_list_Setting) < 1:
        print(f"no set setting {len(get_list_Setting)} ")
        query.answer(f"❌ Not Set Settings")

    else:
        setting = get_list_Setting[0][1]
        # accounts Activity
        ac = 0
        activi = 0
        unactivi = 0
        for Activity in list_phone_Activity:

            lastActivity = str(Activity[1]) + ' ' + str(Activity[2])
            date = DateTime().d
            time = DateTime().t
            TimeNow = str(date) + ' ' + str(time)
            FMT = '%d-%m-%Y %H:%M:%S'
            tdeltaa = datetime.strptime(
                TimeNow, FMT) - datetime.strptime(lastActivity, FMT)
            stdelta = str(tdeltaa)
            activi += 1
            print(f"{activi}    {stdelta}")
            if setting[0] == "d":
                if re.search(r'(\d.*).day', stdelta):
                    bet = re.findall(r'(\d.*).day', stdelta)
                    #print(f"bet: {bet}\n setting:{setting[2:]}|{setting[0]}")
                    if int(bet[0]) >= int(setting[2:]):
                        ac += 1
                        list_accounts_add.append(Activity[0])
                        print(f"{activi}    {stdelta}")
                    else:
                        pass
                        #print('not account')

            elif setting[0] == "t":
                if re.search(r'(\d.*).day', stdelta):
                    bet2 = re.findall(r'(\d.*).day', stdelta)
                    #print(f"bet: {bet}\n setting:{setting[2:]}|{setting[0]}")
                    if int(bet2[0]) >= 1:
                        ac += 1
                        list_accounts_add.append(Activity[0])
                        print(f"{activi}    {stdelta}")
                    else:
                        pass
                        #print('not account')
                else:
                    #print(f"{tdeltaa} |{setting[0]}")
                    Ti = stdelta.split(":")
                    # print(Ti)
                    if len(Ti) == 3:
                        if int(Ti[0]) >= int(setting[2:]):
                            ac += 1
                            list_accounts_add.append(Activity[0])
                            print(f"{activi}    {stdelta}")
                        else:
                            pass
                            #print('not account')
                    else:
                        pass
                        # print("Check")

        len_list_accounts_add = len(list_accounts_add)

        if len_phone > 0:

            keyboard = [

                [button("اکانت های سالم", callback_data="None"),
                 button("اکانت ها", callback_data="None")],
                [button(f"{len_healthy}", callback_data="None"),
                 button(f"{len_phone}", callback_data="None")],

                [button("ریپورت های دائمی", callback_data="None"),
                 button("ریپورت موقت", callback_data="None")],
                [button(f"{len_Permanent}", callback_data="None"),
                 button(f"{len_Temporary}", callback_data="None")],

                [button("حذف شده", callback_data="None"), button(
                    'اکانت های قابل استفاده', callback_data="None")],
                [button(f"{len_delete}", callback_data="None"),
                 button(f"{ac}", callback_data="None")],

                [button("Comeback To Menu 🔙 ", callback_data="ComebackToMenu"), button(
                    "Comeback 🔙", callback_data="StartStat")]

            ]

            app.edit_message_text(
                chat_id, message_id, "Statistics\nStatistics Accounts", reply_markup=markup(keyboard))
        else:
            step = "reStatistics"
            query.answer(f"❌ Not Account")
            Statistics(chat_id, message_id)


def Activityy(chat_id, message_id, query):

    global step
    db = AddStatistics("Model.db")
    db.create_table()
    list_activity = db.get_list_Statistics()
    db.close()

    if len(list_activity) > 0:

        keyboard = [
            [button("درصد دعوت های موفق", callback_data="None"),
             button("دعوت ها", callback_data="None")],
            [button(f"0", callback_data="None"), button(
                f"{list_activity[0][5]}", callback_data="None")],

            [button("درخواست ها", callback_data="None"), button(
                "دعوت های امروز", callback_data="None")],
            [button(f"{list_activity[0][4]}", callback_data="None"), button(
                f"{list_activity[0][3]}", callback_data="None")],

            [button("اخرین فعالیت", callback_data="None"),
             button("اخرین دعوت", callback_data="None")],
            [button(f"{list_activity[0][2]}", callback_data="None"), button(
                f"{list_activity[0][1]}", callback_data="None")],

            [button("Comeback To Menu 🔙 ", callback_data="ComebackToMenu"), button(
                "Comeback 🔙", callback_data="StartStat")]

        ]
        app.edit_message_text(
            chat_id, message_id, "Statistics\nStatistics Activity", reply_markup=markup(keyboard))
    else:
        step = "reStatistics"
        query.answer(f"Not Activity")
        Statistics(chat_id, message_id)


def IDeas(chat_id, message_id, query):
    global step
    db = Username("Model.db")
    db.create_table()
    list_username = db.get_list_username()
    db.close()

    if len(list_username) > 0:

        keyboard = [
            [button("آیدی ها", callback_data="None")],
            [button(f"{len(list_username)}", callback_data="None")],


            [button("Comeback To Menu 🔙 ", callback_data="ComebackToMenu"),
             button("Comeback 🔙", callback_data="StartStat")]

        ]
        app.edit_message_text(
            chat_id, message_id, "Statistics\nStatistics Activity", reply_markup=markup(keyboard))
    else:
        step = "reStatistics"
        query.answer(f"Not ID")
        Statistics(chat_id, message_id)
# /------------------------------------------------------------------------------------------------------------


# Update Account Reports---------------------------------------------------------------------------------------
def StartUAR(chat_id, message_id):
    db = Account("Model.db")
    db.create_table()
    list_Account = db.get_list_phone()
    Message = app.send_message(chat_id, "Start Updating Account Reports")
    l = len(list_Account)
    c = 0
    if len(list_Account) > 0:
        for account in list_Account:
            c += 1
            sleep(3)
            threading.Thread(target=SpamBot, args=[
                             chat_id, message_id, account, c]).start()
    else:
        app.send_message(chat_id, "<code>To update the report status of accounts ... I do not see any accounts</code>",
                         parse_mode='html', reply_to_message_id=message_id)
    db.close()
# /------------------------------------------------------------------------------------------------------------


# Add Member---------------------------------------------------------------------------------------------------
def StartAdd(chat_id, message_id, query):
    global step
    db = Groups("Model.db")
    db.create_table()
    listgroups = db.get_list_groups()
    db.close()

    db = SettingAddmember("Model.db")
    db.create_table()
    listsettings = db.get_list_Setting()
    db.close()

    lenG = len(listgroups)
    lenS = len(listsettings)

    text1 = f"\
<b>Add Member</b>\n\n\
<code>In which group do you want to join?</code>\n\n\
Click on the <b>Group</b> name \n\
If the group name is not in the list, Add the group name to your groups"
    text2 = f"<b>The list of groups is empty and no settings have been set</b>\n\
🔘 <code>Register your group</code>\n\
🔘 <code>Save the relevant invitation settings</code>"
    text3 = f"<b>Settings not set</b>\n\
🔘 <code>Save the relevant invitation settings</code>"
    text4 = f"<b>The list of groups is empty</b>\n\
🔘 <code>Register your group</code>"

    if lenG > 0 and lenS > 0:

        keyboard = [button(f"{group[0]}", callback_data=f"ad{group[1]}")
                    for group in listgroups]
        key = iter(keyboard)
        Output = [list(islice(key, elem))
                  for elem in [2 for n in range(len(keyboard))]]
        Output.append([button(text="Comeback To Menu 🔙 ", callback_data="ComebackToMenu"),
                       button("Comeback 🔙", callback_data="ComebackToMenu")])
        app.edit_message_text(chat_id, message_id, text1,
                              parse_mode="html", reply_markup=markup(Output))

    elif lenG < 1 and lenS < 1:
        app.edit_message_text(chat_id, message_id, text2, parse_mode='html')
    elif lenG > 0 and lenS < 1:
        app.edit_message_text(chat_id, message_id, text3, parse_mode='html')
    elif lenG < 1 and lenS > 0:
        app.edit_message_text(chat_id, message_id, text4, parse_mode='html')
    step = 'None'


def AddToGroups(chat_id, message_id, query, data):
    global step
    app.edit_message_text(
        chat_id, message_id, f"<code> How Many Accounts Do You want to work with? </code>\n<i>For example:</i>  <b>6</b> ", parse_mode="html")
    step = f"GettActivityNumber{data}"


def GettActivityNumber(chat_id, message_id, text, message):
    global step
    UG = step[20:]  # username Group
    update = (f"{str(UG)}",)

    db = Groups("Model.db")
    db.create_table()
    usergroup = db.get_list_username_groups(update)

    AN = text
    step = 'None'
    GeActivityAccounts(chat_id, message_id, usergroup, AN)


def GeActivityAccounts(chat_id, message_id, usergroup, AN):
    db = Account("Model.db")
    db.create_table()
    list_phone_Activity = db.get_list_phone_Activity()
    db.close()
    list_accounts_add = list()

    for Activity in list_phone_Activity:

        db = SettingAddmember("Model.db")
        db.create_table()
        get_list_Setting = db.get_list_Setting()
        db.close()
        try:
            setting = get_list_Setting[0][1]

        except Exception as error:
            print(errors)
        else:
            lastActivity = str(Activity[1]) + ' ' + str(Activity[2])
            date = DateTime().d
            time = DateTime().t
            TimeNow = str(date) + ' ' + str(time)
            FMT = '%d-%m-%Y %H:%M:%S'
            tdeltaa = datetime.strptime(
                TimeNow, FMT) - datetime.strptime(lastActivity, FMT)
            stdelta = str(tdeltaa)
            if setting[0] == "d":
                if re.search(r'(\d.*).day', stdelta):
                    bet = re.findall(r'(\d.*).day', stdelta)
                    #print(f"bet: {bet}\n setting:{setting[2:]}|{setting[0]}")
                    if int(bet[0]) >= int(setting[2:]):
                        list_accounts_add.append(Activity[0])
                    else:
                        pass
                        #print('not account')

            elif setting[0] == "t":
                if re.search(r'(\d.*).day', stdelta):
                    bet2 = re.findall(r'(\d.*).day', stdelta)
                    #print(f"bet: {bet}\n setting:{setting[2:]}|{setting[0]}")
                    if int(bet2[0]) >= 1:
                        list_accounts_add.append(Activity[0])

                    else:
                        pass
                        #print('not account')
                else:
                    #print(f"{tdeltaa} |{setting[0]}")
                    Ti = stdelta.split(":")
                    # print(Ti)
                    if len(Ti) == 3:
                        if int(Ti[0]) >= int(setting[2:]):
                            list_accounts_add.append(Activity[0])

                        else:
                            pass
                            #print('not account')
                    else:
                        pass
                        # print("Check")

    if len(list_accounts_add) >= int(AN):
        list_Account = list_accounts_add[:int(AN)]
        print(len(list_Account))
        ForAddChatMember(chat_id, message_id, list_Account, usergroup)
    else:
        MessageThree(chat_id, message_id)


def ForAddChatMember(chat_id, message_id, list_Account, usergroup):

    for account in list_Account:
        print(f"Start Add -> [{account}]")
        T = threading.Thread(target=AddMemberToGroup, args=[
                             account, usergroup, chat_id, message_id])
        T.start()
        sleep(30)


def AddMemberToGroup(account, usergroup, chat_id, message_id):
    db = SettingAddmember("Model.db")
    db.create_table()
    list_setting = db.get_list_Setting()
    db.close()
    db = Username("Model.db")
    db.create_table()
    list_username = db.get_list_username()

    list_user = [x for x in list_username]
    activity = int(list_setting[0][2])
    today_send_success = 0
    today_send_unsuccess = 0
    F = 0
    list_group_username = list()
    try:
        api_id, api_hash = 13360888, "f9f13233c4bff84f6ee3423f58f796a8"

        Cli = Client(f'sessions/phone{account}', api_id, api_hash)
        Cli.connect()

        if len(list_user) <= 1:
            app.send_message(chat_id, "The ID list is empty")
        else:
            try:
                Cli.join_chat(usergroup[0])

            except Exception as error:
                print(f"[{account}]\tWhen Join Chat: {error}")
            try:
                for member in Cli.iter_chat_members(usergroup[0]):
                    if member.user.username != None and member.user.is_self != True and member.user.is_bot != True and member.status not in ["creator", "administrator"]:
                        status = member.user.status
                        if status == "offline":
                            last_online_date_user = datetime.strptime(time.ctime(
                                member.user.last_online_date), '%a %b %d %H:%M:%S %Y')
                            date_now = datetime.now()
                            c = (date_now - last_online_date_user).days

                        elif status == "within_month" or status == "long_time_ago" or status == "within_week":
                            continue
                        else:
                            c = 0

                        if c < 7:
                            list_group_username.append(member.user.username)
                    else:
                        pass
            except Exception as error:
                print(error)
            else:
                while today_send_success != activity:
                    user_id = choice(db.get_list_username())
                    time.sleep(5)
                    try:

                        if user_id not in list_group_username:
                            add = Cli.add_chat_members(usergroup[0], user_id)
                        else:
                            pass
                    except errors.Forbidden as error:
                        deleteusername = (f"{user_id}",)
                        db.delete_username(deleteusername)
                        print(f"Error [{account}] {error}")
                        today_send_unsuccess += 1
                        continue
                    except errors.PeerFlood as error:
                        today_send_unsuccess += 1
                        F += 1
                        print(f"Error ({F}) [{account}] {error}")
                        if F == 3:
                            print(
                                f"Add [{account}]  Completed.Due to Limitation")
                            break
                        else:
                            continue
                    except errors.FloodWait as error:
                        print(f"Error [{account}] {error}")
                        today_send_unsuccess += 1
                        break
                    except errors.BadRequest as error:
                        print(f"Error [{account}] {error}")
                        continue
                    except Exception as error:
                        print(f"Error Exception [{account}] {error}")
                        today_send_unsuccess += 1
                        continue
                    else:
                        deleteusername = (f"{user_id}",)
                        db.delete_username(deleteusername)
                        today_send_success += 1
                        print(f"[{account}]\tsucessfull: {today_send_success}")
                Cli.disconnect()
                MessageAddMember(
                    chat_id, message_id, today_send_success, today_send_unsuccess, account)

    except errors.SessionRevoked as error:
        print(f"Error 1 {error} Phone: {account}")
        DeleteSessionRevoked(chat_id, message_id, account)

    except errors.UserDeactivated as error:
        print(f"Error 2 {error} Phone: {account}")
        UpdateDeleteAccount(chat_id, message_id, account)
        DeleteSessionRevoked(chat_id, message_id, number)

    except errors.AuthKeyUnregistered as error:
        print(f"Error 3 {error} Phone: {account}")
        DeleteSessionRevoked(chat_id, message_id, account)
        DeleteSessionRevoked(chat_id, message_id, number)

    except errors.UserDeactivatedBan as error:
        print(f"Error 4 {error} Phone: {account}")
        UpdateDeleteAccount(chat_id, message_id, number)
        DeleteSessionRevoked(chat_id, message_id, number)

    except errors.Unauthorized as error:
        print(f"Error 5 {error} Phone: {account}")
        UpdateDeleteAccount(chat_id, message_id, number)
        DeleteSessionRevoked(chat_id, message_id, number)

    except Exception as error:
        print(f"Error 6 {error} Phone: {account}")


def DeleteSessionRevoked(chat_id, message_id, account):
    db = Account("Model.db")
    db.create_table()
    db.delete_account((account,))
    db.close()
    app.send_message(chat_id, f"<b>This account[<code>{account}</code>] can not be activated due to logout.</b>\n\
<code>Deleted from the database. Please re-enter this number in the bot</code>", parse_mode="html")


def UpdateDeleteAccount(chat_id, message_id, account):
    db = Account("Model.db")
    db.create_table()
    db.update_delete(("True", account))
    db.close()
    app.send_message(
        chat_id, f"<b>This account[<code>{account}</code>] was deleted by Telegram</b>", parse_mode="html")


def MessageAddMember(chat_id, message_id, today_send_success, today_send_unsuccess, account):
    app.send_message(
        chat_id, f"<b>Account</b><code>{account}</code><b> did {today_send_success} successful and {today_send_unsuccess}  unsuccessful</b>", parse_mode="html")

    SaveAddsAccount(chat_id, message_id, today_send_success,
                    today_send_unsuccess, account)


def SaveAddsAccount(chat_id, message_id, today_send_success, today_send_unsuccess, account):

    db = Account("Model.db")
    db.create_table()
    aaccount = (f"{account}",)
    list_Addaccount = db.get_SuccessfulAdds_UnSuccessfulAdds_Adds(aaccount)
    date = DateTime().d
    time = DateTime().t
    LastAdd, LastActivity = date, time
    SuccessfulAdds = int(list_Addaccount[0][0])+today_send_success
    UnSuccessfulAdds = int(list_Addaccount[0][1])+today_send_unsuccess
    Adds = int(list_Addaccount[0][2])+today_send_success
    db.close()
    try:
        db = Account("Model.db")
        AllData = (f"{LastAdd}", f"{LastActivity}", f"{SuccessfulAdds}",
                   f"{UnSuccessfulAdds}", f"{Adds}", account)
        db.update_account(AllData)
        db.close()
        print(f"SaveAddsAccount           -> ({account})")
        SaveAddStatistics(chat_id, message_id, today_send_success,
                          today_send_unsuccess, account, date, time)

    except Exception as error:
        print(f"Error:{error}")


def SaveAddStatistics(chat_id, message_id, today_send_success, today_send_unsuccess, account, date, time):

    db = AddStatistics("Model.db")
    db.create_table()
    list_AddStatistics = db.get_list_Statistics()

    if len(list_AddStatistics) < 1:

        LastAdd, LastActivity = date, time
        RequestedAdditions = 1
        Adds = today_send_success
        AddToday = today_send_success
        PercentAddsSuccessful = (today_send_success * 100) / 10
        try:

            AllData = (f"{PercentAddsSuccessful}", f"{LastAdd}", f"{LastActivity}",
                       f"{AddToday}", f"{RequestedAdditions}", f"{Adds}")
            db.insert_data(AllData)
            db.close()
            print("insert   SaveAddStatistics")
        except Exception as error:
            print(f"Error:{error}")

    elif len(list_AddStatistics) >= 1:

        LastAdd, LastActivity = date, time

        Last_timeAdd_dateAdd = db.get_list_Statistics()
        lastActivity = str(
            Last_timeAdd_dateAdd[0][1]) + ' ' + str(Last_timeAdd_dateAdd[0][2])
        TimeNow = str(date) + ' ' + str(time)
        FMT = '%d-%m-%Y %H:%M:%S'
        tdeltaa = datetime.strptime(
            TimeNow, FMT) - datetime.strptime(lastActivity, FMT)

        if re.search(r'(\d).day', str(tdeltaa)):
            bet = re.findall(r'(\d).day', str(tdeltaa))
            if int(bet[0]) >= 1:
                AddToday = today_send_success
            else:
                print(f"else:{bet[0]}")
        else:
            AddToday = int(list_AddStatistics[0][3]) + today_send_success

        RequestedAdditions = int(list_AddStatistics[0][4]) + 1
        Adds = int(list_AddStatistics[0][5]) + today_send_success
        PercentAddsSuccessful = (today_send_success * 100) / 10
        try:

            AllData = (f"{PercentAddsSuccessful}", f"{LastAdd}", f"{LastActivity}",
                       f"{AddToday}", f"{RequestedAdditions}", f"{Adds}", account)
            db.update_data(AllData)
            print(f"Update SaveAddStatistics  -> ({account})")
            db.close()
        except Exception as error:
            print(f"Error:{error}")
# /-------------------------------------------------------------------------------------------------------------


app.start()
print("running..")

idle()
app.stop()
print("app stopped")

