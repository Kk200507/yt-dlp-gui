## yt-dlp GUI

A modern, lightweight desktop graphical interface for yt-dlp, built with Python and CustomTkinter.

This application is designed to make yt-dlp easier to use for non-technical users while keeping behavior transparent, predictable, and respectful of platform restrictions.


## Overview

yt-dlp GUI is a local desktop application that allows users to download publicly accessible media from websites supported by yt-dlp.

The application is:

    simple by design

    explicit about limitations

    focused on usability, not circumvention

    No accounts, no trackers, no background services.

## Features

    Clean, modern desktop UI (CustomTkinter)

    Download video or audio from supported websites

    Quality / resolution selection

    Audio-only downloads

    Optional MP4 output (where supported)

    Custom save location picker

    Real-time progress bar with detailed status

    Background (threaded) downloads - UI remains responsive

    Download history (local only)

    User-friendly error messages

    Cross-platform (Windows, Linux, macOS via Python)

## Supported Websites

This application is not limited to YouTube.

It supports any website compatible with yt-dlp, including (but not limited to):

    YouTube / YouTube Music

    SoundCloud

    Vimeo

    Dailymotion

    Reddit

    Twitter / X

    Instagram (public content only)

    Facebook (public content only)

    Twitch clips and VODs

    Various news and media websites

Availability depends entirely on the website, the content’s accessibility, and yt-dlp’s extractor support.

## What This App Does NOT Do

This application explicitly does not:

    Bypass DRM, encryption, or paywalls

    Download from protected streaming platforms (Netflix, Prime Video, Disney+, Spotify, etc.)

    Circumvent login, subscription, or purchase requirements

    Modify, decrypt, or tamper with media streams

    Execute downloaded files or scripts

    Guarantee copyright-free usage

If yt-dlp cannot legally or technically access content, this application cannot either.


## Legal & Responsibility Disclaimer (Important)

This software is provided for educational and personal use only.

    The developer does not host, distribute, or provide any copyrighted content.

    All downloads are performed locally on the user’s machine using yt-dlp.

    The user is solely responsible for:

        how the software is used

        ensuring compliance with local laws

        respecting website terms of service

        respecting copyright and intellectual property rights

    By using this software, you agree that:

        the developer is not responsible for misuse

        the developer provides no legal guarantees

        any legal consequences resulting from usage are entirely the user’s responsibility

    If downloading content is illegal in your country or violates a platform’s terms, do not use this software.

## Download History & Privacy

    Download history is stored locally as a JSON file

    No data is uploaded, synced, or shared

    No telemetry, analytics, or tracking

    No network requests beyond those required by yt-dlp itself

## Requirements

    Python 3.9+

    yt-dlp

    customtkinter

    ffmpeg (required for merging audio & video)

## Install dependencies

    pip install yt-dlp customtkinter Pillow

Install FFmpeg separately and ensure it is available in your system PATH


## Running the Application

    python main.py


## Credits & Acknowledgements

This project stands on the shoulders of excellent open-source software:

    yt-dlp - core downloading engine
    https://github.com/yt-dlp/yt-dlp

    FFmpeg - media processing and merging
    https://ffmpeg.org/

    CustomTkinter - modern Tkinter UI framework
    https://github.com/TomSchimansky/CustomTkinter

All credit for extraction logic and website support belongs to the yt-dlp contributors.

## License

This project is provided as-is, without warranty of any kind.
Use at your own risk.

## Final Notes

This project is intended to be:

    transparent

    respectful of platform restrictions

    useful without being deceptive

If you are unsure whether downloading specific content is legal - don’t download it.