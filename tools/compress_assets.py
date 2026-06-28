#!/usr/bin/env python3
"""Compress local assets into assets/compressed when optional tools exist."""

from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
OUTPUT = ASSETS / "compressed"
IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp"}
VIDEO_EXTS = {".mp4", ".mov", ".mkv"}
MUSIC_EXTS = {".mp3", ".wav", ".m4a"}


def iter_files(exts: set[str]) -> list[Path]:
    return [
        path
        for path in ASSETS.rglob("*")
        if path.is_file() and path.suffix.lower() in exts and OUTPUT not in path.parents
    ]


def compress_images() -> None:
    images = iter_files(IMAGE_EXTS)
    if not images:
        print("No image assets found.")
        return

    try:
        from PIL import Image
    except ImportError:
        print("Pillow is not installed. Install with: python -m pip install pillow")
        print(f"Found {len(images)} image asset(s) ready for WebP compression.")
        return

    image_output = OUTPUT / "images"
    image_output.mkdir(parents=True, exist_ok=True)
    for source in images:
        target = image_output / f"{source.stem}.webp"
        with Image.open(source) as image:
            image.save(target, "WEBP", quality=72, method=6)
        print(f"Compressed image: {source.relative_to(ROOT)} -> {target.relative_to(ROOT)}")


def print_ffmpeg_guidance(exts: set[str], label: str, command_template: str) -> None:
    files = iter_files(exts)
    if not files:
        print(f"No {label} assets found.")
        return

    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        print(f"ffmpeg is not installed. Found {len(files)} {label} asset(s).")
        for source in files:
            print(command_template.format(input=source.as_posix(), output=(OUTPUT / label / source.name).as_posix()))
        return

    print(f"ffmpeg detected at {ffmpeg}. Suggested {label} compression commands:")
    for source in files:
        target = OUTPUT / label / source.name
        target.parent.mkdir(parents=True, exist_ok=True)
        print(command_template.format(input=source.as_posix(), output=target.as_posix()))


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    compress_images()
    print_ffmpeg_guidance(
        VIDEO_EXTS,
        "videos",
        'ffmpeg -i "{input}" -vcodec libx264 -crf 28 -preset slow -acodec aac -b:a 96k "{output}"',
    )
    print_ffmpeg_guidance(
        MUSIC_EXTS,
        "music",
        'ffmpeg -i "{input}" -codec:a libmp3lame -b:a 128k "{output}"',
    )


if __name__ == "__main__":
    main()
