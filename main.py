import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from data.config import TG, SERVER_IP, SERVER_PASS, GPT_TOKEN, OWNER
from markup.keyboard import *
from data.message import *
from util.db_worker.function import *
from util.parser.function import wb_pos_async, find_wb_async
from util.gpt.function import request
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.dispatcher import DEFAULT_RATE_LIMIT
from aiogram.dispatcher.handler import CancelHandler, current_handler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.utils.exceptions import Throttled
from aiogram.types import InputMediaPhoto
from aiogram.utils.exceptions import BadRequest
import asyncio



logging.basicConfig(level=logging.INFO)
storage = MemoryStorage()
bot = Bot(token=TG, parse_mode="HTML")
dp = Dispatcher(bot, storage=storage)

#States
class link_object(StatesGroup):
    linkName = State()
    linkTo = State()
    linkPrice = State()
    linkTgName = State()
class wboz_object(StatesGroup):
    article = State()
    pos = State()
    request = State()
class post_object(StatesGroup):
    article = State()
    image_count = State()
    style = State()
class admin_object(StatesGroup):
    id = State()
class post_view_object(StatesGroup):
    id = State()
    head = State()
    body = State()
    price = State()
    oldprice = State()

#AntiSpam System
def rate_limit(limit: int, key=None):
    def decorator(func):
        setattr(func, 'throttling_rate_limit', limit)
        if key:
            setattr(func, 'throttling_key', key)
        return func

    return decorator


class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, limit=DEFAULT_RATE_LIMIT, key_prefix='antiflood_'):
        self.rate_limit = limit
        self.prefix = key_prefix
        super(ThrottlingMiddleware, self).__init__()

    async def on_process_message(self, message: types.Message, data: dict):
        handler = current_handler.get()
        dispatcher = Dispatcher.get_current()
        if handler:
            limit = getattr(handler, 'throttling_rate_limit', self.rate_limit)
            key = getattr(handler, 'throttling_key', f"{self.prefix}_{handler.__name__}")
        else:
            limit = self.rate_limit
            key = f"{self.prefix}_message"
        try:
            await dispatcher.throttle(key, rate=limit)
        except Throttled as t:
            await self.message_throttled(message, t)
            raise CancelHandler()

    async def message_throttled(self, message: types.Message, throttled: Throttled):
        handler = current_handler.get()
        dispatcher = Dispatcher.get_current()
        if handler:
            key = getattr(handler, 'throttling_key', f"{self.prefix}_{handler.__name__}")
        else:
            key = f"{self.prefix}_message"
        delta = throttled.rate - throttled.delta
        if throttled.exceeded_count <= 2:
            await message.reply('Спам запрещен!')
        await asyncio.sleep(delta)
        thr = await dispatcher.check_key(key)

            
#Admin menus:

#Main
@dp.message_handler(commands="admin")
async def admin_cmd(message: types.message):
    if(str(message.from_user.id)==OWNER):
        await message.answer(ADMIN_HELLO, parse_mode=types.ParseMode.HTML, reply_markup=owner_kb())
        return 0
    if(is_admin(message.from_user.id)==True):
        await message.answer(ADMIN_HELLO, parse_mode=types.ParseMode.HTML, reply_markup=owner_kb())
    else:
        pass

@dp.callback_query_handler(text="owner")
async def getter_data(call: types.CallbackQuery):
	await call.message.edit_text(ADMIN_HELLO, parse_mode=types.ParseMode.HTML, reply_markup=owner_kb())

#Adding new admin

@dp.callback_query_handler(text="add_admin")
async def getter_data(call: types.CallbackQuery):
    await call.message.edit_text(ADMIN_ADD_US, parse_mode=types.ParseMode.HTML)
    await admin_object.id.set()

@dp.message_handler(state=admin_object.id)
async def get_id_admin(message: types.Message, state: FSMContext):
    await state.update_data(id = message.text)
    data = await state.get_data()
    isAdded = add_admin(data['id'])
    if(isAdded==True):
        await bot.send_message(message.from_user.id, ADMIN_ADDED)
    else:
        await bot.send_message(message.from_user.id, NONE_EXIST)
    await state.finish()

@dp.callback_query_handler(text="admin")
async def getter_data(call: types.CallbackQuery):
	await call.message.edit_text(ADMIN_HELLO, parse_mode=types.ParseMode.HTML, reply_markup=owner_kb())

