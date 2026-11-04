# Example video spec (Krankenkasse 2027, posted 04.11.2026).
# Run from gof/work:  python3 ../kit/examples/kk.py <total_seconds> <out.mp4> [--frames 2,10,30]
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import gofkit
from gofkit import *
gofkit.SUB = "Krankenkasse 2027"; gofkit.FOOT1 = "Keine Beratung · Stand: November 2026"; gofkit.FOOT2 = "Quellen: BMG 30.10.2026 · § 175 SGB V · § 242 SGB V"
SCRIPT = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "kk.txt")).read()
TOTAL = float(sys.argv[1])
_, S = timings(SCRIPT, TOTAL)   # S[i] = start second of sentence i
def build():
    els = []
    def A(img, x, y, *a, **k): els.append(El(img, x, y, *a, **k))
    s=lambda i,d=0.15: S[i]+d
    e = S[2]
    A(T("Deine Krankenkasse", 100), cx, 440, s(0,0.05), e, anchor="c")
    A(T("kostet dich 2027", 80, MUTED, "ExtraBold"), cx, 580, s(0,1.2), e, anchor="c")
    A(T("mehr?", 200, RENT), cx, 680, s(0,2.4), e, anim="pop", anchor="c")
    A(pill("Die meisten merken es nicht", PANEL2, CHALK, 46), cx, 960, s(1), e, anim="up", anchor="c")
    e = S[5]
    A(pill("Ø Zusatzbeitrag 2027", MUST, NAVY, 48, "Black"), cx, 420, s(2), e, anim="pop", anchor="c")
    A(T("2,9 %", 240, MUST), cx, 540, s(2,2.4), e, anim="pop", anchor="c")
    A(pill("nur ein Durchschnitt!", RENT, NAVY, 50, "Black"), cx, 880, s(3), e, anim="pop", anchor="c")
    A(rowcard("Jede Kasse legt ihren Beitrag selbst fest", LIFE, num="!", size=42), cx, 1060, s(4), e, anim="right", anchor="c")
    e = S[7]
    A(T("Die Spanne", 100), cx, 420, s(5), e, anchor="c")
    A(tile("günstig", "2,2 %", SAVE), 75, 620, s(6,0.6), e, anim="left")
    A(tile("teuer", "4,4 %", RENT), W - 75 - 420, 620, s(6,2.0), e, anim="right")
    A(pill("Stand 2026 · bundesweite Kassen", PANEL2, MUTED, 38), cx, 1000, s(6,2.4), e, anim="up", anchor="c")
    e = S[13]
    A(pill("Rechnen wir mal", MUST, NAVY, 50, "Black"), cx, 400, s(7), e, anim="pop", anchor="c")
    A(T("3.500 € brutto", 110), cx, 520, s(8), e, anim="pop", anchor="c")
    A(rowcard("1 Prozentpunkt = 35 € im Monat", LIFE, num=1, size=46), cx, 720, s(9), e, anim="right", anchor="c")
    A(rowcard("Hälfte zahlt dein Arbeitgeber", SAVE, num=2, size=46), cx, 900, s(10), e, anim="right", anchor="c")
    A(T("17,50 € / Monat", 90, MUST), cx, 1080, s(11), e, anim="pop", anchor="c")
    A(T("= 210 € im Jahr", 120, SAVE), cx, 1220, s(12), e, anim="pop", anchor="c")
    e = S[16]
    A(T("Das Wichtigste", 90, MUST), cx, 420, s(13), e, anim="pop", anchor="c")
    A(pill("Kasse erhöht den Beitrag?", PANEL2, CHALK, 48), cx, 580, s(14), e, anim="up", anchor="c")
    A(fit("Sonderkündigungsrecht", 92, 960, SAVE), cx, 720, s(14,1.6), e, anim="pop", anchor="c")
    A(pill("§ 175 SGB V", MUST, NAVY, 46, "Black"), cx, 860, s(14,2.2), e, anim="pop", anchor="c")
    A(rowcard("Erhöhung ab 1. Januar → Frist bis 31. Januar", LIFE, num="!", size=38), cx, 1060, s(15), e, anim="right", anchor="c")
    e = S[18]
    A(T("Du musst nicht", 90), cx, 460, s(16), e, anchor="c")
    A(T("selbst kündigen", 110, SAVE), cx, 580, s(16,0.9), e, anim="pop", anchor="c")
    A(rowcard("Die neue Kasse erledigt alles", SAVE, num="✓" if False else 1, size=46), cx, 840, s(17), e, anim="right", anchor="c")
    e = S[21]
    A(pill("Achtung", RENT, NAVY, 56, "Black"), cx, 420, s(18,0.05), e, anim="pop", anchor="c")
    A(T("Grundsicherung", 110), cx, 560, s(19,0.5), e, anim="pop", anchor="c")
    A(T("vom Jobcenter?", 80, MUTED, "ExtraBold"), cx, 700, s(19,1.6), e, anchor="c")
    A(rowcard("Wechsel spart dir nichts", RENT, num="!", size=48), cx, 900, s(19,3.0), e, anim="right", anchor="c")
    A(rowcard("Jobcenter zahlt den Ø-Beitrag", LIFE, num="i", size=46), cx, 1080, s(20), e, anim="right", anchor="c")
    A(pill("Im Dezember", MUST, NAVY, 52, "Black"), cx, 420, s(21), anim="pop", anchor="c")
    A(T("Post checken!", 120), cx, 560, s(22), anim="pop", anchor="c")
    A(pill("Folge für mehr Geld ohne Filter", SAVE, NAVY, 46, "Black"), cx, 820, s(23), anim="pop", anchor="c")
    return els


if __name__ == "__main__":
    tt = [float(x) for x in sys.argv[sys.argv.index("--frames") + 1].split(",")] if "--frames" in sys.argv else None
    render(build, TOTAL, sys.argv[2], tt)
