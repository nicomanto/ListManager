from telegram import ChatAction
from telegram.ext import ConversationHandler
import logging
import os
import sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


class AddNewListConversation:

    def __init__(self, list_manager):
        self.listManager = list_manager
        self.LISTNAME = 1

    # Define a few command handlers. These usually take the two arguments update and
    # context. Error handlers also receive the raised TelegramError object in error.

    def newList(self, update, context):
        # add is typing
        context.bot.sendChatAction(chat_id=update.message.chat_id,
                                   action=ChatAction.TYPING)

        update.message.reply_text(
            "Come vuoi chiamare la nuova lista❓\n\n/cancel")

        return self.LISTNAME

    def listCreation(self, update, context):
        chat_id = update.message.chat_id
        listName = update.message.text

        # add is typing
        context.bot.sendChatAction(chat_id=chat_id,
                                   action=ChatAction.TYPING)

        if self.listManager.listIsPresent(chat_id, listName):
            logger.warning(
                f'List "{listName}" is already present for chat_id "{chat_id}"')
            update.message.reply_text(
                f'La lista *{listName}* è già presente, digita un nome diverso ⚠️\n\n/cancel', parse_mode="markdown")
            return self.LISTNAME

        self.listManager.createNewList(chat_id, listName)
        logger.info(
            f'List "{listName}" created for chat_id "{chat_id}"')
        update.message.reply_text(
            f'Lista *{listName}* creata con successo ✅', parse_mode="markdown")
        return ConversationHandler.END
