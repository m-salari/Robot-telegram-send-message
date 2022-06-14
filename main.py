from telethon import TelegramClient, events
from telethon.tl.functions.contacts import ImportContactsRequest
from telethon.tl.types import InputPhoneContact
import random
import asyncio
import excel

loop = asyncio.get_event_loop()


def GetConfig():
    f3 = open('config.txt', 'r')
    config = f3.readlines()
    f3.close()
    for z in range(len(config)):
        config[z] = config[z].replace('\n','')

    api_id = int(config[0])
    api_hash = config[1]
    return api_id, api_hash


def GetMessage():
    f = open('message.txt', 'r', encoding='utf-8')
    message = f.read()
    f.close()
    return message


def GetUsernameAdmins():
    f2 = open('username_admin.txt', 'r', encoding='utf-8')
    usernames = f2.readlines()
    for i in range(len(usernames)):
        usernames[i] = usernames[i].replace('\n', '')
    f2.close()
    return usernames


async def AddContact(phone, name):

    contact = InputPhoneContact(client_id=random.randint(0, 9999), phone=phone,
                                first_name=name, last_name='')
    result = await client(ImportContactsRequest(contacts=[contact]))
    print(result.__dict__)
    user_id = int(result.imported[0].user_id)
    return user_id


async def SendMessage(user_id, message):
    await client.send_message(user_id, message)


async def main():
    number_of_columns = excel.LenOfColumns()
    count_of_column = 1

    for j in range(number_of_columns):
        try:
            p = excel.GetNumberInColumnFromExcel(j)
            for phone in p:
                user_id = await AddContact(phone, f'customer {count_of_column}')
                await SendMessage(user_id, message)
                print(j, f'customer {count_of_column} added and send message\t phone :', phone)
                count_of_column += 1

                # await asyncio.sleep(30)
        except:
            pass


api_id, api_hash = GetConfig()
client = TelegramClient('session_name', api_id, api_hash)
message = GetMessage()
usernames = GetUsernameAdmins()

@client.on(events.NewMessage)
async def GetMessage(event):
    if event.is_private:

        message = event.message.message
        if message == '1':

            # user_id = event.message.from_id.user_id
            user_id = event.message.peer_id.user_id

            info = await client.get_entity(user_id)
            phone = info.phone
            username = info.username

            if username != None:
                username = '@' + username

            for username_admin in usernames:
                await SendMessage(f'{username_admin}', f'phone number is: {phone}\n\t username is: {username}')


client.start()
loop.run_until_complete(main())
loop.run_forever()