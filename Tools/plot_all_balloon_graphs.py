import os

import matplotlib.pyplot as plt
import numpy as np


OUT_DIR = r"C:\Users\leona\Documents\PL Mathe\Grafiken"
os.makedirs(OUT_DIR, exist_ok=True)

# Final model with realistic landing speed:
# v(t) = k * t * (t - 3.4) * (t - s), 0 <= t <= 7
# s follows from integral_0^7 v(t) dt = 0.
# k is chosen so that the local maximum is 25 km/h.
r = 3.4
s = ((343 * r / 3) - (2401 / 4)) / ((49 * r / 2) - (343 / 3))


def v(t):
    return k * t * (t - r) * (t - s)


def V(t):
    return k * (t**4 / 4 - (r + s) * t**3 / 3 + r * s * t**2 / 2)


def a(t):
    # First derivative of v(t)
    return k * (3 * t**2 - 2 * (r + s) * t + r * s)


def j(t):
    # Second derivative of v(t)
    return k * (6 * t - 2 * (r + s))


def extrema_of_v():
    coeff = [3, -2 * (r + s), r * s]
    roots = np.roots(coeff)
    return sorted(float(x.real) for x in roots if abs(x.imag) < 1e-9 and 0 <= x.real <= 7)


def local_max_scale(target_max=25):
    t_max = extrema_of_v()[0]
    raw = t_max * (t_max - r) * (t_max - s)
    return target_max / raw


def style_axes(ax, xlim=(0, 7), ylim=None):
    ax.set_xlim(*xlim)
    if ylim is not None:
        ax.set_ylim(*ylim)
    ax.axhline(0, color="#222222", linewidth=1.1, zorder=4)
    ax.axvline(0, color="#222222", linewidth=1.1, zorder=4)
    ax.set_axisbelow(False)
    ax.grid(True, which="major", color="#c9c9c9", linewidth=0.8, alpha=0.95, zorder=2)
    ax.grid(True, which="minor", color="#e5e5e5", linewidth=0.55, alpha=0.9, zorder=2)
    ax.minorticks_on()
    for spine in ["top", "right"]:
        ax.spines[spine].set_visible(False)
    ax.spines["left"].set_color("#333333")
    ax.spines["bottom"].set_color("#333333")


def save(fig, name):
    path = os.path.join(OUT_DIR, name)
    fig.savefig(path, dpi=220, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(path)


t = np.linspace(0, 7, 1000)
special_t = extrema_of_v()
k = local_max_scale(25)
end_distance = V(7)
formula_text = f"v(t) = {k:.3f} · t · (t - {r:.1f}) · (t - {s:.5f})"

plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "font.size": 11,
        "axes.titlesize": 15,
        "axes.labelsize": 12,
        "figure.facecolor": "white",
        "axes.facecolor": "white",
    }
)


# 1. Velocity with integral areas.
fig, ax = plt.subplots(figsize=(11, 6.3))
ax.plot(t, v(t), color="#005f73", linewidth=2.6, zorder=5)
ax.fill_between(t, 0, v(t), where=v(t) >= 0, interpolate=True, color="#2ca25f", alpha=0.42, zorder=1)
ax.fill_between(t, 0, v(t), where=v(t) <= 0, interpolate=True, color="#de2d26", alpha=0.38, zorder=1)
ax.scatter([0, r, s, 7], [0, 0, 0, v(7)], color="#111111", s=38, zorder=6)
for x, y, label, dx, dy in [
    (0, 0, "Start", 0.08, 0.9),
    (r, 0, "1. Richtungswechsel", 0.08, 0.9),
    (s, 0, "2. Richtungswechsel", -1.18, 0.9),
    (7, v(7), "Ende", -0.45, 1.1),
]:
    ax.text(x + dx, y + dy, label)
for x in special_t:
    label = "Hochpunkt" if v(x) > 0 else "Tiefpunkt"
    ax.scatter([x], [v(x)], color="#111111", s=38, zorder=6)
    ax.text(x + 0.08, v(x) + (0.9 if v(x) > 0 else -1.3), label)
