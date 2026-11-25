; Łapacz paczek — gra na CHIP-8
; Klawisze: 4 = w lewo, 6 = w prawo
; Rejestry: V0-V2 BCD, V3 punkty, V4 życia, V5/V7/VE robocze, V6 y kosza (28)
;           V8 x kosza, V9 x paczki, VA y paczki, VB opóźnienie spadania,
;           VC licznik do przyspieszenia, VD licznik klatek

start:  CLS
        LD V3, 0
        LD V4, 3
        LD V8, 28
        LD V6, 28
        LD VB, 4
        LD VC, 0
        LD VD, 1
        CALL hud
        CALL newobj
        LD I, kosz
        DRW V8, V6, 2

loop:   LD V5, DT          ; czekaj na kolejną klatkę (60 Hz)
        SE V5, 0
        JP loop
        LD V5, 1
        LD DT, V5
        LD V5, 4
        SKNP V5
        CALL left
        LD V5, 6
        SKNP V5
        CALL right
        ADD VD, 0xFF       ; paczka spada co VB klatek
        SE VD, 0
        JP loop
        LD VD, VB
        LD I, paczka
        DRW V9, VA, 4
        ADD VA, 1
        DRW V9, VA, 4
        SE VA, 24          ; paczka tuż nad koszem?
        JP loop
        DRW V9, VA, 4      ; zmaż paczkę
        LD V5, V9          ; złapana, gdy 0 <= V9+3-V8 <= 10
        ADD V5, 3
        SUB V5, V8
        LD V7, 10
        SUB V7, V5
        SE VF, 1
        JP miss
        CALL hud           ; złapana: +1 punkt
        ADD V3, 1
        CALL hud
        LD V5, 3
        LD ST, V5
        ADD VC, 1          ; co 5 punktów szybciej
        SE VC, 5
        JP next
        LD VC, 0
        SE VB, 1
        ADD VB, 0xFF
next:   CALL newobj
        JP loop

miss:   CALL hud           ; nie złapana: -1 życie
        ADD V4, 0xFF
        CALL hud
        LD V5, 20
        LD ST, V5
        SE V4, 0
        JP next
        LD V5, K           ; koniec gry: dowolny klawisz = od nowa
        JP start

left:   SE V8, 0
        JP doleft
        RET
doleft: LD I, kosz
        DRW V8, V6, 2
        ADD V8, 0xFF
        DRW V8, V6, 2
        RET

right:  SE V8, 56
        JP dorite
        RET
dorite: LD I, kosz
        DRW V8, V6, 2
        ADD V8, 1
        DRW V8, V6, 2
        RET

newobj: RND V9, 0x3F       ; losowe x, najwyżej 59
        LD V5, 59
        SUB V5, V9
        SE VF, 1
        LD V9, 59
        LD VA, 7
        LD I, paczka
        DRW V9, VA, 4
        RET

hud:    LD I, bcd          ; punkty w lewym górnym rogu, życia w prawym (rysowanie XOR: 2x = zmaż)
        LD B, V3
        LD V2, [I]
        LD V7, 1
        LD VE, 1
        LD F, V1
        DRW VE, V7, 5
        LD VE, 6
        LD F, V2
        DRW VE, V7, 5
        LD VE, 59
        LD F, V4
        DRW VE, V7, 5
        RET

kosz:   DB 0x81, 0xFF
paczka: DB 0xF0, 0xB0, 0xD0, 0xF0
bcd:    DB 0, 0, 0
