import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ChatJoinRequestHandler, ContextTypes

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Конфигурация
BOT_TOKEN = "8327774569:AAGHjpkt8KTbLTRL33FIcnfNU7M-tGHnpDE"
CHANNEL_LINK = "https://t.me/+H8af58DeKVk3MTEy"
MY_CHANNEL_ID = -1003529108574

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /start с вашим текстом"""
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
    
    await update.message.reply_text(
        text, 
        reply_markup=InlineKeyboardMarkup([[button]])
    )
    logging.info(f"Пользователь {update.effective_user.id} запросил доступ")

async def accept_join_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Принятие заявки с вашим текстом"""
    if update.effective_chat.id != MY_CHANNEL_ID:
        logging.warning(f"Игнорируем чужой канал: {update.effective_chat.id}")
        return
    
    try:
        user = update.chat_join_request.from_user
        
        # Принимаем заявку
        await update.chat_join_request.approve()
        logging.info(f"✅ Принята заявка от @{user.username or user.id}")
        
        # Ваше приветственное сообщение
        welcome_message = (
            "🎊 ВАША ЗАЯВКА ПРИНЯТА!\n\n"
            "Добро пожаловать в наш канал! 🤗\n\n"
            f"🔗 Ссылка: {CHANNEL_LINK}\n\n"
            "Приятного просмотра! ❤️"
        )
        
        try:
            # Отправляем приветствие
            button = InlineKeyboardButton("🚀 ПЕРЕЙТИ В КАНАЛ", url=CHANNEL_LINK)
            await context.bot.send_message(
                chat_id=user.id,
                text=welcome_message,
                reply_markup=InlineKeyboardMarkup([[button]])
            )
            logging.info(f"📨 Отправлено приветствие для @{user.username or user.id}")
            
        except Exception as e:
            error_msg = str(e).lower()
            if "user_is_blocked" in error_msg:
                logging.warning(f"Пользователь @{user.username or user.id} заблокировал бота")
            elif "bot can't initiate conversation" in error_msg:
                logging.warning(f"Требуется начать диалог с @{user.username or user.id}")
            else:
                logging.error(f"Ошибка отправки: {e}")
                
    except Exception as e:
        error_msg = str(e)
        if "User_already_participant" in error_msg:
            logging.info(f"Пользователь уже в канале")
            try:
                # Отправляем ссылку если уже в канале
                user = update.chat_join_request.from_user
                button = InlineKeyboardButton("📲 ОТКРЫТЬ КАНАЛ", url=CHANNEL_LINK)
                await context.bot.send_message(
                    chat_id=user.id,
                    text=f"✅ Вы уже в канале! Вот ссылка:\n{CHANNEL_LINK}",
                    reply_markup=InlineKeyboardMarkup([[button]])
                )
            except:
                pass
        elif "CHAT_ADMIN_REQUIRED" in error_msg:
            logging.error("❌ БОТ НЕ АДМИНИСТРАТОР! Добавьте бота в канал как админа")
        else:
            logging.error(f"Ошибка: {error_msg}")

def main():
    """Запуск бота"""
    print("=" * 60)
    print("🤖 БОТ ДЛЯ АВТОМАТИЧЕСКОГО ПРИНЯТИЯ ЗАЯВОК")
    print("=" * 60)
    print(f"🔗 Ссылка на канал: {CHANNEL_LINK}")
    print(f"🆔 ID канала: {MY_CHANNEL_ID}")
    print("=" * 60)
    print("✅ Бот работает 24/7")
    print("✅ Автоматическое принятие заявок")
    print("✅ Защита от чужих каналов")
    print("=" * 60)
    
    # Запускаем бота
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(ChatJoinRequestHandler(accept_join_request))
    
    print("🚀 Бот запущен! Ожидание заявок...")
    app.run_polling(
        drop_pending_updates=True,
        allowed_updates=Update.ALL_TYPES
    )

if __name__ == '__main__':
    main()