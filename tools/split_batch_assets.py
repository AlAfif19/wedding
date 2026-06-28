#!/usr/bin/env python3
"""Split generated batch contact sheets into website asset files."""

from __future__ import annotations

from collections import deque
from pathlib import Path
from PIL import Image, ImageChops, ImageEnhance, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
PROTECTED_HD_OUTPUTS = {
    "assets/images/hero/hero-main.webp",
    "assets/images/gallery/gallery-01-pelaminan.webp",
    "assets/images/gallery/gallery-05-garden.webp",
    "assets/images/gallery/gallery-08-entrance.webp",
    "assets/images/gallery/gallery-09-ballroom.webp",
    "assets/images/gallery/gallery-10-lighting-night.webp",
    "assets/images/gallery/gallery-11-family.webp",
    "assets/images/gallery/gallery-12-catering.webp",
    "assets/images/contact/maps-preview.webp",
}


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def fit_width(image: Image.Image, width: int) -> Image.Image:
    height = round(image.height * (width / image.width))
    return image.resize((width, height), Image.Resampling.LANCZOS)


def enhance_rgb(image: Image.Image) -> Image.Image:
    image = ImageEnhance.Color(image).enhance(1.04)
    image = ImageEnhance.Contrast(image).enhance(1.05)
    image = ImageEnhance.Sharpness(image).enhance(1.55)
    return image.filter(ImageFilter.UnsharpMask(radius=1.4, percent=130, threshold=3))


def enhance_rgba(image: Image.Image) -> Image.Image:
    alpha = image.getchannel("A")
    rgb = enhance_rgb(image.convert("RGB"))
    rgba = rgb.convert("RGBA")
    rgba.putalpha(alpha)
    return rgba


def trim_alpha(image: Image.Image, padding: int = 18) -> Image.Image:
    alpha = image.getchannel("A")
    bbox = alpha.getbbox()
    if not bbox:
        return image
    left = max(0, bbox[0] - padding)
    top = max(0, bbox[1] - padding)
    right = min(image.width, bbox[2] + padding)
    bottom = min(image.height, bbox[3] + padding)
    return image.crop((left, top, right, bottom))


def clean_overlay_alpha(image: Image.Image) -> Image.Image:
    rgba = image.convert("RGBA")
    alpha = rgba.getchannel("A")
    alpha = alpha.point(lambda value: 0 if value < 34 else value)
    alpha = alpha.filter(ImageFilter.MinFilter(3))
    alpha = alpha.filter(ImageFilter.GaussianBlur(0.18))
    rgba.putalpha(alpha)
    return trim_alpha(rgba)


def crop_save(
    source: str,
    box: tuple[int, int, int, int],
    target: str,
    target_width: int,
    quality: int = 88,
) -> None:
    image = Image.open(ROOT / source).convert("RGB")
    piece = enhance_rgb(fit_width(image.crop(box), target_width))
    target_path = ROOT / target
    if target in PROTECTED_HD_OUTPUTS and target_path.exists():
        print(f"skipped protected HD asset {target}")
        return
    ensure_parent(target_path)
    piece.save(target_path, quality=quality, method=6)
    print(f"saved {target}")


def color_distance(a: tuple[int, int, int], b: tuple[int, int, int]) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1]) + abs(a[2] - b[2])


