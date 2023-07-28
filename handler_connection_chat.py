import asyncio
import os

from dotenv import load_dotenv
from telethon import TelegramClient, sync
from telethon.tl.functions.channels import JoinChannelRequest

from database_connector import DatabaseConnector
from handle_captcha import HandlerCaptcha


class ChatHandler:
    def __init__(self, api_id, api_hash, session_name):
        self.api_id = api_id
        self.api_hash = api_hash
        self.session_name = session_name
        self.client = TelegramClient(session_name, api_id, api_hash)
        self.db_connector = DatabaseConnector(host=os.getenv('MYSQL_HOST'), username=os.getenv('MYSQL_USER'),
                                              password=os.getenv('MYSQL_PASSWORD'),
                                              database=os.getenv('MYSQL_DB'), port=os.getenv('MYSQL_PORT'))

    async def join_group(self, group_link):
        await self.client.connect()
        global DATE_FORMAT
        result = await self.client(JoinChannelRequest(group_link))
        return result.chats[0].date

    async def get_message(self, group_link, join_date):
        messages = await self.client.get_messages(group_link, limit=5, offset_date=join_date)
        print(messages)
        for message in messages:
            sender = await message.get_sender()
            if sender.bot is True:
                return message, sender
            else:
                return None, None

    def find_bot(self, bot_data):
        bot_id = bot_data.id
        result = self.db_connector.find_bot_method(bot_id)
        print(result)
        if result is not None:
            return result
        else:
            return None

    def new_bot(self, message, bot_data):
        bot_id = bot_data.id
        query = f"INSERT INTO test_db.new_bots_table (user_id, message, user_data) VALUES ({bot_id}, {str(message)}, {str(bot_data)});"
        self.db_connector.execute_query(query)
        print('bot info added successfully')

    async def run_function(self, function_name, message):
        handle_captcha = HandlerCaptcha(self.client, message)
        if function_name == 'handle_captcha1':
            await handle_captcha.handle_captcha1()
        elif function_name == 'handle_captcha2':
            await handle_captcha.handle_captcha2()


async def main():
    load_dotenv()
    api_id = os.getenv('TELETHON_API_ID')
    api_hash = os.getenv('TELETHON_API_HASH')
    session_name = os.getenv('TELETHON_API_SESSION')
    Channel_name = "Your Telegram channel"

    chat_handler = ChatHandler(api_id, api_hash, session_name)
    chat_handler.db_connector.connect()

    join_date = await chat_handler.join_group(Channel_name)
    message, sender = await chat_handler.get_message(Channel_name, join_date)

    result = chat_handler.find_bot(sender)
    if result is None:
        chat_handler.new_bot(message, sender)
    else:
        await chat_handler.run_function(result, message)


if __name__ == "__main__":
    asyncio.run(main())
