from __future__ import annotations

import base64
import html
import textwrap
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
ASSETS_DIR = REPO_ROOT / "docs" / "assets"
OUTPUT_PATH = ASSETS_DIR / "cinedepth_portfolio_poster.svg"

POSTER_WIDTH = 1920
POSTER_HEIGHT = 1080


def image_data_uri(path: Path) -> str:
    mime = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".webp": "image/webp",
    }.get(path.suffix.lower())
    if mime is None:
        raise ValueError(f"Unsupported image type: {path}")
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{encoded}"


def esc(text: str) -> str:
    return html.escape(text, quote=True)


def wrapped_text(
    x: int,
    y: int,
    text: str,
    *,
    width: int,
    font_size: int,
    line_height: float = 1.35,
    fill: str = "#F5F1E8",
    weight: str = "400",
    family: str = "'Avenir Next', 'Segoe UI', sans-serif",
    letter_spacing: float | None = None,
) -> str:
    approx_chars = max(14, int(width / (font_size * 0.58)))
    lines = textwrap.wrap(text, width=approx_chars)
    attrs = [
        f'x="{x}"',
        f'y="{y}"',
        f'fill="{fill}"',
        f'font-size="{font_size}"',
        f'font-weight="{weight}"',
        f'font-family="{family}"',
    ]
    if letter_spacing is not None:
        attrs.append(f'letter-spacing="{letter_spacing}"')
    spans = []
    for idx, line in enumerate(lines):
        dy = 0 if idx == 0 else font_size * line_height
        spans.append(f'<tspan x="{x}" dy="{dy}">{esc(line)}</tspan>')
    return f"<text {' '.join(attrs)}>{''.join(spans)}</text>"


def pill(x: int, y: int, w: int, h: int, label: str, fill: str, stroke: str, text_fill: str) -> str:
    return (
        f'<g>'
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h / 2}" fill="{fill}" stroke="{stroke}" stroke-width="1.2"/>'
        f'<text x="{x + w / 2}" y="{y + h / 2 + 5}" fill="{text_fill}" font-size="16" font-weight="600" '
        f'font-family="\'Avenir Next\', \'Segoe UI\', sans-serif" text-anchor="middle">{esc(label)}</text>'
        f"</g>"
    )


def info_tile(x: int, y: int, w: int, h: int, title: str, body: str, accent: str) -> str:
    compact = h <= 64
    title_y = y + (40 if compact else 48)
    body_y = y + (56 if compact else 74)
    title_size = 18 if compact else 22
    body_size = 13 if compact else 15
    return (
        f'<g>'
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="20" fill="rgba(255,255,255,0.04)" '
        f'stroke="rgba(255,255,255,0.08)" stroke-width="1.1"/>'
        f'<rect x="{x + 18}" y="{y + 18}" width="42" height="6" rx="3" fill="{accent}"/>'
        f'<text x="{x + 18}" y="{title_y}" fill="#F8F4EB" font-size="{title_size}" font-weight="700" '
        f'font-family="\'Avenir Next\', \'Segoe UI\', sans-serif">{esc(title)}</text>'
        f'{wrapped_text(x + 18, body_y, body, width=w - 36, font_size=body_size, fill="#C9C0B1")}'
        f"</g>"
    )


def phone_card(
    card_id: str,
    x: int,
    y: int,
    w: int,
    h: int,
    label: str,
    image_uri: str,
    label_fill: str,
) -> str:
    clip_id = f"clip_{card_id}"
    return (
        f'<g>'
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="34" fill="#0B0B0D" stroke="rgba(255,255,255,0.12)" stroke-width="1.3"/>'
        f'<rect x="{x + (w / 2) - 24}" y="{y + 12}" width="48" height="6" rx="3" fill="rgba(255,255,255,0.18)"/>'
        f'<clipPath id="{clip_id}"><rect x="{x + 10}" y="{y + 10}" width="{w - 20}" height="{h - 20}" rx="24"/></clipPath>'
        f'<image href="{image_uri}" x="{x + 10}" y="{y + 10}" width="{w - 20}" height="{h - 20}" preserveAspectRatio="xMidYMid slice" clip-path="url(#{clip_id})"/>'
        f'<rect x="{x + 16}" y="{y + 18}" width="{w - 32}" height="34" rx="17" fill="rgba(8,8,10,0.72)" stroke="{label_fill}" stroke-width="1"/>'
        f'<text x="{x + w / 2}" y="{y + 41}" fill="#F8F5EF" font-size="14" font-weight="700" '
        f'font-family="\'Avenir Next\', \'Segoe UI\', sans-serif" text-anchor="middle">{esc(label)}</text>'
        f"</g>"
    )


