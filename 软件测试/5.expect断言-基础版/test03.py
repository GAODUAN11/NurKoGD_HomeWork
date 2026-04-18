from playwright.sync_api import sync_playwright, expect
import re
def test_report_generation(page):
    page.goto("http://localhost:8000/5.expect_practice.html")
    
    page.get_by_role("button", name="生成报告").click()
    
    # 1. 加载器消失
    expect(page.locator(".loading-spinner")).to_be_hidden()
    
    # 2. 按钮文本变为“下载报告”
    expect(page.locator("#report-btn")).to_have_text("下载报告")
    
    # 3. 按钮拥有 active 类（正则匹配）
    expect(page.locator("#report-btn")).to_have_class(re.compile(r"active"))