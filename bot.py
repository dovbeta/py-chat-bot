import json
import openai
import logging
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, CallbackContext

# Load configuration
def load_config():
    try:
        with open("config.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception as e:
        logging.error(f"Error loading configuration: {e}")
        return {}

config = load_config()

# Set OpenAI API key
openai.api_key = config.get("openai_api_key")

# Logging configuration
logging.basicConfig(
    filename="bot_logs.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    encoding="utf-8"
)

# Load context
def load_context():
    try:
        with open("context.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception as e:
        logging.error(f"Error loading context: {e}")
        return {}

# Load allowed chats
def load_allowed_chats():
    try:
        with open("allowed_chats.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception as e:
        logging.error(f"Error loading allowed chats: {e}")
        return []

# Handle messages
async def handle_message(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    user_message = update.message.text
    allowed_chats = load_allowed_chats()

    logging.info(f"Received message: {user_message} (chat: {chat_id})")

    if chat_id not in allowed_chats:
        logging.warning(f"Chat {chat_id} is not allowed.")
        return

    if user_message.strip() == "!" and update.message.reply_to_message:
        user_message = update.message.reply_to_message.text
    elif not user_message.startswith("!"):
        return

    if user_message.startswith("!"):
        user_message = user_message[1:].strip()

    osbb_context = load_context()

    messages = [
        {"role": "system", "content": f"You are a bot helping OSBB residents. Here is the OSBB information:\n{json.dumps(osbb_context, ensure_ascii=False)}"},
        {"role": "user", "content": user_message},
    ]

    try:
        response = await openai.ChatCompletion.acreate(
            model=config.get("openai_model"),
            messages=messages,
            max_tokens=300,
            temperature=config.get("openai_temperature")
        )
        answer = response['choices'][0]['message']['content'].strip()

        logging.info(f"Generated response: {answer}")

        await update.message.reply_text(answer)

    except Exception as e:
        logging.error(f"Error: {e}")

# Main function
def main():
    telegram_token = config.get("telegram_token")

    application = Application.builder().token(telegram_token).build()

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logging.info("Bot started!")
    application.run_polling()

if __name__ == "__main__":
    main()