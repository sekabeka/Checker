import asyncio
import lxml
import random

from dataclasses import dataclass, field

from bs4 import BeautifulSoup
from aiohttp import ClientSession
from playwright.async_api import async_playwright, BrowserContext
from typing import List, Dict

from functions import get_proxy

@dataclass
class dns_object:
    url: str
    price: int = 0
    api_url: str = None



@dataclass
class DNS:
    objects: List[dns_object]
    proxylist: List[dict] = field(default_factory=get_proxy)
    
    def set_proxies_for_playwright_and_aiohttp(self):
        self.proxies_for_playwright = [
            {
                'server' : proxy['host'] + ':' + proxy['port'],
                'username' : proxy['username'],
                'password' : proxy['password']
            } for proxy in self.proxylist
        ]
        self.proxies_for_aiohttp = [
            "http://{}:{}@{}".format(d['username'], d['password'], d['server']) for d in self.proxies_for_playwright
        ]
    
    async def get_cookies(self):
        context = random.choice(self.contexts)
        idx = self.contexts.index(context)
        page = await context.new_page()
        try:
            await page.goto('https://www.dns-shop.ru')
        except:
            pass
        while True:
            await page.wait_for_timeout(1000)
            cookies = {
                i['name'] : i['value'] for i in (await context.cookies())
            }
            if 'qrator_jsid' in cookies:
                await context.clear_cookies()
                await page.close()
                return cookies, self.proxies_for_aiohttp[idx]

    
        

    async def parse(self):
        self.set_proxies_for_playwright_and_aiohttp()
        async with async_playwright() as p:
            browser = await p.firefox.launch()
            self.contexts = [
                await browser.new_context(proxy=proxy) for proxy in self.proxies_for_playwright
            ]
            async with ClientSession() as session:
                while True:
                    cookies, proxy = await self.get_cookies()
                    for obj in self.objects:
                        url = obj.url
                        api_url = obj.api_url
                        if api_url is None:
                            while True:
                                async with session.get(url, cookies=cookies, proxy=proxy) as response:
                                    if response.ok:
                                        soup = BeautifulSoup(await response.text(), 'lxml')
                                        data_id = soup.find('div', class_='container product-card')['data-product-card']
                                        api_url = f"https://www.dns-shop.ru/pwa/pwa/get-product/?id={data_id}"
                                        obj.api_url = api_url
                                        break
                                    else:
                                        print ('change cookies and proxy')
                                cookies, proxy = await self.get_cookies()
                        while True:
                            async with session.get(api_url, cookies=cookies, proxy=proxy) as response:
                                if response.ok:
                                    data = await response.json()
                                    actual_price = data['data']['price']
                                    old_price = obj.price
                                    print (actual_price, api_url)
                                    if actual_price == old_price:
                                        print ('не изменилась')
                                    else:
                                        print ('изменилась')
                                    obj.price = actual_price
                                    break
                                else:
                                    print ('change in api')
                            cookies, proxy = await self.get_cookies()

                    await asyncio.sleep(60)




    
    
