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


class GetElementsConversation:

    def __init__(self, list_manager):
        self.listManager = list_manager
        self.LISTNAME = 1

    def whichList(self, update, context):
        # add is typing
        context.bot.sendChatAction(chat_id=update.message.chat_id,
                                   action=ChatAction.TYPING)

        myLists = [[x]
                   for x in self.listManager.getMyLists(update.message.chat_id)]

        if myLists:
            update.message.reply_text(
                "Scegli il nome della lista da visualizzare 🛍️\n\n/cancel",
                reply_markup=ReplyKeyboardMarkup(
                    keyboard=myLists, resize_keyboard=True, one_time_keyboard=True, input_field_placeholder='Quale lista?'
                ))

            return self.LISTNAME

        logger.warning(
            f'No lists for chat_id "{update.message.chat_id}"')
        update.message.reply_text(
            "Non è presente nessuna lista da visualizzare ⚠️")
        return ConversationHandler.END

    def listVisualization(self, update, context):
        chat_id = update.message.chat_id
        listName = update.message.text

        # add is typing
        context.bot.sendChatAction(chat_id=chat_id,
                                   action=ChatAction.TYPING)

        if self.listManager.listIsPresent(chat_id, listName):
            elements = self.listManager.getElementsFromList(chat_id, listName)

            if elements:
                msg = f"Lista *{listName}* 📋:\n\n"
                msg += "- "+("\n- ".join(x for x in elements))
            else:
                logger.info(
                    f'List "{listName}" empty for chat_id "{chat_id}"')
                msg = f"La lista *{listName}* è *vuota* 📋"

            update.message.reply_text(
                msg, parse_mode="markdown", reply_markup=ReplyKeyboardRemove())
        else:
            logger.warning(
                f'No list "{listName}" for chat_id "{chat_id}"')
            update.message.reply_text(
                f'Lista *{listName}* non presente ⚠️', parse_mode="markdown", reply_markup=ReplyKeyboardRemove())

        return ConversationHandler.END
