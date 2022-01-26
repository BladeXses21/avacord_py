# Токен бота
GLUON = 'NjA2OTI3Mjc0NTkxMzg3NjU4.XUSLqA.7yeVvuU3E_sdsUfSa18ANoQN464'

# ID сервера
GUILD_ID = 606930523964833823

OWNER_ROLE = 607562200433033236

# Префикс бота
PREFIX = '!'

EVENT_START_ROOM_ID = 607574682484342796
PRIVATE_START_ROOM_ID = 607557949937680403

LOVE_ROOM_CATEGORY = 601121015296425994
BOT_PANEL_CHANNEL = 601121046984130569

ADMIN_ROLE = 607563386833600522
MODERATOR_ROLE = 607563987584024636
HELPER_ROLE = 601120957418962954
EVENTER_ROLE = 607564018709692417
MENTOR_ROLE = ADMIN_ROLE
EVENTMEMBER_ROLE = 608412852696645652
GUEST_ROLE = 607228525715652639
GUEST_CHANNEL = 607278928402579456

EMOTIONS_COST = 20

CLANS = {
    'CLANS_CATEGORY': 607559096559992852,
    'CLAN_CHAT_CATEGORY': 607561441909800963,
    'CLAN_LEADER_ROLE': 608451525899059282,
    'CLAN_AVATAR_CHANGE': 2000,
    'CLAN_CREATE_COST': 15000, # stars
    'TEXT_CHANNEL_COST': 5000,
    'CHANGE_NAME_COST': 5000,
    'ROLE_CHANGE_COST': 1000,
    'CLAN_5_SLOTS_COST': 1500,
    'CLAN_POINTS_COEFICIENT': 10
}

# roles.py
# Использование
# <ID роли>: [<'комагда1'>, <'комагда2'>, ...]
ROLES = {
    'ROLES': {
        # 601120975844671508: ['creator', 'творчество'],
        # 601120975626567690: ['horoscope', 'гороскоп'],
        # 601120975031107590: ['nsfw', 'нсфв'],
        # 601120973378551808: ['quote', 'цитата'],
        # 601120976922476544: ['memes', 'мемы'],
        # 605261110521626636: ['filmfan', 'киноман']
    },
    'MODERATION_ROLE': [OWNER_ROLE, ADMIN_ROLE, MODERATOR_ROLE],
    'MODERATION_ROLES': {
        # 608432869639192607: ['chat', 'чат'],
        # 608432801146077354: ['night', 'ночь'],
        # 601120964654268427: ['voice', 'войс'],
        # 608432707399057448: ['lamp', 'лампа'],
        # 601120977413210153: ['dj', 'диджей'],
        # 608432509994139687: ['artist', 'артист'],
        # 608432643926917134: ['rules', 'правила'],
    },
    'EVENTER_ROLE': [EVENTER_ROLE],
    'EVENTER_ROLES': {
        608441463532945439: ['mafia', 'мафия'],
        608450163559890944: ['hat', 'шляпа'],
        608450292022902786: ['monopoly', 'монополия'],
        608440519026147366: ['sigame', 'свояк'],
        608450412269404173: ['excitement', 'азарт'],
        608441878307930122: ['talents', 'талант'],
        608450626690744330: ['crocodile', 'крокодил'],
        608450515545751592: ['codenames', 'коднеймс']
    },
    'GLOVE': 608450944992280576
}

# statuses.py
STATUSES = {
    'VIP_ROLE': 607564706286272522,
}

# admin.py
ADMIN = {
    # ID ролей для мута
    'MUTE_ROLES': [OWNER_ROLE, ADMIN_ROLE, MODERATOR_ROLE, HELPER_ROLE],
    # ID ролей для варна
    'WARN_ROLES': [OWNER_ROLE, ADMIN_ROLE, MODERATOR_ROLE, HELPER_ROLE],
    # ID ролей для инвалида
    'INVALID_ROLES': [OWNER_ROLE, ADMIN_ROLE, MODERATOR_ROLE, HELPER_ROLE],

    'BAN_ROLES': [OWNER_ROLE, ADMIN_ROLE],

    'REPORT_ACCEPT_ROLE': [OWNER_ROLE, ADMIN_ROLE, MODERATOR_ROLE, HELPER_ROLE],

    # ID ролей для размута
    'UNMUTE_ROLES': [OWNER_ROLE, ADMIN_ROLE],
    # ID ролей для снятьинвал
    'UNINVAL_ROLES': [OWNER_ROLE, ADMIN_ROLE],
    # ID ролей для снятьварн
    'UNWARN_ROLES': [OWNER_ROLE, ADMIN_ROLE],

    # ID канала мутов
    'MUTE_CHANNEL': 610976130647982089,
    # ID канала для варнов
    'WARN_CHANNEL': 611530392469504000,
    # ID
    'REPORT_CHANNEL': 611530277260492800,

    'INVALID_CHANNEL': 611530277260492800,

    # ID роли мута
    'MUTE_ROLE': 610450800509976587,
    # ID роли варнов: 1 предупреждение
    'WARN_ROLE': 610450837327577100,
    # ID роли инвалида
    'INVALID_ROLE': 610450964318650378
}

# money.py
# Стартовая валюта
START_MONEY = {
    'silver': 500,
    'energy': 100
}

# mini_games.py
MINI_GAMES = {
    'EVENTER_ROLE': EVENTER_ROLE,
    'EVENTS_REWARD_CHANNEL_ID': 615908768177192961,
    'MENTOR_ROLE_ID': MENTOR_ROLE,
    'EVENTBAN_CHANNEL': 610976081717100574,
    'EVENTBAN_ROLE': 610482122104242197
}

# owners.py
OWNERS = {
    'OWNER_ROLE': OWNER_ROLE,
    'WARN_ROLE': ADMIN['WARN_ROLE'],
}

# economy.py
ECONOMY = {
    'EVERYDAY_BONUS': 200,

    # налог в %
    'TAX': 5
}

DONATE_SHOP = [
    399, 150, 299, 100, 199, 75, 199, 99, 199, 99
]

SHOP = {
    'ROLES': {
        613398396035792910: {'silver': 32000},
        613400788928167946: {'silver': 28600},
        613401290822778981: {'silver': 27000},
        613399250193350673: {'silver': 25000},
        613398766736900141: {'silver': 19867},
        613400217093537813: {'silver': 17889},
        613399799898832929: {'silver': 16798},
        613395840584908800: {'silver': 14000},
        613519255719378945: {'silver': 12000},
        613395593414574082: {'silver': 9500},
        613394705190879235: {'silver': 6247}
    }
}
