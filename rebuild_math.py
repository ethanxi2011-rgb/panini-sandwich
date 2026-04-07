#!/usr/bin/env python3
"""Reorganize math.html into topic groups with group banners and subsection tabs."""

import re

with open('math_original.html', 'r') as f:
    original = f.read()

# ── Extract everything before <main> (head + nav + hero + old toc) ──
# We'll keep head/nav/hero but replace the toc and main content

head_end = original.index('<main>')
# We want everything up to (but not including) the old toc+main
# Find the toc div start
toc_start = original.index('\n<!-- TOC -->')
before_toc = original[:toc_start]  # head + nav + hero

after_main_close = original[original.rindex('</main>') + len('</main>'):]  # footer + </body></html>

# ── Extract each section div by id ──
def extract_section(html, section_id):
    """Extract a <div class="unit" id="..."> ... </div> block."""
    pattern = rf'<div class="unit" id="{re.escape(section_id)}">'
    m = re.search(pattern, html)
    if not m:
        raise ValueError(f"Section not found: {section_id}")
    start = m.start()
    # Walk forward counting div open/close tags
    depth = 0
    i = start
    while i < len(html):
        open_m = re.search(r'<div', html[i:])
        close_m = re.search(r'</div>', html[i:])
        if open_m is None and close_m is None:
            break
        if open_m is None:
            close_pos = i + close_m.start()
        elif close_m is None:
            open_pos = i + open_m.start()
        else:
            open_pos = i + open_m.start()
            close_pos = i + close_m.start()
        
        if close_m is None or (open_m is not None and open_pos < close_pos):
            depth += 1
            i = i + open_m.start() + 1
        else:
            depth -= 1
            i = close_pos + len('</div>')
            if depth == 0:
                return html[start:i]
    raise ValueError(f"Could not find closing tag for: {section_id}")

# ── Group definitions ──
groups = [
    {
        'num': 1,
        'emoji': '📚',
        'title': 'Polynomials — The Basics',
        'gradient': 'linear-gradient(135deg, #1a2a4a, #3b6cf7)',
        'toc_gradient': 'linear-gradient(90deg, #3b6cf7, #5a82f9)',
        'tab_bg': '#eef2ff',
        'tab_border': '#3b6cf7',
        'tab_color': '#1a2a4a',
        'sections': [
            ('intropolynomials', 'Intro to Polynomials'),
            ('simplifypolynomials', 'Simplifying & Standard Form'),
        ]
    },
    {
        'num': 2,
        'emoji': '✖️',
        'title': 'Multiplying Polynomials',
        'gradient': 'linear-gradient(135deg, #0d4a3a, #1a9e78)',
        'toc_gradient': 'linear-gradient(90deg, #1a9e78, #22c49a)',
        'tab_bg': '#e6f7f2',
        'tab_border': '#1a9e78',
        'tab_color': '#0d4a3a',
        'sections': [
            ('mod51day1', 'Monomial × Polynomial (5.1 D1)'),
            ('polynomials', 'FOIL, Distribution, Box Method (5.2 D2)'),
            ('mod53', 'Special Products (5.3)'),
        ]
    },
    {
        'num': 3,
        'emoji': '📉',
        'title': 'Graphing Quadratics',
        'gradient': 'linear-gradient(135deg, #2d1a5a, #7c3cf7)',
        'toc_gradient': 'linear-gradient(90deg, #7c3cf7, #9b62f9)',
        'tab_bg': '#f0ebff',
        'tab_border': '#7c3cf7',
        'tab_color': '#2d1a5a',
        'sections': [
            ('mod61day1', 'Graphing at Origin (6.1 D1)'),
            ('mod61day2', 'Domain, Range & Comparison (6.1 D2)'),
            ('mod62', 'Vertex Form & Transformations (6.2)'),
            ('mod63day1', 'Identifying Quadratics (6.3 D1)'),
            ('graphzeros', 'Graphing Using Zeros'),
            ('standardgraph', 'Graphing in Standard Form'),
        ]
    },
    {
        'num': 4,
        'emoji': '🎯',
        'title': 'Solving Quadratics',
        'gradient': 'linear-gradient(135deg, #4a1a1a, #c73b3b)',
        'toc_gradient': 'linear-gradient(90deg, #c73b3b, #e05555)',
        'tab_bg': '#fdf0f0',
        'tab_border': '#c73b3b',
        'tab_color': '#4a1a1a',
        'sections': [
            ('zeroproduct', 'Zero Product Property'),
            ('distrib', 'Distributive + Zero Product'),
            ('factoringvars', 'Factoring with Variables & Grouping'),
            ('specialfactors', 'Special Factoring Patterns'),
            ('factorsolve', 'Factoring to Solve'),
            ('sqrtmethod', 'Square Root Method'),
            ('ctss', 'Completing the Square to Solve'),
            ('quadformula', 'Quadratic Formula'),
            ('vertexform', 'Vertex Form'),
        ]
    },
    {
        'num': 5,
        'emoji': '🌍',
        'title': 'Word Problems',
        'gradient': 'linear-gradient(135deg, #4a3400, #c78f00)',
        'toc_gradient': 'linear-gradient(90deg, #c78f00, #e0a800)',
        'tab_bg': '#fdf8e6',
        'tab_border': '#c78f00',
        'tab_color': '#4a3400',
        'sections': [
            ('quadratic', 'Real-World Quadratics'),
            ('wordproblems', 'Quadratic Word Problems'),
            ('stdformword', 'Standard Form Extra Examples'),
        ]
    },
    {
        'num': 6,
        'emoji': '🌀',
        'title': 'Complex & Imaginary Numbers',
        'gradient': 'linear-gradient(135deg, #4a0a4a, #b03abf)',
        'toc_gradient': 'linear-gradient(90deg, #b03abf, #cc55d6)',
        'tab_bg': '#faeeff',
        'tab_border': '#b03abf',
        'tab_color': '#4a0a4a',
        'sections': [
            ('complex', 'Complex Numbers'),
            ('imaginary', 'Powers of i'),
            ('imagsolve', 'Imaginary Solutions'),
            ('discdetail', 'The Discriminant'),
        ]
    },
    {
        'num': 7,
        'emoji': '🔵',
        'title': 'Circles & Parabolas',
        'gradient': 'linear-gradient(135deg, #0a3a4a, #1a8ab0)',
        'toc_gradient': 'linear-gradient(90deg, #1a8ab0, #26a8d4)',
        'tab_bg': '#e6f5fa',
        'tab_border': '#1a8ab0',
        'tab_color': '#0a3a4a',
        'sections': [
            ('circles', 'Circles Module 12.1'),
            ('completing', 'Completing the Square — Circles'),
            ('parabolas', 'Parabolas Focus & Directrix'),
            ('focusdirectrix2', 'Parabola Equation from Focus & Directrix'),
            ('systems', 'Linear-Quadratic Systems'),
        ]
    },
    {
        'num': 8,
        'emoji': '√',
        'title': 'Radicals & Conjugates',
        'gradient': 'linear-gradient(135deg, #1a3a1a, #3a8a3a)',
        'toc_gradient': 'linear-gradient(90deg, #3a8a3a, #4db04d)',
        'tab_bg': '#edf7ed',
        'tab_border': '#3a8a3a',
        'tab_color': '#1a3a1a',
        'sections': [
            ('simplifyroots', 'Simplifying Square Roots'),
            ('conjugates', 'Conjugates'),
        ]
    },
]

