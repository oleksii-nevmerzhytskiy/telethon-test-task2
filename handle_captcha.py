

class HandlerCaptcha:

    def __init__(self, client, message):
        self.client = client
        self.message = message

    async def handle_captcha1(self):
        my_user_data = await self.client.get_me()
        first_name = (my_user_data.first_name)
        result = ''
        if f'Привет, {first_name}' in self.message.message:

            for row in self.message.reply_markup.rows:
                for button in row.buttons:
                    if 'Я НЕ БОТ' in button.text:
                        result = await self.message.click(text=button.text, data=button.data)
                        print(result)

    async def handle_captcha2(self):
        my_user_data = await self.client.get_me()
        username = (my_user_data.username)
        message = self.message.message
        i = 0
        ch = message[0]
        expression = ''
        if username in message:
            while ch != ')':
                expression += ch
                i += 1
                ch = message[i]
            expression += ch
        result = eval(expression)
        await self.client.send_message(message.peer_id.channel_id, result)

