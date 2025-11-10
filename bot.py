import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Налаштування логування для Railway
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Отримуємо токен з змінних середовища Railway
BOT_TOKEN = os.environ.get('BOT_TOKEN')

if not BOT_TOKEN:
    logging.error("❌ BOT_TOKEN не знайдено! Перевірте змінні середовища в Railway.")
    exit(1)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_html(
        f"🚀 Привіт, {user.mention_html()}!\n\n"
        "Я успішно розгорнутий на <b>Railway.app</b>!\n"
        "Надішли мені повідомлення, і я його повторю.\n\n"
        "<b>Команди:</b>\n"
        "/start - цей текст\n"
        "/help - довідка\n"
        "/status - статус бота"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📖 <b>Довідка</b>\n\n"
        "Цей бот демонструє розгортання на Railway.app\n"
        "Він повторює ваші повідомлення та має кілька команд.",
        parse_mode='HTML'
    )

async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "✅ <b>Статус: Активний</b>\n\n"
        "🛠 <b>Хостинг:</b> Railway.app\n"
        "💾 <b>Статус:</b> Працює стабільно\n"
        "⚡ <b>Режим:</b> Polling",
        parse_mode='HTML'
    )

async def echo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    user = update.effective_user
    
    await update.message.reply_text(
        f"🔁 <b>Ваше повідомлення:</b>\n<code>{user_message}</code>\n\n"
        f"💬 Прийнято, {user.first_name}!",
        parse_mode='HTML'
    )

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.error(f"Помилка: {context.error}")

def main():
    try:
        application = Application.builder().token(BOT_TOKEN).build()
        
        # Додаємо обробники
        application.add_handler(CommandHandler("start", start_command))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(CommandHandler("status", status_command))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo_handler))
        
        application.add_error_handler(error_handler)
        
        # Запускаємо бота
        logging.info("🟢 Бот запускається на Railway...")
        application.run_polling(
            drop_pending_updates=True,
            allowed_updates=Update.ALL_TYPES
        )
    except Exception as e:
        logging.error(f"❌ Критична помилка: {e}")

if __name__ == '__main__':
    main()
