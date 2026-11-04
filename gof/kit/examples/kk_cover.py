# Example cover. Run from gof/work: python3 ../kit/examples/kk_cover.py  -> work/cover-GoF-Krankenkasse.jpg
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from gof_covers import *
os.makedirs(OUTDIR, exist_ok=True)
cover("Krankenkasse", "§ 175 SGB V", "Krankenkasse 2027:", "bis 210 € sparen", SAVE, doc(780, "BEITRAGSERHÖHUNG", "Zusatzbeitrag ↑ ?,?? %", RED_, stamp="KÜNDIGEN"), "Sonderkündigungsrecht nutzen!", glow=(70, 170, 120))
