import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv

# Завантажуємо змінні середовища
load_dotenv()

# Налаштування логування
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Отримуємо токен з змінних середовища
BOT_TOKEN = os.getenv('BOT_TOKEN')

if not BOT_TOKEN:
    raise ValueError("Будь ласка, встановіть змінну середовища BOT_TOKEN")

# Обробник команди /start
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_html(
        f"Привіт, {user.mention_html()}! 👋\n\n"
        "Я твій перший бот, розгорнутий на Render.com!\n"
        "Надішли мені будь-яке повідомлення, і я його повторю.\n\n"
        "Доступні команди:\n"
        "/start - цей текст\n"
        "/help - допомога\n"
        "/info - інформація про бота"
    )

# Обробник команди /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = """
📖 **Довідка по боту**

Це демонстраційний бот, який:
• Повторює ваші повідомлення
• Має кілька простих команд
• Працює на безкоштовному хостингу Render.com

Просто напиши щось, і я відповіду!
    """
    await update.message.reply_text(help_text)

# Обробник команди /info
async def info_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    info_text = """
ℹ️ **Інформація про бота**

**Хостинг:** Render.com
**Мова:** Python
**Бібліотека:** python-telegram-bot
**Статус:** Активний ✅

Бот успішно працює на безкоштовному тарифі!
    """
    await update.message.reply_text(info_text)

# Обробник звичайних текстових повідомлень
async def echo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    user = update.effective_user
    
    # Проста логіка "відлуння" з покращенням
    response = f"🔄 **Твоє повідомлення:**\n{user_message}\n\n💬 Я отримав його, {user.first_name}!"
    await update.message.reply_text(response)

# Обробник помилок
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.error(f"Помилка: {context.error}")

# Основна функція
def main():
    # Створюємо додаток
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Додаємо обробники
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("info", info_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo_handler))
    
    # Обробник помилок
    application.add_error_handler(error_handler)
    
    # Запускаємо бота
    print("🟢 Бот запускається...")
    application.run_polling(
        drop_pending_updates=True,
        allowed_updates=Update.ALL_TYPES
    )

if __name__ == '__main__':
    main()