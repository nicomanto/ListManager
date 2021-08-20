from telegram.ext import ConversationHandler
from telegram import ReplyKeyboardRemove, ChatAction
from command.DeleteElement import DeleteElementConversation
from command.DeleteList import DeleteListConversation
from command.getElements import GetElementsConversation
from command.AddNewElement import AddNewElementConversation
from command.AddNewList import AddNewListConversation
from command.EmptyList import EmptyListConversation
from ListManager import ListManager

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


class Command:
    # list object manager
    lManager = ListManager()

    # conversation command
    newList = AddNewListConversation(lManager)
    deleteList = DeleteListConversation(lManager)
    emptyList = EmptyListConversation(lManager)
    newElement = AddNewElementConversation(lManager)
    getElements = GetElementsConversation(lManager)
    removeElements = DeleteElementConversation(lManager)

    # Define a few command handlers. These usually take the two arguments update and
    # context. Error handlers also receive the raised TelegramError object in error.

    def start(self, update, context):
        """Create dict for chat_id if not present. Reply with explanation message"""
        if not self.lManager.chatIsPresent(update.message.chat_id):
            self.lManager.createNewUser(update.message.chat_id)
            logger.info(
                f'New user with chat_id "{update.message.chat_id}"')

         # add is typing
        context.bot.sendChatAction(chat_id=update.message.chat_id,
                                   action=ChatAction.TYPING)
        update.message.reply_text(
            f"Ciao 🤖\nSono *ListManager*, il bot che ti aiuterà a gestire le tue *liste* 📋\nHo una fantastica feature che mi permette di collegarmi ad *Alexa* tramite la skill *List Manager*, la quale può inviarmi le liste predefinite gestite da Alexa. Il collegamento avviene tramite l'identificativo della chat. Non ti preoccupare, funziono anche senza il collegamento con Alexa 😉\n\nChe aspetti, prova subito 😊\n\nIl tuo identificativo della chat è *\"{update.message.chat_id}\"*", parse_mode="markdown")

    def getLists(self, update, context):
        """Return list of Lists for specific chat_id"""
        chat_id = update.message.chat_id

        # add is typing
        context.bot.sendChatAction(chat_id=update.message.chat_id,
                                   action=ChatAction.TYPING)

        lists = self.lManager.getMyLists(chat_id)

        if lists:
            msg = "Ecco le tue liste 📋:\n\n"
            msg += "- "+("\n- ".join(x for x in lists))
        else:
            logger.info(
                f'No lists for chat_id "{chat_id}"')
            msg = "Non è presente nessuna lista 📋"

        update.message.reply_text(msg, parse_mode="markdown")

    def cancel(self, update, context):
        """Cancels and ends the conversation."""

        # add is typing
        context.bot.sendChatAction(chat_id=update.message.chat_id,
                                   action=ChatAction.TYPING)

        logger.info(
            f'Delete operation for "{update.message.chat_id}"')
        update.message.reply_text(
            'Operazione annullata ❌', reply_markup=ReplyKeyboardRemove()
        )
        return ConversationHandler.END

    def help(self, update, context):
        """Send a message when the command /help is issued."""

        # add is typing
        context.bot.sendChatAction(chat_id=update.message.chat_id,
                                   action=ChatAction.TYPING)

        update.message.reply_text(
            f"🆘 Ecco i comandi che puoi utilizzare:\n\n/add\_list | Crea una lista\n/delete\_list | Cancella una lista\n/get\_lists | Visualizza le liste\n/empty\_list | Svuota una lista\n/add\_elements | Aggiunge gli elementi ad una lista\n/delete\_element | Elimina un elemento in una lista\n/get\_elements | Visualizza gli elementi in una lista\n/help | Aiuto\n\nL'identificativo della chat per il collegamento con la skill *List Manager* di *Alexa* è *\"{update.message.chat_id}\"*", parse_mode="markdown")

    def error(self, update, context):
        """Log Errors caused by Updates."""
        logger.warning(
            f'Update {update} caused error {context.error} of type {type(context.error).__name__}')
