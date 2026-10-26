"""Trend markera laboratoryjnego: tabela w terminalu + wykres PNG.

Użycie:
  python scripts/trend.py ferrytyna
  python scripts/trend.py LDL HDL trójglicerydy      # kilka markerów, osobne wykresy
  python scripts/trend.py --list                     # jakie markery są w bazie

Wykres trafia do reports/img/trend_<marker>.png.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
RESULTS = ROOT / "data" / "labs" / "results.csv"
IMG_DIR = ROOT / "reports" / "img"


def load() -> pd.DataFrame:
    df = pd.read_csv(RESULTS, dtype=str, keep_default_na=False)
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    for col in ("value", "ref_low", "ref_high"):
        df[col + "_num"] = pd.to_numeric(df[col], errors="coerce")
    return df.sort_values("date")


def plot(sub: pd.DataFrame, marker: str) -> Path | None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    numeric = sub.dropna(subset=["value_num"])
    if numeric.empty:
        return None
    IMG_DIR.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(numeric["date"], numeric["value_num"], marker="o", linewidth=2)
    for _, r in numeric.iterrows():
        ax.annotate(f"{r['value_num']:g}", (r["date"], r["value_num"]),
                    textcoords="offset points", xytext=(0, 8), ha="center", fontsize=8)
    lo, hi = numeric["ref_low_num"].dropna(), numeric["ref_high_num"].dropna()
    if not lo.empty and not hi.empty:
        ax.axhspan(lo.iloc[-1], hi.iloc[-1], alpha=0.12, color="green", label="norma lab (ostatnia)")
    elif not hi.empty:
        ax.axhline(hi.iloc[-1], color="red", linestyle="--", alpha=0.6, label=f"górna granica normy {hi.iloc[-1]:g}")
    elif not lo.empty:
        ax.axhline(lo.iloc[-1], color="red", linestyle="--", alpha=0.6, label=f"dolna granica normy {lo.iloc[-1]:g}")
    if not lo.empty or not hi.empty:
        ax.legend(loc="best")
    # skala osi Y wg danych, nie wg (często bardzo szerokiej) normy – pasmo normy widać tylko w pobliżu wyników
    ymin, ymax = numeric["value_num"].min(), numeric["value_num"].max()
    pad = max((ymax - ymin) * 0.35, abs(ymax) * 0.1, 1e-9)
    ax.set_ylim(ymin - pad, ymax + pad)
    unit = numeric["unit"].iloc[-1]
    ax.set_title(f"{marker} ({unit})" if unit else marker)
    ax.grid(alpha=0.3)
    fig.autofmt_xdate()
    fig.tight_layout()
    safe = "".join(c if c.isalnum() else "_" for c in marker)
    out = IMG_DIR / f"trend_{safe}.png"
    fig.savefig(out, dpi=120)
    plt.close(fig)
    return out


def show(df: pd.DataFrame, marker: str) -> None:
    sub = df[df["test"].str.lower() == marker.lower()]
    if sub.empty:
        print(f"[{marker}] brak wyników w bazie. Dostępne: {', '.join(sorted(df['test'].unique()))}")
        return
    print(f"\n=== {marker} ===")
    cols = ["date", "value", "unit", "ref_low", "ref_high", "flag", "lab", "notes"]
    view = sub[cols].copy()
    view["date"] = view["date"].dt.strftime("%Y-%m-%d")
    print(view.to_string(index=False))
    numeric = sub.dropna(subset=["value_num"])
    if len(numeric) >= 2:
        first, last = numeric.iloc[0], numeric.iloc[-1]
        delta = last["value_num"] - first["value_num"]
        pct = delta / first["value_num"] * 100 if first["value_num"] else float("nan")
        days = (last["date"] - first["date"]).days
        print(f"\nZmiana {first['date']:%Y-%m-%d} → {last['date']:%Y-%m-%d} ({days} dni): "
              f"{first['value_num']:g} → {last['value_num']:g}  ({delta:+g}, {pct:+.1f}%)")
        print(f"Min {numeric['value_num'].min():g}, max {numeric['value_num'].max():g}, "
              f"średnia {numeric['value_num'].mean():.2f}, n={len(numeric)}")
    out = plot(sub, marker)
    if out:
        print(f"Wykres: {out.relative_to(ROOT)}")


def main(argv: list[str]) -> int:
    if not argv or argv == ["-h"] or argv == ["--help"]:
        print(__doc__)
        return 0
    df = load()
    if argv == ["--list"]:
        counts = df.groupby("test").size().sort_values(ascending=False)
        print(counts.to_string())
        return 0
    for marker in argv:
        show(df, marker)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
