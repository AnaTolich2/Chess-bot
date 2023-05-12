#from envir import TOKEN
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from telegram.ext import ConversationHandler, filters

from telegram.ext import Updater, MessageHandler

TOKEN = '5889445140:AAG7yKvNoL0SZJE3Z-Eo71pHriGjotS7MgQ'
import io
from chess_bot import Game
from rules import rule

base_keyboard = [['Выход', 'Сыграть сначала']]
alpha_keyboard = [['Начать игру',"Помощь и правила",'Выход']]
close_keyboard = [['Сыграть снова', 'Выход']]
base_markup = ReplyKeyboardMarkup(base_keyboard, one_time_keyboard=True)
alpha_markup = ReplyKeyboardMarkup(alpha_keyboard, one_time_keyboard=True)
close_markup = ReplyKeyboardMarkup(close_keyboard, one_time_keyboard=True)

game = Game()
async def start(update, context):
    text = '''Привет, сыграем в шахматы?'''
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=text)
    await update.message.reply_text('Выбирай:', reply_markup=alpha_markup)
    return 1

#async def difficulty(update, context):
    #await update.message.reply_text('Введите сложность от 1 до 10')
    #game.diff = update.message.text
    #lkl = game.set_diff(game.diff)
    #if lkl :
        #await context.bot.send_message(chat_id=update.effective_chat.id,text="Сложность: "+
                                        #game.diff)
        #return 1
    #else:
        #await context.bot.send_message(chat_id=update.effective_chat.id,text="Ошибка ввода")
        #return 1

async def the_begining(update, context):   
    im = game.showBoard(game.desk)
    im_resize = im.resize((410, 426))
    buf = io.BytesIO()
    im_resize.save(buf, format='JPEG')
    byte_im = buf.getvalue()
    await context.bot.send_photo(chat_id=update.effective_chat.id,
                           photo=byte_im)
    await update.message.reply_text('Вы играете белыми')
    await update.message.reply_text('Ваш ход:',reply_markup=base_markup)
    return 2

async def help(update, context):   
    await update.message.reply_text(text=rule,reply_markup=alpha_markup)
    return 1

async def get_move(update, context):
    game.end_of_game(game.board,game.end,game.reason)
    if game.end :
        await context.bot.send_message(chat_id=update.effective_chat.id,text=game.reason, reply_markup=close_markup)
        return 3  
    else:
        hod = update.message.text
        f = game.is_valid_move(hod, game.board, game.desk, game.ch, game.commands)
        if f :
            game.make_move(hod, game.board, game.desk, game.engine)
            im = game.showBoard(game.desk)
            im_resize = im.resize((410, 426))
            buf = io.BytesIO()
            im_resize.save(buf, format='JPEG')
            byte_im = buf.getvalue()
            await context.bot.send_photo(chat_id=update.effective_chat.id,
                                         photo=byte_im)
            await update.message.reply_text('Ваш ход:')
            return 2
        else:
            await update.message.reply_text('Невозможный ход')
            await context.bot.send_message(chat_id=update.effective_chat.id,text=
                                        game.ch)
            await update.message.reply_text("Ваш ход:")
            return 2 

async def stop(update, context):
    await update.message.reply_text('Пока!',
                              reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


def main():
    application = ApplicationBuilder().token(TOKEN).build()
    conv_handler = ConversationHandler(

        entry_points=[CommandHandler('start', start)],

        states={
            1: [MessageHandler(filters.Text('Начать игру'), the_begining),
                MessageHandler(filters.Text(['Выход']), stop),
                #MessageHandler(filters.Text(['Сменить сложность']), difficulty),
                MessageHandler(filters.Text(['Помощь и правила']), help),
                ],
            2: [MessageHandler(filters.Text(['Выход']), stop),
                MessageHandler(filters.Text(['Сыграть сначала']), the_begining),
                MessageHandler(filters.Text(), get_move),
                ],
            
            3: [MessageHandler(filters.Text(['Выход']), stop),
                MessageHandler(filters.Text(['Сыграть снова']), the_begining)]
        },

        fallbacks=[CommandHandler('stop', stop)]
    )
    application.add_handler(conv_handler)
    application.add_handler(CommandHandler("start", start))
    # application.add_handler(CommandHandler("help", help))
    application.add_handler(CommandHandler("stop", stop))

    application.run_polling()


if __name__ == '__main__':
    main()
