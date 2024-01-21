from telegram import Update
from telegram.ext import ContextTypes

from cinematch_guess_bot.game_logic import api_request

# Используем строковые константы для задания состояний
STATE_START = "start"
STATE_PLAYING = "playing"


async def newgame(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Проверяем, находится ли пользователь в состоянии игры
    if context.user_data.get("state") == STATE_PLAYING:
        await context.bot.send_message(update.effective_chat.id,
                                       text="Вы уже в игре. Завершите текущую игру, чтобы начать новую.")
        return

    # Загружаем новый фильм
    api_response = api_request()

    # Сохраняем информацию о текущем фильме и устанавливаем состояние игры в "playing"
    context.user_data["title"] = api_response["title"]
    context.user_data["photo"] = api_response["posterUrl"]
    context.user_data["attempts"] = 3
    context.user_data["state"] = STATE_PLAYING

    # Отправляем описание фильма пользователю
    await context.bot.send_message(update.effective_chat.id, text=api_response["description"])
    await context.bot.send_message(update.effective_chat.id, text="Угадайте название фильма. У вас 3 попытки.")

