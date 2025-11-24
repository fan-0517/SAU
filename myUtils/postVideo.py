import asyncio
from pathlib import Path

from conf import BASE_DIR
from uploader.douyin_uploader.main import DouYinVideo
from uploader.ks_uploader.main import KSVideo
from uploader.tk_uploader.main import TiktokVideo
from uploader.tencent_uploader.main import TencentVideo
from uploader.xiaohongshu_uploader.main import XiaoHongShuVideo
from utils.constant import TencentZoneTypes
from utils.files_times import generate_schedule_time_next_day


def post_video_tencent(title,files,tags,account_file,category=TencentZoneTypes.LIFESTYLE.value,enableTimer=False,videos_per_day = 1, daily_times=None,start_days = 0, is_draft=False):
    # 生成文件的完整路径
    account_file = [Path(BASE_DIR / "cookiesFile" / file) for file in account_file]
    files = [Path(BASE_DIR / "videoFile" / file) for file in files]
    if enableTimer:
        publish_datetimes = generate_schedule_time_next_day(len(files), videos_per_day, daily_times,start_days)
    else:
        publish_datetimes = [0 for i in range(len(files))]
    for index, file in enumerate(files):
        for cookie in account_file:
            print(f"文件路径{str(file)}")
            # 打印视频文件名、标题和 hashtag
            print(f"视频文件名：{file}")
            print(f"标题：{title}")
            print(f"Hashtag：{tags}")
            app = TencentVideo(title, str(file), tags, publish_datetimes[index], cookie, category, is_draft)
            asyncio.run(app.main(), debug=False)


def post_video_DouYin(title,files,tags,account_file,category=TencentZoneTypes.LIFESTYLE.value,enableTimer=False,videos_per_day = 1, daily_times=None,start_days = 0,
                      thumbnail_path = '',
                      productLink = '', productTitle = ''):
    # 生成文件的完整路径
    account_file = [Path(BASE_DIR / "cookiesFile" / file) for file in account_file]
    files = [Path(BASE_DIR / "videoFile" / file) for file in files]
    if enableTimer:
        publish_datetimes = generate_schedule_time_next_day(len(files), videos_per_day, daily_times,start_days)
    else:
        publish_datetimes = [0 for i in range(len(files))]
    for index, file in enumerate(files):
        for cookie in account_file:
            print(f"文件路径{str(file)}")
            # 打印视频文件名、标题和 hashtag
            print(f"视频文件名：{file}")
            print(f"标题：{title}")
            print(f"Hashtag：{tags}")
            app = DouYinVideo(title, str(file), tags, publish_datetimes[index], cookie, thumbnail_path, productLink, productTitle)
            asyncio.run(app.main(), debug=False)


def post_video_ks(title,files,tags,account_file,category=TencentZoneTypes.LIFESTYLE.value,enableTimer=False,videos_per_day = 1, daily_times=None,start_days = 0):
    # 生成文件的完整路径
    account_file = [Path(BASE_DIR / "cookiesFile" / file) for file in account_file]
    files = [Path(BASE_DIR / "videoFile" / file) for file in files]
    if enableTimer:
        publish_datetimes = generate_schedule_time_next_day(len(files), videos_per_day, daily_times,start_days)
    else:
        publish_datetimes = [0 for i in range(len(files))]
    for index, file in enumerate(files):
        for cookie in account_file:
            print(f"文件路径{str(file)}")
            # 打印视频文件名、标题和 hashtag
            print(f"视频文件名：{file}")
            print(f"标题：{title}")
            print(f"Hashtag：{tags}")
            app = KSVideo(title, str(file), tags, publish_datetimes[index], cookie)
            asyncio.run(app.main(), debug=False)

