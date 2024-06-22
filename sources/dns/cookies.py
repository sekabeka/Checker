from playwright.async_api import BrowserContext
from typing import Dict, AsyncGenerator, Any


url = 'https://www.dns-shop.ru'


async def async_generator_cookies(context: BrowserContext) -> AsyncGenerator[Any, Dict]:
    while True:
        page = await context.new_page()
        try:
            await page.goto(url)
        except:
            pass
        while True:
            await page.wait_for_timeout(1000)
            cookies = {
                item['name'] : item['value'] for item in (await context.cookies())
            }
            if 'qrator_jsid' in cookies:
                yield cookies
                break
        await context.clear_cookies()
        await page.close()


        