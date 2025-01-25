from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Указываем номер билда вручную
BUILD_NUMBER ="хер вам" # Поменяйте этот номер вручную при каждом новом билде


# Функция для обработки команды /start
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(
        f'Привет! Я Ванек! (Build {BUILD_NUMBER})')


# Функция эхо: повторяет полученное сообщение и добавляет номер билда
async def echo(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text  # Получаем сообщение от пользователя
    response = f"Build {BUILD_NUMBER}: {user_message}"  # Добавляем номер билда к сообщению
    await update.message.reply_text(response)  # Отправляем ответ с номером билда


def main():
    # Замените 'YOUR_TOKEN' на токен вашего бота
    token = "6350322365:AAEA8ziByqPd-RMAK2afjPxikbfL5-2o-LM"

    # Создаем приложение
    application = Application.builder().token(token).build()

    # Выводим номер билда при запуске
    print(f"Bot started with BUILD NUMBER: {BUILD_NUMBER}")

    # Регистрируем обработчики команд и сообщений
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Начинаем поиск обновлений
    application.run_polling()


if __name__ == '__main__':
    main()

