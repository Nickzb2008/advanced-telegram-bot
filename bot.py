import os
import logging
import time

logging.basicConfig(level=logging.DEBUG)

def check_railway_environment():
    """Спеціальна функція для перевірки Railway середовища"""
    
    # Спеціальні змінні Railway
    railway_vars = [
        'RAILWAY_ENVIRONMENT',
        'RAILWAY_SERVICE_NAME', 
        'RAILWAY_PROJECT_NAME',
        'RAILWAY_GIT_COMMIT_SHA',
        'BOT_TOKEN'
    ]
    
    logging.info("🔍 ПЕРЕВІРКА RAILWAY СЕРЕДОВИЩА")
    
    all_vars_found = False
    for var in railway_vars:
        value = os.environ.get(var)
        if value:
            logging.info(f"✅ {var} = {value}")
            all_vars_found = True
        else:
            logging.info(f"❌ {var} = НЕ ЗНАЙДЕНО")
    
    if not all_vars_found:
        logging.error("🚨 СЕРЕДОВИЩЕ RAILWAY НЕ ЗАВАНТАЖЕНЕ!")
        logging.error("💡 Можливі причини:")
        logging.error("   - Неправильний тип сервісу (потрібен Web Service)")
        logging.error("   - Проблема з платформою Railway")
        logging.error("   - Потрібно створити новий проект")
    
    return all_vars_found

def main():
    logging.info("🚀 Запуск перевірки Railway середовища...")
    time.sleep(3)
    
    # Перевіряємо середовище Railway
    env_ok = check_railway_environment()
    
    if not env_ok:
        logging.error("❌ Неможливо продовжити - середовище не налаштоване")
        return
    
    # Перевіряємо BOT_TOKEN
    bot_token = os.environ.get('BOT_TOKEN')
    if bot_token:
        logging.info(f"✅ BOT_TOKEN знайдено! Довжина: {len(bot_token)}")
        
        # Спробуємо запустити бота
        try:
            from telegram.ext import Application
            app = Application.builder().token(bot_token).build()
            logging.info("🟢 Бот ініціалізований успішно!")
            
            from telegram import Update
            from telegram.ext import ContextTypes, CommandHandler
            
            async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
                await update.message.reply_text("🎉 Бот працює на Railway!")
            
            app.add_handler(CommandHandler("start", start))
            app.run_polling()
            
        except Exception as e:
            logging.error(f"❌ Помилка бота: {e}")
    else:
        logging.error("❌ BOT_TOKEN не знайдено навіть після перевірки середовища")

if __name__ == '__main__':
    main()
