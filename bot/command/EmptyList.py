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


class EmptyListConversation:

    def __init__(self, list_manager):
        self.listManager = list_manager
        self.LISTNAME = 1

    def wichList(self, update, context):
        # add is typing
        context.bot.sendChatAction(chat_id=update.message.chat_id,
                                   action=ChatAction.TYPING)

        myLists = [[x]
                   for x in self.listManager.getMyLists(update.message.chat_id)]

        if myLists:
            update.message.reply_text(
                "Scegli la lista che vuoi svuotare 🛍️\n\n/cancel",
                reply_markup=ReplyKeyboardMarkup(
                    keyboard=myLists, resize_keyboard=True, one_time_keyboard=True, input_field_placeholder='Quale lista?'
                ))

            return self.LISTNAME

        logger.warning(
            f'No lists for chat_id "{update.message.chat_id}"')
        update.message.reply_text(
            "Non è presente nessuna lista da svuotare ⚠️")
        return ConversationHandler.END

    def emptyList(self, update, context):
        chat_id = update.message.chat_id
        listName = update.message.text

        # add is typing
        context.bot.sendChatAction(chat_id=chat_id,
                                   action=ChatAction.TYPING)

        self.listManager.emptyList(chat_id, listName)

        logger.info(
            f'List "{listName}" emptied for chat_id "{chat_id}"')
        update.message.reply_text(
            f'Lista *{listName}* svuotata 🗑️', parse_mode="markdown", reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END
