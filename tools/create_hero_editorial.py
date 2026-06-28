from __future__ import annotations

import random
from pathlib import Path

from PIL import Image, ImageEnhance, ImageFilter


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets/images/hero/hero-main.webp"
TARGET = ROOT / "assets/images/hero/hero-editorial.webp"


def main() -> None:
    image = Image.open(SOURCE).convert("RGB")
    image = ImageEnhance.Color(image).enhance(0.72)
    image = ImageEnhance.Contrast(image).enhance(0.88)
    image = ImageEnhance.Brightness(image).enhance(1.06)
    image = image.filter(ImageFilter.GaussianBlur(radius=0.28))
    image = image.filter(ImageFilter.UnsharpMask(radius=1.1, percent=42, threshold=8))

    noise = Image.new("L", image.size)
    rng = random.Random(1906)
    noise.putdata([rng.randrange(118, 138) for _ in range(image.width * image.height)])
    grain = Image.merge("RGB", (noise, noise, noise)).filter(ImageFilter.GaussianBlur(radius=0.35))
    image = Image.blend(image, grain, 0.045)

    warm = Image.new("RGB", image.size, (255, 245, 228))
    image = Image.blend(image, warm, 0.055)

    image.save(TARGET, "WEBP", quality=90, method=6)
    print(f"saved {TARGET.relative_to(ROOT).as_posix()} {image.width}x{image.height}")


if __name__ == "__main__":
    main()