def pipeline_step(x: int, y: int, idx: int, title: str, body: str, accent: str) -> str:
    return (
        f'<g>'
        f'<circle cx="{x}" cy="{y}" r="26" fill="{accent}" filter="url(#glow)"/>'
        f'<text x="{x}" y="{y + 8}" fill="#0D1014" font-size="22" font-weight="800" '
        f'font-family="\'Avenir Next\', \'Segoe UI\', sans-serif" text-anchor="middle">{idx}</text>'
        f'<text x="{x + 44}" y="{y - 4}" fill="#F6F2EA" font-size="22" font-weight="700" '
        f'font-family="\'Avenir Next\', \'Segoe UI\', sans-serif">{esc(title)}</text>'
        f'{wrapped_text(x + 44, y + 20, body, width=250, font_size=15, fill="#C9C0B1")}'
        f"</g>"
    )


def architecture_block(x: int, y: int, w: int, h: int, title: str, role: str, files: list[str], accent: str) -> str:
    file_lines = []
    for idx, line in enumerate(files):
        file_lines.append(
            f'<text x="{x + 18}" y="{y + 88 + idx * 18}" fill="#BEB5A8" font-size="13" font-weight="500" '
            f'font-family="\'SF Mono\', Menlo, monospace">{esc(line)}</text>'
        )
    return (
        f'<g>'
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="18" fill="rgba(255,255,255,0.04)" stroke="rgba(255,255,255,0.08)" stroke-width="1.1"/>'
        f'<rect x="{x + 18}" y="{y + 18}" width="52" height="6" rx="3" fill="{accent}"/>'
        f'<text x="{x + 18}" y="{y + 46}" fill="#F8F4EC" font-size="20" font-weight="700" '
        f'font-family="\'Avenir Next\', \'Segoe UI\', sans-serif">{esc(title)}</text>'
        f'{wrapped_text(x + 18, y + 64, role, width=w - 36, font_size=14, fill="#CCC3B7")}'
        f'{"".join(file_lines)}'
        f"</g>"
    )


def feature_chip(x: int, y: int, w: int, label: str, accent: str, text_fill: str = "#111318") -> str:
    return (
        f'<rect x="{x}" y="{y}" width="{w}" height="42" rx="21" fill="{accent}" opacity="0.96"/>'
        f'<text x="{x + w / 2}" y="{y + 28}" fill="{text_fill}" font-size="15" font-weight="700" '
        f'font-family="\'Avenir Next\', \'Segoe UI\', sans-serif" text-anchor="middle">{esc(label)}</text>'
    )


