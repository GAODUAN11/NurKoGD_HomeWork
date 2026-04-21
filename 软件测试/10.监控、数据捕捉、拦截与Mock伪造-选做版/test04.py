# test04_practice4_auth.py
import sys, re
from playwright.sync_api import sync_playwright
from playwright.sync_api import expect

def test_auth_matrix(role: str):
    print(f"🧪 测试角色: {role}")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        def handle_admin(route):
            headers = {**route.request.headers, "Authorization": f"Bearer {role}_token"}
            if role == "admin":
                route.fulfill(status=200, json={"role": "admin"})
            else:
                # ✅ 修复：用 body 而不是 text
                route.fulfill(status=403, body="Forbidden")

        page.route("**/api/admin/info", handle_admin)
        page.goto("http://localhost:8000/10.Mock_API_Practice.html")
        page.get_by_role("button", name=re.compile(r"获取管理信息")).click()

        if role == "admin":
            expect(page.locator("#admin-content")).to_be_visible()
            expect(page.locator("#auth-error")).not_to_be_visible()
        else:
            expect(page.locator("#admin-content")).not_to_be_visible()
            expect(page.locator("#auth-error")).to_be_visible()

        page.wait_for_timeout(3000)
        browser.close()

if __name__ == "__main__":
    role = sys.argv[1] if len(sys.argv) > 1 else "admin"
    if role not in ["admin", "guest"]:
        print("Usage: python test04.py [admin|guest]")
        sys.exit(1)
    test_auth_matrix(role)