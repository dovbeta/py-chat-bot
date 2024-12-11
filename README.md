# Telegram OSBB Chat Bot

## Overview
This project is a Telegram bot built using Python for the residents of an OSBB group chat. The bot answers frequently asked questions using OpenAI integration.

## Features
- Responds to messages starting with an exclamation mark.
- Logs queries to a general log file.
- Provides context-based answers using OpenAI API.

## Prerequisites
- Python 3.8 or higher
- A Telegram bot token
- An OpenAI API key

## Installation
1. Clone the repository to your local machine.
    ```sh
    git clone https://github.com/yourusername/telegram-osbb-chat-bot.git
    ```
2. Navigate to the project directory.
    ```sh
    cd telegram-osbb-chat-bot
    ```
3. Install the required dependencies.
    ```sh
    pip install -r requirements.txt
    ```

## Configuration
1. Open the `config.json` file.
2. Update the bot's token and OpenAI API token.
    ```json
    {
      "telegram_token": "your_actual_telegram_token",
      "openai_api_key": "your_actual_openai_api_key",
      "openai_model": "gpt-3.5-turbo",
      "openai_temperature": 0.3
    }
    ```
3. Specify the OpenAI model and temperature settings as needed.

## Usage
1. Start the bot.
    ```sh
    python bot.py
    ```
2. In the group chat, type messages starting with an exclamation mark to interact with the bot.
    ```text
    !What are the OSBB rules?
    ```
3. The bot will respond with answers based on the provided context.

## License
This project is licensed under the MIT License. See the `LICENSE` file for more details.