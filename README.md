# 多平台无水印下载器

在线粘贴分享链接，无水印下载视频、提取音频、保存图文图片。

## 在线地址

https://fzpnowm.top

## 支持平台

| 平台 | 提取方式 | 下载画质 |
|------|---------|---------|
| 抖音 | 直接 HTTP 爬取 | 1080p |
| X/Twitter | fxtwitter API | 最高码率 |
| TikTok | tikwm.com API | 最高画质 |
| B站 | Bilibili API | 最高画质 |
| 快手 | 移动端页面爬取 | Ultra 最高画质 |

## 功能

- 视频无水印 MP4
- MP3 音频提取
- 图文作品逐张下载原图
- 幻灯片自动合成 MP4（图片 + 背景音乐 → ffmpeg）
- 粘贴分享文本自动提取链接
- 响应式布局，桌面端和手机端均可使用

## API

| 接口 | 说明 |
|------|------|
| `POST /api/parse` | 解析链接，返回视频信息 |
| `GET /api/stream?video_url=<url>&quality=1080p` | 流式播放视频 |
| `POST /api/download` | 下载视频/音频/图片 |

## 技术栈

| 层 | 方案 |
|---|------|
| 后端 | Python FastAPI |
| 下载引擎 | 平台 API + 直接 HTTP 爬取 + yt-dlp |
| 前端 | HTML + Tailwind CSS + GSAP |
| 设计 | Apple Liquid Glass |
| 视频合成 | ffmpeg |
| 部署 | CentOS + Cloudflare Tunnel |

## 源码

https://github.com/f3271174706-tech/douyin-downloader-2.0

## 本地开发

```bash
cd douyin-downloader 2.0
pip install -r requirements.txt
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

浏览器打开 http://localhost:8000

## 部署

详见 [DEPLOY.md](DEPLOY.md)

## 依赖

- Python 3.9+
- FastAPI + uvicorn + httpx
- yt-dlp
- ffmpeg

## 成本

| 项目 | 价格 |
|------|------|
| 域名 fzpnowm.top | ~7 元/年 |
| 云服务器 2核2G 5M | 68/年 |
| Cloudflare Tunnel | 免费 |
| 合计 | ~75 元/年 |
