from aiogram import types


def main_kb():
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    buttons = [
        types.InlineKeyboardButton(text="📎Управление ссылками", callback_data="link"),
        types.InlineKeyboardButton(text="🤖Генерация постов", callback_data="posts"),
        types.InlineKeyboardButton(text="🏆Позиция WB/OZON", callback_data="position"),
        types.InlineKeyboardButton(text="🆘Поддержка", callback_data="help")
    ]
    keyboard.add(buttons[0], buttons[1])
    keyboard.add(buttons[2])
    keyboard.add(buttons[3])
    return keyboard

def control_link_kb():
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    buttons = [
		types.InlineKeyboardButton(text="👤Мои ссылки", callback_data="my_link"),
		types.InlineKeyboardButton(text="➕Создать ссылку", callback_data="create_link"),
    types.InlineKeyboardButton(text="📄Таблица EXCEL", callback_data="excel"),
    types.InlineKeyboardButton(text="↩️Назад", callback_data="start")
    ]
    keyboard.add(*buttons)
    return keyboard

def none_kb():
  keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
  buttons = [
    types.KeyboardButton(text="Не указывать"),
    types.KeyboardButton(text="❌Отмена")
  ]
  keyboard.add(*buttons)
  return keyboard

def all_posts_kb(posts):
  keyboard = types.InlineKeyboardMarkup(row_width=1)
  buttons = [
  ]
  for item in posts:
    button = types.InlineKeyboardButton(text=f"{item[2][:20]}...", callback_data=f"post:{item[0]}")
    buttons.append(button)
  button_exit = types.InlineKeyboardButton(text="↩️Назад", callback_data="posts")
  buttons.append(button_exit)
  keyboard.add(*buttons)
  return keyboard

def post_kb():
  keyboard = types.InlineKeyboardMarkup(row_width=1)
  buttons = [
    types.InlineKeyboardButton(text="📑Мои посты", callback_data="my_posts"),
    types.InlineKeyboardButton(text="➕Создать пост", callback_data="post_create"),
    types.InlineKeyboardButton(text="📄Таблица EXCEL", callback_data=f"post_excel"),
    types.InlineKeyboardButton(text="↩️Назад", callback_data="start")
  ]    
  keyboard.add(*buttons)
  return keyboard

def inpost_kb(post):
  keyboard = types.InlineKeyboardMarkup(row_width=1)
  buttons = [
    types.InlineKeyboardButton(text="📄Редактировать", callback_data=f"edit_post:{post[0]}"),
    types.InlineKeyboardButton(text="🗑Удалить", callback_data=f"del_post:{post[0]}"),
    types.InlineKeyboardButton(text="❌Закрыть", callback_data="my_posts")
  ]    
  keyboard.add(*buttons)
  return keyboard

def editpost_kb(post_id):
  keyboard = types.InlineKeyboardMarkup(row_width=1)
  buttons = [
    types.InlineKeyboardButton(text="📑Изменить заголовок", callback_data=f"edit_head:{post_id}"),
    types.InlineKeyboardButton(text="📖Изменить тело", callback_data=f"edit_body:{post_id}"),
    types.InlineKeyboardButton(text="💰Изменить цену", callback_data=f"edit_price:{post_id}"),
    types.InlineKeyboardButton(text="💸Изменить старую цену", callback_data=f"edit_oldprice:{post_id}"),
    types.InlineKeyboardButton(text="↩️Назад", callback_data="my_posts")
  ]    
  keyboard.add(*buttons)
  return keyboard


def links_kb(link):
  keyboard = types.InlineKeyboardMarkup(row_width=1)
  buttons = []
  for item in link:
    button = types.InlineKeyboardButton(text=f"{item[1]} │ {item[7]}", callback_data=f"token:{item[0]}")
    buttons.append(button)
  button_exit = types.InlineKeyboardButton(text="↩️Назад", callback_data="link")
  buttons.append(button_exit)
  keyboard.add(*buttons)
  return keyboard

def inlink_kb(token):
  keyboard = types.InlineKeyboardMarkup(row_width=1)
  buttons = [
    types.InlineKeyboardButton(text="➖Удалить ссылку", callback_data=f"delete_link:{token}"),
    types.InlineKeyboardButton(text="🔄Перезагрузить", callback_data=f"token:{token}"),
    types.InlineKeyboardButton(text="❌Закрыть", callback_data="my_link")
  ]
  keyboard.add(*buttons)
  return keyboard
  
def parse_kb():
  keyboard = types.InlineKeyboardMarkup(row_width=2)
  buttons = [
    types.InlineKeyboardButton(text="🟣Wildberries", callback_data=f"wb"),
    types.InlineKeyboardButton(text="🔵Ozon(IN-DEV)", callback_data="ozon"),
    types.InlineKeyboardButton(text="↩️Назад", callback_data="start")
  ]
  keyboard.add(*buttons)
  return keyboard

