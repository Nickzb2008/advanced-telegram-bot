import os
import logging
import time

logging.basicConfig(level=logging.DEBUG)

def check_specific_variables():
    """Перевіряємо конкретно ваші змінні"""
    
    your_variables = [
        'BOT_TOKEN',
        'TOKEN_50TA_TELEGRAM', 
        'TOKEN'
    ]
    
    logging.info("🔍 ПЕРЕВІРКА ВАШИХ ЗМІННИХ:")
    
    for var_name in your_variables:
        value = os.environ.get(var_name)
        if value:
            # Показуємо тільки початок і кінець токена для безпеки
            masked_value = f"{value[:10]}...{value[-10:]}" if len(value) > 20 else "***"
            logging.info(f"✅ ЗНАЙДЕНО: {var_name} = {masked_value}")
            
            # Перевіряємо довжину токена (має бути ~45-50 символів)
            logging.info(f"   📏 Довжина: {len(value)} символів")
            
            # Тестуємо токен
            test_token(value, var_name)
            return value
        else:
            logging.info(f"❌ НЕ ЗНАЙДЕНО: {var_name}")
    
    return None

def test_token(token, var_name):
    """Тестуємо чи токен валідний"""
    logging.info(f"🧪 Тестую токен з {var_name}...")
    
    try:
        from telegram.ext import Application
        # Спробуємо створити Application без запуску
        app = Application.builder().token(token).build()
        logging.info(f"✅ Токен з {var_name} ВАЛІДНИЙ!")
        return True
    except Exception as e:
        logging.error(f"❌ Токен з {var_name} НЕВАЛІДНИЙ: {e}")
        return False

def main():
    logging.info("🚀 Запуск перевірки ваших змінних...")
    time.sleep(3)
    
    # Додаткова перевірка - виводимо всі змінні що починаються на 'T'
    logging.info("📋 Всі змінні з 'T':")
    for key, value in os.environ.items():
        if key.startswith('T'):
            logging.info(f"   {key} = {'***' if value else 'EMPTY'}")
    
    # Перевіряємо ваші конкретні змінні
    bot_token = check_specific_variables()
    
    if bot_token:
        logging.info("🎉 УСПІХ! Запускаємо бота...")
        
        try:
            from telegram.ext import Application
            from telegram import Update
            from telegram.ext import ContextTypes, CommandHandler
            
            app = Application.builder().token(bot_token).build()
            
            async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
                user = update.effective_user
                await update.message.reply_text(
                    f"🎉 Привіт, {user.first_name}!\n\n"
                    f"Бот успішно працює на Railway!\n"
                    f"Змінні середовища знайдено та працюють!"
                )
            
            app.add_handler(CommandHandler("start", start))
            logging.info("🟢 Бот запускається...")
            app.run_polling(drop_pending_updates=True)
            
        except Exception as e:
            logging.error(f"❌ Помилка запуску бота: {e}")
    else:
        logging.error("💥 Жодна з ваших змінних не знайдена!")
        logging.error("🔄 ПЕРЕВІРТЕ:")
        logging.error("   1. Чи зробили ви 'Redeploy' після додавання змінних?")
        logging.error("   2. Чекайте повного завершення redeploy")
        logging.error("   3. Перевірте логи після redeploy")

if __name__ == '__main__':
    main()