def post_video_xhs(title,files,tags,account_file,category=TencentZoneTypes.LIFESTYLE.value,enableTimer=False,videos_per_day = 1, daily_times=None,start_days = 0):
    # 生成文件的完整路径
    account_file = [Path(BASE_DIR / "cookiesFile" / file) for file in account_file]
    files = [Path(BASE_DIR / "videoFile" / file) for file in files]
    file_num = len(files)
    if enableTimer:
        publish_datetimes = generate_schedule_time_next_day(file_num, videos_per_day, daily_times,start_days)
    else:
        publish_datetimes = 0
    for index, file in enumerate(files):
        for cookie in account_file:
            # 打印视频文件名、标题和 hashtag
            print(f"视频文件名：{file}")
            print(f"标题：{title}")
            print(f"Hashtag：{tags}")
            app = XiaoHongShuVideo(title, file, tags, publish_datetimes, cookie)
            asyncio.run(app.main(), debug=False)



def post_video_TikTok(title, file_list, tags, account_list, schedule=None, schedule_date=None, schedule_time=None, thumbnail=None, enableTimer=False, videos_per_day=1, daily_times=None, start_days=0):
    try:
        # 批量发布模式（带enableTimer参数）
        if enableTimer is not None:
            # 生成发布时间列表
            if enableTimer:
                publish_datetimes = generate_schedule_time_next_day(len(file_list), videos_per_day, daily_times, start_days)
            else:
                publish_datetimes = [0] * len(file_list)
            
            for index, file in enumerate(file_list):
                for account in account_list:
                    file_path = os.path.join("upload", file)
                    account_file = os.path.join("cookies", "tk_uploader", f"{account}.json")
                    
                    # 检查账号cookie是否有效
                    if not os.path.exists(account_file):
                        logger.error(f"账号cookie文件不存在: {account_file}")
                        continue
                    
                    # 设置封面文件
                    thumbnail_path = None
                    if os.path.exists(file_path.replace('.mp4', '.png')):
                        thumbnail_path = file_path.replace('.mp4', '.png')
                    
                    # 初始化TikTok视频上传类
                    app = TiktokVideo(title, file_path, tags, publish_datetimes[index], account_file, thumbnail_path)
                    try:
                        # 执行上传
                        asyncio.run(app.main())
                        logger.info(f"TikTok视频发布成功: {file} - {account}")
                    except Exception as e:
                        logger.error(f"TikTok视频发布失败: {str(e)}")
        # 单视频发布模式（带schedule参数）
        else:
            # 构建发布时间
            schedule_datetime = 0
            if schedule == 1:
                schedule_datetime = datetime.strptime(f"{schedule_date} {schedule_time}", "%Y-%m-%d %H:%M")
            
            result_list = []
            for file in file_list:
                for account in account_list:
                    file_path = os.path.join("upload", file)
                    account_file = os.path.join("cookies", "tk_uploader", f"{account}.json")
                    
                    # 检查账号cookie是否有效
                    if not os.path.exists(account_file):
                        result_list.append({
                            'account': account,
                            'file': file,
                            'status': 'error',
                            'message': '账号cookie文件不存在'
                        })
                        continue
                    
                    # 设置封面文件
                    thumbnail_path = None
                    if thumbnail and os.path.exists(os.path.join("upload", thumbnail)):
                        thumbnail_path = os.path.join("upload", thumbnail)
                    elif os.path.exists(file_path.replace('.mp4', '.png')):
                        thumbnail_path = file_path.replace('.mp4', '.png')
                    
                    # 初始化TikTok视频上传类
                    app = TiktokVideo(title, file_path, tags, schedule_datetime, account_file, thumbnail_path)
                    try:
                        # 执行上传
                        asyncio.run(app.main())
                        result_list.append({
                            'account': account,
                            'file': file,
                            'status': 'success',
                            'message': '视频发布成功'
                        })
                    except Exception as e:
                        logger.error(f"TikTok视频发布失败: {str(e)}")
                        result_list.append({
                            'account': account,
                            'file': file,
                            'status': 'error',
                            'message': f'发布失败: {str(e)}'
                        })
            
            return {
                'status': 'success',
                'message': '发布任务完成',
                'data': result_list
            }
    except Exception as e:
        logger.error(f"TikTok视频发布主函数异常: {str(e)}")
        if enableTimer is not None:
            # 批量模式不需要返回值
            pass
        else:
            return {
                'status': 'error',
                'message': f'发布过程异常: {str(e)}'
            }

# post_video("333",["demo.mp4"],"d","d")
# post_video_DouYin("333",["demo.mp4"],"d","d")