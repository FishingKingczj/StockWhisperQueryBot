from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import telegram
from stock import Stock
import sys
import traceback
import datetime
import time
BOT_UPDATING = False


def clear(update, context):
    return


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Enter $CODE to query the infomation of stock')


def stock(update, context):
    if BOT_UPDATING:
        context.bot.send_message(chat_id=update.effective_chat.id, text='Bot Updating, Please Wait...')

    stock = Stock.Create(update.message.text[1:])
    if stock is not None:
        context.bot.send_message(
            chat_id=update.effective_chat.id, text=stock.stockInfo(),
            parse_mode=telegram.ParseMode.HTML, disable_web_page_preview=True)
        if stock.state == 0:
            news = stock.stockNews()
            if len(news > 0):
                context.bot.send_message(
                    chat_id=update.effective_chat.id, text=news,
                    parse_mode=telegram.ParseMode.HTML, disable_web_page_preview=True)

            context.bot.send_photo(chat_id=update.effective_chat.id, photo=stock.pic_url)


def err(update, context):
    print('Error happened Time: {}, Message: {}'.format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), update.message.text))
    traceback.print_exc(file=sys.stdout)
    context.bot.send_message(chat_id=update.effective_chat.id, text='Oops, some error happened. Please contact the bot manager to fix it.')


updater = Updater(token='1167599822:AAGHpgIYWqs37vHfu9aos179TW4wQc7l4qY', use_context=True)
print('clear history message...')
dispatcher = updater.dispatcher
clear_handler = MessageHandler(Filters.all, clear)
dispatcher.add_handler(clear_handler)
updater.start_polling()
time.sleep(10)
dispatcher.remove_handler(clear_handler)
updater.stop()
print('clear finish, reboot...')

start_handler = CommandHandler('start', start)
stock_handler = MessageHandler(Filters.regex(r'^\$.{0,8}$'), stock)
dispatcher.add_error_handler(err)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(stock_handler)
print('start bot...')
updater.start_polling()
updater.idle()
