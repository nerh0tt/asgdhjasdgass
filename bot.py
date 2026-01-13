import os
import logging
from flask import Flask
from threading import Thread
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ChatJoinRequestHandler, ContextTypes

# Создаем Flask сервер для Render
app = Flask(__name__)

@app.route('/')
def home():
    return "🤖 Бот работает! (только для принятия заявок)"

@app.route('/health')
def health():
    return "OK", 200

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Конфигурация
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8327774569:AAGHjpkt8KTbLTRL33FIcnfNU7M-tGHnpDE")
CHANNEL_LINK = os.environ.get("CHANNEL_LINK", "https://t.me/+H8af58DeKVk3MTEy")
MY_CHANNEL_ID = int(os.environ.get("MY_CHANNEL_ID", "-1003529108574"))

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /start"""
    button = InlineKeyboardButton("🔥 ПОДАТЬ ЗАЯВКУ", url=CHANNEL_LINK)
    
    text = (
        "🎉 ДОБРО ПОЖАЛОВАТЬ! В КАНАЛ СО ШЛЮХАМИ!\n\n"
        "Нажмите кнопку ниже, чтобы подать заявку\n"
        "на вступление в шлюший канал где сук столько что ты просто ахуеешь.\n\n"
        "✅ Автоматическое принятие\n"
        "⏱️ Мгновенное подтверждение\n"
        "🎁 Доступ к эксклюзивному контенту\n\n"
        "👇 Нажимай на кнопку что бы увидеть сливы всех блогерш, тик токерш, и всех сук онлика!"
    )
    
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup([[button]]))

async def accept_join_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Принятие заявки"""
    if update.effective_chat.id != MY_CHANNEL_ID:
        return
    
    try:
        user = update.chat_join_request.from_user
        await update.chat_join_request.approve()
        
        welcome_message = (
            "🎊 ВАША ЗАЯВКА ПРИНЯТА!\n\n"
            "Добро пожаловать в наш канал! 🤗\n\n"
            f"🔗 Ссылка: {CHANNEL_LINK}\n\n"
            "Приятного просмотра! ❤️"
        )
        
        try:
            button = InlineKeyboardButton("🚀 ПЕРЕЙТИ В КАНАЛ", url=CHANNEL_LINK)
            await context.bot.send_message(
                user.id,
                welcome_message,
                reply_markup=InlineKeyboardMarkup([[button]])
            )
        except:
            pass
            
    except Exception as e:
        if "already" not in str(e).lower():
            print(f"Ошибка: {e}")

def run_flask():
    """Запуск веб-сервера на порту 10000"""
    app.run(host='0.0.0.0', port=10000)

def main():
    print("=" * 60)
    print("🤖 БОТ ЗАПУСКАЕТСЯ С ВЕБ-СЕРВЕРОМ")
    print("=" * 60)
    
    # Запускаем Flask в отдельном потоке
    flask_thread = Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()
    
    # Запускаем Telegram бота
    bot_app = Application.builder().token(BOT_TOKEN).build()
    bot_app.add_handler(CommandHandler("start", start_command))
    bot_app.add_handler(ChatJoinRequestHandler(accept_join_request))
    
    print("✅ Веб-сервер запущен на порту 10000")
    print("✅ Telegram бот запущен")
    print("=" * 60)
    print("🚀 Ожидание заявок...")
    
    bot_app.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    main()
