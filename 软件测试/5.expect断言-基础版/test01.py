# test01.py
from playwright.sync_api import expect
import re

def test_login_success(page):
    # 使用本地 HTTP 服务器地址
    page.goto("http://localhost:8000/5.expect_practice.html")
    
    page.get_by_label("用户名").fill("admin")
    page.get_by_role("button", name="登录").click()
    
    # ✅ 现在 pushState 可以正常工作！
    expect(page).to_have_url(re.compile(r".*/dashboard$"))
    
    expect(page.locator("#user-name")).to_have_text("欢迎回来，测试员")