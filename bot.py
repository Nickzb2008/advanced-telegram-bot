import os
import logging
import time

# Детальне логування
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def debug_environment():
    logging.info("🔍 === ПОЧАТОК ДЕБАГУ СЕРЕДОВИЩА ===")
    
    # Отримуємо BOT_TOKEN
    bot_token = os.environ.get('BOT_TOKEN')
    logging.info(f"🎯 BOT_TOKEN = {bot_token}")
    
    # Перевіряємо довжину токена
    if bot_token:
        logging.info(f"📏 Довжина токена: {len(bot_token)} символів")
    else:
        logging.info("❌ Токен не знайдено або порожній")
    
    # Виводимо ВСІ змінні середовища (для дебагу)
    logging.info("📋 ВСІ змінні середовища:")
    for key, value in os.environ.items():
        if any(word in key.upper() for word in ['BOT', 'TOKEN', 'SECRET', 'KEY']):
            masked_value = value[:10] + '...' + value[-10:] if len(value) > 20 else value
            logging.info(f"   {key} = {masked_value}")
    
    logging.info("🔚 === КІНЕЦЬ ДЕБАГУ ===")
    
    return bot_token

def main():
    logging.info("🚀 Запуск бота...")
    
    # Чекаємо 5 секунд (іноді змінні завантажуються з затримкою)
    time.sleep(5)
    
    # Дебаг середовища
    bot_token = debug_environment()
    
    if not bot_token:
        logging.error("❌ КРИТИЧНА ПОМИЛКА: BOT_TOKEN не знайдено!")
        logging.error("🛠 Дії для вирішення:")
        logging.error("1. Перейдіть в Railway → Variables")
        logging.error("2. Переконайтесь що змінна називається 'BOT_TOKEN'")
        logging.error("3. Переконайтесь що значення введено правильно")
        logging.error("4. Натисніть 'Redeploy' після змін")
        return
    
    # Якщо токен знайдено, продовжуємо
    logging.info("✅ BOT_TOKEN знайдено! Спробуємо ініціалізувати бота...")
    
    try:
        from telegram.ext import Application
        
        app = Application.builder().token(bot_token).build()
        logging.info("🟢 Бот успішно ініціалізований!")
        
        # Додаємо просту команду для тесту
        from telegram import Update
        from telegram.ext import ContextTypes, CommandHandler
        
        async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
            await update.message.reply_text("🎉 Бот успішно працює на Railway!")
        
        app.add_handler(CommandHandler("start", start))
        
        # Запускаємо
        logging.info("🟢 Запускаємо опитування...")
        app.run_polling(drop_pending_updates=True)
        
    except Exception as e:
        logging.error(f"❌ Помилка ініціалізації: {e}")

if __name__ == '__main__':
    main()
