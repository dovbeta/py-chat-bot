import json
import openai
import logging
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, CallbackContext

def load_json_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception as e:
        logging.error(f"Error loading {file_path}: {e}")
        return {}

def load_config():
    return load_json_file("config.json")

def load_context():
    return load_json_file("context.json")

def load_allowed_chats():
    return load_json_file("allowed_chats.json")

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

# Handle messages
async def handle_message(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    user_message = update.message.text
    allowed_chats = load_allowed_chats()

    logging.info(f"Received message: {user_message} (chat: {chat_id})")

    if chat_id not in allowed_chats:
        logging.warning(f"Chat {chat_id} is not allowed.")
        return

    # If the message is a reply to another message, use the replied message as input
    # Otherwise, use the message itself
    if user_message.strip() == "!" and update.message.reply_to_message:
        user_message = update.message.reply_to_message.text
    elif user_message.startswith("!"):
        user_message = user_message[1:].strip()
    else:
        return

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