import logging
import asyncio
import random
import lxml

import aiogram.utils.formatting as fm

from playwright.async_api import async_playwright
from dataclasses import dataclass, field
from aiohttp import ClientSession
from bs4 import BeautifulSoup
from typing import List
from aiogram import Bot

from functions import get_proxy
from database import db
from bot.keyboards import (
    get_item_keyboard
)

logger = logging.getLogger('dns_checker')

@dataclass
class DNS:
    bot: Bot
    delay: int = 60
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

    async def work_with_data_id(self, url: str, obj: dict, session: ClientSession):
        while True:
            async with session.get(url, cookies=self.cookies, proxy=self.proxy) as response:
                if response.ok:
                    soup = BeautifulSoup(await response.text(), 'lxml')
                    data_id = soup.find('div', class_='container product-card')['data-product-card']
                    api_url = f"https://www.dns-shop.ru/pwa/pwa/get-product/?id={data_id}"
                    obj['api_url'] = api_url
                    await db['users'].update_one(
                        {"data.tracked_items.url": url},
                        {"$set" : {"data.tracked_items.$.api_url" : api_url}}
                    )
                    return api_url
                else:
                    logger.debug('change cookies and proxy in data_id function')
            self.cookies, self.proxy = await self.get_cookies()

    async def work_with_api_url(self, api_url: str, obj: dict, session: ClientSession):
        while True:
            async with session.get(api_url, cookies=self.cookies, proxy=self.proxy) as response:
                if response.ok:
                    data = await response.json()
                    actual_price = data['data']['price']
                    old_price = obj['price']
                    obj['price'] = actual_price
                    await db['users'].update_one(
                        {"data.tracked_items.api_url": api_url},
                        {"$set" : {"data.tracked_items.$.price" : actual_price}}
                    )
                    if actual_price == old_price:
                        #return None
                        return (old_price, actual_price)
                    else:
                        return (old_price, actual_price)
                else:
                    logger.debug('change cookies and proxy in api_url function')
            self.cookies, self.proxy = await self.get_cookies()
        

    async def parse(self):
        self.set_proxies_for_playwright_and_aiohttp()
        async with async_playwright() as p:
            browser = await p.firefox.launch()
            self.contexts = [
                await browser.new_context(proxy=proxy) for proxy in self.proxies_for_playwright
            ]
            logger.debug('successfully initialize contexts')
            async with ClientSession() as session:
                while True:
                    self.cookies, self.proxy = await self.get_cookies()
                    async for user in db['users'].find({}):
                        for obj in user['data']['tracked_items']:
                            url = obj['url']
                            api_url = obj['api_url']
                            if api_url is None:
                                api_url = await self.work_with_data_id(url, obj, session)
                            result = await self.work_with_api_url(api_url, obj, session)
                            if result is not None:
                                await self.push_message(user['data']['id'], url, result)
                            await asyncio.sleep(random.randint(1, 2))
                        logger.debug('we send all messages for {}'.format(user['data']['name']))
                    logger.debug('we send all messages. sleeping {} seconds...'.format(self.delay))

                    await asyncio.sleep(self.delay)
    
    async def push_message(self, _id: str, url:str, prices: tuple):
        old_price, actual_price = prices
        if old_price == 0:
            return
        await self.bot.send_message(
            _id,
            **fm.as_list(
                fm.Bold('Цена изменилась!'),
                fm.as_key_value(
                    'Отслеживаемый товар',
                    fm.TextLink(
                        'клац!',
                        url=url
                    )
                ),
                fm.as_key_value(
                    fm.Bold('Старая цена'),
                    str(old_price) + ' руб.'
                ),
                fm.as_key_value(
                    fm.Bold('Новая цена'),
                    str(actual_price) + ' руб.'
                ),
                sep='\n\n'
            ).as_kwargs(),
            reply_markup=get_item_keyboard(url)
        )

    
    
