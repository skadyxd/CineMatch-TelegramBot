import logging

from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from dotenv import load_dotenv

from cinematch_guess_bot import handlers
from cinematch_guess_bot.config import TELEGRAM_BOT_TOKEN

COMMAND_HANDLERS = {
    "start": handlers.start,
    "newgame": handlers.newgame
}

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

load_dotenv()


def main():
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    for command_name, command_handler in COMMAND_HANDLERS.items():
        application.add_handler(CommandHandler(command_name, command_handler))

        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handlers.guess))

    application.run_polling()


if __name__ == "__main__":
    try:
        main()
    except Exception:
        import traceback

        logger.warning(traceback.format_exc())
