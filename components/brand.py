"""
Brand mark for the app, shared by every surface that shows the logo
(landing navbar, mobile bar, landing footer, sidebar header, in-app home).
"""


def logo_svg(uid: str, size: int = 30) -> str:
    """Dataset mark: three table rows that start ragged and broken on the
    left ("raw") and come out solid, aligned and equal-length on the right
    ("ready"), with an arrow doing the "2" in between and an AI sparkle
    above — a literal read of the Raw2Ready AI name, shown at every screen
    size (mobile bar, desktop row, sidebar, footer all call this).

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

    gid = f"logoGrad-{uid}"

    parts = [
        f'<svg width="{size}" height="{size}" viewBox="0 0 32 32" role="img"'
        f' aria-label="Raw2Ready AI" xmlns="http://www.w3.org/2000/svg">',
        f'<defs><linearGradient id="{gid}" x1="0%" y1="0%" x2="100%" y2="100%">',
        '<stop offset="0%" stop-color="#F472B6"/>',
        '<stop offset="100%" stop-color="#DB2777"/>',
        '</linearGradient></defs>',
        # badge
        f'<rect x="1.25" y="1.25" width="29.5" height="29.5" rx="9" fill="url(#{gid})" opacity="0.16"/>',
        f'<rect x="1.25" y="1.25" width="29.5" height="29.5" rx="9" fill="none"'
        f' stroke="url(#{gid})" stroke-width="1.5"/>',
        # AI sparkle
        f'<path d="M24.3 4.9 L25.2 6.4 L26.7 7.3 L25.2 8.2 L24.3 9.7 L23.4 8.2 L21.9 7.3 L23.4 6.4 Z"'
        f' fill="url(#{gid})"/>',
        # raw: ragged, broken, unequal rows
        f'<g fill="url(#{gid})" opacity="0.5">',
        '<rect x="6.9" y="10.8" width="4.6" height="2.6" rx="1.3"/>',
        '<rect x="12.4" y="10.8" width="1.6" height="2.6" rx="0.8"/>',
        '<rect x="6.9" y="15.9" width="6.2" height="2.6" rx="1.3"/>',
        '<rect x="6.9" y="21.0" width="3.2" height="2.6" rx="1.3"/>',
        '<rect x="11.2" y="21.0" width="2.4" height="2.6" rx="1.2"/>',
        '</g>',
        # the "2": raw becomes ready
        f'<path d="M15.3 13.9 L17.9 17.2 L15.3 20.5" fill="none" stroke="url(#{gid})"'
        f' stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"/>',
        # ready: solid, aligned, equal rows
        f'<g fill="url(#{gid})">',
        '<rect x="19.4" y="10.8" width="5.9" height="2.6" rx="1.3"/>',
        '<rect x="19.4" y="15.9" width="5.9" height="2.6" rx="1.3"/>',
        '<rect x="19.4" y="21.0" width="5.9" height="2.6" rx="1.3"/>',
        '</g>',
        '</svg>',
    ]

    return "".join(parts)
