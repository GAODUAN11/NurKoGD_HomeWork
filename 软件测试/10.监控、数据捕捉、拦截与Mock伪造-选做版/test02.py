# test02_practice2_balance.py
from playwright.sync_api import sync_playwright
from playwright.sync_api import expect

def test_balance_mock_and_assert():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        def mock_balance(route):
            route.fulfill(json={"amount": -100.0, "currency": "CNY"})

        # 拦截生产环境余额接口
        page.route("https://api.production.com/api/user/balance", mock_balance)
        page.goto("http://localhost:8000/10.Mock_API_Practice.html")

        with page.expect_response("https://api.production.com/api/user/balance") as response_info:
            page.get_by_role("button", name="刷新余额").click()

        expect(page.locator("#balance-warning")).to_be_visible()
        # ✅ 修复：使用 to_contain_class 或完整类名
        expect(page.locator("#balance-card")).to_contain_class("danger-ui")

        data = response_info.value.json()
        assert data["amount"] == -100.0
        assert data["currency"] == "CNY"

        browser.close()

if __name__ == "__main__":
    test_balance_mock_and_assert()