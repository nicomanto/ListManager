from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, ChatAction
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


class DeleteListConversation:

    def __init__(self, list_manager):
        self.listManager = list_manager
        self.LISTNAME = 1

    # Define a few command handlers. These usually take the two arguments update and
    # context. Error handlers also receive the raised TelegramError object in error.

    def wichList(self, update, context):
        # add is typing
        context.bot.sendChatAction(chat_id=update.message.chat_id,
                                   action=ChatAction.TYPING)

        myLists = [[x]
                   for x in self.listManager.getMyLists(update.message.chat_id)]

        if myLists:
            update.message.reply_text(
                "Scegli la lista da eliminare (perderai tutti gli elementi al suo interno) 🛍️\n\n/cancel",
                reply_markup=ReplyKeyboardMarkup(
                    keyboard=myLists, resize_keyboard=True, one_time_keyboard=True, input_field_placeholder='Quale lista?'
                ))

            return self.LISTNAME

        logger.warning(
            f'No lists for chat_id "{update.message.chat_id}"')
        update.message.reply_text(
            "Non è presente nessuna lista da poter eliminare ⚠️")
        return ConversationHandler.END

    def deleteList(self, update, context):
        chat_id = update.message.chat_id
        listName = update.message.text

        # add is typing
        context.bot.sendChatAction(chat_id=chat_id,
                                   action=ChatAction.TYPING)

        if not self.listManager.listIsPresent(chat_id, listName):
            logger.warning(
                f'No list "{listName}" for chat_id "{chat_id}"')
            update.message.reply_text(
                f'Lista *{listName}* non presente ⚠️', parse_mode="markdown", reply_markup=ReplyKeyboardRemove())
        else:
            self.listManager.deleteList(chat_id, listName)
            logger.info(
                f'List "{listName}" created for chat_id "{chat_id}"')
            update.message.reply_text(
                f'Lista *{listName}* eliminata con successo 🗑️', parse_mode="markdown", reply_markup=ReplyKeyboardRemove())

        return ConversationHandler.END
