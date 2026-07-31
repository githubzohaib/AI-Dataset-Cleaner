"""
Brand mark for the app, shared by every surface that shows the logo
(landing navbar, mobile bar, landing footer, sidebar header, in-app home).
"""

# Streamlit's own default face first so the monogram matches the wordmark
# sitting next to it, then platform fallbacks.
_FONT_STACK = (
    "'Source Sans Pro','Segoe UI',system-ui,-apple-system,"
    "'Helvetica Neue',Arial,sans-serif"
)


def logo_svg(uid: str, size: int = 30) -> str:
    """R2R monogram: the Raw2Ready initials in a rounded gradient badge,
    with the "2" carrying the brand gradient and the two R's in a brighter
    pink so all three glyphs stay legible at 30px.

    Takes a unique id per call site: several copies of this SVG land in the
    DOM at once (mobile bar, desktop row, footer), and a shared gradient id
    would collide — when the first copy sits inside a `display:none`
    ancestor (e.g. the desktop row while the mobile bar is showing), browsers
    resolve every `url(#logoGrad)` reference to that hidden copy's gradient
    and the icon silently fails to paint anywhere on the page.

    Returned as ONE line with no blank lines and no comments: every caller
    feeds this to st.markdown, which parses the string as Markdown before
    the HTML reaches the DOM. A blank line closes an open HTML block
    (CommonMark), so an SVG pretty-printed with blank lines between its
    groups gets truncated at the first one and paints as an empty box.
    """

    badge = f"badgeGrad-{uid}"
    text = f"textGrad-{uid}"

    parts = [
        f'<svg width="{size}" height="{size}" viewBox="0 0 32 32" role="img"'
        f' aria-label="Raw2Ready AI" xmlns="http://www.w3.org/2000/svg">',
        '<defs>',
        f'<linearGradient id="{badge}" x1="0%" y1="0%" x2="100%" y2="100%">',
        '<stop offset="0%" stop-color="#F472B6"/>',
        '<stop offset="100%" stop-color="#DB2777"/>',
        '</linearGradient>',
        # A brighter ramp for the glyphs: the badge gradient's dark end
        # disappears against the app's near-black background at this size.
        f'<linearGradient id="{text}" x1="0%" y1="0%" x2="100%" y2="100%">',
        '<stop offset="0%" stop-color="#FBCFE8"/>',
        '<stop offset="100%" stop-color="#EC4899"/>',
        '</linearGradient>',
        '</defs>',
        # badge
        f'<rect x="1.25" y="1.25" width="29.5" height="29.5" rx="9" fill="url(#{badge})" opacity="0.16"/>',
        f'<rect x="1.25" y="1.25" width="29.5" height="29.5" rx="9" fill="none"'
        f' stroke="url(#{badge})" stroke-width="1.5"/>',
        # R2R monogram, centred by anchor so it survives font substitution
        f'<text x="16" y="16.2" text-anchor="middle" dominant-baseline="central"'
        f' font-family="{_FONT_STACK}" font-size="11.5" font-weight="800"'
        f' letter-spacing="-0.2" fill="#F9A8D4">'
        f'R<tspan fill="url(#{text})">2</tspan>R'
        f'</text>',
        '</svg>',
    ]

    return "".join(parts)
