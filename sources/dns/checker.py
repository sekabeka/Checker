import asyncio

from playwright.async_api import Browser, BrowserContext
from dataclasses import dataclass
from bs4 import BeautifulSoup
from aiohttp import ClientSession
from typing import List, Dict, Tuple



@dataclass
class dns_checker:
    proxylist: List[Dict]
    browser: Browser
    session: ClientSession
    tasks: asyncio.Queue
    pairs: List[Tuple]
    url: str = 'https://www.dns-shop.ru'

    async def update_cookies_in_one_context(self, context: BrowserContext):
        while True:
            page = await context.new_page()
            try:
                await page.goto(self.url)
            except:
                pass
            while True:
                await page.wait_for_timeout(1000)
                cookies = {
                    item['name'] : item['value'] for item in (await context.cookies())
                }
                if 'qrator_jsid' in cookies:
                    await context.clear_cookies()
                    await page.close()
                    return cookies

    

    
    async def pairs(self, contexts: List[BrowserContext]):
        while True:
            tasks = [
                asyncio.create_task(self.update_cookies(context)) for context in contexts
            ]
            self.pairs = await asyncio.gather(*tasks)

    async def add_task(self, url: str):
        pass
                
        
    
    async def run(self):
        contexts = [
            await self.browser.new_context(proxy=proxy) for proxy in self.proxylist
        ]

