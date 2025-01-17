from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Функция для обработки команды /start
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Привет! Я бот, отправь мне что-нибудь, и я верну это обратно!')

# Функция эхо: повторяет полученное сообщение
async def echo(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(update.message.text)

def main():
    # Замените 'YOUR_TOKEN' на токен вашего бота
    application = Application.builder().token("6350322365:AAEA8ziByqPd-RMAK2afjPxikbfL5-2o-LM").build()

    # Регистрируем обработчики команд и сообщенийsgsggssg
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Начинаем поиск обновлен
    application.run_polling()
if __name__ == '__main__':
    main()

