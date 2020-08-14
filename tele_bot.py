from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ParseMode
import Stock


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Enter $CODE to query the infomation of stock')


def stock(update, context):
    stock = Stock.Create(update.message.text[1:])
    if stock is not None:
        context.bot.send_message(
            chat_id=update.effective_chat.id, text=stock.message(),
            parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)


updater = Updater(token='1167599822:AAGHpgIYWqs37vHfu9aos179TW4wQc7l4qY', use_context=True)
dispatcher = updater.dispatcher

start_handler = CommandHandler('start', start)
stock_handler = MessageHandler(Filters.regex(r'^\$.{0,8}$'), stock)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(stock_handler)
updater.start_polling()
updater.idle()
