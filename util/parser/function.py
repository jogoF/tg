from aiohttp import ClientSession
import json
import math
import aiofiles
from uuid import uuid4
import asyncio
from PIL import Image


wb_headers = {
        'Accept': '*/*',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Origin': 'https://www.wildberries.by',
        'Referer': 'https://www.wildberries.by/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
        'sec-ch-ua': 'Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': 'macOS',
    }

locations = {
    'MOSCOW_NORTH': '80,38,83,4,64,33,68,70,30,40,86,69,1,31,66,110,48,22,114',
    'MOSCOW_SOUTH': '80,38,83,4,64,33,68,70,30,40,86,75,69,1,31,66,110,48,22,71,114',
    'VLADIVASTOK': '80,38,4,64,30,40,86,69,1,66,48,112,114',
    'EKATERENBURG': '80,38,83,4,64,33,68,70,30,40,86,69,1,31,66,110,48,22,114',
    'KAZAN': '80,38,83,4,64,33,68,70,30,40,86,69,1,31,66,110,48,22,114',
    'KRASNODAR': '80,38,83,4,64,33,68,70,30,40,86,69,1,31,66,110,48,22,114', 
    'NOVOSIBIRSK': '80,38,83,4,64,33,68,70,30,40,86,69,1,31,66,48,22,114',
    'SANKT_PETERBURG': '80,38,83,4,64,33,68,70,30,40,86,69,1,31,66,48,22,114',
    'VLADIKAVKAZ': '80,38,83,4,64,33,68,70,30,40,86,69,1,31,66,110,48,22,114'
}

async def wb_pos_async(request, article, region):
    region = locations[region]
    page = 1
    async with ClientSession() as session:
        while True:
            url = f'https://search.wb.ru/exactmatch/ru/common/v4/search?TestGroup=no_test&TestID=no_test&appType=1&curr=rub&dest=-1257786&page={page}&query={request}&regions={region}&resultset=catalog&sort=popular&spp=35&suppressSpellcheck=false'
            async with session.get(url=url, headers=wb_headers) as response:
                text = await response.text()
                if len(text) < 100:
                    break
                if str(article) in text:
                    return page
                page = page + 1



async def download_photo_async(url, image_count, needed_count):
    path = []
    step = round(image_count/needed_count)
    async with ClientSession() as session:
        base_url = '/'.join(url.split('/')[:-3]) + '/'
        for i in range(1,image_count+1,step):
            image_url = base_url+f"images/c516x688/{i}.webp"
            async with session.get(url=image_url, headers=wb_headers) as response:
                file_path = f"temp/{uuid4()}"
                print(image_url)
                async with aiofiles.open(file_path+".webp", 'wb') as file:
                    await file.write(await response.read())
                    webp_image = Image.open(file_path+".webp")
                    png_image = webp_image.convert("RGBA")
                    png_image.save(file_path+".png", "PNG")
                    path.append(file_path)
    return path


async def wb_image_count_async(url):
    base_url = '/'.join(url.split('/')[:-3]) + '/'
    async with ClientSession() as session:
        for i in range(1,100):
            image_url = base_url+f"images/c516x688/{i}.webp"
            async with session.get(url=image_url, headers=wb_headers) as response:
                if response.status == 404:
                    return i-1



                
async def find_wb_async(article, needed_count):
    async with ClientSession() as session:
        for i in ["01","03","05", "07","09", "10", "11", "12", "02", "04", "06", "08", "13"]:
            for vol in range(2,5):
                for part in range(4,7):
                    url = f"https://basket-{i}.wb.ru/vol{str(article)[:vol]}/part{str(article)[:part]}/{article}/info/ru/card.json"
                    async with session.get(url=url, headers=wb_headers) as response:
                        if len(await response.text())>300:
                            json_object = await response.json()
                            name = json_object['imt_name']
                            description = json_object['description']
                            image_count = await wb_image_count_async(url)
                            paths = await download_photo_async(url, image_count, needed_count)
                            purl = f"https://card.wb.ru/cards/detail?appType=1&curr=rub&spp=31&nm={article}"
                            price = None
                            async with session.get(url=purl, headers=wb_headers) as response:
                                json_object = await response.json()
                                price = str(json_object['data']['products'][0]['salePriceU'])[:-2]
                                oldprice = str(json_object['data']['products'][0]['priceU'])[:-2]
                            return [name, description, price, oldprice, paths]
        return None


if __name__ == "__main__":
    print(asyncio.run(find_wb_async(133551332, 4)))
