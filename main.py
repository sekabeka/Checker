import asyncio
import aiohttp

from playwright.async_api import async_playwright
from sites.dns import DnsChecker

async def main():
    proxy = {
        'username' : 'CWH2sr',
        'password' : 'HR8KMv',
        'server' : '185.128.213.216:9056'
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
