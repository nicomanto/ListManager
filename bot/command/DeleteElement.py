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


class DeleteElementConversation:

    def __init__(self, list_manager):
        self.listManager = list_manager
        self.LISTNAME, self.ELEMENTNAME = range(2)
        self.listName = ""

    def wichList(self, update, context):
        # add is typing
        context.bot.sendChatAction(chat_id=update.message.chat_id,
                                   action=ChatAction.TYPING)

        myLists = [[x]
                   for x in self.listManager.getMyLists(update.message.chat_id)]

        if myLists:
            update.message.reply_text(
                "Scegli la lista a cui rimuovere gli elementi 🛍️\n\n/cancel",
                reply_markup=ReplyKeyboardMarkup(
                    keyboard=myLists, resize_keyboard=True, one_time_keyboard=True, input_field_placeholder='Quale lista?'
                ))

            return self.LISTNAME

        logger.warning(
            f'No lists for chat_id "{update.message.chat_id}"')
        update.message.reply_text(
            "Non è presente nessuna lista in cui poter eliminare un elemento ⚠️")
        return ConversationHandler.END

    def wichElement(self, update, context):
        chat_id = update.message.chat_id
        self.listName = update.message.text

        # add is typing
        context.bot.sendChatAction(chat_id=chat_id,
                                   action=ChatAction.TYPING)

        if self.listManager.listIsPresent(chat_id, self.listName):
            myElement = [[x] for x in self.listManager.getElementsFromList(
                update.message.chat_id, self.listName)]
            if myElement:
                update.message.reply_text(
                    f"Scegli l'elemento da rimuovere nella lista *{self.listName}* 🛍️\n\n/cancel",
                    parse_mode="markdown",
                    reply_markup=ReplyKeyboardMarkup(
                        keyboard=myElement, resize_keyboard=True, one_time_keyboard=True, input_field_placeholder='Quale elemento?'
                    ))

                return self.ELEMENTNAME
            else:
                logger.warning(
                    f'List "{self.listName}" empty for chat_id "{chat_id}"')
                update.message.reply_text(
                    f"Non è presente nessun elemento nella lista *{self.listName}* ⚠️", parse_mode="markdown", reply_markup=ReplyKeyboardRemove())
        else:
            logger.warning(
                f'No list "{self.listName}" for chat_id "{chat_id}"')
            update.message.reply_text(
                f'Lista *{self.listName}* non presente ⚠️', parse_mode="markdown", reply_markup=ReplyKeyboardRemove())

        return ConversationHandler.END

    def removeElement(self, update, context):
        element = update.message.text
        chat_id = update.message.chat_id

        # add is typing
        context.bot.sendChatAction(chat_id=chat_id,
                                   action=ChatAction.TYPING)

        if not self.listManager.elementIsPresent(chat_id, self.listName, element):
            logger.warning(
                f'Element "{element}" not present in list "{self.listName}" for chat_id "{chat_id}"')
            update.message.reply_text(
                f'Elemento *{element}* non presente nella lista *{self.listName}* ⚠️', parse_mode="markdown", reply_markup=ReplyKeyboardRemove())
        else:
            self.listManager.removeElementFromList(
                chat_id, self.listName, element)

            logger.info(
                f'Element "{element}" inserted into list "{self.listName}" for chat_id "{chat_id}"')
            update.message.reply_text(
                f'*{element}* rimosso dalla lista *{self.listName}* 🗑️', parse_mode="markdown", reply_markup=ReplyKeyboardRemove())

        return ConversationHandler.END
