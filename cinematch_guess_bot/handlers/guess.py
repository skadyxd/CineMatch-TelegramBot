from telegram import Update
from telegram.ext import ContextTypes

from cinematch_guess_bot.handlers.newgame import STATE_PLAYING, STATE_START


async def guess(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Проверяем, находится ли пользователь в состоянии игры
    if context.user_data.get("state") != STATE_PLAYING:
        await context.bot.send_message(update.effective_chat.id,
                                       text="Вы не в игре. Начните новую игру с команды /newgame.")
        return

    # Получаем ответ пользователя
    user_guess = update.message.text

    # Проверяем, совпадает ли ответ с загаданным фильмом
    if user_guess.lower() == context.user_data["title"].lower():
        await context.bot.send_message(update.effective_chat.id, text="Поздравляем! Вы угадали!")
        await context.bot.send_photo(update.effective_chat.id, context.user_data['photo'])
        # Завершаем игру
        context.user_data["state"] = STATE_START
    else:
        # Уменьшаем количество попыток и проверяем, закончились ли они
        context.user_data["attempts"] -= 1
        if context.user_data["attempts"] > 0:
            await context.bot.send_message(update.effective_chat.id,
                                           text=f"Неверно. У вас осталось {context.user_data['attempts']} попыток.")
        else:
            await context.bot.send_message(update.effective_chat.id,
                                           text=f"Вы проиграли. Правильный ответ: {context.user_data['title']}.")
            await context.bot.send_photo(update.effective_chat.id, context.user_data['photo'])
            # Завершаем игру
            context.user_data["state"] = STATE_START


