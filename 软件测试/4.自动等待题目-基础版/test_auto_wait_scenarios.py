import pytest
from playwright.sync_api import sync_playwright, expect
import os

# 获取当前 HTML 文件的绝对路径
HTML_FILE = os.path.abspath("4.auto_wait_practice.html")
PAGE_URL = f"file://{HTML_FILE}"

def test_scenario_1_loading_overlay():
    """场景 1：消失的加载层 —— 验证 Receives Events 检查"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # headless=False 方便观察
        page = browser.new_page()
        page.goto(PAGE_URL)

        # 直接点击“详情”按钮（此时被 Loading 遮罩覆盖）
        # Playwright 会自动等待遮罩消失（Receives Events 检查通过）
        page.get_by_role("button", name="详情").click()

        # 验证操作成功
        expect(page.locator("#result")).to_have_text("操作结果：成功点击详情按钮！")

        browser.close()


def test_scenario_2_sliding_button():
    """场景 2：滑动的登录框 —— 验证 Stable 检查"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(PAGE_URL)

        # 触发动画：让按钮开始滑动
        page.get_by_role("button", name="开始滑动").click()

        # 立即尝试点击正在滑动的按钮
        # Playwright 会等待动画结束（元素稳定）后再点击
        page.get_by_role("button", name="滑动的登录").click()

        # 验证操作成功
        expect(page.locator("#result")).to_have_text("操作结果：成功点击移动中的按钮！")

        browser.close()
