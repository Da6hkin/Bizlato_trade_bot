import logging

from aiogram import executor

from loader import dp, db
import middlewares, filters, handlers
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands


async def on_startup(dispatcher):

    logging.info("Создаем подключение к базе")
    await db.create()
    logging.info("Создаем таблицу аккаунтов")

    await db.create_table_accounts()

    await set_default_commands(dispatcher)
    logging.info("Готово")
    # Уведомляет про запуск
    await on_startup_notify(dispatcher)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