#Delete admins
@dp.callback_query_handler(text="del_admin")
async def delete_admin(call: types.CallbackQuery):
	await call.message.edit_text(ADMIN_HELLO, parse_mode=types.ParseMode.HTML, reply_markup=admin_del_kb(get_admins()))

@dp.callback_query_handler(text="admins")
async def getter_data(call: types.CallbackQuery):
	await call.message.edit_text(ADMIN_HELLO, parse_mode=types.ParseMode.HTML, reply_markup=admins_edit_kb())

#List of users
@dp.callback_query_handler(text="user_base")
async def getter_data(call: types.CallbackQuery):
	await call.message.edit_text(ADMIN_SELECT, parse_mode=types.ParseMode.HTML, reply_markup=data_kb())

@dp.callback_query_handler(text="usernames")
async def getter_usernames(call: types.CallbackQuery):
    gen_txt_usernames()
    path = "temp/users.txt"
    await bot.send_document(call.from_user.id, open(path, 'rb'))
    await delete_file(path)

@dp.callback_query_handler(text="ids")
async def getter_usernames(call: types.CallbackQuery):
    gen_txt_ids()
    path = "temp/ids.txt"
    await bot.send_document(call.from_user.id, open(path, 'rb'))
    await delete_file(path)

#User part
#Main menu
@rate_limit(10, 'start')
@dp.message_handler(commands="start")
async def start_cmd(message: types.message):
    if(check_exist(message.from_user.id)==False):
        add_user(message.from_user.id, message.from_user.username)
        await message.answer(FIRST_START, parse_mode=types.ParseMode.HTML, reply_markup=main_kb())
    else:
        await message.answer(FIRST_START, parse_mode=types.ParseMode.HTML, reply_markup=main_kb())

#Stopping States
@rate_limit(10, '❌Отмена')
@dp.message_handler(state='*', text='❌Отмена')
async def cancel_handler(message: types.Message, state: FSMContext):
    if(state!=None):
        await state.finish()
        await message.reply(ALL_STATES_STOPPED, reply_markup=types.ReplyKeyboardRemove())
        await message.answer(FIRST_START, reply_markup=main_kb())
    else:
        pass

#Start query
@dp.callback_query_handler(text="start")
async def start_query(call: types.CallbackQuery):
	await call.message.edit_text(FIRST_START, parse_mode=types.ParseMode.HTML, reply_markup=main_kb())

#Main menu buttons:
@dp.callback_query_handler(text="ozon")
async def ozon_dev(call: types.CallbackQuery):
	await call.answer(IN_DEV)

@dp.callback_query_handler(text="ozon_ai")
async def ozon_adev(call: types.CallbackQuery):
	await call.answer(IN_DEV)

@dp.callback_query_handler(text="link")
async def link_menu(call: types.CallbackQuery):
	await call.message.edit_text(EDIT_LINK, reply_markup=control_link_kb())

#Link menu
@dp.callback_query_handler(text="create_link")
async def create_link(call: types.CallbackQuery):
    await bot.send_message(call.from_user.id, GET_NAME_LINK, reply_markup=del_states())
    await link_object.linkName.set()

@dp.message_handler(state=link_object.linkName)
async def get_name(message: types.Message, state: FSMContext):
    await state.update_data(linkName = message.text)
    await bot.send_message(message.from_user.id, GET_LINK_TO, reply_markup=del_states())
    await link_object.linkTo.set()

@dp.message_handler(state=link_object.linkTo)
async def get_dest(message: types.Message, state: FSMContext):
    await state.update_data(linkTo = message.text)
    await bot.send_message(message.from_user.id, GET_PRICE_AD, reply_markup=none_kb())
    await link_object.linkPrice.set()

@dp.message_handler(state=link_object.linkPrice)
async def get_price(message: types.Message, state: FSMContext):
    if(message.text=="Не указывать"):
        await state.update_data(linkPrice = "Не указан")
    else:
        await state.update_data(linkPrice = message.text)
    await bot.send_message(message.from_user.id, GET_TG_USERNAME, reply_markup=none_kb())
    await link_object.linkTgName.set()

