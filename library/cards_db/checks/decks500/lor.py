"""Legends of Runeterra deck codes: decode to [(card code, count)] (Riot's published format: base32, varints, groups by count)."""
import base64
FAC = {0: 'DE', 1: 'FR', 2: 'IO', 3: 'NX', 4: 'PZ', 5: 'SI', 6: 'BW', 7: 'SH', 9: 'MT', 10: 'BC', 12: 'RU'}


def _varints(b):
    i = 0
    while i < len(b):
        v = s = 0
        while True:
            x = b[i]; i += 1
            v |= (x & 0x7F) << s; s += 7
            if not x & 0x80: break
        yield v


def decode(code):
    code = code.strip().upper()
    raw = base64.b32decode(code + '=' * (-len(code) % 8))
    it = _varints(raw[1:])
    out = []
    for count in (3, 2, 1):
        for _ in range(next(it)):
            n, st, fa = next(it), next(it), next(it)
            for _ in range(n): out.append((f'{st:02d}{FAC[fa]}{next(it):03d}', count))
    rest = list(it)
    for i in range(0, len(rest) - 3, 4):
        k, st, fa, num = rest[i:i + 4]
        out.append((f'{st:02d}{FAC[fa]}{num:03d}', k))
    return out
