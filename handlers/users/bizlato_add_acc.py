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
from keyboards.inline import qiwi_keyboard, bizlato_keyboard, set_callback, back_keyboard, bizlato_accs_keyboard, \
    bizlato_accept_acc
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
    if resp.status_code == 200:
        return [resp.status_code, json.dumps(json_key)]
    else:
        return [resp.status_code]


@dp.callback_query_handler(state=AddAcc.ButtonAdd)
async def bizlato_add_button(call: types.CallbackQuery, state=FSMContext):
    await call.answer()
    callback_data = call.data.split(":")
    if callback_data[0] == "back":
        await state.finish()
        await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
        await call.message.answer(text="Вы вернулись назад", reply_markup=start_keyboard)
    elif len(callback_data) == 3 and callback_data[1] == "bizlato" and callback_data[2] == "add_acc":
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
async def input_bizlato_email(message: Union[types.Message, types.CallbackQuery], state=FSMContext):
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
                accs = await db.check_bizlato_exists(email)
                if accs[0]:
                    await message.answer(text="Данный аккаунт уже зарегистрирован в базе\n"
                                              "Попробуйте еще раз...\n"
                                              "<b>Введите email Bitzlato аккаунта:</b>", reply_markup=back_keyboard)
                    await AddAcc.InputEmail.set()
                else:
                    await state.update_data(
                        {
                            "api_key": data[1]
                        }
                    )
                    await message.answer(
                        text="Введите секретный код двухфакторной аутентификации,\nуказанный на сайте при активации:",
                        reply_markup=back_keyboard)
                    await AddAcc.InputCode.set()
            else:
                login_error = BITZLATO_LOGIN_EXCEPTIONS.get(str(data[0]))
                await message.answer(text=login_error + "\n" + "Попробуйте еще раз\n"
                                                               "<b>Введите email Bitzlato аккаунта:</b>",
                                     reply_markup=back_keyboard)
                await AddAcc.InputEmail.set()
        except Exception as err:
            print(err)
            await message.answer(text="Что-то пошло не так, попробуйте еще раз..."
                                      "<b>Введите email Bitzlato аккаунта:</b>", reply_markup=back_keyboard)
            await AddAcc.InputEmail.set()


@dp.callback_query_handler(state=AddAcc.InputCode)
@dp.message_handler(state=AddAcc.InputCode)
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
        await message.answer(f"Проверьте правильность секретного кода.\nВы указали <i>{message.text}</i>",
                             reply_markup=bizlato_accept_acc)
        await state.update_data({
            "code": message.text
        })
        await AddAcc.Accept_acc.set()


@dp.callback_query_handler(state=AddAcc.Accept_acc)
async def input_bizlato_acc(message: types.CallbackQuery, state=FSMContext):
    if message.data == "back":
        acc_data = await state.get_data()
        email = acc_data.get("email")
        api_key = acc_data.get("api_key")
        await state.reset_data()
        await state.update_data(
            {
                "api_key": api_key,
                "email": email
            }
        )
        await bot.delete_message(chat_id=message.from_user.id, message_id=message.message.message_id)
        await message.message.answer(
            text="Введите секретный код двухфакторной аутентификации,\nуказанный на сайте при активации:",
            reply_markup=back_keyboard)
        await AddAcc.InputCode.set()
    elif message.data == "accept_acc":
        acc_data = await state.get_data()
        email = acc_data.get("email")
        api_key = acc_data.get("api_key")
        code = acc_data.get("code")
        await db.create_bizlato_acc(message.from_user.id, email, api_key, code)
        await bot.delete_message(chat_id=message.from_user.id, message_id=message.message.message_id)
        await message.message.answer("Аккаунт был успешно создан", reply_markup=start_keyboard)
        await state.finish()
    else:
        await bot.delete_message(chat_id=message.from_user.id, message_id=message.message.message_id)
        await AddAcc.Accept_acc.set()
