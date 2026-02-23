from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "assets" / "icon-token-orbit-a-1024.png"


def _lerp(a: int, b: int, t: float) -> int:
    return int(a + (b - a) * t)


def _vertical_gradient(width: int, height: int, top: tuple[int, int, int], bottom: tuple[int, int, int]) -> Image.Image:
    img = Image.new("RGBA", (width, height))
    draw = ImageDraw.Draw(img)
    for y in range(height):
        t = y / (height - 1)
        color = (
            _lerp(top[0], bottom[0], t),
            _lerp(top[1], bottom[1], t),
            _lerp(top[2], bottom[2], t),
            255,
        )
        draw.line((0, y, width, y), fill=color)
    return img


def build_icon(size: int = 1024) -> Image.Image:
    scale = 2
    s = size * scale
    base = Image.new("RGBA", (s, s), (0, 0, 0, 0))

    bg = _vertical_gradient(s, s, top=(9, 25, 43), bottom=(16, 55, 89))
    mask = Image.new("L", (s, s), 0)
    mdraw = ImageDraw.Draw(mask)
    margin = int(0.08 * s)
    radius = int(0.23 * s)
    mdraw.rounded_rectangle((margin, margin, s - margin, s - margin), radius=radius, fill=255)
    base.paste(bg, (0, 0), mask)

    glow = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(glow)
    gdraw.ellipse(
        (int(0.18 * s), int(0.16 * s), int(0.82 * s), int(0.80 * s)),
        fill=(48, 125, 188, 95),
    )
    glow = glow.filter(ImageFilter.GaussianBlur(int(0.05 * s)))
    base.alpha_composite(glow)

    ring = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    rdraw = ImageDraw.Draw(ring)
    ring_box = (int(0.17 * s), int(0.17 * s), int(0.83 * s), int(0.83 * s))
    rdraw.arc(ring_box, start=0, end=359, fill=(138, 170, 205, 58), width=int(0.032 * s))

    # Orbit arc: bright cyan progress-like segment with subtle overlap.
    rdraw.arc(ring_box, start=208, end=18, fill=(42, 226, 213, 255), width=int(0.082 * s))
    inner_ring_box = (int(0.19 * s), int(0.19 * s), int(0.81 * s), int(0.81 * s))
    rdraw.arc(inner_ring_box, start=212, end=14, fill=(148, 250, 242, 120), width=int(0.018 * s))
    base.alpha_composite(ring)

    # Orbit node
    node = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    ndraw = ImageDraw.Draw(node)
    cx, cy = int(0.78 * s), int(0.30 * s)
    nr = int(0.026 * s)
    ndraw.ellipse((cx - nr, cy - nr, cx + nr, cy + nr), fill=(179, 255, 248, 255))
    node = node.filter(ImageFilter.GaussianBlur(int(0.0035 * s)))
    base.alpha_composite(node)

    # T shadow
    t_shadow = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(t_shadow)
    shadow = (16, 20, 32, 145)
    sdraw.rounded_rectangle((int(0.32 * s), int(0.35 * s), int(0.68 * s), int(0.44 * s)), radius=int(0.03 * s), fill=shadow)
    sdraw.rounded_rectangle((int(0.46 * s), int(0.42 * s), int(0.54 * s), int(0.70 * s)), radius=int(0.03 * s), fill=shadow)
    t_shadow = t_shadow.filter(ImageFilter.GaussianBlur(int(0.01 * s)))
    base.alpha_composite(t_shadow)

    # T glyph
    t_layer = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    tdraw = ImageDraw.Draw(t_layer)
    white = (236, 246, 255, 255)
    highlight = (190, 224, 255, 84)
    tdraw.rounded_rectangle((int(0.315 * s), int(0.34 * s), int(0.685 * s), int(0.43 * s)), radius=int(0.032 * s), fill=white)
    tdraw.rounded_rectangle((int(0.457 * s), int(0.41 * s), int(0.543 * s), int(0.70 * s)), radius=int(0.032 * s), fill=white)
    tdraw.rounded_rectangle((int(0.338 * s), int(0.352 * s), int(0.662 * s), int(0.376 * s)), radius=int(0.011 * s), fill=highlight)
    base.alpha_composite(t_layer)

    # Top-left soft sheen
    sheen = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    shdraw = ImageDraw.Draw(sheen)
    shdraw.ellipse(
        (int(0.12 * s), int(0.08 * s), int(0.66 * s), int(0.48 * s)),
        fill=(255, 255, 255, 44),
    )
    sheen = sheen.filter(ImageFilter.GaussianBlur(int(0.06 * s)))
    base.alpha_composite(sheen)

    return base.resize((size, size), Image.Resampling.LANCZOS)


def main() -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    icon = build_icon(size=1024)
    icon.save(OUTPUT)
    print(f"generated: {OUTPUT}")


if __name__ == "__main__":
    main()
