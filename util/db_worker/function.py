import sqlite3
import secrets
from datetime import datetime
from aiohttp import ClientSession
import aiohttp
import xlsxwriter
import os
import re
import asyncio
import aiofiles


conn = sqlite3.connect('db.db')
cur = conn.cursor()

async def createRequest(ip, password, link, linkTo, token):
  async with ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
    url = f"https://{ip}create?password={password}&link={link}&linkTo={linkTo}&token={token}"
    async with session.post(url=url) as response:
      return 0

async def deleteRequest(ip, password, token):
    async with ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
      url = f"https://{ip}delete?password={password}&token={token}"
      async with session.post(url=url) as response:
        return 0

async def getOpenCount(ip, password, token):
  async with ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
    url = f"https://{ip}openning?password={password}&token={token}"
    async with session.get(url=url) as response:
        return await response.text()

def check_exist(id):
  info = cur.execute('SELECT * FROM users WHERE user_id=?', (id, ))
  if(info.fetchone()!=None):
    check = True
  else:
    check = False
  return check


def add_user(id, username):
  cur_data = str(datetime.today().strftime('%Y.%m.%d'))
  cur.execute(f"INSERT INTO users VALUES (?,?,?,?)", (id, username, cur_data, 0))
  conn.commit()

def get_list_users():
  cur.execute("SELECT user_id FROM users")
  rows = cur.fetchall()
  users_list = []
  for row in rows:
      users_list.append(f"{row[0]}")
  return "\n".join(users_list)

async def add_link(linkName, linkTo, linkAdPrice, linkTG, id, sip, pasw):
  token = secrets.token_urlsafe(16)
  link_view = gen_link(linkTo)
  cur_data = str(datetime.today().strftime('%Y.%m.%d'))
  cur_time = str(datetime.now().strftime("%H:%M"))
  query = "INSERT INTO links (token, name, link_view, link_to, ad_price, tgch_username, user_id, create_date, create_time) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
  if(linkAdPrice!="Не указан"):
    linkAdPrice = int(linkAdPrice)
  else:
    linkAdPrice = 0
  cur.execute(query, (token, linkName, link_view, linkTo, linkAdPrice, linkTG, id, cur_data, cur_time))
  await createRequest(sip, pasw, link_view, linkTo, token)
  conn.commit()
  return link_view

def create_post(head, body, price, old_price, id, fid, article):
  post_id = secrets.randbits(30)
  cur.execute(f"INSERT INTO posts VALUES (?,?,?,?,?,?,?,?)", (post_id, id, head, body, price, old_price, article, str(fid)))
  conn.commit()


def get_posts_by_user_id(id):
  info = cur.execute('SELECT * FROM posts WHERE user_id=?', (id, )).fetchall()
  return info


def get_post_by_id(post_id):
  info = cur.execute('SELECT * FROM posts WHERE post_id=?', (post_id, )).fetchone()
  return info

def del_post_by_id(post_id):
  cur.execute("DELETE FROM posts WHERE post_id=?", (post_id, ))
  conn.commit()

def post_edit_head(head, post_id):
  cur.execute(f"UPDATE posts SET post_head=? WHERE post_id=?", (head, post_id))
  conn.commit()

def post_edit_body(body, post_id):
  cur.execute(f"UPDATE posts SET post_body=? WHERE post_id=?", (body, post_id))
  conn.commit()

def post_edit_price(price, post_id):
  cur.execute(f"UPDATE posts SET post_price=? WHERE post_id=?", (price, post_id))
  conn.commit()

def post_edit_oldprice(oldprice, post_id):
  cur.execute(f"UPDATE posts SET post_oldprice=? WHERE post_id=?", (oldprice, post_id))
  conn.commit()

def post_edit_imgs(imgs, post_id):
  cur.execute(f"UPDATE posts SET file_id=? WHERE post_id=?", (str(imgs), post_id))
  conn.commit()

async def clear_temp(file_ids):
  for file in file_ids:
    async with aiofiles.open(file, mode='w'):
          os.remove(f"{file}.png")
          os.remove(f"{file}.webp")


async def get_all_clicks(ip, password, id):
  links = get_tokens_by_id(5987641607)
  opennings = []
  for item in links:
    token = item[0]
    opennings.append(await getOpenCount(ip, password, token))
  return opennings

async def click_price(ip, password, user_id):
  tokens = []
  price = 0
  opennings = 0
  data = cur.execute('SELECT * FROM links WHERE user_id=?', (user_id, )).fetchall()
  for item in data:
    tokens.append(item[0])
    price+=item[4]
  for item in tokens:
    open = await getOpenings(item, ip, password)
    opennings+=int(open)
  if(opennings!=0):
    return [opennings, round(price/opennings, 2)]
  else:
    return [opennings, 0, 2]

async def open_counts_all(ip, password, user_id):
  opens = []
  data = cur.execute('SELECT token FROM links WHERE user_id=?', (user_id, )).fetchall()
  for item in range(0,len(data)):
    opens.append(await getOpenings(data[item][0], ip, password))
  return opens

