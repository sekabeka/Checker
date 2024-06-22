import lxml
import asyncio

from dataclasses import dataclass
from aiohttp import ClientSession
from playwright.async_api import BrowserContext
from bs4 import BeautifulSoup

@dataclass
class DnsChecker:
    context: BrowserContext
    url: str
    session: ClientSession
    proxy: str

    async def cookiesGenerator(self):
        while True:
            page = await self.context.new_page()
            try:
                await page.goto(self.url)
            except:
                pass
            while True:
                await page.wait_for_timeout(1000)
                cookies = {
                    item['name'] : item['value'] for item in (await self.context.cookies())
                }
                if 'qrator_jsid' in cookies:
                    yield cookies
                    break
            await self.context.clear_cookies()
            await page.close()
    
    async def data(self):
        self.generator = self.cookiesGenerator()
        cookies = await anext(self.generator)
        async with self.session.get(self.url, cookies=cookies, proxy=self.proxy) as response:
            soup = BeautifulSoup(await response.text(), 'lxml')
            self.data_id = soup.find('div', class_='container product-card')['data-product-card']
        api_url = f"https://www.dns-shop.ru/pwa/pwa/get-product/?id={self.data_id}"
        print (api_url)
        while True:
            cookies = await anext(self.generator)
            while True:
                async with self.session.get(api_url, cookies=cookies, proxy=self.proxy) as response:
                    if response.ok:
                        data = await response.json()
                        print (data['data']['price'])
                    else:
                        print ('continue...')
                        continue
                    await asyncio.sleep(10)


