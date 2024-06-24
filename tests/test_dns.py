import asyncio
import pytest
import pytest_asyncio
import requests
import re
import random

from playwright.async_api import async_playwright
from src.websites.dns.app import DNS
from src.main import get_proxies_for_playwright

def get_test_links():
    response = requests.get(
        "https://www.dns-shop.ru/products3.xml"
    )
    return re.findall(
        r"<loc>(.*?)</loc>",
        response.text
    )

async def m():
    async with async_playwright() as p:
        browser = await p.firefox.launch()
        contexts = [
            await browser.new_context(proxy=proxy) for proxy in get_proxies_for_playwright()
        ]
        obj = DNS(contexts)
        urls = get_test_links()
        random.shuffle(urls)
        for url in urls:
            await obj.getPrice(url)


@pytest.mark.asyncio
async def test_getPrice():
    await m()