# Gry w kodach QR

Gry HTML, z których każda mieści się w całości w jednym kodzie QR. Skanujesz telefonem, stukasz w link i grasz.

**Strona z grami:** https://husk007.github.io/qr/

| Gra | Opis | Link |
|---|---|---|
| [Ptak](gry/ptak) | Zręcznościówka w stylu „flappy” | 2266 znaków, QR v35 |
| [Kurier ORLEN Paczka](gry/kurier) | Bus kurierski, paczki, automaty APM i paliwo | 2848 znaków, QR v40 |
| [Memory APM](gry/memory-apm) | Gra w pary w automacie paczkowym | 2570 znaków, QR v38 |
| [Hop!](gry/hop) | Platformówka z jedną pełną planszą | 2949 znaków, QR v40 |
| [QR Linux](gry/qr-linux) | Udawany terminal Linuksa z poleceniami i mini-grą | 2937 znaków, QR v40 |
| [CHIP-8: Łapacz paczek](gry/chip8) | Emulator CHIP-8 i gra w kodzie maszynowym (213 B) | 2784 znaki, QR v39 |

Każdy folder w `gry/` zawiera kod gry (`gra.html`), kod QR (`qr.png`), link (`link.txt`) i opis (`README.md`).

## Jak to działa

Największy kod QR (wersja 40, korekcja L) mieści 2953 bajty. Gra ma 3–4 KB kodu, więc:

1. HTML jest kompresowany algorytmem deflate (ten sam co w ZIP),
2. kodowany w Base64 (wariant URL: `-` i `_` zamiast `+` i `/`),
3. doklejany do linku po znaku `#`: `https://husk007.github.io/qr/#<dane>`.

`index.html` to jednocześnie ładowarka i strona z grami. Gdy link ma dane po `#`, strona rozpakowuje je wbudowanym w przeglądarkę `DecompressionStream('deflate-raw')` i podmienia się na grę przez `document.write`. Bez danych pokazuje listę gier.

Część linku po `#` nie jest wysyłana na serwer, więc gra żyje wyłącznie w kodzie QR. Jedna ładowarka obsługuje dowolną liczbę gier.

## Narzędzia

- `narzedzia/zrob_qr.py` — zamienia plik HTML w link i kod QR
- `narzedzia/chip8_asm.py` — asembler CHIP-8

## Własna gra

```bash
pip install qrcode pillow zopfli
python3 narzedzia/zrob_qr.py moja_gra.html moja_gra_qr.png
```

Skrypt usuwa znaki nowej linii, więc każda linia kodu JS musi kończyć się średnikiem albo klamrą. Wypisze długość linku i odmówi, jeśli przekroczy limit.

## Bezpieczeństwo

Ładowarka uruchomi każdy kod HTML dopisany do linku, w domenie `husk007.github.io`. Dla gier jest to nieszkodliwe, ale w tej domenie nie warto trzymać niczego wrażliwego.
