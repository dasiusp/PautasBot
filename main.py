#  Copyright 2020 DASIUSP
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
# documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of
# the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
# THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import database
from telegram import Update, Bot
from telegram.ext import Dispatcher, CommandHandler


def start_callback(bot, update, args):
    if database.has_agenda(update.message.chat_id):
        update.message.reply_text("Este chat já possui uma pauta!", quote=False)
        list_callback(bot, update, args)
    else:
        update.message.reply_text("Certo, vamos começar! Digite /add [\"Item Da Pauta Aqui\"] para adicionar um novo item!!", quote=False)
        database.initialize_agenda(update.message.chat_id)


def add_callback(bot, update, args):
    if not database.has_agenda(update.message.chat_id):
        update.message.reply_text("Opa, você se esqueceu de iniciar uma nova pauta! Use /start para fazer isso.", quote=False)
    else:
        text = ' '.join(args)
        database.add_to_agenda(update.message.chat_id, text)
        update.message.reply_text("Ótimo! Vou guardar isso.", quote=False)
        list_callback(bot, update, args)


def remove_callback(bot, update, args):
    if not database.has_agenda(update.message.chat_id):
        update.message.reply_text("Opa, você se esqueceu de iniciar uma nova pauta! Use /start para fazer isso.", quote=False)
    else:
        text = ' '.join(args)
        if not database.has_item(update.message.chat_id, text):
            update.message.reply_text("Acho que esse item de pauta não está aqui!", quote=False)
            list_callback(bot, update, args)
        else:
            database.remove_from_agenda(update.message.chat_id, text)
            update.message.reply_text("Beleza, removendo o item!", quote=False)
            list_callback(bot, update, args)


def finish_callback(bot, update, args):
    if not database.has_agenda(update.message.chat_id):
        update.message.reply_text("Opa, você se esqueceu de iniciar uma nova pauta! Use /start para fazer isso.", quote=False)
    else:
        update.message.reply_text("Certo, finalizando!", quote=False)
        list_callback(bot, update, args)
        database.finalize_agenda(update.message.chat_id)


def list_callback(bot, update, args):
    curr_agenda = database.current_agenda(update.message.chat_id)
    text = "A pauta atual é:\n"
    agenda = ["-" + item for item in curr_agenda]
    if not curr_agenda:
        text = text + "Vazia!"
    else:
        text = text + '\n'.join(agenda)
    update.message.reply_text(text, quote=False)


def webhook(request):
    bot = Bot(token=os.environ["TELEGRAM_TOKEN"])
    dispatcher = Dispatcher(bot, None, 0)
    dispatcher.add_handler(CommandHandler("start", start_callback, pass_args=True))
    dispatcher.add_handler(CommandHandler("add", add_callback, pass_args=True))
    dispatcher.add_handler(CommandHandler("remove", remove_callback, pass_args=True))
    dispatcher.add_handler(CommandHandler("finish", finish_callback, pass_args=True))
    dispatcher.add_handler(CommandHandler("list", list_callback, pass_args=True))

    if request.method == "POST":
        update = Update.de_json(request.get_json(force=True), bot)
        dispatcher.process_update(update)
    return "ok"