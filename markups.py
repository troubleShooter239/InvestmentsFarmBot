from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup

from config import PRODUCTS
from buttons import BotButtons as bb


class BotMarkups:
    # Start Markup with reply keyboard buttons
    markup_start = (
        ReplyKeyboardMarkup(resize_keyboard=True).add(*bb.get_reply_buttons()))
    # Markup for shop and heroes options
    markup_shop_heroes = (
        InlineKeyboardMarkup().add(bb.btn_shop, bb.btn_heroes))
    # Markup for buying a product with a back button
    markup_buy_product = (
        InlineKeyboardMarkup().add(bb.btn_buy, bb.btn_back_shop))
    # Markup with a back button for the shop
    markup_back_shop = InlineKeyboardMarkup().add(bb.btn_back_shop)
    # Markup with a back button for shop and heroes
    markup_back_shop_heroes = InlineKeyboardMarkup().add(bb.btn_back)
    # Markup for the personal account with a top-up button
    markup_personal_account = InlineKeyboardMarkup().add(bb.btn_top_up)
    # Markup for the personal account with admin and back buttons
    markup_personal_account_back = (
        InlineKeyboardMarkup().add(bb.btn_admin, bb.btn_back_personal_account))
    # Admin Markup
    markup_admin = InlineKeyboardMarkup().add(bb.btn_admin)
    # Withdraw Markup
    markup_withdraw = InlineKeyboardMarkup().add(bb.btn_withdraw)
    # Markup for about bot with admin and chat buttons
    markup_about_bot = (
        InlineKeyboardMarkup().add(bb.btn_admin, bb.btn_chat))

    @staticmethod
    async def create_shop_markup() -> InlineKeyboardMarkup:
        """
        Create a dynamic shop markup based on available products.

        Returns:
            InlineKeyboardMarkup: A markup with product buttons.
        """
        button_rows = []
        current_row = []

        for key, value in PRODUCTS.items():
            current_row.append(InlineKeyboardButton(text=value[1],
                                                    callback_data=f'btn_{key}'))

            if len(current_row) == 3:
                button_rows.append(current_row)
                current_row = []

        if current_row:
            button_rows.append(current_row)

        return InlineKeyboardMarkup(inline_keyboard=button_rows)
