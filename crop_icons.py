"""ภาพเวกเตอร์ (SVG) ของพืชทั้ง 22 ชนิด วาดเองแบบ flat ใช้ viewBox 64x64"""

_LEAF = "#5E9E4B"
_LEAF_D = "#3F7A35"
_STEM = "#7A5A3A"


def _svg(body: str) -> str:
    return f'<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">{body}</svg>'


def _leaf(x, y, rot, s=1.0, c=_LEAF):
    return (f'<ellipse cx="{x}" cy="{y}" rx="{7*s}" ry="{3.4*s}" fill="{c}" '
            f'transform="rotate({rot} {x} {y})"/>')


def _pod(fill, seed, n, seed_r=3.6):
    """ฝักถั่วเฉียง + เมล็ด n เม็ด"""
    seeds = "".join(
        f'<circle cx="{17 + i * (30 / max(n - 1, 1)):.1f}" cy="{43 - i * (22 / max(n - 1, 1)):.1f}" r="{seed_r}" fill="{seed}"/>'
        for i in range(n))
    return (f'<path d="M10 50 C8 40 30 14 50 10 C56 9 56 14 53 18 C44 32 26 50 14 53 C11 54 10 52 10 50Z" fill="{fill}"/>'
            f'{seeds}<path d="M50 10 C54 6 57 5 58 4" stroke="{_LEAF_D}" stroke-width="2.5" stroke-linecap="round" fill="none"/>')


def _beans(color, shine="#ffffff55", shape="oval", n=5, mark=None):
    pos = [(22, 40), (38, 42), (30, 28), (46, 28), (16, 26)][:n]
    out = ""
    for i, (x, y) in enumerate(pos):
        rot = [-20, 25, 10, -35, 40][i]
        if shape == "disc":
            out += f'<ellipse cx="{x}" cy="{y}" rx="9" ry="7.5" fill="{color}" transform="rotate({rot} {x} {y})"/>'
            out += f'<ellipse cx="{x}" cy="{y}" rx="6" ry="4.5" fill="none" stroke="{shine}" stroke-width="1.5" transform="rotate({rot} {x} {y})"/>'
        else:
            out += f'<ellipse cx="{x}" cy="{y}" rx="8" ry="5.5" fill="{color}" transform="rotate({rot} {x} {y})"/>'
            out += f'<ellipse cx="{x-2}" cy="{y-2}" rx="3" ry="1.5" fill="{shine}" transform="rotate({rot} {x} {y})"/>'
            if mark:
                out += f'<ellipse cx="{x}" cy="{y}" rx="2.6" ry="1.1" fill="{mark}" transform="rotate({rot} {x} {y})"/>'
    return out


