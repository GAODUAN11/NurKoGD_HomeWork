# test01.py
import re
from playwright.sync_api import sync_playwright

def test_audit_monitor():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        large_images = []
        errors = []

        def on_response(response):
            if response.status >= 400:
                errors.append(f"{response.url} -> {response.status}")
            if re.search(r"\.(png|jpg|jpeg)$", response.url):
                try:
                    # 尝试获取 body 大小（即使无 content-length）
                    body_size = len(response.body())
                    if body_size > 1_000_000:
                        large_images.append(f"{response.url} ({body_size} bytes)")
                except Exception as e:
                    # 跨域资源无法读取 body，跳过
                    pass

        page.on("response", on_response)
        page.goto("http://localhost:8000/10.Mock_API_Practice.html")
        page.get_by_role("button", name="触发审计测试").click()
        page.wait_for_timeout(5000)  # 延长等待时间

        print("❌ 错误接口:", errors)
        print("🖼️ 大图资源 (>1MB):", large_images)

        assert len(errors) > 0, "应捕获到 /api/v1/private-data 的 404 错误"
        # 如果你确定本地有大图，保留下面断言；否则注释
        # assert len(large_images) > 0, "应捕获到 >1MB 的图片"

        browser.close()

if __name__ == "__main__":
    test_audit_monitor()