# ── Build CSS additions (injected into <style> before </style>) ──
extra_css = """
    /* ── GROUP & SUBSECTION STYLES ── */
    .group-banner {
      color: white;
      padding: 1.5rem 2rem;
      margin: 3rem 0 0;
      border-radius: 1rem 1rem 0 0;
    }
    .group-banner-num {
      font-size: 0.7rem;
      font-weight: 700;
      letter-spacing: 0.2em;
      text-transform: uppercase;
      opacity: 0.7;
      margin-bottom: 0.3rem;
    }
    .group-banner-title {
      font-family: 'Playfair Display', serif;
      font-size: 1.6rem;
      font-weight: 700;
    }

    .subsection-wrapper {
      margin-bottom: 0.5rem;
    }
    .subsection-tab {
      display: flex;
      align-items: center;
      gap: 0.75rem;
      padding: 0.55rem 1.5rem;
      border-left: 4px solid transparent;
      margin-top: 0.5rem;
    }
    .subsection-tab-num {
      font-size: 0.68rem;
      font-weight: 800;
      letter-spacing: 0.15em;
      text-transform: uppercase;
      font-family: 'JetBrains Mono', monospace;
    }
    .subsection-tab-name {
      font-size: 0.78rem;
      font-weight: 600;
      letter-spacing: 0.04em;
    }

    .unit {
      margin-top: 0 !important;
      border-top: none !important;
      background: white;
      border: 1px solid #dde8ff;
      border-top: none;
      border-radius: 0 0 0.75rem 0.75rem;
      padding: 2rem 2rem 2rem;
    }

    /* TOC groups */
    .toc-wrapper {
      max-width: 900px;
      margin: 2rem auto;
      padding: 0 1rem;
    }
    .toc-group {
      background: white;
      border-radius: 1rem;
      border: 1px solid #dde8ff;
      margin-bottom: 0.75rem;
      overflow: hidden;
    }
    .toc-group-header {
      padding: 0.75rem 1.25rem;
      font-size: 0.78rem;
      font-weight: 700;
      letter-spacing: 0.1em;
      text-transform: uppercase;
      color: white;
    }
    .toc-group-links {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 0;
      padding: 0.5rem 1rem 0.75rem;
    }
    .toc-group-links a {
      text-decoration: none;
      color: var(--accent);
      font-size: 0.88rem;
      font-weight: 600;
      padding: 0.25rem 0.25rem;
      display: block;
      border-bottom: 1px solid #f0f4ff;
      transition: color 0.2s;
    }
    .toc-group-links a:hover { color: var(--blue); }
"""

