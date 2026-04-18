from playwright.sync_api import sync_playwright, expect
import re
def test_registration_button_enabled(page):
    page.goto("http://localhost:8000/5.expect_practice.html")
    
    reg_btn = page.locator("#reg-btn")
    agree_check = page.locator("#agree-check")
    
    # 1. 初始为禁用
    expect(reg_btn).to_be_disabled()
    
    # 2. 勾选协议
    agree_check.check()
    
    # 3. 按钮变为可用并点击
    expect(reg_btn).to_be_enabled()
    reg_btn.click()