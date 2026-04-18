from playwright.sync_api import expect


def test_profile_fields_soft_assert(page):
    page.goto("http://localhost:8000/5.expect_practice.html")

    errors = []
    checks = [
        ("#p-username", "张三"),
        ("#p-phone", "13800000000"),
        ("#p-email", "test@example.com"),
        ("#p-level", "V5"),
        ("#p-points", "100"),
    ]

    for selector, expected_text in checks:
        try:
            expect(page.locator(selector)).to_have_text(expected_text)
            print(f"[PASS] {selector} == {expected_text}")
        except AssertionError as exc:
            print(f"[FAIL] {selector} != {expected_text}")
            errors.append(f"{selector} 断言失败: {exc}")

        # 为了在 headed 模式下看清“失败后继续执行”的过程
        page.wait_for_timeout(300)

    assert not errors, "\n".join(errors)