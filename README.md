# 多平台无水印下载器

在线粘贴抖音、X(Twitter)、B站、快手、TikTok 分享链接，无水印下载视频、提取音频、保存图文图片。

## 在线地址

https://fzpnowm.top

## 功能

- 视频无水印 MP4，可选 720p / 1080p / HD 画质
- MP3 音频提取
- 图文作品逐张下载原图
- 幻灯片自动合成 MP4（图片 + 背景音乐 → ffmpeg）
- 粘贴分享文本自动提取链接
- 响应式布局，桌面端和手机端均可使用

## API

| 接口 | 说明 |
|------|------|
| `GET /api/info?url=<链接>` | 视频/图文信息 |
| `GET /api/video?url=<链接>&quality=1080p` | 301 跳转无水印视频 |
| `GET /api/image_redirect?url=<链接>&index=0` | 301 跳转图片 |
| `GET /api` | 接口文档 |

## 技术栈

| 层 | 方案 |
|---|------|
| 后端 | Python FastAPI |
| 下载引擎 | yt-dlp + 直接 HTTP 爬取 |
| 前端 | HTML + Tailwind CSS + GSAP |
| 设计 | Apple Liquid Glass |
| 视频合成 | ffmpeg |
| 部署 | CentOS + Cloudflare Tunnel |

## 源码

https://github.com/f3271174706-tech/-tiktok-

## 本地开发

```bash
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```
或：python -m uvicorn main:app --host 0.0.0.0 --port 8001 --reload

浏览器打开 `http://localhost:8000`。

## 部署

详见 [DEPLOY.md](DEPLOY.md)

## 依赖

- Python 3.10+
- FastAPI + uvicorn + httpx
- yt-dlp + curl-cffi
- ffmpeg

## 成本

| 项目 | 价格 |
|------|------|
| 域名 fzpnowm.top | ~7 元/年 |
| 云服务器 2核2G 5M | 68/年 |
| Cloudflare Tunnel | 免费 |
| 合计 | ~75 元/年 |
