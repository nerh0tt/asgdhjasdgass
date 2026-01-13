import os
import logging
import http.server
import socketserver
import threading
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ChatJoinRequestHandler, ContextTypes

# Простой HTTP сервер для Render
def run_http_server():
    class Handler(http.server.SimpleHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'<h1>🤖 Bot is running</h1>')
    
    with socketserver.TCPServer(("", 10000), Handler) as httpd:
        print("🌐 HTTP сервер запущен на порту 10000")
        httpd.serve_forever()

# Запускаем HTTP сервер в фоне
server_thread = threading.Thread(target=run_http_server, daemon=True)
server_thread.start()

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Конфигурация
BOT_TOKEN = "8327774569:AAGHjpkt8KTbLTRL33FIcnfNU7M-tGHnpDE"
CHANNEL_LINK = "https://t.me/+H8af58DeKVk3MTEy"
MY_CHANNEL_ID = -1003529108574

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

def main():
    """Запуск бота"""
    print("=" * 60)
    print("🤖 БОТ ЗАПУЩЕН")
    print("=" * 60)
    print("🌐 HTTP сервер: порт 10000")
    print("🤖 Telegram бот: активен")
    print("=" * 60)
    
    # Запускаем Telegram бота
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(ChatJoinRequestHandler(accept_join_request))
    
    print("✅ Ожидание заявок...")
    app.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    main()
