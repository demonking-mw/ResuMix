"""
Escape user text for reportlab's Paragraph markup.

Paragraph parses a small XML dialect, so raw resume text containing something
that looks like a tag was silently swallowed — "Wrote a <div> renderer" rendered
as "Wrote a renderer". The editor documents <b>, <i> and <a href=...> as
supported formatting, so those are kept, but only when they are balanced:
"Compared <b> and <i> handling" is prose, not markup, and an unbalanced tag
makes reportlab raise.
"""

import re

from .fonts import cid_font_for, ensure_cid_font

# Tags the resume editor documents, plus the inline ones reportlab supports.
PAIRED_TAGS = ("a", "b", "i", "u", "em", "font", "strike", "strong", "sub", "super")
VOID_TAGS = ("br",)

_OPEN_RE = {
    tag: re.compile(rf"<{tag}(?:\s[^<>]*)?>", re.IGNORECASE) for tag in PAIRED_TAGS
}
_CLOSE_RE = {tag: re.compile(rf"</{tag}\s*>", re.IGNORECASE) for tag in PAIRED_TAGS}
_VOID_RE = re.compile(r"<(?:" + "|".join(VOID_TAGS) + r")\s*/?>", re.IGNORECASE)
_ENTITY_RE = re.compile(r"&(?:#\d+|#x[0-9A-Fa-f]+|[A-Za-z][A-Za-z0-9]*);")


def _balanced_tags(text: str) -> tuple:
    """Tag names that appear as matching open/close pairs in this text."""
    return tuple(
        tag
        for tag in PAIRED_TAGS
        if len(_OPEN_RE[tag].findall(text)) == len(_CLOSE_RE[tag].findall(text))
        and _OPEN_RE[tag].search(text)
    )


def _escape(chunk: str) -> str:
    parts = []
    pos = 0
    for entity in _ENTITY_RE.finditer(chunk):
        parts.append(chunk[pos : entity.start()].replace("&", "&amp;"))
        parts.append(entity.group(0))
        pos = entity.end()
    parts.append(chunk[pos:].replace("&", "&amp;"))
    return "".join(parts).replace("<", "&lt;").replace(">", "&gt;")


def _tag_cjk(chunk: str) -> str:
    """Wrap CJK runs so reportlab renders them with a CID font."""
    out = []
    run = []
    run_font = None
    for char in chunk:
        font = cid_font_for(char)
        if font != run_font:
            if run:
                out.append(_emit(run, run_font))
            run, run_font = [], font
        run.append(char)
    if run:
        out.append(_emit(run, run_font))
    return "".join(out)


def _emit(run: list, font) -> str:
    text = "".join(run)
    if font and ensure_cid_font(font):
        return f'<font name="{font}">{text}</font>'
    return text


def safe_markup(text) -> str:
    """Escape everything except balanced, supported inline tags."""
    if not isinstance(text, str):
        return text

    keep = _balanced_tags(text)
    patterns = [_VOID_RE]
    for tag in keep:
        patterns.append(_OPEN_RE[tag])
        patterns.append(_CLOSE_RE[tag])

    spans = sorted(
        (m.start(), m.end(), m.group(0))
        for pattern in patterns
        for m in pattern.finditer(text)
    )

    out = []
    pos = 0
    for start, end, tag in spans:
        if start < pos:
            continue
        out.append(_tag_cjk(_escape(text[pos:start])))
        out.append(tag)
        pos = end
    out.append(_tag_cjk(_escape(text[pos:])))
    return "".join(out)