style_axes(ax, ylim=(-30, 30))
ax.set_title("Horizontalgeschwindigkeit der Ballonfahrt")
ax.set_xlabel("Zeit t in Stunden")
ax.set_ylabel("Geschwindigkeit v(t) in km/h")
ax.text(
    0.02,
    -0.18,
    f"{formula_text}    |    Endabstand: 0 km    |    v(7) = {v(7):.1f} km/h",
    transform=ax.transAxes,
)
save(fig, "01_geschwindigkeit_mit_flaechen.png")


# 1b. Clean velocity plot without filled areas.
fig, ax = plt.subplots(figsize=(11, 6.3))
ax.plot(t, v(t), color="#005f73", linewidth=2.6, zorder=5)
ax.scatter([0, r, s, 7], [0, 0, 0, v(7)], color="#111111", s=38, zorder=6)
for x, y, label, dx, dy in [
    (0, 0, "Start", 0.08, 0.6),
    (r, 0, "1. Richtungswechsel", 0.08, 0.6),
    (s, 0, "2. Richtungswechsel", -1.18, 0.6),
    (7, v(7), "Ende", -0.45, 0.7),
]:
    ax.text(x + dx, y + dy, label)
for x in special_t:
    label = "lokaler Hochpunkt" if v(x) > 0 else "lokaler Tiefpunkt"
    ax.scatter([x], [v(x)], color="#111111", s=38, zorder=6)
    ax.text(x + 0.08, v(x) + (0.7 if v(x) > 0 else -1.0), label)
style_axes(ax, ylim=(-30, 30))
ax.set_title("Geschwindigkeitsfunktion ohne Flaechenmarkierung")
ax.set_xlabel("Zeit t in Stunden")
ax.set_ylabel("Geschwindigkeit v(t) in km/h")
ax.text(
    0.02,
    -0.18,
    formula_text,
    transform=ax.transAxes,
)
save(fig, "01b_geschwindigkeit_ohne_flaechen.png")


# 2. Antiderivative / horizontal position.
fig, ax = plt.subplots(figsize=(11, 6.3))
ax.plot(t, V(t), color="#7b3294", linewidth=2.6, zorder=5)
ax.scatter([0, 7], [V(0), V(7)], color="#111111", s=38, zorder=6)
ax.text(0.08, V(0) + 0.8, "Startpunkt")
ax.text(6.28, V(7) + 0.8, "Landepunkt")
style_axes(ax, ylim=(-5, 60))
ax.set_title("Stammfunktion: horizontaler Abstand vom Startpunkt")
ax.set_xlabel("Zeit t in Stunden")
ax.set_ylabel("Abstand S(t) in km")
ax.text(
    0.02,
    -0.18,
    "S(t) = ∫ v(t) dt, mit S(0)=0. Weil S(7)=0 gilt, liegt der Landepunkt horizontal wieder am Startpunkt.",
    transform=ax.transAxes,
)
save(fig, "02_stammfunktion_abstand.png")


# 3. First derivative.
fig, ax = plt.subplots(figsize=(11, 6.3))
ax.plot(t, a(t), color="#d95f02", linewidth=2.6, zorder=5)
for x in special_t:
    ax.scatter([x], [0], color="#111111", s=38, zorder=6)
    ax.text(x + 0.08, 0.55, f"t = {x:.2f}")
style_axes(ax, ylim=(-8, 42))
ax.set_title("Erste Ableitung der Geschwindigkeit")
ax.set_xlabel("Zeit t in Stunden")
ax.set_ylabel("v'(t)")
ax.text(
    0.02,
    -0.18,
    "Die Nullstellen von v'(t) liefern Hochpunkt und Tiefpunkt des Geschwindigkeitsgraphen.",
    transform=ax.transAxes,
)
save(fig, "03_erste_ableitung.png")