@dp.message_handler(state=link_object.linkTgName)
async def get_tg(message: types.Message, state: FSMContext):
    if(message.text=="Не указывать"):
        await state.update_data(linkTG = "Не указан")
    else:
        await state.update_data(linkTG = message.text)
    await bot.send_message(message.from_user.id, IN_CREATING_LINK, parse_mode=types.ParseMode.HTML, reply_markup=types.ReplyKeyboardRemove())
    async with state.proxy() as data:
        try:
            link_view = await add_link(data['linkName'], data['linkTo'], data['linkPrice'], data['linkTG'], message.from_user.id, SERVER_IP, SERVER_PASS)
            await message.answer(DATA_SAVED(link_view, SERVER_IP), parse_mode=types.ParseMode.HTML, reply_markup=link_back_kb())
            await state.finish()
        except:
            await message.answer(CREATING_EXCEPTION, parse_mode=types.ParseMode.HTML, reply_markup=link_back_kb())
            await state.finish()

#Main menu

@dp.callback_query_handler(text="posts")
async def posts_menu(call: types.CallbackQuery):
	await call.message.edit_text(POST_CONTROL_MENU, reply_markup=post_kb())

@dp.callback_query_handler(text="my_posts")
async def posts_menu(call: types.CallbackQuery):
	await call.message.edit_text(ALL_YOUR_POSTS, reply_markup=all_posts_kb(get_posts_by_user_id(call.from_user.id)))

@dp.callback_query_handler(text="post_create")
async def posts_menu(call: types.CallbackQuery):
	await call.message.edit_text(AIPOST, reply_markup=post_create_kb())

@dp.callback_query_handler(text="my_link")
async def link_menu(call: types.CallbackQuery):
	await call.message.edit_text(GET_LINKS_DATA(get_list_links(call.from_user.id), get_user(call.from_user.id), await click_price(SERVER_IP, SERVER_PASS, call.from_user.id)), parse_mode=types.ParseMode.HTML, reply_markup=links_kb(get_list_links(call.from_user.id)))

@dp.callback_query_handler(text="position")
async def ai_posts(call: types.CallbackQuery):
	await call.message.edit_text(WBOZPOS, reply_markup=parse_kb())

@dp.callback_query_handler(text="help")
async def help_menu(call: types.CallbackQuery):
	await call.message.edit_text(HELP_TEXT, parse_mode="HTML", reply_markup=back_kb())

#Wb/oz pos menu
@dp.callback_query_handler(text="wb")
async def wb_pos_f(call: types.CallbackQuery):
    await bot.send_message(call.from_user.id, GET_LINK, reply_markup=del_states())
    await wboz_object.article.set()


