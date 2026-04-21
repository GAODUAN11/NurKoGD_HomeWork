# test03_practice3_redirect.py
from playwright.sync_api import sync_playwright

def test_redirect_production_to_test():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        def redirect_route(route):
            original = route.request.url
            new_url = original.replace("api.production.com", "api.test-env.com")
            print(f"✅ 拦截成功！重写 URL:\n  原始: {original}\n  新URL: {new_url}")
            route.continue_(url=new_url)

        page.route("https://api.production.com/**/*", redirect_route)
        page.goto("http://localhost:8000/10.Mock_API_Practice.html")

        # 触发请求（来自 checkAuth 函数中的 fetch）
        page.evaluate("fetch('https://api.production.com/v1/login').catch(()=>{})")
        page.wait_for_timeout(1000)

        browser.close()

if __name__ == "__main__":
    test_redirect_production_to_test()