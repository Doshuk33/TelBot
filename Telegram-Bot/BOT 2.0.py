import logging
import nest_asyncio
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler
import asyncio

# Применяем nest_asyncio
nest_asyncio.apply()

# Включаем логирование
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Токен Telegram-бота
TOKEN = "7636905672:AAH_9oH_C2pvQIgnE656rkvF3N5RoCVP-uk"

# CRM-данные клиентов (замените на свои данные)
CRM_DATA = {
    "client1": {"name": "Иван", "chat_id": None, "reason": None, "feedback": None, "rate": None}
}

# Состояния диалога
START, ASK_REASON, ASK_FEEDBACK, ASK_RATE = range(4)

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    CRM_DATA["client1"]["chat_id"] = update.effective_chat.id
    await update.message.reply_text('Привет! Это бот для возврата клиентов.')
    await update.message.reply_text('Почему вы ушли?')
    return ASK_REASON

# Обработка ответа на вопрос о причине ухода
async def ask_reason(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    reason = update.message.text
    CRM_DATA["client1"]["reason"] = reason
    await update.message.reply_text('Спасибо за ответ!')
    await send_proposal(update, context)
    await update.message.reply_text('Оцените наше предложение:')
    return ASK_FEEDBACK

# Обработка ответа на вопрос о предложении
async def ask_feedback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    feedback = update.message.text
    CRM_DATA["client1"]["feedback"] = feedback
    await update.message.reply_text('Спасибо за отзыв!')
    await update.message.reply_text('Оцените наше предложение по шкале от 1 до 10:')
    return ASK_RATE

# Обработка ответа на вопрос о оценке
async def ask_rate(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    rate = update.message.text
    CRM_DATA["client1"]["rate"] = rate
    await update.message.reply_text('Спасибо за оценку!')
    await update.message.reply_text('Ваш отзыв и оценка сохранены!')
    return ConversationHandler.END

# Обработка команды /report
async def report(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Отчет:')
    for client, data in CRM_DATA.items():
        await update.message.reply_text(f'Имя: {data["name"]}, Причина ухода: {data["reason"]}, Отзыв: {data["feedback"]}, Оценка: {data["rate"]}')

# Обработка команды /help
async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Часто задаваемые вопросы:')
    await update.message.reply_text('1. Почему вы ушли?')
    await update.message.reply_text('2. Как оценить наше предложение?')
    await update.message.reply_text('3. Как оставить отзыв?')

# Обработка ошибок
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if context.error:
        logger.warning(f'Update {update} caused error {context.error}')
    else:
        logger.info('Update {update} caused error')

# Обработка команды /cancel
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Диалог отменен.')
    return ConversationHandler.END

# Обработка команды /dash
async def dash(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('http://localhost:8000/')

# Обработка команды /send_proposal
async def send_proposal(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    for client, data in CRM_DATA.items():
        await context.bot.send_message(chat_id=data['chat_id'], text='Предложение от нашей компании:')

async def main():
    application = ApplicationBuilder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            ASK_REASON: [MessageHandler(filters.TEXT, ask_reason)],
            ASK_FEEDBACK: [MessageHandler(filters.TEXT, ask_feedback)],
            ASK_RATE: [MessageHandler(filters.TEXT, ask_rate)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    application.add_handler(conv_handler)
    application.add_handler(CommandHandler('report', report))
    application.add_handler(CommandHandler('help', help))
    application.add_handler(CommandHandler('dash', dash))

    application.add_error_handler(error)

    await application.run_polling()

if __name__ == '__main__':
    asyncio.run(main())