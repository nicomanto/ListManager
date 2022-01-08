import logging
import time
import threading
import os

from telegram import ChatAction, error
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler

from command.Command import Command

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# set the port number to listen in for the webhook
PORT = int(os.environ.get('PORT', None))
TOKEN = os.environ.get('BOT_TOKEN', None)
IP = os.environ.get('IP', None)


def checkUserBlockTheBot(list_manager, bot):
    """Check if user block the bot in order to delete chat_id and lists"""
    entryToDelete = []
    while(True):
        logger.info("Check blocked bot")
        time.sleep(1500)  # 25 minutes
        for x in list_manager.getAllChatId():
            try:
                bot.sendChatAction(chat_id=x,
                                   action=ChatAction.TYPING)
            except error.Unauthorized:
                entryToDelete.append(x)

        for x in entryToDelete:
            logger.info(f'chat_id "{x}" blocked the bot')
            list_manager.deleteChat(x)
        entryToDelete.clear()


def main():
    """Start the bot."""
    updater = Updater(
        TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # get command object
    comm = Command()

    # create list conversation
    createList = ConversationHandler(
        entry_points=[CommandHandler('add_list', comm.newList.newList)],
        states={
            comm.newList.LISTNAME: [MessageHandler(
                Filters.text & ~Filters.command, comm.newList.listCreation)]
        },
        fallbacks=[CommandHandler('cancel', comm.cancel)],
    )

    # delete list conversation
    deleteList = ConversationHandler(
        entry_points=[CommandHandler(
            'delete_list', comm.deleteList.wichList)],
        states={
            comm.newList.LISTNAME: [MessageHandler(
                Filters.text & ~Filters.command, comm.deleteList.deleteList)]
        },
        fallbacks=[CommandHandler('cancel', comm.cancel)],
    )

    # empty list conversation
    emptyList = ConversationHandler(
        entry_points=[CommandHandler(
            'empty_list', comm.emptyList.wichList)],
        states={
            comm.emptyList.LISTNAME: [MessageHandler(Filters.text & ~Filters.command, comm.emptyList.emptyList)]},
        fallbacks=[CommandHandler('cancel', comm.cancel)],
    )

    # add element conversation
    addElement = ConversationHandler(
        entry_points=[CommandHandler(
            'add_elements', comm.newElement.wichList)],
        states={
            comm.newElement.LISTNAME: [MessageHandler(Filters.text & ~Filters.command, comm.newElement.wichElement)],
            comm.newElement.ELEMENTNAME: [MessageHandler(
                Filters.text & ~Filters.command, comm.newElement.addElement)]
        },
        fallbacks=[CommandHandler('cancel', comm.cancel)],
    )

    # get elements conversation
    getElements = ConversationHandler(
        entry_points=[CommandHandler(
            'get_elements', comm.getElements.whichList)],
        states={
            comm.newList.LISTNAME: [MessageHandler(
                Filters.text & ~Filters.command, comm.getElements.listVisualization)]
        },
        fallbacks=[CommandHandler('cancel', comm.cancel)],
    )

    # remove element conversation
    removeElement = ConversationHandler(
        entry_points=[CommandHandler(
            'delete_element', comm.removeElements.wichList)],
        states={
            comm.removeElements.LISTNAME: [MessageHandler(Filters.text & ~Filters.command, comm.removeElements.wichElement)],
            comm.removeElements.ELEMENTNAME: [MessageHandler(
                Filters.text & ~Filters.command, comm.removeElements.removeElement)]
        },
        fallbacks=[CommandHandler('cancel', comm.cancel)],
    )

    # add simple command
    dp.add_handler(CommandHandler("start", comm.start))
    dp.add_handler(CommandHandler("help", comm.help))
    dp.add_handler(CommandHandler("get_lists", comm.getLists))

    # add conversation command
    dp.add_handler(createList)
    dp.add_handler(deleteList)
    dp.add_handler(emptyList)
    dp.add_handler(addElement)
    dp.add_handler(getElements)
    dp.add_handler(removeElement)

    # log all errors
    dp.add_error_handler(comm.error)

    # Start the Bot
    # updater.start_polling()
    updater.start_webhook(listen=IP,
                          port=PORT,
                          url_path=TOKEN,
                          webhook_url=f'https://list-manager-bot.herokuapp.com/{TOKEN}')

    # Create checker of blocked bot
    x = threading.Thread(target=checkUserBlockTheBot, daemon=True, name="Checker blocked bot",
                         args=(comm.lManager, updater.bot))
    logger.info(f'Start "{x.name}" thread')
    x.start()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
