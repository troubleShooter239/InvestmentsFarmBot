# Bot Token (your value)
BOT_TOKEN = '' 

# Database Name
DB_FILE = 'project.db'

# Links
SUPPORT_LINK = "https://t.me/"
WITHDRAW_LINK = "https://t.me/"
CHAT_LINK = "https://t.me/"
REFERRAL_LINK = "https://t.me/bot?start="

# Referral Bonus
REFERRAL_BONUS = 0.25

# Store Catalog
WEED_PRICE = 25
WEED_SPEED = 0.25

WHEAT_PRICE = 100
WHEAT_SPEED = 1

CORN_PRICE = 200
CORN_SPEED = 5

APPLE_PRICE = 400
APPLE_SPEED = 10

CHICKEN_PRICE = 800
CHICKEN_SPEED = 20

PIG_PRICE = 1600
PIG_SPEED = 40

TURKEY_PRICE = 3500
TURKEY_SPEED = 80

COW_PRICE = 5000
COW_SPEED = 100

SPEED_MULTIPLIERS = (
        0,
        WEED_SPEED,
        WHEAT_SPEED,
        CORN_SPEED,
        APPLE_SPEED,
        CHICKEN_SPEED,
        PIG_SPEED,
        TURKEY_SPEED,
        COW_SPEED
)

PRODUCTS = {
        'weed': ('weed', '🌿', 'weed.jpg', WEED_SPEED, WEED_PRICE),
        'wheat': ('wheat', '🌾', 'wheat.jpg', WHEAT_SPEED, WHEAT_PRICE),
        'corn': ('corn', '🌽', 'corn.jpg', CORN_SPEED, CORN_PRICE),
        'apple': ('apple tree', '🍎', 'apple.jpg', APPLE_SPEED, APPLE_PRICE),
        'chicken': ('chicken', '🐓', 'chicken.jpg', CHICKEN_SPEED, CHICKEN_PRICE),
        'pig': ('piglet', '🐷', 'pig.jpg', PIG_SPEED, PIG_PRICE),
        'turkey': ('turkey', '🦃', 'turkey.jpg', TURKEY_SPEED, TURKEY_PRICE),
        'cow': ('calf', '🐮', 'cow.jpg', COW_SPEED, COW_PRICE),
}