def main() -> None:
    montage = image_data_uri(ASSETS_DIR / "sample1_side_by_side_montage.jpg")
    depth = image_data_uri(ASSETS_DIR / "sample1_depthmap_HD.jpg")
    transition = image_data_uri(ASSETS_DIR / "sample1_transition.jpg")
    retouched = image_data_uri(ASSETS_DIR / "sample1_depthmap_retouched.jpg")

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{POSTER_WIDTH}" height="{POSTER_HEIGHT}" viewBox="0 0 {POSTER_WIDTH} {POSTER_HEIGHT}">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#0C1014"/>
      <stop offset="42%" stop-color="#151A21"/>
      <stop offset="100%" stop-color="#211D18"/>
    </linearGradient>
    <radialGradient id="amberGlow" cx="28%" cy="8%" r="70%">
      <stop offset="0%" stop-color="#FFCB63" stop-opacity="0.34"/>
      <stop offset="45%" stop-color="#FFCB63" stop-opacity="0.08"/>
      <stop offset="100%" stop-color="#FFCB63" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="tealGlow" cx="84%" cy="76%" r="44%">
      <stop offset="0%" stop-color="#63E3D1" stop-opacity="0.16"/>
      <stop offset="100%" stop-color="#63E3D1" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="cardStroke" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="rgba(255,255,255,0.18)"/>
      <stop offset="100%" stop-color="rgba(255,255,255,0.05)"/>
    </linearGradient>
    <filter id="shadow" x="-20%" y="-20%" width="140%" height="160%">
      <feDropShadow dx="0" dy="18" stdDeviation="20" flood-color="#000000" flood-opacity="0.24"/>
    </filter>
    <filter id="glow" x="-120%" y="-120%" width="340%" height="340%">
      <feGaussianBlur stdDeviation="11" result="blur"/>
      <feColorMatrix in="blur" type="matrix" values="1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 0.42 0"/>
      <feBlend in="SourceGraphic" in2="blur"/>
    </filter>
    <clipPath id="heroClip">
      <rect x="590" y="176" width="792" height="360" rx="26"/>
    </clipPath>
  </defs>

  <rect width="{POSTER_WIDTH}" height="{POSTER_HEIGHT}" fill="url(#bg)"/>
  <rect width="{POSTER_WIDTH}" height="{POSTER_HEIGHT}" fill="url(#amberGlow)"/>
  <rect width="{POSTER_WIDTH}" height="{POSTER_HEIGHT}" fill="url(#tealGlow)"/>

  <circle cx="1654" cy="170" r="84" fill="#FFCB63" opacity="0.08"/>
  <circle cx="1598" cy="228" r="30" fill="#FFF1C6" opacity="0.18"/>
  <circle cx="1748" cy="232" r="46" fill="#63E3D1" opacity="0.11"/>
  <circle cx="126" cy="908" r="92" fill="#FFCB63" opacity="0.06"/>
  <circle cx="250" cy="956" r="28" fill="#E7D5AA" opacity="0.12"/>

  <g transform="translate(48 30)">
    <circle cx="36" cy="36" r="36" fill="#11161C" stroke="#FFCB63" stroke-width="2"/>
    <circle cx="36" cy="36" r="22" fill="none" stroke="#F8E2AB" stroke-width="3"/>
    <circle cx="36" cy="36" r="10" fill="#63E3D1"/>
    <path d="M36 8 L44 24 L64 36 L44 48 L36 64 L28 48 L8 36 L28 24 Z" fill="none" stroke="#FFCB63" stroke-opacity="0.45" stroke-width="2"/>
    <text x="92" y="30" fill="#FFCB63" font-size="18" font-weight="700" font-family="'Avenir Next', 'Segoe UI', sans-serif" letter-spacing="2.4">PORTFOLIO POSTER</text>
    <text x="92" y="74" fill="#F7F3EA" font-size="54" font-weight="800" font-family="'Avenir Next', 'Segoe UI', sans-serif">CineDepth Pro</text>
    <text x="92" y="103" fill="#C9C0B1" font-size="20" font-weight="500" font-family="'Avenir Next', 'Segoe UI', sans-serif">Z-depth computational photography engine for mobile portrait rendering</text>
  </g>

  {pill(1320, 58, 118, 38, "Android", "#FFCB63", "#FFDF9B", "#17120A")}
  {pill(1452, 58, 92, 38, "AGSL", "rgba(255,255,255,0.05)", "rgba(255,255,255,0.14)", "#F7F3EA")}
  {pill(1556, 58, 106, 38, "TFLite", "rgba(255,255,255,0.05)", "rgba(255,255,255,0.14)", "#F7F3EA")}
  {pill(1676, 58, 110, 38, "Depth Pro", "rgba(99,227,209,0.16)", "rgba(99,227,209,0.34)", "#DDFCF7")}

  <rect x="48" y="150" width="500" height="470" rx="34" fill="rgba(7,9,12,0.72)" stroke="rgba(255,255,255,0.10)" stroke-width="1.2" filter="url(#shadow)"/>
  <text x="86" y="200" fill="#FFCB63" font-size="18" font-weight="700" font-family="'Avenir Next', 'Segoe UI', sans-serif" letter-spacing="2.1">PROJECT POSITIONING</text>
  {wrapped_text(86, 246, "A repo-level showcase of mobile CV, GPU rendering, and editing UX", width=398, font_size=30, line_height=1.0, fill="#F8F4EB", weight="780")}
  {wrapped_text(86, 378, "Single-image portrait rendering that combines ML depth, portrait segmentation, and AGSL lens simulation. The repository is framed as an end-to-end engineering showcase: preview, retouch, server fallback, and photo-safe export.", width=410, font_size=16, fill="#CAC2B5")}
  {info_tile(80, 472, 188, 82, "On-device ML", "Depth-Anything-V2 on device.", "#FFCB63")}
  {info_tile(282, 472, 220, 82, "HD fallback", "Depth Pro server fallback.", "#63E3D1")}
  {info_tile(80, 562, 188, 58, "Retouchable", "Direct depth repair.", "#8CB6FF")}
  {info_tile(282, 562, 220, 58, "Photo-safe export", "EXIF preserved.", "#F2D7A5")}

  <rect x="568" y="150" width="844" height="470" rx="34" fill="rgba(7,9,12,0.74)" stroke="rgba(255,255,255,0.10)" stroke-width="1.2" filter="url(#shadow)"/>
  <text x="598" y="196" fill="#FFCB63" font-size="18" font-weight="700" font-family="'Avenir Next', 'Segoe UI', sans-serif" letter-spacing="2.1">REAL OUTPUT</text>
  <text x="598" y="230" fill="#F8F4EB" font-size="28" font-weight="720" font-family="'Avenir Next', 'Segoe UI', sans-serif">Source capture vs CineDepth Pro render</text>
  <rect x="590" y="176" width="792" height="360" rx="26" fill="#101317"/>
  <image href="{montage}" x="590" y="176" width="792" height="360" preserveAspectRatio="xMidYMid slice" clip-path="url(#heroClip)"/>
  <rect x="610" y="194" width="130" height="36" rx="18" fill="rgba(8,8,10,0.68)" stroke="rgba(255,255,255,0.14)" stroke-width="1"/>
  <text x="675" y="217" fill="#F8F4EB" font-size="16" font-weight="700" font-family="'Avenir Next', 'Segoe UI', sans-serif" text-anchor="middle">Original</text>
  <rect x="1230" y="194" width="154" height="36" rx="18" fill="rgba(8,8,10,0.68)" stroke="rgba(255,203,99,0.55)" stroke-width="1.2"/>
  <text x="1307" y="217" fill="#FFF3D0" font-size="16" font-weight="700" font-family="'Avenir Next', 'Segoe UI', sans-serif" text-anchor="middle">CineDepth Pro</text>
  {wrapped_text(598, 572, "This scene montage comes from the repo assets and demonstrates the project goal clearly: keep the subject credible while pushing the background into a lens-shaped depth-of-field treatment.", width=776, font_size=18, fill="#C8C0B5")}

  <rect x="1432" y="150" width="440" height="470" rx="34" fill="rgba(7,9,12,0.72)" stroke="rgba(255,255,255,0.10)" stroke-width="1.2" filter="url(#shadow)"/>
  <text x="1462" y="196" fill="#63E3D1" font-size="18" font-weight="700" font-family="'Avenir Next', 'Segoe UI', sans-serif" letter-spacing="2.1">INTERACTIVE WORKFLOW</text>
  <text x="1462" y="230" fill="#F8F4EB" font-size="28" font-weight="720" font-family="'Avenir Next', 'Segoe UI', sans-serif">Depth review, contour tuning, retouch confirmation</text>
  {phone_card("depth", 1458, 264, 126, 320, "HD depth", depth, "#FFCB63")}
  {phone_card("transition", 1589, 264, 126, 320, "Edge controls", transition, "#63E3D1")}
  {phone_card("retouch", 1720, 264, 126, 320, "Retouch fill", retouched, "#F6D89E")}

  <rect x="48" y="650" width="1180" height="360" rx="34" fill="rgba(7,9,12,0.72)" stroke="rgba(255,255,255,0.10)" stroke-width="1.2" filter="url(#shadow)"/>
  <text x="86" y="698" fill="#FFCB63" font-size="18" font-weight="700" font-family="'Avenir Next', 'Segoe UI', sans-serif" letter-spacing="2.1">SYSTEM PIPELINE</text>
  <text x="86" y="734" fill="#F8F4EB" font-size="30" font-weight="740" font-family="'Avenir Next', 'Segoe UI', sans-serif">From single image input to portfolio-grade export</text>

  <path d="M206 786 H330" stroke="rgba(255,255,255,0.22)" stroke-width="3" stroke-linecap="round"/>
  <path d="M506 786 H630" stroke="rgba(255,255,255,0.22)" stroke-width="3" stroke-linecap="round"/>
  <path d="M806 786 H930" stroke="rgba(255,255,255,0.22)" stroke-width="3" stroke-linecap="round"/>
  <path d="M1106 786 H1160" stroke="rgba(255,255,255,0.22)" stroke-width="3" stroke-linecap="round"/>

  {pipeline_step(180, 786, 1, "Input photo", "User selects a portrait or lifestyle shot inside the Compose app.", "#FFCB63")}
  {pipeline_step(480, 786, 2, "Depth + seg", "Depth estimation and portrait segmentation run in parallel to keep the preview responsive.", "#63E3D1")}
  {pipeline_step(780, 786, 3, "Refine depth", "A luma-guided refinement shader snaps coarse depth edges back to image structure.", "#8CB6FF")}
  {pipeline_step(1080, 786, 4, "Retouch matte", "Selection and draw tools repair hats, hair, and contour transitions numerically.", "#F5D6A0")}
  {pipeline_step(180, 888, 5, "Lens render", "AGSL passes synthesize blur, highlights, and anamorphic flare.", "#FFCB63")}
  {pipeline_step(780, 888, 6, "Save export", "4K render copies EXIF tags so the result still behaves like a photo asset.", "#63E3D1")}

  <path d="M506 888 H630" stroke="rgba(255,255,255,0.22)" stroke-width="3" stroke-linecap="round"/>
  <path d="M1106 888 H1160" stroke="rgba(255,255,255,0.22)" stroke-width="3" stroke-linecap="round"/>

  <rect x="82" y="964" width="1112" height="36" rx="18" fill="rgba(255,255,255,0.05)" stroke="rgba(255,255,255,0.10)" stroke-width="1"/>
  <text x="638" y="987" fill="#D0C7BB" font-size="16" font-weight="600" font-family="'Avenir Next', 'Segoe UI', sans-serif" text-anchor="middle">DepthBlurEngine measures depth inference, shader pass, and total render time while keeping preview caches for iteration.</text>

  <rect x="1256" y="650" width="616" height="188" rx="30" fill="rgba(7,9,12,0.72)" stroke="rgba(255,255,255,0.10)" stroke-width="1.2" filter="url(#shadow)"/>
  <text x="1288" y="698" fill="#63E3D1" font-size="18" font-weight="700" font-family="'Avenir Next', 'Segoe UI', sans-serif" letter-spacing="2.1">REPO ARCHITECTURE</text>
  {architecture_block(1282, 724, 182, 96, "Android UI", "Compose app shell, AGSL shaders, preview and export.", ["AppRoot.kt + DepthBlurEngine.kt"], "#FFCB63")}
  {architecture_block(1474, 724, 182, 96, "Research", "Python sandbox for focus interaction and lens experiments.", ["main.py + lens_sim.py"], "#8CB6FF")}
  {architecture_block(1666, 724, 182, 96, "Ultra Depth", "FastAPI service plus client hook for Depth Pro fallback.", ["app.py + UltraDepthClient.kt"], "#63E3D1")}

  <rect x="1256" y="850" width="616" height="160" rx="30" fill="rgba(7,9,12,0.72)" stroke="rgba(255,255,255,0.10)" stroke-width="1.2" filter="url(#shadow)"/>
  <text x="1288" y="892" fill="#FFCB63" font-size="18" font-weight="700" font-family="'Avenir Next', 'Segoe UI', sans-serif" letter-spacing="2.1">KEY DIFFERENTIATORS</text>
  {feature_chip(1286, 912, 170, "Golden-angle bokeh", "#FFCB63")}
  {feature_chip(1468, 912, 160, "Portrait fusion", "#63E3D1")}
  {feature_chip(1640, 912, 206, "Anamorphic flare mode", "#F4D9A4")}
  {feature_chip(1286, 960, 172, "Edge-aware depth", "#8CB6FF")}
  {feature_chip(1470, 960, 152, "Lens presets", "#F2C6A0")}
  {feature_chip(1634, 960, 212, "EXIF-preserving export", "#E8E0D2")}
  {wrapped_text(1288, 1020, "Repo screenshots anchor the board, while the vector workflow and architecture layers turn it into a clean engineering portfolio poster instead of a README collage.", width=552, font_size=15, fill="#CBC2B7")}

  <text x="48" y="1056" fill="#8D877E" font-size="14" font-weight="600" font-family="'SF Mono', Menlo, monospace">Generated from /docs/assets plus source modules in android_ui_prototype/, research_prototype/, and ultra_depth_server/.</text>
</svg>
"""

    OUTPUT_PATH.write_text(svg, encoding="utf-8")
    print(f"Wrote {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
