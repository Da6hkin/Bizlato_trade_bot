import datetime
import json
import random
import time
from typing import Union
import aiohttp
from data.config import BITZLATO_LOGIN_EXCEPTIONS
import asyncpg.exceptions
import requests
from aiogram.dispatcher import FSMContext
from jose import jws
from jose.constants import ALGORITHMS

from keyboards.default import cancel_keyboard, start_keyboard
from keyboards.inline import qiwi_keyboard, bizlato_keyboard, set_callback, back_keyboard, bizlato_accs_keyboard
from loader import dp, bot, db
from aiogram import types
from states import AddAcc, QiwiSettings


def check_bitzlato(email, key):
    json_key = json.loads(key)
    dt = datetime.datetime.now()
    ts = time.mktime(dt.timetuple())
    claims = {
        # user identificator
        "email": email,
        # leave as is
        "aud": "usr",
        # token issue time
        "iat": int(ts),
        # unique token identificator
        "jti": hex(random.getrandbits(64))
    }
    print(claims)
    # make token with claims from secret user key
    token = jws.sign(claims, json_key, headers={"kid": "1"}, algorithm=ALGORITHMS.ES256)

    resp = requests.get('https://bitzlato.com/api/p2p/public/exchange/dsa/', headers={
        "Authorization": "Bearer " + token
    },
                        params={})

    return {resp.status_code: token}


@dp.callback_query_handler(state=AddAcc.ButtonAdd)
async def bizlato_add_button(call: types.CallbackQuery, state=FSMContext):
    await call.answer()
    callback_data = call.data.split(":")
    if callback_data[0] == "back":
        await state.finish()
        await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
        await call.message.answer(text="Вы вернулись назад", reply_markup=start_keyboard)
    elif len(callback_data) == 3 and callback_data[1] == "bizlato" and callback_data[2] == "add_acc":
        await state.update_data(
            {
                "return_qiwi": True
            }
        )
        await bot.edit_message_reply_markup(chat_id=call.from_user.id, message_id=call.message.message_id,
                                            reply_markup=None)
        await call.message.answer(text="<b>Введите email Bitzlato аккаунта:</b>",
                                  reply_markup=back_keyboard)
        await AddAcc.InputEmail.set()
    else:
        await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
        await AddAcc.ButtonAdd.set()


@dp.callback_query_handler(state=AddAcc.InputEmail)
@dp.message_handler(state=AddAcc.InputEmail)
async def input_bizlato_acc(message: Union[types.Message, types.CallbackQuery], state=FSMContext):
    message_type = type(message)
    data = await state.get_data()
    if message_type == types.CallbackQuery:
        if message.data == "back":
            await state.finish()
            await bot.delete_message(chat_id=message.from_user.id, message_id=message.message.message_id)
            await message.message.answer(text="Вы отменили добавление аккаунта", reply_markup=start_keyboard)
        else:
            await bot.delete_message(chat_id=message.from_user.id, message_id=message.message.message_id)
            await AddAcc.InputEmail.set()
    elif message_type == types.Message:
        answer = message.text
        await state.update_data(
            {
                "email": answer
            }
        )
        await message.answer(text="Введите ключ API Bitzlato в Формате:\n"
                                  "<code>{'kty':'EC',\n"
                                  "'alg':'ES256',\n"
                                  "'crv':'P-256',\n"
                                  "'x':'EjDTE4kXWR1vOuWkFyZNgm_82ACJUzJVpMSowHFqxP0',\n"
                                  "'y':'jP3uNx4dhddy4hDJ3EJcQBnbqFB604ACY1TOAzzQ-rw',\n"
                                  "'d':'0NeSRzoCcB HmHCIhZPvDPCn6vU25aOsfe5Fvk_VEP2E'}</code>",
                             reply_markup=back_keyboard)
        await AddAcc.InputAcc.set()
    else:
        await AddAcc.InputEmail.set()


@dp.callback_query_handler(state=AddAcc.InputAcc)
@dp.message_handler(state=AddAcc.InputAcc)
async def input_bizlato_acc(message: Union[types.Message, types.CallbackQuery], state=FSMContext):
    message_type = type(message)
    if message_type == types.CallbackQuery:
        if message.data == "back":
            await state.finish()
            await bot.delete_message(chat_id=message.from_user.id, message_id=message.message.message_id)
            await message.message.answer(text="Вы отменили добавление аккаунта", reply_markup=start_keyboard)
        else:
            await bot.delete_message(chat_id=message.from_user.id, message_id=message.message.message_id)
            await AddAcc.InputEmail.set()
    elif message_type == types.Message:
        email_data = await state.get_data()
        email = email_data.get("email")
        api_key = message.text
        try:
            data = check_bitzlato(email, api_key)
            if data[0] == 200:
                accs = await db.check_bizlato_exists(data[1])
                if accs[0]:
                    await message.answer(text="Данный аккаунт уже зарегистрирован в базе\n"
                                              "Попробуйте еще раз...\n"
                                              "<b>Введите email Bitzlato аккаунта:<\b>", reply_markup=back_keyboard)
                    await AddAcc.InputEmail.set()
                else:
                    await db.create_bizlato_acc(
                        user_id=message.from_user.id,
                        bizlato_email=email,
                        bizlato_api_key=data[1]
                    )
                    await state.finish()
                    await message.answer(text="<i>Аккаунт Bitzlato был добавлен</i>", reply_markup=start_keyboard)
            else:
                login_error = BITZLATO_LOGIN_EXCEPTIONS.get(str(data[0]))
                await message.answer(text=login_error + "\n" + "Попробуйте еще раз\n"
                                                               "<b>Введите email Bitzlato аккаунта:</b>",
                                     reply_markup=back_keyboard)
                await AddAcc.InputEmail.set()
        except:
            await message.answer(text="Что-то пошло не так, попробуйте еще раз..."
                                      "<b>Введите email Bitzlato аккаунта:</b>", reply_markup=back_keyboard)
            await AddAcc.InputEmail.set()
