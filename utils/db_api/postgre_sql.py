from typing import Union

import asyncpg
from asyncpg import Pool, Connection

from data import config


class Database:

    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        self.pool = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASS,
            host=config.DB_HOST,
            database=config.DB_NAME
        )

    async def execute(self, command, *args,
                      fetch: bool = False,
                      fetchval: bool = False,
                      fetchrow: bool = False,
                      execute: bool = False
                      ):
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
                return result

    async def create_table_accounts(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Accounts(
        id SERIAL PRIMARY KEY,
        user_id BIGINT NOT NULL, 
        bizlato_email VARCHAR(255) NULL UNIQUE ,
        bizlato_api_key VARCHAR(255) NULL UNIQUE,
        qiwi_wallets VARCHAR(255)[] NULL
        );
        """
        await self.execute(sql, execute=True)

    async def select_all_account(self):
        sql = "SELECT * FROM Accounts"
        return await self.execute(sql, fetch=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ${num}" for num, item in enumerate(parameters.keys(), start=1)
        ])
        return sql, tuple(parameters.values())

    async def select_account(self, **kwargs):
        sql = "SELECT * FROM WHERE"
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def create_qiwi_wallet(self, bizlato_api_key, qiwi_wallets):
        sql = "UPDATE Accounts SET qiwi_wallets = ARRAY [$2] WHERE bizlato_api_key=$1"
        return await self.execute(sql, bizlato_api_key, qiwi_wallets, execute=True)

    async def create_bizlato_acc(self, user_id, bizlato_email, bizlato_api_key):
        sql = "INSERT INTO Accounts (user_id,bizlato_email,bizlato_api_key) VALUES ($1,$2,$3)"
        return await self.execute(sql, user_id, bizlato_email, bizlato_api_key, execute=True)

    async def add_qiwi_wallet(self, bizlato_api_key, qiwi_wallets):
        sql = "UPDATE Accounts SET qiwi_wallets = array_append(qiwi_wallets,$2) WHERE bizlato_api_key=$1"
        return await self.execute(sql, bizlato_api_key, qiwi_wallets, execute=True)

    async def delete_qiwi_wallet(self, bizlato_api_key, qiwi_wallets):
        sql = "UPDATE Accounts SET qiwi_wallets = array_remove(qiwi_wallets,$2) WHERE bizlato_api_key=$1"
        return await self.execute(sql, bizlato_api_key, qiwi_wallets, execute=True)

    async def show_wallets(self, bizlato_api_key):
        sql = "SELECT qiwi_wallets FROM Accounts WHERE bizlato_api_key=$1"
        return await self.execute(sql, bizlato_api_key, fetchrow=True)

    async def show_email(self, bizlato_api_key):
        sql = "SELECT bizlato_email FROM Accounts WHERE bizlato_api_key=$1"
        return await self.execute(sql, bizlato_api_key, fetchrow=True)

    async def show_bizlato_accs(self, user_id):
        sql = "SELECT bizlato_email FROM Accounts WHERE user_id=$1"
        return await self.execute(sql, user_id, fetch=True)

    async def show_bizlato_keys(self, bizlato_email):
        sql = "SELECT bizlato_api_key FROM Accounts WHERE bizlato_email=$1"
        return await self.execute(sql, bizlato_email, fetch=True)

    async def check_bizlato_exists(self, bizlato_api_key):
        sql = "SELECT EXISTS(SELECT 1 FROM Accounts WHERE bizlato_email = $1)"
        return await self.execute(sql, bizlato_api_key, fetchrow=True)

    async def check_qiwi_exists(self, qiwi_wallets):
        sql = "SELECT EXISTS(SELECT 1 FROM Accounts WHERE $1=any(qiwi_wallets))"
        return await self.execute(sql, qiwi_wallets, fetchrow=True)

    async def delete_all_accs(self):
        await self.execute("DELETE FROM Accounts WHERE TRUE", execute=True)
