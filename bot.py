from asyncio import run
from os.path import isfile

from aiogram import Bot, types, Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from bot_func import start_text, personal_account_text, refresh_balance, button_handlers
from config import PRODUCTS, BOT_TOKEN, DB_FILE
from buttons import BotButtons as bb
from markups import BotMarkups as bm
import db_func


async def main():
    """
    Main function of the bot. Creates a database, initializes the bot and dispatcher,
    and sets up message and event handlers.
    """
    if not BOT_TOKEN:
        print("You did not enter the bot token!")
        return
    # Create a database if it doesn't exist
    if not isfile(DB_FILE):
        await db_func.create_db()

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(bot=bot)
    scheduler = AsyncIOScheduler()

    @dp.message_handler(commands=['start'])
    async def start(msg: types.Message):
        """
        Command handler for /start. Initiates interaction with the bot and processes referral links.
        """
        user_id = msg.from_user.id

        try:  # Add a user to the database
            if not await db_func.check_user_exists(user_id):
                await db_func.add_user_to_db(user_id)

                if " " in msg.text:  # If there is additional text after /start
                    referrer_candidate = int(msg.text.split()[1])

                    if user_id != referrer_candidate and db_func.check_user_exists(referrer_candidate):
                        await db_func.add_referral_bonus(referrer_candidate)
                        await db_func.upd_referred_by(user_id, referrer_candidate)

                        await bot.send_message(chat_id=user_id,
                                               text='🥳 You have successfully followed a referral link!')
                    else:
                        await bot.send_message(chat_id=user_id,
                                               text='😔 User with this ID was not found!')
        except ValueError:
            pass

        await msg.answer(text=await start_text(msg.from_user.first_name),
                         reply_markup=bm.markup_start)
        # Waiting for the function to complete
        scheduler.add_job(refresh_balance, 'interval', hours=1, args=[user_id])
        scheduler.start()

    @dp.message_handler(commands=['balance'])
    async def add_balance(msg: types.Message):
        """
        Adds balance to the user.
        /balance user_id balance
        """
        if (msg.from_user.username == 'admin_username'):
            if " " in msg.text:
                text = msg.text.split()
                user_id = int(text[1])
                balance = int(text[2])
                await db_func.upd_balance(user_id=user_id, upd=balance)

                referred_by = await db_func.get_referred_by(user_id=user_id)

                if referred_by:
                    await db_func.upd_balance(user_id=referred_by, upd=balance * 0.1)

    @dp.message_handler(content_types=['text'])
    async def menu(msg: types.Message):
        """
        Bot menu.
        """
        handler = await button_handlers(msg.text, bb.get_reply_buttons())

        if handler:
            await handler(msg)

    @dp.callback_query_handler(lambda c: c.data.startswith('btn'))
    async def process_button_click(query: types.CallbackQuery):
        """
        Handler for user button clicks.
        """
        user_id = query.from_user.id
        btn_pressed = query.data[4:]
        await bot.answer_callback_query(query.id)

        if not btn_pressed == 'red':  # Delete previous bot messages
            await bot.delete_message(query.message.chat.id, query.message.message_id)

        if btn_pressed in PRODUCTS:
            markup_product = (await bm.create_shop_markup()).add(bb.btn_back)

            product_name, sticker, photo_filename, product_speed, product_price = PRODUCTS[btn_pressed]

            photo = open(f'./photos/{photo_filename}', 'rb')
            caption = (f"{sticker + product_name.capitalize()}\n"
                       f"Speed: {product_speed}$/hour\n"
                       f"Price: {product_price}$")

            bb.btn_red.callback_data = f'btn_red_{btn_pressed}'

            row, col = divmod(list(PRODUCTS.keys()).index(btn_pressed), 3)
            markup_product.inline_keyboard[row][col] = bb.btn_red

            await bot.send_photo(user_id,
                                 photo=photo,
                                 caption=caption,
                                 reply_markup=markup_product)

        elif btn_pressed.startswith('red_'):
            product_name = btn_pressed[4:]

            sticker = PRODUCTS[product_name][1]
            caption = f"Buy {sticker + PRODUCTS[product_name][0].capitalize()}?"
            photo = open(f'./photos/{product_name}.jpg', 'rb')

            bb.btn_buy.callback_data = f'btn_buy_{product_name}'

            await bot.send_photo(user_id,
                                 photo=photo,
                                 caption=caption,
                                 reply_markup=bm.markup_buy_product)

        elif btn_pressed.startswith('buy_'):
            product_name = btn_pressed[4:]
            balance = await db_func.get_balance(user_id)

            if balance >= PRODUCTS[product_name][4]:
                await db_func.upd_balance(user_id, balance - PRODUCTS[product_name][4])
                amount_characters = await db_func.get_amount_characters(user_id)
                await db_func.upd_amount_characters(user_id, amount_characters + 1)
                acquired_character = await db_func.get_amount_acquired_character(user_id, product_name)
                await db_func.upd_acquired_character(user_id, product_name, acquired_character + 1)

                await bot.send_message(user_id,
                                       text='🥳 Product purchased!',
                                       reply_markup=bm.markup_back_shop)
            else:
                await bot.send_message(user_id,
                                       text='😔 Insufficient funds!',
                                       reply_markup=bm.markup_back_shop)

        elif btn_pressed == 'heroes':
            amount_characters = await db_func.get_amount_characters(user_id)

            if amount_characters:
                await db_func.get_all_characters(user_id)
                await bot.send_message(user_id,
                                       text=f"Number of acquired characters: {amount_characters}",
                                       reply_markup=bm.markup_back_shop_heroes)
            else:
                await bot.send_message(user_id,
                                       text="You have no acquired characters!",
                                       reply_markup=bm.markup_back_shop_heroes)

        elif btn_pressed == 'top_up':
            await bot.send_message(user_id,
                                   text='To top up your balance, please contact the administration '
                                        'and specify the exact amount to top up.',
                                   reply_markup=bm.markup_personal_account_back)

        elif btn_pressed == 'back':
            await bot.send_message(user_id,
                                   text='Choose where to go:',
                                   reply_markup=bm.markup_shop_heroes)

        elif btn_pressed == 'back_personal_account':
            photo = open('./photos/house.png', 'rb')
            user_data = await db_func.get_user_data(user_id)

            await bot.send_photo(user_id,
                                 photo=photo,
                                 caption=await personal_account_text(query.from_user.first_name, user_data),
                                 reply_markup=bm.markup_personal_account)
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    run(main())
