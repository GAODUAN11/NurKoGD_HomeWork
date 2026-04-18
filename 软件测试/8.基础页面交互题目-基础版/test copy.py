from playwright.sync_api import sync_playwright, expect

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=200)
        page = browser.new_page()
        page.goto("http://localhost:8000/8.actions_practice.html")
        page.wait_for_load_state("networkidle")

        # 1. 输入账号
        page.locator("#login-account").fill("test_user")
        # 2. 勾选记住我
        page.locator("#remember-me").check()
        # 3. 选择角色
        page.locator("#user-role").select_option("admin")
        # 4. 点击登录
        login_btn = page.get_by_role("button", name="立即登录")
        login_btn.click()

        print("✅ 登录流程完成！应弹出'登录成功'提示，按回车关闭。")
        input()
        browser.close()

if __name__ == "__main__":
    main()