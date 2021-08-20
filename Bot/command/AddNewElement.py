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


class AddNewElementConversation:

    def __init__(self, list_manager):
        self.listManager = list_manager
        self.LISTNAME, self.ELEMENTNAME = range(2)
        self.listName = ""

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
                "Scegli la lista in cui inserire gli elementi 🛍️\n\n/cancel",
                reply_markup=ReplyKeyboardMarkup(
                    keyboard=myLists, resize_keyboard=True, one_time_keyboard=True, input_field_placeholder='Quale lista?'
                ))

            return self.LISTNAME

        logger.warning(
            f'No lists for chat_id "{update.message.chat_id}"')
        update.message.reply_text(
            "Non è presente nessuna lista in cui poter inserire un elemento ⚠️\n\nCreane una tramite il comando /add_list")
        return ConversationHandler.END

    def wichElement(self, update, context):
        chat_id = update.message.chat_id
        self.listName = update.message.text

        # add is typing
        context.bot.sendChatAction(chat_id=chat_id,
                                   action=ChatAction.TYPING)

        if self.listManager.listIsPresent(chat_id, self.listName):
            update.message.reply_text(
                'ℹ Inserisci gli elementi separati dal carattere *invio*\n\nEsempio:\n*nome elemento\nnome elemento*\n\n/cancel', parse_mode="markdown", reply_markup=ReplyKeyboardRemove())
            return self.ELEMENTNAME

        logger.warning(
            f'No list "{self.listName}" for chat_id "{chat_id}"')
        update.message.reply_text(
            f'Lista *{self.listName}* non presente ⚠️', parse_mode="markdown", reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END

    def addElement(self, update, context):
        chat_id = update.message.chat_id

        # add is typing
        context.bot.sendChatAction(chat_id=chat_id,
                                   action=ChatAction.TYPING)

        elements = [x.strip() for x in update.message.text.split("\n") if x]

        self.listManager.addElementToList(chat_id, self.listName, elements)

        logger.info(
            f'Elements inserted into list "{self.listName}" for chat_id "{chat_id}"')
        update.message.reply_text(
            f'Elementi aggiunti alla lista *{self.listName}* ✅', parse_mode="markdown")
        return ConversationHandler.END