CROP_SVG = {
    "rice": _svg(
        '<path d="M32 60 C32 44 30 28 22 12" stroke="#B8962E" stroke-width="2.5" fill="none" stroke-linecap="round"/>'
        '<path d="M32 60 C34 46 40 32 48 20" stroke="#B8962E" stroke-width="2.5" fill="none" stroke-linecap="round"/>'
        + "".join(f'<ellipse cx="{x}" cy="{y}" rx="3" ry="5.2" fill="#E9C46A" transform="rotate({r} {x} {y})"/>'
                  for x, y, r in [(22, 12, -25), (19, 20, -50), (28, 18, 10), (24, 28, -50), (31, 27, 15),
                                  (48, 20, 30), (50, 29, 60), (42, 26, 5), (45, 36, 60), (38, 35, 15)])
        + _leaf(22, 50, -40, 1.4) + _leaf(42, 52, 35, 1.4)),
    "maize": _svg(
        '<path d="M32 8 C42 10 46 24 44 38 C42 50 36 56 32 56 C28 56 22 50 20 38 C18 24 22 10 32 8Z" fill="#F4C430"/>'
        + "".join(f'<circle cx="{x}" cy="{y}" r="2.2" fill="#E0A800"/>'
                  for y in range(16, 52, 7) for x in (26, 32, 38))
        + '<path d="M32 60 C20 56 12 44 14 26 C20 36 26 46 32 52Z" fill="#6BAF4F"/>'
          '<path d="M32 60 C44 56 52 44 50 26 C44 36 38 46 32 52Z" fill="#4E9A3A"/>'),
    "chickpea": _svg(
        _beans("#E3BF7A", shape="oval", n=5).replace('rx="8" ry="5.5"', 'rx="8" ry="7"')
        + "".join(f'<path d="M{x+4} {y-6} l3 -3" stroke="#B8914A" stroke-width="2" stroke-linecap="round"/>'
                  for x, y in [(22, 40), (38, 42), (30, 28), (46, 28), (16, 26)])),
    "kidneybeans": _svg(
        "".join(f'<path d="M{x} {y} c-8 -1 -12 -8 -8 -13 c3 -4 8 -2 11 -1 c4 1 9 -1 11 3 c3 6 -4 12 -14 11Z" '
                f'fill="#9B2335" transform="rotate({r} {x} {y})"/>'
                f'<path d="M{x-3} {y-9} c2 -1 4 -1 6 0" stroke="#ffffff66" stroke-width="2" fill="none" transform="rotate({r} {x} {y})"/>'
                for x, y, r in [(26, 34, -10), (42, 50, 15), (24, 56, 5), (46, 30, -25)])),
    "pigeonpeas": _svg(_pod("#8DBF5A", "#C9A227", 4)),
    "mothbeans": _svg(_pod("#B08A5A", "#7A5230", 5, 3.0)),
    "mungbean": _svg(_beans("#4F9D3A", shine="#ffffff66")),
    "blackgram": _svg(_beans("#2B2B2B", shine="#ffffff44", mark="#EDEDED")),
    "lentil": _svg(_beans("#E07A3F", shine="#F6B48A", shape="disc")),
    "pomegranate": _svg(
        '<circle cx="32" cy="38" r="20" fill="#C0392B"/>'
        '<path d="M24 20 L26 12 L30 17 L32 10 L34 17 L38 12 L40 20Z" fill="#A93226"/>'
        '<ellipse cx="25" cy="32" rx="5" ry="3" fill="#ffffff44" transform="rotate(-30 25 32)"/>'),
    "banana": _svg(
        '<path d="M12 22 C14 44 34 56 54 46 C56 45 56 42 53 42 C38 46 22 38 18 20 C17 16 12 17 12 22Z" fill="#F7D046"/>'
        '<path d="M16 26 C22 42 36 48 50 45 C40 50 22 46 16 26Z" fill="#E5B92E"/>'
        '<path d="M14 18 L13 12 L18 12 L18 18Z" fill="#6B4E2E"/>'
        '<path d="M53 42 L57 44 L55 47Z" fill="#4A3520"/>'),
    "mango": _svg(
        '<path d="M30 14 C46 12 56 26 52 42 C48 56 30 60 20 50 C10 40 14 16 30 14Z" fill="#F4A62A"/>'
        '<path d="M30 14 C40 16 52 26 50 40 C46 30 40 22 30 14Z" fill="#E8862A"/>'
        '<ellipse cx="24" cy="30" rx="5" ry="3" fill="#ffffff55" transform="rotate(-40 24 30)"/>'
        '<path d="M30 14 L32 8" stroke="#6B4E2E" stroke-width="2.5" stroke-linecap="round"/>'
        + _leaf(40, 9, -15, 1.3)),
    "grapes": _svg(
        "".join(f'<circle cx="{x}" cy="{y}" r="6" fill="#6C3483"/><circle cx="{x-2}" cy="{y-2}" r="1.8" fill="#ffffff55"/>'
                for x, y in [(22, 24), (34, 24), (46, 24), (28, 34), (40, 34), (34, 44), (34, 54)])
        + '<path d="M34 18 L34 8" stroke="#6B4E2E" stroke-width="2.5" stroke-linecap="round"/>'
        + _leaf(44, 10, -20, 1.4)),
    "watermelon": _svg(
        '<path d="M6 26 A26 26 0 0 0 58 26Z" fill="#3E8E41"/>'
        '<path d="M10 26 A22 22 0 0 0 54 26Z" fill="#E8F5D0"/>'
        '<path d="M13 26 A19 19 0 0 0 51 26Z" fill="#E74C3C"/>'
        + "".join(f'<ellipse cx="{x}" cy="{y}" rx="1.4" ry="2.4" fill="#2B2B2B"/>'
                  for x, y in [(22, 32), (32, 36), (42, 32), (27, 40), (37, 40), (32, 30)])),
    "muskmelon": _svg(
        '<circle cx="32" cy="34" r="22" fill="#D8C27A"/>'
        '<path d="M16 22 L48 46 M14 34 L40 56 M24 14 L54 36 M48 22 L16 46 M50 34 L24 56 M40 14 L10 36" '
        'stroke="#B39A50" stroke-width="1.6"/>'
        '<path d="M32 12 L32 6" stroke="#6B4E2E" stroke-width="2.5" stroke-linecap="round"/>'),
    "apple": _svg(
        '<path d="M32 20 C24 14 10 16 10 32 C10 48 22 58 28 58 C30 58 31 57 32 57 C33 57 34 58 36 58 C42 58 54 48 54 32 C54 16 40 14 32 20Z" fill="#D63031"/>'
        '<ellipse cx="20" cy="30" rx="4" ry="6" fill="#ffffff44" transform="rotate(20 20 30)"/>'
        '<path d="M32 20 C32 14 34 10 36 8" stroke="#6B4E2E" stroke-width="2.5" fill="none" stroke-linecap="round"/>'
        + _leaf(42, 12, -25, 1.2)),
    "orange": _svg(
        '<circle cx="32" cy="36" r="21" fill="#F39C12"/>'
        + "".join(f'<circle cx="{x}" cy="{y}" r="0.9" fill="#D68910"/>'
                  for x, y in [(24, 30), (36, 28), (42, 40), (28, 46), (20, 40), (38, 50), (46, 32)])
        + '<ellipse cx="24" cy="28" rx="5" ry="3" fill="#ffffff55" transform="rotate(-30 24 28)"/>'
        + '<circle cx="32" cy="15" r="2" fill="#6B4E2E"/>' + _leaf(40, 12, -20, 1.2)),
    "papaya": _svg(
        '<path d="M32 6 C46 8 54 26 50 44 C47 56 40 60 32 60 C24 60 17 56 14 44 C10 26 18 8 32 6Z" fill="#7DB544"/>'
        '<path d="M32 10 C43 12 49 27 46 43 C44 53 38 56 32 56 C26 56 20 53 18 43 C15 27 21 12 32 10Z" fill="#F08A4B"/>'
        '<ellipse cx="32" cy="38" rx="7" ry="13" fill="#F6B48A"/>'
        + "".join(f'<circle cx="{x}" cy="{y}" r="1.8" fill="#2B2B2B"/>'
                  for x, y in [(30, 30), (34, 33), (30, 37), (34, 41), (30, 45), (33, 48), (31, 26)])),
    "coconut": _svg(
        '<circle cx="32" cy="34" r="22" fill="#7B4A2A"/>'
        '<circle cx="32" cy="34" r="16" fill="#FDF8EE"/>'
        '<path d="M10 34 L54 34 A22 22 0 0 1 10 34Z" fill="#7B4A2A"/>'
        '<path d="M16 34 L48 34 A16 16 0 0 1 16 34Z" fill="#F2EAD8"/>'
        '<path d="M10 34 L54 34" stroke="#5A3520" stroke-width="2"/>'
        '<circle cx="28" cy="20" r="1.6" fill="#5A3520"/><circle cx="36" cy="20" r="1.6" fill="#5A3520"/>'),
    "cotton": _svg(
        '<path d="M32 60 L32 42" stroke="#6B4E2E" stroke-width="3" stroke-linecap="round"/>'
        '<path d="M18 40 C22 50 42 50 46 40 L40 44 L32 40 L24 44Z" fill="#8B5E3C"/>'
        + "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#FFFFFF" stroke="#DADADA" stroke-width="1.2"/>'
                  for x, y, r in [(22, 30, 10), (42, 30, 10), (32, 22, 11), (32, 36, 10)])),
    "jute": _svg(
        '<path d="M26 60 L26 6 M38 60 L38 10" stroke="#5E8F3A" stroke-width="3" stroke-linecap="round"/>'
        + _leaf(19, 16, 30, 1.2) + _leaf(33, 22, -30, 1.2) + _leaf(19, 32, 30, 1.2)
        + _leaf(45, 18, -30, 1.2, _LEAF_D) + _leaf(31, 38, -30, 1.2, _LEAF_D) + _leaf(45, 34, -30, 1.2, _LEAF_D)
        + _leaf(19, 48, 30, 1.2) + _leaf(45, 50, -30, 1.2, _LEAF_D)),
    "coffee": _svg(
        "".join(f'<ellipse cx="{x}" cy="{y}" rx="10" ry="13" fill="#6F4E37" transform="rotate({r} {x} {y})"/>'
                f'<path d="M{x} {y-11} C{x-4} {y-4} {x+4} {y+4} {x} {y+11}" stroke="#3E2A1E" stroke-width="2" fill="none" transform="rotate({r} {x} {y})"/>'
                for x, y, r in [(24, 38, -25), (42, 30, 20)])
        + '<circle cx="46" cy="52" r="5" fill="#C0392B"/><circle cx="54" cy="47" r="4.5" fill="#C0392B"/>'
        + _leaf(14, 16, 30, 1.2)),
}

CROP_TH = {
    "rice": "ข้าว", "maize": "ข้าวโพด", "chickpea": "ถั่วลูกไก่", "kidneybeans": "ถั่วแดง",
    "pigeonpeas": "ถั่วมะแฮะ", "mothbeans": "ถั่วมอธ", "mungbean": "ถั่วเขียว",
    "blackgram": "ถั่วเขียวผิวดำ", "lentil": "ถั่วเลนทิล", "pomegranate": "ทับทิม",
    "banana": "กล้วย", "mango": "มะม่วง", "grapes": "องุ่น", "watermelon": "แตงโม",
    "muskmelon": "เมลอน", "apple": "แอปเปิล", "orange": "ส้ม", "papaya": "มะละกอ",
    "coconut": "มะพร้าว", "cotton": "ฝ้าย", "jute": "ปอ", "coffee": "กาแฟ",
}
