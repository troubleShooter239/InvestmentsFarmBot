from markups import BotMarkups as bm
from config import CHAT_LINK, SPEED_MULTIPLIERS, REFERRAL_LINK
from db_func import count_users, get_all_characters, get_balance, upd_balance, get_user_data

from asyncio import create_task


async def button_handlers(msg_text, reply_button):
    """
    Determine the action to take based on the user's button press.

    Args:
        msg_text (str): The text from the user's button press.
        reply_button (list): List of reply buttons.

    Returns:
        function: The handler function for the button press.
    """
    handlers = {
        reply_button[0].text:
            lambda msg: msg.answer('Choose where to go:',
                                   reply_markup=bm.markup_shop_heroes),
        reply_button[1].text:
            lambda msg: msg.answer('🎲 Games are disabled!'),
        reply_button[2].text:
            lambda msg: create_task(withdraw_handler(msg)),
        reply_button[3].text:
            lambda msg: personal_account_handler(msg),
        reply_button[4].text:
            lambda msg: create_task(referrals_handler(msg)),
        reply_button[5].text:
            lambda msg: create_task(about_bot_handler(msg)),
    }

    return handlers.get(msg_text)


async def withdraw_handler(msg):
    """
    Handle the withdrawal process for the user.

    Args:
        msg (types.Message): The message from the user.
    """
    text = await withdraw_text(msg.from_user.id)
    await msg.answer(text=text, reply_markup=bm.markup_withdraw)


async def referrals_handler(msg):
    """
    Handle the referrals functionality and provide information to the user.

    Args:
        msg (types.Message): The message from the user.
    """
    text = await referrals_text(msg.from_user.id)
    await msg.answer(text=text)


async def about_bot_handler(msg):
    """
    Provide information about the bot to the user.

    Args:
        msg (types.Message): The message from the user.
    """
    text = await about_bot()
    await msg.answer(text=text, reply_markup=bm.markup_about_bot)


async def personal_account_handler(msg):
    """
    Handle the user's personal account and provide relevant information.

    Args:
        msg (types.Message): The message from the user.
    """
    photo = open('./photos/house.png', 'rb')
    user_data = await get_user_data(msg.from_user.id)
    await msg.answer_photo(photo=photo,
                           caption=await personal_account_text(msg.from_user.first_name, user_data),
                           reply_markup=bm.markup_personal_account)


async def start_text(first_name: str) -> str:
    """
    Generate the welcome message for new users.

    Args:
        first_name (str): The user's first name.

    Returns:
        str: The welcome message.
    """
    return f'Welcome, {first_name}!\n' \
           f'This is the best long-term bot with per-second accruals.\n' \
           f'🏝 Chat link: {CHAT_LINK}'


async def withdraw_text(user_id) -> str:
    """
    Generate the withdrawal instructions and information for users.

    Args:
        user_id: The user's ID.

    Returns:
        str: The withdrawal information.
    """
    return f'Here you can withdraw your earnings to your card\n\n' \
           f'Minimum withdrawal amount: 50₽\n\n' \
           f'Your current balance: {await get_balance(user_id)}₽\n\n' \
           f'❗️To withdraw funds, please send a message from the bot ' \
           f'to the administrator and specify the exact withdrawal amount. ' \
           f'Enjoy your investments!❗️\n\n' \
           f'Expect payment within 24 hours!'


async def personal_account_text(first_name: str, user_data) -> str:
    """
    Generate the personal account information for users.

    Args:
        first_name (str): The user's first name.
        user_data: User data from the database.

    Returns:
        str: The personal account information.
    """
    return f'🟢 Simply top up your balance to buy heroes for any amount, and ' \
           f'every hour you will receive a percentage of the heroes\' profits on your balance.\n\n' \
           f'🟢 You can also withdraw your earnings - DAILY\n\n' \
           f'🟢 The more heroes you can buy, the BIGGER your daily earnings\n\n' \
           f'🟢 Investment term - lifetime\n\n' \
           f'📝 Name: {first_name}\n' \
           f'🔐 Registration Date: {user_data[1]}\n\n' \
           f'💵 Balance: {round(user_data[2], 2)}₽\n\n' \
           f'📊 Characters: {user_data[3]}\n\n' \
           f'💸 Replenished: {round(user_data[4], 2)}₽\n' \
           f'🤑 Withdrawn: {round(user_data[5], 2)}₽'


async def referrals_text(user_id: int) -> str:
    """
    Generate information about the referral program for users.

    Args:
        user_id (int): The user's ID.

    Returns:
        str: Information about the referral program.
    """
    return f'🤝 Referral Program:\n' \
           f'🔑 You get:\n' \
           f'▫️ 0.25₽ for each invited partner\n' \
           f'▫️ 10% of your partners\' top-ups:\n\n' \
           f'🔗 Your referral link: {REFERRAL_LINK + str(user_id)}'


async def about_bot() -> str:
    """
    Return information about bot

    Returns:
        str: About bot info.
    """
    number_users = await count_users()
    amount = number_users if number_users else 0

    return f'📊 Project Statistics:\n\n' \
           f'👨‍💻 Users in the game: {amount}\n' \
           f'🕐 The bot started on 01/08/2023\n\n' \
           f'Start earning with the farm right now 👩‍🌾'


async def refresh_balance(user_id):
    """
    Refresh the user's balance based on the acquired characters.

    Args:
        user_id: The user's ID.
    """
    characters = await get_all_characters(user_id)
    balance = await get_balance(user_id)

    for character_id, character_count in enumerate(characters[1:], start=1):
        if character_count:
            balance += character_count * SPEED_MULTIPLIERS[character_id]

    await upd_balance(user_id, balance)
