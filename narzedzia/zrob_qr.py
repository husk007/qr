#!/usr/bin/env python3
"""Zamienia plik HTML gry w link do ładowarki i kod QR.

Użycie:
    pip install qrcode pillow          # wymagane
    pip install zopfli                 # opcjonalnie, kompresja lepsza o ok. 1%
    python3 zrob_qr.py gra.html qr.png

Skrypt usuwa znaki nowej linii, więc każda linia kodu JS musi kończyć się
średnikiem albo klamrą. Limit kodu QR (wersja 40, korekcja L) to 2953 znaki.
"""
import base64
import sys
import zlib

import qrcode

LOADER = "https://husk007.github.io/qr/#"
LIMIT = 2953


def deflate(data: bytes) -> bytes:
    try:
        from zopfli import zopfli
        raw = zopfli.compress(data, numiterations=2000)[2:-4]  # zlib -> surowy deflate
    except ImportError:
        c = zlib.compressobj(9, zlib.DEFLATED, -15)
        raw = c.compress(data) + c.flush()
    assert zlib.decompress(raw, -15) == data
    return raw


def main() -> None:
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    src, out = sys.argv[1], sys.argv[2]
    html = open(src, encoding="utf-8").read().replace("\n", "")
    url = LOADER + base64.urlsafe_b64encode(deflate(html.encode())).rstrip(b"=").decode()
    print(f"kod: {len(html.encode())} B, link: {len(url)} / {LIMIT} znaków")
    if len(url) > LIMIT:
        sys.exit(f"Za długo o {len(url) - LIMIT} znaków — skróć grę.")
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=5, border=4)
    qr.add_data(url, optimize=0)
    qr.make(fit=True)
    qr.make_image().save(out)
    print(f"QR w wersji {qr.version} zapisany do {out}")
    print(url)


if __name__ == "__main__":
    main()
