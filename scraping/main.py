import json
import csv
import asyncio
import aiohttp
import datetime
from bs4 import BeautifulSoup

async def get_page_data(session, url):
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36"
    }

    async with session.get(url=url, headers=headers) as response:
        response_text = await response.text()

        soup = BeautifulSoup(response_text, "html.parser")

        sweets_data = []

        for item in soup.select(".product-miniature.js-product-miniature"):
            sweets_title = item.select_one(".h3.product-title a").text.strip()

            try:
                sweets_price = item.select_one(".product-price-and-shipping span.price").text.strip()
            except:
                sweets_price = "Нет цены"

            sweets_data.append(
                {
                    "sweets_title": sweets_title,
                    "sweets_price": sweets_price,
                }
            )

        return sweets_data

async def gather_data():
    async with aiohttp.ClientSession() as session:
        url = "https://www.lasoshhi.com.ua/ru/konfety-v-korobkakh/3-nabor-konfet-bazhayemo-sshastya-zhitomirskie-lasosshi-4823103001363.html"
        sweets_data = await get_page_data(session, url)
        return sweets_data

def main():
    sweets_data = asyncio.run(gather_data())
    cur_time = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M")

    with open(f"sweets_{cur_time}_async.json", "w", encoding="utf-8") as file:
        json.dump(sweets_data, file, indent=4, ensure_ascii=False)

    with open(f"sweets_{cur_time}_async.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        writer.writerow(
            (
                "Название конфет",
                "Цена конфет",
            )
        )

        for sweet in sweets_data:
            writer.writerow(
                (
                    sweet["sweets_title"],
                    sweet["sweets_price"],
                )
            )

if __name__ == "__main__":
    main()
