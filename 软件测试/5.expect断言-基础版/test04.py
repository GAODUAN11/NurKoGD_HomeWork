from playwright.sync_api import sync_playwright, expect
import re

def test_skeleton_screen(page):
    page.goto("http://localhost:8000/5.expect_practice.html")
    buy_btn = page.locator("#buy-btn")
    
    # 1. 初始包含 skeleton 类
    expect(buy_btn).to_have_class(re.compile(r"skeleton"))
    
    # 2. 等待 5 秒后文本变为“立即购买”
    expect(buy_btn).to_have_text("立即购买", timeout=6000)
    
    # 3. 拥有 data-id="ITEM_999"
    expect(buy_btn).to_have_attribute("data-id", "ITEM_999")