from datetime import datetime
from aiosqlite import connect

from config import REFERRAL_BONUS, DB_FILE


async def create_db():
    """
    Create the database tables if they do not exist.
    """
    async with connect(DB_FILE) as db:
        await db.execute('''CREATE TABLE IF NOT EXISTS user_data (
                                    user_id INTEGER PRIMARY KEY,
                                    registration_date TEXT,
                                    balance REAL,
                                    amount_characters INTEGER,
                                    replenished REAL,
                                    withdrawn REAL,
                                    referred_by INTEGER)''')

        await db.execute('''CREATE TABLE IF NOT EXISTS acquired_characters (
                                    user_id INTEGER PRIMARY KEY,
                                    weed INTEGER,
                                    wheat INTEGER,
                                    corn INTEGER,
                                    apple INTEGER,
                                    chicken INTEGER,
                                    pig INTEGER,
                                    turkey INTEGER,
                                    cow INTEGER)''')
        await db.commit()


async def add_user_to_db(user_id: int = 0, registration_date: str = datetime.now().strftime('%d/%m/%Y'),
                         balance: float = 0, amount_characters: int = 0,
                         replenished: float = 0, withdrawn: float = 0,
                         referred_by: int = 0,
                         weed: int = 0, wheat: int = 0,
                         corn: int = 0, apple: int = 0,
                         chicken: int = 0, pig: int = 0,
                         turkey: int = 0, cow: int = 0):
    """
    Add a user's data to the database.
    """
    async with connect(DB_FILE) as db:
        await db.execute('''INSERT INTO user_data (
                         user_id,
                         registration_date,
                         balance,
                         amount_characters,
                         replenished,
                         withdrawn,
                         referred_by)
                         VALUES (?, ?, ?, ?, ?, ?, ?)''',
                         (user_id, registration_date, balance,
                          amount_characters, replenished,
                          withdrawn, referred_by))

        await db.execute('''INSERT INTO acquired_characters (
                         user_id,
                         weed,
                         wheat,
                         corn,
                         apple,
                         chicken,
                         pig,
                         turkey,
                         cow)
                         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                         (user_id, weed,
                          wheat, corn,
                          apple, chicken,
                          pig, turkey, cow))
        await db.commit()


async def add_referral_bonus(user_id: int):
    """
    Add a referral bonus to the user's balance.
    """
    async with connect(DB_FILE) as db:

        await db.execute('UPDATE user_data SET balance = balance + ? WHERE user_id = ?',
                         (REFERRAL_BONUS, user_id))
        await db.commit()


async def upd_referred_by(user_id: int, upd):
    """
    Update the referred_by field in the user's data.
    """
    async with connect(DB_FILE) as db:

        await db.execute('UPDATE user_data SET referred_by = ? WHERE user_id = ?',
                         (upd, user_id))
        await db.commit()


async def get_referred_by(user_id: int):
    """
    Get the user's referral information.
    """
    async with connect(DB_FILE) as db:

        cursor = await db.execute('SELECT referred_by FROM user_data WHERE user_id = ?',
                                  (user_id,))
        result = await cursor.fetchone()

        return result[0]


async def upd_balance(user_id: int, upd):
    """
    Update the user's balance.
    """
    async with connect(DB_FILE) as db:

        await db.execute('UPDATE user_data SET balance = ? WHERE user_id = ?',
                         (upd, user_id))
        await db.commit()


async def upd_amount_characters(user_id: int, upd):
    """
    Update the number of characters owned by the user.
    """
    async with connect(DB_FILE) as db:

        await db.execute('UPDATE user_data SET amount_characters = ? WHERE user_id = ?',
                         (upd, user_id))
        await db.commit()


async def count_users():
    """
    Count the total number of users in the database.
    """
    async with connect(DB_FILE) as db:
        async with db.execute('SELECT COUNT(*) FROM user_data') as cursor:
            result = await cursor.fetchone()

            return result[0]


async def check_user_exists(user_id: int):
    """
    Check if a user exists in the database.
    """
    async with connect(DB_FILE) as db:
        async with db.execute('SELECT 1 FROM user_data WHERE user_id = ?',
                              (user_id,)) as cursor:
            return await cursor.fetchone() is not None


async def get_balance(user_id: int):
    """
    Get the user's balance.
    """
    async with connect(DB_FILE) as db:

        cursor = await db.execute('SELECT balance FROM user_data WHERE user_id = ?',
                                  (user_id,))
        result = await cursor.fetchone()

        return result[0]


async def get_amount_characters(user_id: int):
    """
    Get the number of characters owned by the user.
    """
    async with connect(DB_FILE) as db:

        cursor = await db.execute('SELECT amount_characters FROM user_data WHERE user_id = ?',
                                  (user_id,))
        result = await cursor.fetchone()

        return result[0]


async def get_user_data(user_id: int):
    """
    Get all data associated with a user.
    """
    async with connect(DB_FILE) as db:

        cursor = await db.execute('SELECT * FROM user_data WHERE user_id = ?',
                                  (user_id,))

        return await cursor.fetchone()


async def get_all_characters(user_id: int):
    """
    Get all acquired characters for a user.
    """
    async with connect(DB_FILE) as db:

        cursor = await db.execute('SELECT * FROM acquired_characters WHERE user_id = ?',
                                  (user_id,))

        return await cursor.fetchone()


async def get_amount_acquired_character(user_id: int, name: str):
    """
    Get the count of a specific acquired character for a user.
    """
    async with connect(DB_FILE) as db:
        cursor = await db.execute(f'SELECT {name} FROM acquired_characters WHERE user_id = ?',
                                  (user_id,))
        result = await cursor.fetchone()

        return result[0]


async def upd_acquired_character(user_id: int, name: str, upd):
    """
    Update the acquired character count for the user.
    """
    async with connect(DB_FILE) as db:
        await db.execute(f'UPDATE acquired_characters SET {name} = ? WHERE user_id = ?',
                         (upd, user_id))
        await db.commit()
