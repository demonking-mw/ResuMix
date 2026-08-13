"""
PDF font handling.

The base-14 PDF fonts (Times, Helvetica) only cover Latin-1, so anything outside
it — Cyrillic, Greek, CJK, emoji — rendered as black boxes. This module registers
a Unicode TrueType family when one can be found and maps the base-14 names onto
it. If nothing suitable is available the base-14 names are used unchanged, so PDF
generation never fails because of a missing font.

Point RESUMIX_PDF_FONT at a .ttf (or a directory holding Regular/Bold/Italic
variants) to choose the font yourself — for example a CJK-capable one.
"""

import os
from pathlib import Path

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.fonts import addMapping

FAMILY = "ResuMix"

# (regular, bold, italic, bold-italic); later entries are fallbacks.
# Noto CJK is deliberately absent: those files use PostScript outlines that
# reportlab cannot embed. CJK is handled by the CID fonts further down.
_CANDIDATES = [
    (
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Italic.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif-BoldItalic.ttf",
    ),
    (
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Oblique.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-BoldOblique.ttf",
    ),
    (
        "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSerif-BoldItalic.ttf",
    ),
    (
        "/Library/Fonts/Arial Unicode.ttf",
        "/Library/Fonts/Arial Unicode.ttf",
        "/Library/Fonts/Arial Unicode.ttf",
        "/Library/Fonts/Arial Unicode.ttf",
    ),
    (
        "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/arialbd.ttf",
        "C:/Windows/Fonts/ariali.ttf",
        "C:/Windows/Fonts/arialbi.ttf",
    ),
]

# Base-14 names used by the templates, mapped onto the registered family.
_BASE14_TO_FAMILY = {
    "Times-Roman": FAMILY,
    "Helvetica": FAMILY,
    "Times-Bold": f"{FAMILY}-Bold",
    "Helvetica-Bold": f"{FAMILY}-Bold",
    "Times-Italic": f"{FAMILY}-Italic",
    "Helvetica-Oblique": f"{FAMILY}-Italic",
    "Times-BoldItalic": f"{FAMILY}-BoldItalic",
    "Helvetica-BoldOblique": f"{FAMILY}-BoldItalic",
}


def _from_env():
    configured = (os.getenv("RESUMIX_PDF_FONT") or "").strip()
    if not configured:
        return None
    path = Path(configured).expanduser()
    if path.is_dir():
        faces = sorted(path.glob("*.[tT][tT][fF]"))
        if not faces:
            return None
        regular = next((f for f in faces if "bold" not in f.name.lower()), faces[0])
        bold = next((f for f in faces if "bold" in f.name.lower()), regular)
        italic = next(
            (f for f in faces if "italic" in f.name.lower() or "oblique" in f.name.lower()),
            regular,
        )
        return (str(regular), str(bold), str(italic), str(bold))
    if path.is_file():
        return (str(path),) * 4
    return None


def _make_font(name: str, path: str) -> TTFont:
    """TrueType collections need a subfont index."""
    if path.lower().endswith(".ttc"):
        return TTFont(name, path, subfontIndex=0)
    return TTFont(name, path)


def _register() -> dict:
    """Register the first available Unicode family; return the name mapping."""
    options = [c for c in ([_from_env()] + _CANDIDATES) if c]
    for regular, bold, italic, bold_italic in options:
        if not Path(regular).is_file():
            continue
        try:
            pdfmetrics.registerFont(_make_font(FAMILY, regular))
            for suffix, face in (
                ("-Bold", bold),
                ("-Italic", italic),
                ("-BoldItalic", bold_italic),
            ):
                pdfmetrics.registerFont(
                    _make_font(
                        f"{FAMILY}{suffix}", face if Path(face).is_file() else regular
                    )
                )
            addMapping(FAMILY, 0, 0, FAMILY)
            addMapping(FAMILY, 1, 0, f"{FAMILY}-Bold")
            addMapping(FAMILY, 0, 1, f"{FAMILY}-Italic")
            addMapping(FAMILY, 1, 1, f"{FAMILY}-BoldItalic")
            return dict(_BASE14_TO_FAMILY)
        except Exception as exc:  # noqa: BLE001 - fall back to base-14
            print(f"WARNING: could not register {regular}: {exc}")
    print(
        "WARNING: no Unicode TTF found; PDFs fall back to Latin-1 fonts and "
        "non-Latin characters will not render. Set RESUMIX_PDF_FONT to a .ttf."
    )
    return {}


_FONT_MAP = _register()

UNICODE_FONTS_AVAILABLE = bool(_FONT_MAP)


def resolve_font(font_name: str) -> str:
    """Map a base-14 font name onto the registered Unicode family, if any."""
    return _FONT_MAP.get(font_name, font_name)


# --------------------------------------------------------------------- CJK ---
# TrueType families rarely carry CJK glyphs, and the Noto CJK files shipped on
# most Linux distributions use PostScript outlines that reportlab cannot embed.
# reportlab does ship CID fonts for these scripts, so CJK runs are tagged to use
# them instead of silently disappearing.
_CID_FONTS = {
    "cjk": "STSong-Light",  # Chinese
    "kana": "HeiseiMin-W3",  # Japanese
    "hangul": "HYSMyeongJo-Medium",  # Korean
}
_registered_cid: set = set()


def cid_font_for(char: str):
    """Return the CID font name needed to render this character, if any."""
    code = ord(char)
    if 0x3040 <= code <= 0x30FF:
        return _CID_FONTS["kana"]
    if 0xAC00 <= code <= 0xD7AF or 0x1100 <= code <= 0x11FF:
        return _CID_FONTS["hangul"]
    if (
        0x3400 <= code <= 0x4DBF
        or 0x4E00 <= code <= 0x9FFF
        or 0xF900 <= code <= 0xFAFF
        or 0x3000 <= code <= 0x303F
    ):
        return _CID_FONTS["cjk"]
    return None


def ensure_cid_font(name: str) -> bool:
    """Register a built-in CID font on first use."""
    if name in _registered_cid:
        return True
    try:
        from reportlab.pdfbase.cidfonts import UnicodeCIDFont

        pdfmetrics.registerFont(UnicodeCIDFont(name))
        _registered_cid.add(name)
        return True
    except Exception as exc:  # noqa: BLE001
        print(f"WARNING: could not register CID font {name}: {exc}")
        return False
