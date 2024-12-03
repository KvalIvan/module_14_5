from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from crud_functions import *

api = '8025568952:AAGUU75mlfLbGZU7pbPMdbfsVW-iHMut7cc'
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup(resize_keyboard=True)
button_calories = KeyboardButton('Рассчитать норму калорий')
button_info = KeyboardButton(text='Информация')
button_formula = KeyboardButton('Формулы расчёта')
button_buy = KeyboardButton('Купить')
button_registration = KeyboardButton('Регистрация')
kb.add(button_calories, button_info)
kb.add(button_buy, button_formula)
kb.add(button_registration)

kb_buy = InlineKeyboardMarkup(resize_keyboard=True)
button_buy1 = InlineKeyboardButton('Продукт 1', callback_data='product_buying')
button_buy2 = InlineKeyboardButton('Продукт 2', callback_data='product_buying')
button_buy3 = InlineKeyboardButton('Продукт 3', callback_data='product_buying')
button_buy4 = InlineKeyboardButton('Продукт 4', callback_data='product_buying')
kb_buy.row(button_buy1, button_buy2, button_buy3, button_buy4)


class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()
    balance = 1000


@dp.message_handler(text='Регистрация')
async def sing_up(message):
    await message.answer('Введите имя пользователя (только латинский алфавит):')
    await RegistrationState.username.set()


@dp.message_handler(state=RegistrationState.username)
async def set_username(message, state):
    if is_included(message.text) is False:
        await state.update_data(username=message.text)
        await message.answer('Укажите ваш email:')
        await RegistrationState.email.set()
    else:
        await message.answer('Пользователь существует, введите другое имя')
        await RegistrationState.username.set()


@dp.message_handler(state=RegistrationState.email)
async def set_email(message, state):
    await state.update_data(email=message.text)
    await message.answer('Введите свой возраст:')
    await RegistrationState.age.set()


@dp.message_handler(state=RegistrationState.age)
async def set_age(message, state):
    await state.update_data(age=message.text)
    data = await state.get_data()
    add_user(data['username'], data['email'], data['age'])
    await message.answer('Регистрация прошла успешно')
    await message.answer("Регистрация закончена", reply_markup=kb)
    await state.finish()


@dp.message_handler(commands='start')
async def start(message):
    await message.answer(text='Вас приветствует калькулятор калорий', reply_markup=kb)
    get_all_products()


@dp.message_handler(text='Информация')
async def info(message):
    await message.answer(text='Вас приветствует калькулятор калорий '
                              'в котором вы можете рассчитать и понять сколько нужно калорий '
                              'в день именно Вам')


@dp.message_handler(text='Формулы расчёта')
async def get_formulas(call):
    await call.message.answer('для мужчин: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5 '
                              'для женщин: 10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161')
    await call.answer()


@dp.message_handler(text='Купить')
async def get_buying_list(message):
    for i in range(0, 4):
        sports_nutrition = get_all_products()[i]
        with open('img.jpg', 'rb') as img:
            await message.answer_photo(img, f'Название: {sports_nutrition[1]} | Описание: {sports_nutrition[2]} '
                                            f'| {sports_nutrition[3]}')
    await message.answer('Выберите продукт для покупки:', reply_markup=kb_buy)


@dp.callback_query_handler(text=['product_buying'])
async def send_confirm_message(call):
    await call.message.answer('Вы успешно приобрели продукт!')


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.callback_query_handler(text=['calories'])
async def set_age(call):
    await call.message.answer('Введите свой возраст')
    await call.answer()
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    calories = int(data['weight']) * 10 + int(data['growth']) * 6.25 - int(data['age']) * 5
    await message.answer(f'Ваша норма калорий: {calories}')

    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
