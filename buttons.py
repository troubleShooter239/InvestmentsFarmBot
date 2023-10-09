from aiogram.types import KeyboardButton, InlineKeyboardButton

from config import SUPPORT_LINK, CHAT_LINK, WITHDRAW_LINK


class BotButtons:
    # Keyboard Buttons
    KB_INVESTMENTS = KeyboardButton('📊 Investments')
    KB_ARENA = KeyboardButton('🏟 Arena')
    KB_WITHDRAW = KeyboardButton('💸 Withdraw')
    KB_PERSONAL_ACCOUNT = KeyboardButton('🖥 Personal Account')
    KB_REFERRALS = KeyboardButton('👥 Referrals')
    KB_ABOUT_BOT = KeyboardButton('📚 About Bot')
    # Inline Keyboard Buttons
    btn_red = InlineKeyboardButton(text='🔴',
                                   callback_data='btn_red')

    btn_back = InlineKeyboardButton(text='◀️ Back',
                                    callback_data='btn_back')
    btn_back_shop = InlineKeyboardButton(text='◀️ Back',
                                         callback_data='btn_weed')
    btn_buy = InlineKeyboardButton(text='🛒Buy',
                                   callback_data='btn_buy_weed')

    btn_shop = InlineKeyboardButton(text='Shop',
                                    callback_data="btn_weed")
    btn_heroes = InlineKeyboardButton(text='My Heroes',
                                      callback_data="btn_heroes")

    btn_top_up = InlineKeyboardButton(text="💳 Top Up",
                                      callback_data='btn_top_up')
    btn_back_personal_account = InlineKeyboardButton(text='◀️ Back',
                                                     callback_data='btn_back_personal_account')

    btn_admin = InlineKeyboardButton(text='Administrator',
                                     url=SUPPORT_LINK)
    btn_withdraw = InlineKeyboardButton(text='Administrator',
                                        url=WITHDRAW_LINK)
    btn_chat = InlineKeyboardButton(text='Chat',
                                    url=CHAT_LINK)

    @staticmethod
    def get_reply_buttons() -> tuple:
        """
        Get the list of reply keyboard buttons.

        Returns:
            tuple: A tuple of keyboard buttons.
        """
        return (
            BotButtons.KB_INVESTMENTS,
            BotButtons.KB_ARENA,
            BotButtons.KB_WITHDRAW,
            BotButtons.KB_PERSONAL_ACCOUNT,
            BotButtons.KB_REFERRALS,
            BotButtons.KB_ABOUT_BOT
        )