def post_create_kb():
  keyboard = types.InlineKeyboardMarkup(row_width=2)
  buttons = [
    types.InlineKeyboardButton(text="🟣Wildberries", callback_data=f"wb_ai"),
    types.InlineKeyboardButton(text="🔵Ozon(IN-DEV)", callback_data="ozon_ai"),
    types.InlineKeyboardButton(text="↩️Назад", callback_data="posts")
  ]
  keyboard.add(*buttons)
  return keyboard

def post_back_kb():
  keyboard = types.InlineKeyboardMarkup(row_width=1)
  buttons = [
    types.InlineKeyboardButton(text="❌Закрыть", callback_data="ai")
  ]
  keyboard.add(*buttons)
  return keyboard

def inlink_back_kb():
  keyboard = types.InlineKeyboardMarkup(row_width=1)
  buttons = [
    types.InlineKeyboardButton(text="❌Закрыть", callback_data="my_link")
  ]
  keyboard.add(*buttons)
  return keyboard

def del_post_back_kb():
  keyboard = types.InlineKeyboardMarkup(row_width=1)
  buttons = [
    types.InlineKeyboardButton(text="❌Закрыть", callback_data="my_posts")
  ]
  keyboard.add(*buttons)
  return keyboard


def parse_back_kb():
  keyboard = types.InlineKeyboardMarkup(row_width=1)
  buttons = [
    types.InlineKeyboardButton(text="❌Закрыть", callback_data="position")
  ]
  keyboard.add(*buttons)
  return keyboard

def del_states():
  keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
  buttons = [
    types.KeyboardButton(text="❌Отмена")
  ]
  keyboard.add(*buttons)
  return keyboard

def link_back_kb():
  keyboard = types.InlineKeyboardMarkup(row_width=1)
  buttons = [
    types.InlineKeyboardButton(text="↩️Назад", callback_data="link")
  ]
  keyboard.add(*buttons)
  return keyboard

def style_kb():
  keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
  buttons = [
    types.KeyboardButton(text="🔗Первое лицо"),
    types.KeyboardButton(text="🔗Третье лицо"),
    types.KeyboardButton(text="❌Отмена")
  ]
  keyboard.add(*buttons)
  return keyboard

def back_kb():
  keyboard = types.InlineKeyboardMarkup(row_width=1)
  buttons = [
    types.InlineKeyboardButton(text="↩️Назад", callback_data="start")
  ]
  keyboard.add(*buttons)
  return keyboard



def owner_kb():
  keyboard = types.InlineKeyboardMarkup(row_width=1)
  buttons = [
    types.InlineKeyboardButton(text="База пользователей", callback_data="user_base"),
    types.InlineKeyboardButton(text="Админы", callback_data="admins")
  ]
  keyboard.add(*buttons)
  return keyboard

def data_kb():
  keyboard = types.InlineKeyboardMarkup(row_width=2)
  buttons = [
    types.InlineKeyboardButton(text="@usernames", callback_data="usernames"),
    types.InlineKeyboardButton(text="@ids", callback_data="ids"),
    types.InlineKeyboardButton(text="↩️Назад", callback_data="admin")
  ]
  keyboard.add(*buttons)
  return keyboard

def admins_edit_kb():
  keyboard = types.InlineKeyboardMarkup(row_width=2)
  buttons = [
    types.InlineKeyboardButton(text="➕Добавить админа", callback_data="add_admin"),
    types.InlineKeyboardButton(text="➖Удалить админа", callback_data="del_admin"),
    types.InlineKeyboardButton(text="↩️Назад", callback_data="owner")
  ]
  keyboard.add(*buttons)
  return keyboard

def admin_del_kb(admins):
  keyboard = types.InlineKeyboardMarkup(row_width=1)
  buttons = []
  for item in admins:
    btn = types.InlineKeyboardButton(text=f"{item[0]}", callback_data=f"del_admin:{item[0]}")
    buttons.append(btn)
  back = types.InlineKeyboardButton(text="↩️Назад", callback_data="owner")
  buttons.append(back)
  keyboard.add(*buttons)
  return keyboard

def get_position_kb():
  keyboard = types.InlineKeyboardMarkup(row_width=3)
  buttons = [
    types.InlineKeyboardButton(text="МОСКВА(C)", callback_data="MOSCOW_NORTH"),
    types.InlineKeyboardButton(text="МОСКВА(Ю)", callback_data="MOSCOW_SOUTH"),
    types.InlineKeyboardButton(text="ВЛАДИВОСТОК", callback_data="VLADIVASTOK"),
    types.InlineKeyboardButton(text="ЕКАТЕРЕНБУРГ", callback_data="EKATERENBURG"),
    types.InlineKeyboardButton(text="КАЗАНЬ", callback_data="KAZAN"),
    types.InlineKeyboardButton(text="КРАСНОДАР", callback_data="KRASNODAR"),
    types.InlineKeyboardButton(text="НОВОСИБИРСК", callback_data="NOVOSIBIRSK"),
    types.InlineKeyboardButton(text="СПБ", callback_data="SANKT_PETERBURG"),
    types.InlineKeyboardButton(text="ВЛАДИКАВКАЗ", callback_data="VLADIKAVKAZ")
    ]
  keyboard.add(*buttons)
  return keyboard