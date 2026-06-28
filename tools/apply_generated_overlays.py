from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
HELPER = Path.home() / ".codex" / "skills" / ".system" / "imagegen" / "scripts" / "remove_chroma_key.py"

GENERATED = Path.home() / ".codex" / "generated_images" / "019f07e6-347a-7380-9179-d6f3586d4fe1"

ITEMS = [
    (
        GENERATED / "ig_0e5424b01f8e29ca016a40cb6aac848191bf04ad000e56e3d7.png",
        ROOT / "assets/overlays/ornaments/ornament-petal.png",
    ),
    (
        GENERATED / "ig_0e5424b01f8e29ca016a40cb2ae400819183bc73ef882ae685.png",
        ROOT / "assets/overlays/ribbons/ribbon-side.png",
    ),
    (
        GENERATED / "ig_0e5424b01f8e29ca016a40cae7b58481919e460a0752a712ee.png",
        ROOT / "assets/overlays/rings/ring-floating.png",
    ),
    (
        GENERATED / "ig_0e5424b01f8e29ca016a40ca9fdd388191a4d846633293c206.png",
        ROOT / "assets/overlays/flowers/flower-top-corner.png",
    ),
    (
        GENERATED / "ig_0e5424b01f8e29ca016a40ca5555f08191b06ef43a5beee0bc.png",
        ROOT / "assets/overlays/flowers/flower-left-large.png",
    ),
]


def remove_background(source: Path, target: Path) -> None:
    subprocess.run(
        [
            sys.executable,
            str(HELPER),
            "--input",
            str(source),
            "--out",
            str(target),
            "--auto-key",
            "border",
            "--soft-matte",
            "--transparent-threshold",
            "18",
            "--opaque-threshold",
            "220",
            "--despill",
            "--edge-contract",
            "1",
            "--force",
        ],
        check=True,
    )


def main() -> None:
    for source, target in ITEMS:
        remove_background(source, target)
        image = Image.open(target)
        print(f"{target.relative_to(ROOT).as_posix()} {image.width}x{image.height}")

    left = Image.open(ROOT / "assets/overlays/flowers/flower-left-large.png").convert("RGBA")
    right = left.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    target = ROOT / "assets/overlays/flowers/flower-right-large.png"
    right.save(target, "PNG", optimize=True)
    print(f"{target.relative_to(ROOT).as_posix()} {right.width}x{right.height}")


if __name__ == "__main__":
    main()