# 4. Second derivative.
fig, ax = plt.subplots(figsize=(11, 6.3))
ax.plot(t, j(t), color="#1b9e77", linewidth=2.6, zorder=5)
zero_second = (r + s) / 3
ax.scatter([zero_second], [0], color="#111111", s=38, zorder=6)
ax.text(zero_second + 0.08, 0.45, f"Wendestelle von v: t = {zero_second:.2f}")
style_axes(ax, ylim=(-18, 20))
ax.set_title("Zweite Ableitung der Geschwindigkeit")
ax.set_xlabel("Zeit t in Stunden")
ax.set_ylabel("v''(t)")
ax.text(
    0.02,
    -0.18,
    "Die zweite Ableitung ist linear. Ihre Nullstelle zeigt, wo der Geschwindigkeitsgraph seine Kruemmung wechselt.",
    transform=ax.transAxes,
)
save(fig, "04_zweite_ableitung.png")


# 5. Overview sheet.
fig, axs = plt.subplots(2, 2, figsize=(13, 8.5))
plots = [
    (axs[0, 0], v(t), "v(t): Geschwindigkeit", "km/h", "#005f73"),
    (axs[0, 1], V(t), "S(t): Abstand", "km", "#7b3294"),
    (axs[1, 0], a(t), "v'(t): erste Ableitung", "", "#d95f02"),
    (axs[1, 1], j(t), "v''(t): zweite Ableitung", "", "#1b9e77"),
]
for ax, y, title, ylabel, color in plots:
    ax.plot(t, y, color=color, linewidth=2.2, zorder=5)
    ax.set_title(title)
    ax.set_xlabel("t in h")
    ax.set_ylabel(ylabel)
    pad = max(1, (float(np.max(y)) - float(np.min(y))) * 0.12)
    style_axes(ax, ylim=(float(np.min(y)) - pad, float(np.max(y)) + pad))
fig.suptitle("Ballonfahrt: Funktion, Stammfunktion und Ableitungen", fontsize=17)
fig.tight_layout()
save(fig, "00_uebersicht_alle_graphen.png")


# 6. Decision comparison: smooth numbers vs. realistic landing speed.
def model_from_first_root(first_root, target_max=25):
    second_root = ((343 * first_root / 3) - (2401 / 4)) / ((49 * first_root / 2) - (343 / 3))
    coeff = [3, -2 * (first_root + second_root), first_root * second_root]
    roots = sorted(float(x.real) for x in np.roots(coeff) if abs(x.imag) < 1e-9 and 0 <= x.real <= 7)
    raw = lambda x: x * (x - first_root) * (x - second_root)
    scale = target_max / raw(roots[0])
    return second_root, scale, lambda x: scale * raw(x)


smooth_s, smooth_k, smooth_v = model_from_first_root(3.0)
final_s, final_k, final_v = model_from_first_root(3.4)
fig, ax = plt.subplots(figsize=(11, 6.3))
ax.plot(t, smooth_v(t), color="#8c8c8c", linewidth=2.2, linestyle="--", label=f"verworfene glatte Variante: r=3, s={smooth_s:.1f}")
ax.plot(t, final_v(t), color="#005f73", linewidth=2.8, label=f"finale Variante: r=3,4, s={final_s:.5f}")
ax.scatter([7, 7], [smooth_v(7), final_v(7)], color=["#8c8c8c", "#005f73"], s=45, zorder=6)
ax.text(6.15, smooth_v(7) + 1.0, f"v(7)={smooth_v(7):.1f} km/h", color="#555555")
ax.text(5.9, final_v(7) + 1.0, f"v(7)={final_v(7):.1f} km/h", color="#005f73")
style_axes(ax, ylim=(-35, 48))
ax.set_title("Modellentscheidung: glatte Zahlen oder realistische Landegeschwindigkeit")
ax.set_xlabel("Zeit t in Stunden")
ax.set_ylabel("Geschwindigkeit v(t) in km/h")
ax.legend(loc="lower left", frameon=False)
ax.text(
    0.02,
    -0.18,
    "Beide Modelle landen horizontal wieder am Startpunkt. Die finale Variante hat aber eine deutlich langsamere Landegeschwindigkeit.",
    transform=ax.transAxes,
)
save(fig, "10_modellentscheidung_vergleich.png")
