# test05_practice5_semi_mock.py
from playwright.sync_api import sync_playwright
from playwright.sync_api import expect

def test_semi_mock_long_username():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        def handle_users(route):
            real_res = route.fetch()
            users = real_res.json()
            users[0]["name"] = "Mocked_User_" + "X" * 87  # 总长 100
            route.fulfill(
                status=real_res.status,
                headers=real_res.headers,
                json=users
            )

        page.route("https://jsonplaceholder.typicode.com/users", handle_users)
        page.goto("http://localhost:8000/10.Mock_API_Practice.html")
        page.get_by_role("button", name="获取真实用户列表").click()
        page.wait_for_selector("#user-list li", timeout=10000)

        first_user = page.locator("#user-list li").first
        expect(first_user).to_contain_text("Mocked_User_XXXXXXXXXX")  # 验证篡改成功

        browser.close()

if __name__ == "__main__":
    test_semi_mock_long_username()