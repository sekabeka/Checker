import asyncio
import aiohttp
import os

from dotenv import load_dotenv
from playwright.async_api import async_playwright
from sites.dns import DnsChecker

load_dotenv()

async def main():
    proxy = {
        'username' : os.getenv('USERNAME'),
        'password' : os.getenv('PASSWORD'),
        'server' : os.getenv('SERVER')
    }
    async with async_playwright() as p:
        browser = await p.firefox.launch()
        context = await browser.new_context(
            proxy=proxy
        )
        async with aiohttp.ClientSession() as session:
            first = DnsChecker(
                context,
                'https://www.dns-shop.ru/product/adaa3dcbe745ed20/videokarta-msi-geforce-rtx-3050-lp-oc-geforce-rtx-3050-lp-6g-oc/',
                session,
                "http://{}:{}@{}".format(proxy['username'], proxy['password'], proxy['server'])
            )
            await first.data()



asyncio.run(main())