async def del_link(token, sip, pasw):
  cur.execute("DELETE FROM links WHERE token=?", (token, ))
  await deleteRequest(sip, pasw, token)
  conn.commit()


async def getOpenings(token, sip, pasw):
  return str(await getOpenCount(sip, pasw, token))

def get_article_adaptive(str):
  numbers = re.findall(r'\d+', str)
  result_string = ''.join(numbers)
  return result_string


def gen_link(link):
  link_view = ""
  if(link.find("wildberries")!=-1):
    link_view = f"wb_{secrets.token_urlsafe(8)}"
  elif(link.find("ozon")!=-1):
    link_view = f"oz_{secrets.token_urlsafe(8)}"
  else:
    link_view = f"{secrets.token_urlsafe(10)}"
  return link_view

async def delete_file(path):
  os.remove(path=path)

def get_tokens_by_id(id):
  return(cur.execute('SELECT token FROM links WHERE user_id=?', (id, )).fetchall())



def get_list_links(id):
  return(cur.execute('SELECT * FROM links WHERE user_id=?', (id, )).fetchall())

async def get_excel(id, sip, password):
  workbook = xlsxwriter.Workbook(f'temp/{id}.xlsx')
  worksheet = workbook.add_worksheet()
  worksheet.write('A1', 'Имя')
  worksheet.write('B1', 'Ссылка')
  worksheet.write('C1', 'Назначение')
  worksheet.write('D1', 'Цена рекламы')
  worksheet.write('E1', 'Канал')
  worksheet.write('F1', 'Кол-во переходов')
  worksheet.write('G1', 'Цена клика')
  data = get_links_by_token(id)
  opens = await open_counts_all(sip, password, id)
  line = 2
  open_index = 0
  for item in data:
    worksheet.write(f'A{line}', f'{item[1]}')
    worksheet.write(f'B{line}', f'https://{sip}{item[2]}')
    worksheet.write(f'C{line}', f'{item[3]}')
    worksheet.write(f'D{line}', f'{item[4]}')
    worksheet.write(f'E{line}', f'{item[5]}')
    worksheet.write(f'F{line}', f'{str(opens[open_index])}')
    if(item[4]!=0 and opens[open_index]!='0'):
      worksheet.write(f'G{line}', f'{round(item[4]/int(opens[open_index]), 2)}')
    else:
      worksheet.write(f'G{line}', f'0')
    line+=1
    open_index+=1
  workbook.close()
  
    
async def get_excel_posts(posts, user_id):
  workbook = xlsxwriter.Workbook(f'temp/{user_id}.xlsx')
  worksheet = workbook.add_worksheet()
  worksheet.write('A1', 'Заголовок')
  worksheet.write('B1', 'Тело')
  worksheet.write('C1', 'Цена')
  worksheet.write('D1', 'Старая цена')
  worksheet.write('E1', 'Артикул')
  line = 2
  for item in posts:
    worksheet.write(f'A{line}', f'{item[2]}')
    worksheet.write(f'B{line}', f'{item[3]}')
    worksheet.write(f'C{line}', f'{item[4]}')
    worksheet.write(f'D{line}', f'{item[5]}')
    worksheet.write(f'E{line}', f'{item[6]}')
    line+=1
  workbook.close()


def get_user(id):
  info = cur.execute('SELECT * FROM users WHERE user_id=?', (id, )).fetchone()
  return info

def get_link(token):
  info = cur.execute('SELECT * FROM links WHERE token=?', (token, )).fetchone()
  return info

def get_links_by_token(id):
  info = cur.execute('SELECT * FROM links WHERE user_id=?', (id, )).fetchall()
  return info

def is_admin(id):
  info = cur.execute('SELECT * FROM users WHERE user_id=?', (id, )).fetchone()
  if(info[3]!=1):
    return False
  else:
    return True

def gen_txt_usernames():
  info = cur.execute('SELECT username FROM users').fetchall()
  f = open('temp/users.txt', 'w')
  for i in range(0, len(info)):
    f.write('@'+info[i][0] + '\n')
  f.close()

def gen_txt_ids():
  info = cur.execute('SELECT user_id FROM users').fetchall()
  f = open('temp/ids.txt', 'w')
  for i in range(0, len(info)):
    f.write(str(info[i][0]) + '\n')
  f.close()



def add_admin(id):
  if(check_exist(id)!=False):
    sql = ''' UPDATE users
              SET role = ?
              WHERE user_id = ?'''
    cur.execute(sql, [1,id])
    conn.commit()
    return True
  else:
    return False

def del_admin(id):
  if(check_exist(id)!=False):
    sql = ''' UPDATE users
              SET role = ?
              WHERE user_id = ?'''
    cur.execute(sql, [0,id])
    conn.commit()
    return True
  else:
    return False

def get_admins():
  info = cur.execute('SELECT user_id FROM users WHERE role=?', (1, )).fetchall()
  return info