@dp.message_handler(state=wboz_object.article)
async def get_article(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(article = message.text)
    else:
        await state.update_data(article = get_article_adaptive(message.text))
    await bot.send_message(message.from_user.id, GET_REQUEST)
    await wboz_object.request.set()

@dp.message_handler(state=wboz_object.request)
async def get_request(message: types.Message, state: FSMContext):
    await state.update_data(request = message.text)
    await bot.send_message(message.from_user.id, IN_FINDING, parse_mode=types.ParseMode.HTML, reply_markup=get_position_kb())
    await wboz_object.pos.set()


@dp.callback_query_handler(state=wboz_object.pos)
async def process_pos(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(pos = call.data)
    data = await state.get_data()
    await bot.send_message(call.from_user.id, IN_FINDING, parse_mode=types.ParseMode.HTML, reply_markup=types.ReplyKeyboardRemove())
    pos = await wb_pos_async(data['request'], data['article'], data['pos'])
    await bot.send_message(call.from_user.id, POS_RESULT(pos, data['article']), parse_mode=types.ParseMode.HTML, reply_markup=parse_back_kb())
    await state.finish()

@dp.callback_query_handler(text="ai")
async def ai_menu(call: types.CallbackQuery):
	await call.message.edit_text(AIPOST, reply_markup=post_kb())

@dp.callback_query_handler(text="post_excel")
async def excel_posts(call: types.CallbackQuery):
    id = call.from_user.id
    await get_excel_posts(get_posts_by_user_id(id), id)
    path = f"temp/{id}.xlsx"
    await bot.send_document(id, open(path, 'rb'))
    await delete_file(path)

@dp.callback_query_handler(text="excel")
async def ai_menu(call: types.CallbackQuery):
    path = f"temp/{call.from_user.id}.xlsx"
    await get_excel(call.from_user.id, SERVER_IP, SERVER_PASS)
    await bot.send_document(call.from_user.id, open(path, 'rb'))
    await delete_file(path)

@dp.callback_query_handler(text="wb_ai")
async def wb_ai1(call: types.CallbackQuery):
    await bot.send_message(call.from_user.id, GET_LINK, reply_markup=del_states())
    await post_object.article.set()

@dp.message_handler(state=post_object.article)
async def get_article_ai(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(article = message.text)
    else:
        await state.update_data(article = get_article_adaptive(message.text))
    await bot.send_message(message.from_user.id, GET_IMAGE_COUNT)
    await post_object.image_count.set()

@dp.message_handler(state=post_object.image_count)
async def get_image_count(message: types.Message, state: FSMContext):
    if message.text.isdigit() and not int(message.text)>4:
        await state.update_data(image_count = message.text)
        await bot.send_message(message.from_user.id, GET_STYLE, reply_markup=style_kb())
        await post_object.style.set()   
    else:
        await bot.send_message(message.from_user.id, INVALID_IMAGE_COUNT)


@dp.message_handler(state=post_object.style)
async def get_style(message: types.Message, state: FSMContext):
    if(message.text=="🔗Первое лицо" or message.text=="🔗Третье лицо"):
        await state.update_data(style = message.text)
        data = await state.get_data()
        await bot.send_message(message.from_user.id, IN_GEN, parse_mode=types.ParseMode.HTML, reply_markup=types.ReplyKeyboardRemove())
        try:
            wb_data = await find_wb_async(data["article"], int(data["image_count"]))
            res = await request(GPT_TOKEN, wb_data, data["style"])
            post = POST_GEN(res, data["article"], wb_data[2], wb_data[3])
            media = types.MediaGroup()
            media.attach_photo(types.InputFile(f'{wb_data[4][-1]}.png'), caption=post)
            for i in wb_data[4][:-1]:
                media.attach_photo(types.InputFile(f'{i}.png'))
            post_img = await bot.send_media_group(message.from_user.id,media=media)
            file_ids = []
            for msg in post_img:
                file_id = msg.photo[-1].file_id
                file_ids.append(file_id)
            create_post(str(res[0]), str(res[1]), int(wb_data[2]), int(wb_data[3]), message.from_user.id, file_ids, int(data["article"]))
            await clear_temp(wb_data[4])
            await message.answer(POST_SAVED, reply_markup=post_back_kb())
            await state.finish()
        except:
            await bot.send_message(message.from_user.id, INVILID_ERROR, reply_markup=post_back_kb())
            await state.finish()
    else:
        await bot.send_message(message.from_user.id, INPUT_ERROR, reply_markup=style_kb())


async def handle_token_callback(call: types.CallbackQuery, server_ip: str, server_pass: str):
    token_link = call.data.split(":")[1]
    link_info = get_link(token_link)
    openings = await getOpenings(token_link, server_ip, server_pass)
    await asyncio.sleep(1)
    try:
        await call.message.edit_text(
            LINK_DATA(link_info, openings, server_ip),
            parse_mode=types.ParseMode.HTML,
            reply_markup=inlink_kb(token_link),
            disable_web_page_preview=True
        )
    except Exception as e:
        logging.error(f"Error editing message: {e}")

async def handle_delete_link_callback(call: types.CallbackQuery, server_ip: str, server_pass: str):
    token_link = call.data.split(":")[1]
    await del_link(token_link, server_ip, server_pass)
    await call.message.edit_text(DATA_DELETED, reply_markup=inlink_back_kb())

#I am very sorry about my code, i really try to avoid that(
#EDIT POST HEAD
async def handle_edit_post_head_callback(call: types.CallbackQuery, state=FSMContext):
    post_id = call.data.split(":")[1]
    await bot.send_message(call.from_user.id, EDIT_POST_HEAD)
    await state.update_data(id=post_id)
    await post_view_object.head.set()

@dp.message_handler(state=post_view_object.head)
async def get(message: types.Message, state: FSMContext):
    await state.update_data(head=message.text)
    data = await state.get_data()
    post_edit_head(data['head'], data['id'])
    await bot.send_message(message.from_user.id, POST_SAVED_AFTER_EDITING, reply_markup=del_post_back_kb())
    await state.finish()

#EDIT POST BODY
async def handle_edit_post_body_callback(call: types.CallbackQuery, state=FSMContext):
    post_id = call.data.split(":")[1]
    await bot.send_message(call.from_user.id, EDIT_POST_BODY)
    await state.update_data(id=post_id)
    await post_view_object.body.set()

@dp.message_handler(state=post_view_object.body)
async def get(message: types.Message, state: FSMContext):
    await state.update_data(body=message.text)
    data = await state.get_data()
    post_edit_body(data['body'], data['id'])
    await bot.send_message(message.from_user.id, POST_SAVED_AFTER_EDITING, reply_markup=del_post_back_kb())
    await state.finish()

#EDIT POST PRICE
async def handle_edit_post_price_callback(call: types.CallbackQuery, state=FSMContext):
    post_id = call.data.split(":")[1]
    await bot.send_message(call.from_user.id, EDIT_POST_PRICE)
    await state.update_data(id=post_id)
    await post_view_object.price.set()
    
    
@dp.message_handler(state=post_view_object.price)
async def get(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await bot.send_message(message.from_user.id, INVALID_DATA_ERROR)
        return
    await state.update_data(price=message.text)
    data = await state.get_data()
    post_edit_price(data['price'], data['id'])
    await bot.send_message(message.from_user.id, POST_SAVED_AFTER_EDITING, reply_markup=del_post_back_kb())
    await state.finish()

#EDIT POST OLDPRICE
async def handle_edit_post_oldprice_callback(call: types.CallbackQuery, state=FSMContext):
    post_id = call.data.split(":")[1]
    await bot.send_message(call.from_user.id, EDIT_POST_OLDPRICE)
    await state.update_data(id=post_id)
    await post_view_object.oldprice.set()


@dp.message_handler(state=post_view_object.oldprice)
async def get(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await bot.send_message(message.from_user.id, INVALID_DATA_ERROR)
        return
    await state.update_data(oldprice=message.text)
    data = await state.get_data()
    post_edit_oldprice(data['oldprice'], data['id'])
    await bot.send_message(message.from_user.id, POST_SAVED_AFTER_EDITING, reply_markup=del_post_back_kb())
    await state.finish()

#DELETE ADMIN
async def handle_delete_admin_callback(call: types.CallbackQuery):
    admin_id = call.data.split(":")[1]
    del_admin(admin_id)
    await call.message.edit_text(ADMIN_DELETED)

#EDITING POST KEYBOARD
async def handle_edit_post(call: types.CallbackQuery):
    post_id = call.data.split(":")[1]
    await call.message.edit_text(POST_EDIT, reply_markup=editpost_kb(post_id))


#PRVIEW POST FROM DB
async def handle_post_callback(call: types.CallbackQuery):
    post_id = call.data.split(":")[1]
    post = get_post_by_id(post_id)
    generated_post = POST_GEN([post[2], post[3]], post[6], post[4], post[5])
    images = eval(post[7])
    media = types.MediaGroup()
    media.attach_photo(types.InputMediaPhoto(f'{images[-1]}', caption=generated_post))
    for i in images[:-1]:
        media.attach_photo(types.InputMediaPhoto(f'{i}'))
    await bot.send_media_group(call.from_user.id, media=media)
    await bot.send_message(call.from_user.id, IN_POST_MESSAGE, reply_markup=inpost_kb(post))

#DELETE POST FROM DB
async def handle_delete_post_callback(call: types.CallbackQuery):
    post_id = call.data.split(":")[1]
    del_post_by_id(post_id)
    await call.message.edit_text(POST_DELETED, reply_markup=del_post_back_kb())

#And for that i am sorry too
@dp.callback_query_handler(state="*")
async def handle_callback_query(call: types.CallbackQuery, state: FSMContext):
    callback_data = call.data
    if callback_data.startswith("token:"):
        await handle_token_callback(call, SERVER_IP, SERVER_PASS)
    elif callback_data.startswith("delete_link:"):
        await handle_delete_link_callback(call, SERVER_IP, SERVER_PASS)
    elif callback_data.startswith("del_admin:"):
        await handle_delete_admin_callback(call)
    elif callback_data.startswith("post:"):
        await handle_post_callback(call)
    elif callback_data.startswith("del_post:"):
        await handle_delete_post_callback(call)
    elif callback_data.startswith("edit_post:"):
        await handle_edit_post(call)
    elif callback_data.startswith("edit_head:"):
        await handle_edit_post_head_callback(call, state)
    elif callback_data.startswith("edit_body:"):
        await handle_edit_post_body_callback(call, state)
    elif callback_data.startswith("edit_price:"):
        await handle_edit_post_price_callback(call, state)
    elif callback_data.startswith("edit_oldprice:"):
        await handle_edit_post_oldprice_callback(call, state)

            

    

if __name__ == "__main__":
    dp.middleware.setup(ThrottlingMiddleware())
    executor.start_polling(dp, skip_updates=True)

