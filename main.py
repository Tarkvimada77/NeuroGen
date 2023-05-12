import telebot
import config


class NeuroGen:

    def __init__(self):
        # Создание бота и первой клавиатуры
        self.bot = telebot.TeleBot(config.TOKEN)

        self.keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1)
        self.one_btn = telebot.types.KeyboardButton("СОЗДАТЬ МОДЕЛЬ🕸️")
        self.two_btn = telebot.types.KeyboardButton("ГАЙДЫℹ️")

        self.keyboard.add(self.one_btn)
        self.keyboard.add(self.two_btn)

    def start(self):

        # Обработка старта
        @self.bot.message_handler(commands=['start'])
        def start_hand(message):
            self.bot.send_message(message.chat.id,
                                  f"<b>Привет {message.from_user.username}!✌️</b>\nЯ Нейроген, бот для удобной разработки <b>реккурентных нейронных</b> сетей в Telegram!📱\nДумаю с управлением ты разберёшься😊",
                                  reply_markup=self.keyboard, parse_mode="HTML")


    def rns(self):
        # Создание инлайн клавиатуры
        inlinee_kbd = telebot.types.InlineKeyboardMarkup()

        inline_btn1 = telebot.types.InlineKeyboardButton('Выделение ключевых слов', callback_data='kl')
        inline_btn2 = telebot.types.InlineKeyboardButton('Построение языковой модели', callback_data='lan')
        inline_btn3 = telebot.types.InlineKeyboardButton('Дообучение модели GPT', callback_data='gpt')

        inlinee_kbd.add(inline_btn1)
        inlinee_kbd.add(inline_btn2)
        inlinee_kbd.add(inline_btn3)

        @self.bot.message_handler(func=lambda message: message.text == "СОЗДАТЬ МОДЕЛЬ🕸️")
        def rns_hand(message):
            self.bot.reply_to(message, "Отлично! теперь давайте определимся с типом сети: ", reply_markup=inlinee_kbd)

        # обработка звонков от инлайн кнопок
        @self.bot.callback_query_handler(func=lambda call: True)
        def callback_inline(call):
            if call.data == 'kl':
                pass

            if call.data == 'lan':
                inline_lang = telebot.types.InlineKeyboardMarkup()

                lang_btn = telebot.types.InlineKeyboardButton('Русский', callback_data='ru')
                lang_btn1 = telebot.types.InlineKeyboardButton('Английский', callback_data='en')
                lang_btn2 = telebot.types.InlineKeyboardButton('Произвольный', callback_data='ar')

                inline_lang.add(lang_btn)
                inline_lang.add(lang_btn1)
                inline_lang.add(lang_btn2)

                self.bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                           text="Выберете язык на котором будет обучаться модель:",
                                           reply_markup=inline_lang)
            if call.data == 'gpt':
                pass

    def run(self):
        self.bot.polling(none_stop=True)


if __name__ == "__main__":
    a = NeuroGen()
    a.start()
    a.rns()
    a.run()
