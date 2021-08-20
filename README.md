# ListManager

[ListManager-bot](https://t.me/ListManager8aBot)

## Introduction

Telegram's bot that manage lists. The repository include an Alexa's Skill that send defaults Alexa's Lists (shopping and to-do) to the bot

## Technology

- [MongoDB](https://www.mongodb.com/)
- [Alexa Skill SDK](https://developer.amazon.com/en-US/alexa/devices/alexa-built-in/development-resources/sdk)
- [Heroku](https://www.heroku.com/)
- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)

## Folders structure

- **bot:** contains the source code of the Telegram's bot
- **skill:** contains the source code of the Alexa's skill
- **requirements.txt:** contains dependendcy of bot
- **skill/lambda/requirements.txt:** contains dependendcy of skill
- **Procfile:** file that run bot on _Heroku_

## Usage

### Bot

Bot is hosted on _Heroku_. The bot manage list (create, delete, update list and item) and persist data of lists in _MongoDB_. If an user block the bot, the data will be removed after **25 minutes**.

### Skill

Skill was deployed with [Alexa Developer Console](https://developer.amazon.com/alexa/console/ask). The skill is not published in the skills store of Alexa. Skill can be connected to the bot through **chat_id** and with this it can send _to-do_ and _shopping list_ to the chat

### Use the code

If you want to use the code, you need to replace environment variables:

- **MONGO_URI:** connection to the Database
- **BOT_TOKEN:** token of the Telegram's bot
- **IP and PORT:** ip and port used by _webhook_ for _Heroku_
