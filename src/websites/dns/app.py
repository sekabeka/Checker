import re
import logging

from playwright.async_api import (
    BrowserContext,
)
from typing import (
    List,
    AsyncGenerator,
    Any,
)

logging.basicConfig(filemode='w', filename='src/logs/dns.log', encoding='utf-8', level=logging.DEBUG)

class DNS:
    def __init__(
        self,
        contexts: List[BrowserContext]
    ):
        self.contexts = contexts
        self.context_generator = self.__context_generator__()

    async def __context_generator__(self) -> AsyncGenerator[Any, BrowserContext]:
        while True:
            for context in self.contexts:
                yield context

    async def get_price(self, url: str):
        try:
            context: BrowserContext = await anext(self.context_generator)
            page = await context.new_page()
            async with page.expect_response(re.compile(r"https://www\.dns-shop\.ru/pwa/pwa/get-product/\?id=.+"), timeout=1000*10) as wait:
                await page.goto(url)
            response = await wait.value
            data = await response.json()
            await context.clear_cookies()
            await page.close()
            price = data['data']['price']
            return price
        except Exception as e:
            logging.error(e, stack_info=True)
        finally:
            await page.close()
            await context.clear_cookies()