# ── Build TOC HTML ──
def build_toc(groups):
    lines = ['\n<!-- TOC -->\n<div class="toc-wrapper">\n']
    for g in groups:
        lines.append(f'  <div class="toc-group">')
        lines.append(f'    <div class="toc-group-header" style="background: {g["toc_gradient"]};">'
                     f'{g["emoji"]} Group {g["num"]} — {g["title"]}</div>')
        lines.append(f'    <div class="toc-group-links">')
        for idx, (sid, sname) in enumerate(g['sections'], 1):
            # escape & in names
            safe_name = sname.replace('&', '&amp;')
            lines.append(f'      <a href="#{sid}">{g["num"]}.{idx} · {safe_name}</a>')
        lines.append(f'    </div>')
        lines.append(f'  </div>\n')
    # Quick ref
    lines.append('  <div class="toc-group">')
    lines.append('    <div class="toc-group-header" style="background: linear-gradient(90deg, #1a2a4a, #2a3a5a);">⚡ Quick Reference</div>')
    lines.append('    <div class="toc-group-links"><a href="#quickref">⚡ All Key Formulas (Cheat Sheet)</a></div>')
    lines.append('  </div>\n')
    lines.append('</div>\n')
    return '\n'.join(lines)

# ── Build main content HTML ──
def build_main(groups, original_html):
    lines = ['\n<main>\n']
    
    for g in groups:
        # Group banner
        lines.append(f'  <!-- {"═"*50} -->')
        lines.append(f'  <!-- GROUP {g["num"]}: {g["title"].upper()} -->')
        lines.append(f'  <!-- {"═"*50} -->')
        lines.append(f'  <div class="group-banner" style="background: {g["gradient"]};">')
        lines.append(f'    <div class="group-banner-num">Group {g["num"]}</div>')
        lines.append(f'    <div class="group-banner-title">{g["emoji"]} {g["title"]}</div>')
        lines.append(f'  </div>')
        lines.append('')
        
        for idx, (sid, sname) in enumerate(g['sections'], 1):
            safe_name = sname.replace('&', '&amp;')
            section_html = extract_section(original_html, sid)
            # Subsection wrapper + tab + unit
            lines.append(f'  <div class="subsection-wrapper">')
            lines.append(
                f'    <div class="subsection-tab" style="'
                f'background: {g["tab_bg"]}; '
                f'border-left-color: {g["tab_border"]}; '
                f'color: {g["tab_color"]};">'
            )
            lines.append(
                f'      <span class="subsection-tab-num">{g["num"]}.{idx}</span>'
                f'<span class="subsection-tab-name">{safe_name}</span>'
            )
            lines.append(f'    </div>')
            # Indent the section block
            indented = '\n'.join('    ' + ln for ln in section_html.split('\n'))
            lines.append(indented)
            lines.append(f'  </div>\n')
    
    # Quick ref (no group wrapper needed, just append at bottom)
    quickref = extract_section(original_html, 'quickref')
    lines.append('  <!-- QUICK REFERENCE -->')
    lines.append(quickref)
    lines.append('')
    lines.append('</main>')
    return '\n'.join(lines)

# ── Inject extra CSS before </style> ──
head_with_css = before_toc.replace('</style>', extra_css + '\n  </style>')

# Also update the nav links to reflect new structure
new_nav = '''<nav>
  <a href="/" class="logo">🥪 Panini</a>
  <button class="nav-toggle" onclick="document.querySelector('nav ul').classList.toggle('open')" aria-label="Menu">
    <span></span><span></span><span></span>
  </button>
  <ul>
    <li><a href="#intropolynomials">Polynomials</a></li>
    <li><a href="#mod61day1">Graphing</a></li>
    <li><a href="#zeroproduct">Solving</a></li>
    <li><a href="#complex">Complex #s</a></li>
    <li><a href="#circles">Circles</a></li>
    <li><a href="/">🥪 Home</a></li>
  </ul>
</nav>'''

# Replace old nav block
old_nav_match = re.search(r'<nav>.*?</nav>', head_with_css, re.DOTALL)
if old_nav_match:
    head_with_css = head_with_css[:old_nav_match.start()] + new_nav + head_with_css[old_nav_match.end():]

# Update hero description
head_with_css = head_with_css.replace(
    'Simplified notes covering Circles, Linear-Quadratic Systems, Complex Numbers, and Imaginary Numbers.',
    'Simplified notes covering Polynomials, Quadratics, Graphing, Complex Numbers, Circles, and more — organized by topic.'
)

toc_html = build_toc(groups)
main_html = build_main(groups, original)

output = head_with_css + toc_html + main_html + after_main_close

with open('math.html', 'w') as f:
    f.write(output)

print(f"Done! Output: {len(output.splitlines())} lines, {len(output):,} bytes")
