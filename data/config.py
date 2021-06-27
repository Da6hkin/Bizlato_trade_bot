from environs import Env

# Теперь используем вместо библиотеки python-dotenv библиотеку environs
env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")  # Забираем значение типа str
ADMINS = env.list("ADMINS")  # Тут у нас будет список из админов
IP = env.str("ip")  # Тоже str, но для айпи адреса хоста

DB_USER = env.str("DB_USER")
DB_PASS = env.str("DB_PASS")
DB_NAME = env.str("DB_NAME")
DB_HOST = env.str("DB_HOST")

BITZLATO_LOGIN_EXCEPTIONS = {
    "401": "authentication information is absent or incorrect. Access token is outdated and authentication should be done again",
    "403": "requested information is related to another user or access token do not corresponds this gateway.",
    "500": "Something goes wrong. Should be no such errors if work is correct."
}
