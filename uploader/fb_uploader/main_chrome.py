"""
Facebook平台视频上传核心实现
"""
import asyncio
import json
import logging
import os
from pathlib import Path
from datetime import datetime
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class FacebookVideo:
    """
    Facebook视频上传器类
    
    Args:
        title (str): 视频标题
        video_path (str): 视频文件路径
        tags (str): 话题标签，多个标签用空格分隔
        publish_time (int): 定时发布时间戳，0表示立即发布
        cookie_path (str): Cookie文件路径
        **platform_specific_args: 平台特定参数
    """
    
    def __init__(self, title, video_path, tags, publish_time, cookie_path, **kwargs):
        self.title = title
        self.video_path = video_path
        self.tags = tags
        self.publish_time = publish_time
        self.cookie_path = cookie_path
        self.browser = None
        self.page = None
        # 初始化平台特定参数
        self.platform_specific_params = kwargs
    
    async def init_browser(self):
        """
        初始化浏览器实例
        """
        try:
            playwright = await async_playwright().start()
            # 可配置无头/有头模式
            headless = os.environ.get('HEADLESS', 'false').lower() == 'true'
            self.browser = await playwright.chromium.launch(
                headless=headless,
                args=[
                    '--no-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-gpu',
                    '--ignore-certificate-errors'
                ]
            )
            self.page = await self.browser.new_page(
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            )
            logger.info("浏览器初始化成功")
        except Exception as e:
            logger.error(f"浏览器初始化失败: {str(e)}")
            raise
    
    async def load_cookie(self):
        """
        加载Cookie文件
        """
        try:
            # 先导航到平台主页再加载Cookie
            await self.page.goto('https://www.facebook.com')
            
            if os.path.exists(self.cookie_path):
                with open(self.cookie_path, 'r', encoding='utf-8') as f:
                    cookies = json.load(f)
                    await self.page.context.add_cookies(cookies)
                logger.info(f"成功加载Cookie文件: {self.cookie_path}")
            else:
                logger.warning(f"Cookie文件不存在: {self.cookie_path}")
                raise FileNotFoundError(f"Cookie文件不存在: {self.cookie_path}")
        except Exception as e:
            logger.error(f"加载Cookie失败: {str(e)}")
            raise
    
    async def navigate_to_upload_page(self):
        """
        导航到视频上传页面
        """
        try:
            # 重新加载主页以应用Cookie
            await self.page.goto('https://www.facebook.com', wait_until='networkidle')
            
            # 点击上传按钮
            upload_button = await self.page.query_selector("//span[text()='Photo/Video']")
            if not upload_button:
                # 尝试使用页面上传按钮
                upload_button = await self.page.query_selector("//span[text()='Create Post']")
            
            if upload_button:
                await upload_button.click()
                logger.info("成功点击上传按钮")
            else:
                raise Exception("未找到上传按钮")
                
        except Exception as e:
            logger.error(f"导航到上传页面失败: {str(e)}")
            raise
    
    async def upload_video(self):
        """
        上传视频文件
        """
        try:
            # 确保视频文件存在
            if not os.path.exists(self.video_path):
                raise FileNotFoundError(f"视频文件不存在: {self.video_path}")
            
            # 上传文件
            file_input = await self.page.query_selector('input[type="file"]')
            if not file_input:
                raise Exception("未找到文件上传元素")
            
            await file_input.set_input_files(self.video_path)
            logger.info(f"开始上传视频: {self.video_path}")
            
            # 等待上传完成（这里需要根据平台特性自定义等待逻辑）
            await self.page.wait_for_selector('[aria-label="Add a description"]', timeout=300000)  # 5分钟超时
            logger.info("视频上传完成")
        except Exception as e:
            logger.error(f"视频上传失败: {str(e)}")
            raise
    
    async def set_video_info(self):
        """
        设置视频信息（标题、标签等）
        """
        try:
            # 设置标题和描述
            content_editable = await self.page.query_selector('[aria-label="Add a description"]')
            if content_editable:
                await content_editable.fill(f"{self.title}\n\n{self.tags}")
            
            logger.info(f"成功设置视频信息: 标题='{self.title}', 标签='{self.tags}'")
        except Exception as e:
            logger.error(f"设置视频信息失败: {str(e)}")
            raise
    
    async def set_schedule_time(self):
        """
        设置定时发布时间
        """
        try:
            if self.publish_time <= 0:
                return  # 不需要定时发布
            
            # 点击定时发布按钮
            schedule_button = await self.page.query_selector("//span[text()='Schedule']")
            if not schedule_button:
                logger.warning("未找到定时发布按钮，跳过定时设置")
                return
            
            await schedule_button.click()
            
            # 解析时间戳并设置日期时间（这里需要根据平台的时间选择器特性自定义）
            publish_datetime = datetime.fromtimestamp(self.publish_time)
            
            # 示例：设置日期和时间
            await self.page.fill('[aria-label="Date"]', publish_datetime.strftime('%Y-%m-%d'))
            await self.page.fill('[aria-label="Time"]', publish_datetime.strftime('%H:%M'))
            
            logger.info(f"成功设置定时发布时间: {publish_datetime}")
        except Exception as e:
            logger.error(f"设置定时发布时间失败: {str(e)}")
            raise
    
    async def set_platform_specific_info(self):
        """
        设置平台特定信息
        """
        try:
            # 根据平台特定参数设置额外信息
            # 例如：商品链接、封面选择、分类设置等
            if self.platform_specific_params:
                logger.info(f"应用平台特定参数: {self.platform_specific_params}")
                # 这里添加平台特定的设置逻辑
        except Exception as e:
            logger.error(f"设置平台特定信息失败: {str(e)}")
            raise
    
    async def publish(self):
        """
        发布视频
        """
        try:
            # 点击发布按钮
            publish_button = await self.page.query_selector("//span[text()='Post']")
            if not publish_button:
                # 尝试查找定时发布按钮
                publish_button = await self.page.query_selector("//span[text()='Schedule Post']")
            
            if not publish_button:
                raise Exception("未找到发布按钮")
            
            # 等待发布完成（这里需要根据平台特性自定义等待逻辑）
            async with self.page.expect_navigation(timeout=300000):
                await publish_button.click()
            
            logger.info(f"视频发布成功: {self.title}")
        except Exception as e:
            logger.error(f"视频发布失败: {str(e)}")
            raise
    
    async def close_browser(self):
        """
        关闭浏览器
        """
        try:
            if self.browser:
                await self.browser.close()
                logger.info("浏览器已关闭")
        except Exception as e:
            logger.error(f"关闭浏览器失败: {str(e)}")
    
    async def main(self):
        """
        主入口函数，协调整个上传流程
        """
        try:
            # 初始化浏览器
            await self.init_browser()
            
            # 加载Cookie
            await self.load_cookie()
            
            # 导航到上传页面
            await self.navigate_to_upload_page()
            
            # 上传视频
            await self.upload_video()
            
            # 设置视频信息（标题、标签等）
            await self.set_video_info()
            
            # 设置定时发布（如果需要）
            if self.publish_time > 0:
                await self.set_schedule_time()
            
            # 设置平台特定信息
            await self.set_platform_specific_info()
            
            # 发布视频
            await self.publish()
            
            logger.info(f"✅ 视频发布成功: {self.title}")
            return True
        except Exception as e:
            logger.error(f"❌ 视频发布失败: {str(e)}")
            raise
        finally:
            # 关闭浏览器
            await self.close_browser()

# 主函数调用示例
async def run_upload(title, video_path, tags, publish_time, cookie_path, **kwargs):
    """
    运行上传任务
    
    Args:
        title (str): 视频标题
        video_path (str): 视频文件路径
        tags (str): 标签
        publish_time (int): 发布时间戳
        cookie_path (str): Cookie路径
        **kwargs: 额外参数
    """
    uploader = FacebookVideo(title, video_path, tags, publish_time, cookie_path, **kwargs)
    return await uploader.main()

if __name__ == "__main__":
    # 示例运行代码
    asyncio.run(run_upload(
        "测试视频",
        "videos/demo.mp4",
        "测试 标签",
        0,  # 立即发布
        "cookies/fb_cookie.json"
    ))
