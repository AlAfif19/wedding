from __future__ import annotations

import math
import time
from io import BytesIO
from pathlib import Path
from urllib.request import Request, urlopen

from PIL import Image, ImageDraw, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets/images/contact/maps-preview.webp"

LAT = -6.9144512
LON = 107.4970353
ZOOM = 14
WIDTH = 1600
HEIGHT = 620
TILE_SIZE = 256


def latlon_to_pixel(lat: float, lon: float, zoom: int) -> tuple[float, float]:
    scale = TILE_SIZE * 2**zoom
    x = (lon + 180.0) / 360.0 * scale
    lat_rad = math.radians(lat)
    y = (1 - math.log(math.tan(lat_rad) + 1 / math.cos(lat_rad)) / math.pi) / 2 * scale
    return x, y


def fetch_tile(x: int, y: int, zoom: int) -> Image.Image:
    url = f"https://tile.openstreetmap.org/{zoom}/{x}/{y}.png"
    request = Request(
        url,
        headers={
            "User-Agent": "AliyaWeddingOrganizerStaticPreview/1.0 (local development)",
        },
    )
    with urlopen(request, timeout=20) as response:
        return Image.open(BytesIO(response.read())).convert("RGB")


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
    ]
    for candidate in candidates:
        path = Path(candidate)
        if path.exists():
            return ImageFont.truetype(str(path), size=size)
    return ImageFont.load_default()


def rounded_pin(image: Image.Image, x: int, y: int) -> None:
    shadow = Image.new("RGBA", (170, 170), (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow)
    shadow_draw.ellipse((40, 44, 130, 134), fill=(63, 39, 18, 95))
    shadow = shadow.filter(ImageFilter.GaussianBlur(14))

    pin = Image.new("RGBA", (170, 190), (0, 0, 0, 0))
    pin_draw = ImageDraw.Draw(pin)
    pin_draw.ellipse((39, 18, 131, 110), fill=(184, 126, 58, 255))
    pin_draw.polygon([(85, 168), (54, 94), (116, 94)], fill=(184, 126, 58, 255))
    pin_draw.ellipse((57, 36, 113, 92), fill=(255, 250, 240, 255))
    pin_draw.ellipse((70, 49, 100, 79), fill=(184, 126, 58, 255))

    image.alpha_composite(shadow, (x - 85, y - 78))
    image.alpha_composite(pin, (x - 85, y - 162))


def main() -> None:
    center_x, center_y = latlon_to_pixel(LAT, LON, ZOOM)
    left = center_x - WIDTH / 2
    top = center_y - HEIGHT / 2

    start_tx = math.floor(left / TILE_SIZE)
    start_ty = math.floor(top / TILE_SIZE)
    end_tx = math.floor((left + WIDTH) / TILE_SIZE)
    end_ty = math.floor((top + HEIGHT) / TILE_SIZE)

    canvas = Image.new("RGB", (WIDTH, HEIGHT), "#efe6d8")
    for tx in range(start_tx, end_tx + 1):
        for ty in range(start_ty, end_ty + 1):
            tile = fetch_tile(tx, ty, ZOOM)
            px = round(tx * TILE_SIZE - left)
            py = round(ty * TILE_SIZE - top)
            canvas.paste(tile, (px, py))
            time.sleep(0.04)

    overlay = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    draw.rectangle((0, 0, WIDTH, HEIGHT), fill=(255, 248, 237, 42))
    draw.rectangle((0, HEIGHT - 190, WIDTH, HEIGHT), fill=(255, 248, 237, 168))

    rounded_pin(overlay, WIDTH // 2, HEIGHT // 2 + 8)

    card = (48, HEIGHT - 168, 720, HEIGHT - 34)
    draw.rounded_rectangle(card, radius=26, fill=(255, 250, 242, 232), outline=(191, 138, 69, 120), width=2)
    draw.text((82, HEIGHT - 142), "Aliya Wedding Organizer", font=font(28, bold=True), fill=(63, 45, 32, 255))
    draw.text((82, HEIGHT - 100), "Batujajar, Bandung Regency, West Java", font=font(22), fill=(98, 82, 69, 255))
    draw.text((82, HEIGHT - 68), "Lokasi sesuai tautan Google Maps", font=font(18), fill=(143, 103, 50, 255))
    draw.text((WIDTH - 330, HEIGHT - 30), "Map data © OpenStreetMap contributors", font=font(16), fill=(91, 82, 75, 190))

    result = Image.alpha_composite(canvas.convert("RGBA"), overlay).convert("RGB")
    result.save(OUT, "WEBP", quality=92, method=6)
    print(f"saved {OUT.relative_to(ROOT).as_posix()} {WIDTH}x{HEIGHT}")


if __name__ == "__main__":
    main()
