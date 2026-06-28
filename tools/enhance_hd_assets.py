from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageEnhance, ImageFilter


ROOT = Path(__file__).resolve().parents[1]


TARGETS = {
    "assets/images/hero": 1920,
    "assets/images/gallery": 1600,
    "assets/images/packages": 1600,
    "assets/images/testimonials": 1200,
    "assets/images/contact": 1600,
    "assets/images/logo": 1040,
    "assets/overlays": 1600,
}


def target_long_edge(path: Path) -> int:
    rel = path.relative_to(ROOT).as_posix()
    for folder, size in TARGETS.items():
        if rel.startswith(folder):
            return size
    return 1400


def is_photo(path: Path) -> bool:
    rel = path.relative_to(ROOT).as_posix()
    return rel.startswith("assets/images/") and not rel.startswith("assets/images/logo/")


def upscale_if_needed(image: Image.Image, long_edge: int) -> Image.Image:
    width, height = image.size
    current_long = max(width, height)
    if current_long >= long_edge:
        return image

    scale = long_edge / current_long
    size = (round(width * scale), round(height * scale))
    return image.resize(size, Image.Resampling.LANCZOS)


def enhance_rgb(image: Image.Image, photo: bool) -> Image.Image:
    image = image.convert("RGB")
    if photo:
        image = ImageEnhance.Color(image).enhance(1.05)
        image = ImageEnhance.Contrast(image).enhance(1.07)
        image = ImageEnhance.Sharpness(image).enhance(1.28)
        return image.filter(ImageFilter.UnsharpMask(radius=1.7, percent=145, threshold=3))

    image = ImageEnhance.Contrast(image).enhance(1.04)
    image = ImageEnhance.Sharpness(image).enhance(1.16)
    return image.filter(ImageFilter.UnsharpMask(radius=1.2, percent=110, threshold=3))


def enhance_rgba(image: Image.Image) -> Image.Image:
    image = image.convert("RGBA")
    alpha = image.getchannel("A")
    rgb = enhance_rgb(Image.new("RGB", image.size, (255, 250, 242)), photo=False)
    rgb.paste(image.convert("RGB"), mask=alpha)
    rgba = rgb.convert("RGBA")
    rgba.putalpha(alpha.filter(ImageFilter.UnsharpMask(radius=0.8, percent=80, threshold=2)))
    return rgba


def save_image(image: Image.Image, path: Path) -> None:
    suffix = path.suffix.lower()
    if suffix == ".webp":
        image.save(path, "WEBP", quality=92, method=6)
    elif suffix == ".png":
        image.save(path, "PNG", optimize=True)
    elif suffix in {".jpg", ".jpeg"}:
        image.convert("RGB").save(path, "JPEG", quality=92, optimize=True, progressive=True)
    else:
        raise ValueError(f"Unsupported image type: {path}")


def process(path: Path) -> None:
    with Image.open(path) as opened:
        image = opened.copy()

    before = image.size
    image = upscale_if_needed(image, target_long_edge(path))
    if image.mode == "RGBA" or "transparency" in image.info:
        image = enhance_rgba(image)
    else:
        image = enhance_rgb(image, photo=is_photo(path))
    save_image(image, path)
    print(f"{path.relative_to(ROOT).as_posix()} {before[0]}x{before[1]} -> {image.width}x{image.height}")


def main() -> None:
    paths = [
        path
        for path in (ROOT / "assets").rglob("*")
        if path.suffix.lower() in {".webp", ".png", ".jpg", ".jpeg"}
    ]
    for path in sorted(paths):
        process(path)


if __name__ == "__main__":
    main()
