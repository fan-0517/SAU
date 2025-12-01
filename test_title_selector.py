from myUtils.platform_configs import PLATFORM_CONFIGS
from playwright.async_api import async_playwright
import asyncio

async def test_douyin_title_selector():
    """测试抖音标题选择器是否能正确定位到唯一的作品标题输入框"""
    # 获取抖音平台配置
    douyin_config = PLATFORM_CONFIGS['douyin']
    title_selectors = douyin_config['selectors']['title_editor']
    
    print("抖音标题选择器列表:")
    for selector in title_selectors:
        print(f"  - {selector}")
    
    # 使用Playwright测试选择器
    async with async_playwright() as p:
        # 启动浏览器（无头模式）
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        
        try:
            # 访问抖音创作服务平台
            await page.goto("https://creator.douyin.com/creator-micro/content/upload")
            await page.wait_for_load_state("networkidle")
            await page.wait_for_timeout(2000)  # 等待页面加载完成
            
            print("\n测试选择器匹配情况:")
            for selector in title_selectors:
                try:
                    # 使用locator查找元素并获取计数
                    count = await page.locator(selector).count()
                    print(f"  选择器 '{selector}' 匹配到 {count} 个元素")
                    
                    if count == 1:
                        print(f"  ✅ 选择器 '{selector}' 定位成功，匹配到唯一元素")
                        # 测试点击操作
                        await page.locator(selector).click()
                        print(f"  ✅ 选择器 '{selector}' 点击成功")
                        # 测试输入操作
                        await page.keyboard.insert_text("测试标题")
                        await page.wait_for_timeout(500)
                        # 获取输入的文本验证
                        input_value = await page.locator(selector).input_value()
                        if input_value == "测试标题":
                            print(f"  ✅ 选择器 '{selector}' 输入成功，当前值: '{input_value}'")
                        else:
                            print(f"  ❌ 选择器 '{selector}' 输入失败，当前值: '{input_value}'")
                        # 清空输入
                        await page.keyboard.press("Control+A")
                        await page.keyboard.press("Delete")
                        return True
                except Exception as e:
                    print(f"  ❌ 选择器 '{selector}' 测试失败: {str(e)}")
            
            print("\n❌ 所有标题选择器测试失败，未能定位到唯一的作品标题输入框")
            return False
        finally:
            await context.close()
            await browser.close()

if __name__ == "__main__":
    asyncio.run(test_douyin_title_selector())
