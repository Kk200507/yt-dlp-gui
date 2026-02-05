# yt-dlp GUI 

A modern, lightweight desktop GUI for **yt-dlp**, built with **Python** and **CustomTkinter**.  
Designed for simplicity, clarity, and safe usage — no clutter, no gimmicks.

This project provides a user-friendly way to download media from supported websites while keeping the core logic transparent and extensible.

---

## Features

- Clean, modern desktop UI (CustomTkinter)
- Download video or audio from supported sites
- Quality / resolution selection
- Audio-only downloads
- Custom save location picker
- Real-time progress bar with detailed status
- Threaded downloads (no UI freezing)
- Cross-platform (Windows, Linux, macOS — Python-based)

---

## Supported Websites

This application is **not limited to YouTube**.

It works with any website supported by **yt-dlp**, including (but not limited to):

- YouTube / YouTube Music
- SoundCloud
- Vimeo
- Dailymotion
- Reddit
- Twitter / X
- Instagram (public content)
- Facebook (public content)
- Twitch clips and VODs
- Many news and media websites

> Availability depends on the website and whether the content is publicly accessible and not DRM-protected.

---

## What This App Does NOT Do

- ❌ Does NOT bypass DRM or protected streaming services  
- ❌ Does NOT support Netflix, Amazon Prime, Disney+, Spotify, etc.  
- ❌ Does NOT execute website scripts or run downloaded files  
- ❌ Does NOT guarantee copyright-free downloads  

---

## Requirements

- Python 3.9+
- `yt-dlp`
- `customtkinter`

Install dependencies:
```bash
pip install yt-dlp customtkinter ffmpeg Pillow