def remove_edge_background(
    image: Image.Image,
    tolerance: int = 70,
    white_threshold: int = 238,
) -> Image.Image:
    """Flood-fill edge-connected background without deleting inner light details."""
    rgba = image.convert("RGBA")
    pixels = rgba.load()
    width, height = rgba.size
    edge_samples: list[tuple[int, int, int]] = []

    for x in range(width):
        edge_samples.append(pixels[x, 0][:3])
        edge_samples.append(pixels[x, height - 1][:3])
    for y in range(height):
        edge_samples.append(pixels[0, y][:3])
        edge_samples.append(pixels[width - 1, y][:3])

    bg = tuple(sum(sample[i] for sample in edge_samples) // len(edge_samples) for i in range(3))
    queue: deque[tuple[int, int]] = deque()
    seen = set()

    for x in range(width):
        queue.append((x, 0))
        queue.append((x, height - 1))
    for y in range(height):
        queue.append((0, y))
        queue.append((width - 1, y))

    while queue:
        x, y = queue.popleft()
        if (x, y) in seen or x < 0 or y < 0 or x >= width or y >= height:
            continue
        seen.add((x, y))
        r, g, b, a = pixels[x, y]
        is_background = color_distance((r, g, b), bg) <= tolerance or min(r, g, b) >= white_threshold
        if not is_background:
            continue

        pixels[x, y] = (r, g, b, 0)
        queue.extend(((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)))

    return rgba


def overlay_save(source: str, box: tuple[int, int, int, int], target: str, target_width: int) -> None:
    image = Image.open(ROOT / source).convert("RGB")
    piece = image.crop(box)
    transparent = clean_overlay_alpha(remove_edge_background(piece))
    transparent = enhance_rgba(fit_width(transparent, target_width))
    transparent.putalpha(transparent.getchannel("A").point(lambda value: 0 if value < 18 else value))
    target_path = ROOT / target
    ensure_parent(target_path)
    transparent.save(target_path)
    print(f"saved {target}")


def write_logo_svg(target: str, dark: bool = False) -> None:
    bg = "#17120f" if dark else "transparent"
    gold = "#c99649"
    subtitle = "#f2d49c" if dark else "#b88743"
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 420">
  <rect width="1000" height="420" fill="{bg}"/>
  <text x="500" y="215" text-anchor="middle" font-family="Parisienne, Brush Script MT, cursive" font-size="178" fill="{gold}">Aliya</text>
  <text x="500" y="310" text-anchor="middle" font-family="Inter, Arial, sans-serif" font-size="42" letter-spacing="16" fill="{subtitle}">WEDDING ORGANIZER</text>
</svg>
"""
    target_path = ROOT / target
    ensure_parent(target_path)
    target_path.write_text(svg, encoding="utf-8")
    print(f"saved {target}")


def split_batch_1() -> None:
    crops = [
        ("batch 1.png", (18, 106, 451, 442), "assets/images/hero/hero-main.webp", 1600),
        ("batch 1.png", (466, 106, 919, 442), "assets/images/hero/hero-cinematic.webp", 1600),
        ("batch 1.png", (934, 106, 1372, 442), "assets/images/hero/hero-booking.webp", 1600),
        ("batch 1.png", (18, 526, 462, 773), "assets/images/gallery/gallery-01-pelaminan.webp", 1200),
        ("batch 1.png", (482, 526, 920, 773), "assets/images/gallery/gallery-02-akad.webp", 1200),
        ("batch 1.png", (936, 526, 1372, 773), "assets/images/gallery/gallery-03-couple.webp", 1200),
        ("batch 1.png", (18, 811, 462, 1070), "assets/images/gallery/gallery-04-table-setting.webp", 1200),
        ("batch 1.png", (482, 811, 920, 1070), "assets/images/gallery/gallery-05-garden.webp", 1200),
        ("batch 1.png", (936, 811, 1372, 1070), "assets/images/gallery/gallery-06-ring-detail.webp", 1200),
    ]
    for source, box, target, width in crops:
        crop_save(source, box, target, width)


def split_batch_2() -> None:
    crops = [
        ("batch 2.png", (18, 116, 253, 365), "assets/images/gallery/gallery-07-bouquet.webp", 1050),
        ("batch 2.png", (258, 116, 502, 365), "assets/images/gallery/gallery-08-entrance.webp", 1200),
        ("batch 2.png", (510, 116, 775, 365), "assets/images/gallery/gallery-09-ballroom.webp", 1200),
        ("batch 2.png", (782, 116, 1026, 365), "assets/images/gallery/gallery-10-lighting-night.webp", 1200),
        ("batch 2.png", (1031, 116, 1288, 365), "assets/images/gallery/gallery-11-family.webp", 1200),
        ("batch 2.png", (1293, 116, 1513, 365), "assets/images/gallery/gallery-12-catering.webp", 1050),
        ("batch 2.png", (18, 450, 502, 710), "assets/images/packages/package-silver.webp", 1400),
        ("batch 2.png", (512, 450, 1020, 710), "assets/images/packages/package-gold.webp", 1400),
        ("batch 2.png", (1029, 450, 1512, 710), "assets/images/packages/package-platinum.webp", 1400),
    ]
    for source, box, target, width in crops:
        crop_save(source, box, target, width)


def split_batch_3() -> None:
    crops = [
        ("batch 3.png", (18, 104, 219, 319), "assets/images/testimonials/client-rina-fajar.webp", 600),
        ("batch 3.png", (228, 104, 430, 319), "assets/images/testimonials/client-dewi-arif.webp", 600),
        ("batch 3.png", (438, 104, 630, 319), "assets/images/testimonials/client-siska-bimo.webp", 600),
        ("batch 3.png", (552, 406, 725, 589), "assets/images/logo/logo-aliya-gold.png", 520),
        ("batch 3.png", (748, 407, 1512, 615), "assets/images/contact/maps-preview.webp", 1400),
    ]
    for source, box, target, width in crops:
        crop_save(source, box, target, width)

    overlays = [
        ((642, 103, 792, 319), "assets/overlays/flowers/flower-left-large.png", 1440),
        ((799, 103, 948, 319), "assets/overlays/flowers/flower-right-large.png", 1440),
        ((955, 103, 1082, 319), "assets/overlays/flowers/flower-top-corner.png", 1360),
        ((1092, 103, 1191, 319), "assets/overlays/rings/ring-floating.png", 1200),
        ((1202, 103, 1350, 319), "assets/overlays/ribbons/ribbon-side.png", 1120),
        ((1357, 103, 1514, 319), "assets/overlays/ornaments/ornament-petal.png", 1280),
    ]
    for box, target, width in overlays:
        overlay_save("batch 3.png", box, target, width)

    write_logo_svg("assets/images/logo/logo-aliya.svg")
    write_logo_svg("assets/images/logo/logo-aliya-dark.svg", dark=True)


def main() -> None:
    missing = [name for name in ("batch 1.png", "batch 2.png", "batch 3.png") if not (ROOT / name).exists()]
    if missing:
        raise SystemExit(f"Missing batch file(s): {', '.join(missing)}")

    split_batch_1()
    split_batch_2()
    split_batch_3()


if __name__ == "__main__":
    main()
