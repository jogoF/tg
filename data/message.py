FIRST_START = "Добро пожаловать в бота для аналитики ссылок! Жми скорее на кнопку создать."
COMMAND_START = "Главное меню бота!"
ADMIN_HELLO = "Привет админ! Выберай что настраивать)"
EDIT_LINK = "Меню настройки и управления ссылками"
WBOZPOS = "Здесь ты можешь узнать на какой строчке находится твой товар."
AIPOST = "Здесь ты можешь сгенерировать пост для твоего товара."
ADMIN_SELECT = "Выберите в каком формате отправить файл:"
ADMIN_ADD_US = "Укажите id администратора:"
ADMIN_ADDED = "Админ успешно добавлен!"
ADMIN_DELETED = "Админ успешно удален!"
NONE_EXIST = "Такого пользователя не существует!"
ALL_STATES_STOPPED = "Сброшено"
GET_NAME_LINK = "Укажите название ссылки:"
GET_LINK_TO = "Укажите куда должна вести ссылка: "
GET_PRICE_AD = "Укажите цену рекламы (не обязательно)"
GET_TG_USERNAME = "Укажите канал на котором будет реклама (не обязательно)"
DATA_DELETED = "Ссылка была успешно удалена!"
HELP_TEXT = "Ответы на все вопросы и подробная инструкция здесь - @SKYMOUNT_SUPPORT\nЕсли возникнут сложности или дополнительные вопросы, то обращайтесь в личные сообщения:\n@suter_agutin\n@Leonid_Leeshin\nС уважением команда SKYMOUNT☁️"
CREATING_EXCEPTION = "Извините, произошла ошибка генерации ссылки, попробуйте еще раз позже!"
INPUT_ERROR = "Сделайте выбор с помощью кнопок!"
GET_LINK = "Укажите артикул/ссылку товара:"
GET_STYLE = "Укажите стиль написания поста:"
GET_REQUEST = "Укажите вводимый запрос:"
IN_FINDING = "Процесс поиска начат!✅"
IN_GEN = "Процесс генерации начат!✅"
IN_CREATING_LINK = "Подождите, ссылка генерируется!✅"
IN_DEV = "Данная функция ещё в разработке!"
INVILID_ERROR = "Произошла ошибка, сообщите администраци бота."
GET_IMAGE_COUNT = "Выберите количество картинок используемых в посте(не больше 4):"
INVALID_IMAGE_COUNT = "Не больше 4 картинок!"
POST_SAVED="Пост сохранен в ваш профиль, для его редактирования или удаления перейдите в раздел управления постами."
POST_CONTROL_MENU = "Тут ты можешь создавать, редактировать и удалять свои посты"
ALL_YOUR_POSTS="Тут находятся все ваши посты"
IN_POST_MESSAGE = "Тут ты можешь управлять своим постом"
POST_DELETED="Пост был успешно удален!"

EDIT_POST_HEAD="Укажите заголовок поста:"
EDIT_POST_BODY="Укажите тело поста:"
EDIT_POST_PRICE="Укажите цену:"
INVALID_DATA_ERROR="Цена должна быть в виде числа!"
EDIT_POST_OLDPRICE="Укажите старую цену:"
EDIT_POST_PIC="Отправьте новые картинки поста:"

POST_EDIT = "Режим редактирования постов включен"
POST_SAVED_AFTER_EDITING = "Пост сохранен!"

def DATA_SAVED(link, sip):
    message = f"<b>Ваша ссылка создана!</b>\n\n<code>https://{sip}{link}</code>"
    return message
    
def GET_LINKS_DATA(link, user, md):
    link_count = 0
    wb_count = 0
    oz_count = 0
    another = 0
    for item in link:
        link_count+=1
        if(str(item[2]).startswith("wb")):
            wb_count+=1
        elif(str(item[2]).startswith("oz")):
            oz_count+=1
        else:
            another+=1
    message = f"<b>👤Мои ссылки:</b>\n\n👁‍🗨 <b>Кол-во ссылок:</b> {link_count}\n<b>👁‍🗨 Кол-во кликов:</b> {md[0]}\n<b>👁‍🗨 Стоимость клика:</b> {md[1]}₽\n\n🔎 <b>Моя статистика ссылок:</b>\n├ <b>WB:</b> {wb_count}\n├ <b>OZON:</b> {oz_count}\n└ <b>Другие:</b> {another}"
    return message

def LINK_DATA(link, openings, sip):
    open_prices = 0
    if(openings!="0"):
        open_prices = int(link[4])/int(openings)
    message = f"<b>⚙️Подробная информация</b>\n🔗<b>Для ссылки:</b> {link[3]}\n\n<b>🔎Информация:</b>\n├ <b>Название:</b> {link[1]}\n├ <b>Дата создания:</b> {link[7]} в {link[8]}\n└ <b>Сокращенная ссылка:</b> <code>https://{sip}{link[2]}</code>\n\n<b>💼Подробные данные:</b>\n├ Цена рекламы: {link[4]}₽\n├ Цена клика: {open_prices}₽\n└ Канал: {link[5]}\n\nКоличество переходов: {openings}"
    return message

def POS_RESULT(pos, article):
    message = f"<b>Результаты парсинга:</b>\n(Товар: {article})\n\nВаш товар находится на странице <b>{pos}</b>"
    return message

def POST_GEN(res, article, price, oldprice):
    message = f"💜<b>{res[0]}</b>\n\n💵Цена: <s>{oldprice}₽</s> {price}₽\n\n💬{res[1]}\n\n🔗 <a href='https://www.wildberries.ru/catalog/{article}/detail.aspx'>Заказать можно тут</a>"
    return message

