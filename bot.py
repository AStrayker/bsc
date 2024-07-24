import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext

# Вставьте свой токен здесь
TELEGRAM_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def start(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("авто транспортировка", callback_data='transport_auto')],
        [InlineKeyboardButton("транспортировка вагонами", callback_data='transport_train')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Выберите способ транспортировки:', reply_markup=reply_markup)

def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    choice = query.data

    if choice.startswith('transport_'):
        context.user_data['transport'] = choice.split('_')[1]
        keyboard = [
            [InlineKeyboardButton("Песок", callback_data='cargo_sand')],
            [InlineKeyboardButton("Цемент М400", callback_data='cargo_cement400')],
            [InlineKeyboardButton("Цемент М500", callback_data='cargo_cement500')],
            [InlineKeyboardButton("Щебень 5x20", callback_data='cargo_gravel5x20')],
            [InlineKeyboardButton("Щебень 10x20", callback_data='cargo_gravel10x20')],
            [InlineKeyboardButton("Щебень 20x40", callback_data='cargo_gravel20x40')],
            [InlineKeyboardButton("Щебень 5x70", callback_data='cargo_gravel5x70')],
            [InlineKeyboardButton("Металлопрокат", callback_data='cargo_metal')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text(text="Выберите груз:", reply_markup=reply_markup)

    elif choice.startswith('cargo_'):
        context.user_data['cargo'] = choice.split('_')[1]
        if choice == 'cargo_metal':
            keyboard = [
                [InlineKeyboardButton("Отправитель А", callback_data='sender_a')],
                [InlineKeyboardButton("Отправитель Б", callback_data='sender_b')],
                [InlineKeyboardButton("Отправитель В", callback_data='sender_c')]
            ]
        else:
            keyboard = [
                [InlineKeyboardButton("Отправитель 1", callback_data='sender_1')],
                [InlineKeyboardButton("Отправитель 2", callback_data='sender_2')],
                [InlineKeyboardButton("Отправитель 3", callback_data='sender_3')]
            ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text(text="Выберите отправителя:", reply_markup=reply_markup)

    elif choice.startswith('sender_'):
        context.user_data['sender'] = choice.split('_')[1]
        keyboard = [
            [InlineKeyboardButton("1", callback_data='quantity_1')],
            [InlineKeyboardButton("2", callback_data='quantity_2')],
            [InlineKeyboardButton("3", callback_data='quantity_3')],
            [InlineKeyboardButton("4", callback_data='quantity_4')],
            [InlineKeyboardButton("5", callback_data='quantity_5')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text(text="Выберите количество:", reply_markup=reply_markup)

    elif choice.startswith('quantity_'):
        context.user_data['quantity'] = choice.split('_')[1]
        if context.user_data['transport'] == 'train':
            keyboard = [
                [InlineKeyboardButton("Нет уточнения", callback_data='status_none')],
                [InlineKeyboardButton("Не разгружено", callback_data='status_not_unloaded')],
                [InlineKeyboardButton("Разгружено", callback_data='status_unloaded')],
                [InlineKeyboardButton("Частично разгружено", callback_data='status_partial_unloaded')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.edit_message_text(text="Выберите статус разгрузки:", reply_markup=reply_markup)
        else:
            summary(update, context)

    elif choice.startswith('status_'):
        context.user_data['status'] = choice.split('_')[1]
        summary(update, context)

def summary(update: Update, context: CallbackContext) -> None:
    transport = context.user_data['transport']
    cargo = context.user_data['cargo']
    sender = context.user_data['sender']
    quantity = context.user_data['quantity']
    status = context.user_data.get('status', 'N/A')

    message = (
        f"Доставка: {'машинами' if transport == 'auto' else 'вагонами'}\n"
        f"Груз: {cargo}\n"
        f"Отправитель: {sender}\n"
        f"Количество: {quantity} {'машин' if transport == 'auto' else 'вагонов'}\n"
    )
    if transport == 'train':
        message += f"Статус разгрузки: {status}"

    update.callback_query.edit_message_text(text=message)

def main() -> None:
    updater = Updater(TELEGRAM_TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CallbackQueryHandler(button))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
