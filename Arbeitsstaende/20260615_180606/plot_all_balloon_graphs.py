import os

import matplotlib.pyplot as plt
import numpy as np


OUT_DIR = r"C:\Users\leona\Documents\PL Mathe\Grafiken"
os.makedirs(OUT_DIR, exist_ok=True)

# Final model with simple, presentation-friendly numbers:
# v(t) = 0.5 * t * (t - 3) * (t - 6.3), 0 <= t <= 7
k = 0.5
r = 3.0
s = 6.3


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


def style_axes(ax, xlim=(0, 7), ylim=None):
    ax.set_xlim(*xlim)
    if ylim is not None:
        ax.set_ylim(*ylim)
    ax.axhline(0, color="#222222", linewidth=1.1)
    ax.axvline(0, color="#222222", linewidth=1.1)
    ax.set_axisbelow(False)
    ax.grid(True, which="major", color="#c9c9c9", linewidth=0.8, alpha=0.95, zorder=4)
    ax.grid(True, which="minor", color="#e5e5e5", linewidth=0.55, alpha=0.9, zorder=4)
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
end_distance = V(7)

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
ax.plot(t, v(t), color="#005f73", linewidth=2.6)
ax.fill_between(t, 0, v(t), where=v(t) >= 0, interpolate=True, color="#2ca25f", alpha=0.42, zorder=1)
ax.fill_between(t, 0, v(t), where=v(t) <= 0, interpolate=True, color="#de2d26", alpha=0.38, zorder=1)
ax.scatter([0, r, s, 7], [0, 0, 0, v(7)], color="#111111", s=38, zorder=5)
for x, y, label, dx, dy in [
    (0, 0, "Start", 0.08, 0.9),
    (r, 0, "1. Richtungswechsel", 0.08, 0.9),
    (s, 0, "2. Richtungswechsel", -1.18, 0.9),
    (7, v(7), "Ende", -0.45, 1.1),
]:
    ax.text(x + dx, y + dy, label)
for x in special_t:
    label = "Hochpunkt" if v(x) > 0 else "Tiefpunkt"
    ax.scatter([x], [v(x)], color="#111111", s=38, zorder=5)
    ax.text(x + 0.08, v(x) + (0.9 if v(x) > 0 else -1.3), label)
style_axes(ax, ylim=(-8, 12))
ax.set_title("Horizontalgeschwindigkeit der Ballonfahrt")
ax.set_xlabel("Zeit t in Stunden")
ax.set_ylabel("Geschwindigkeit v(t) in km/h")
ax.text(
    0.02,
    -0.18,
    "v(t) = 0,5 · t · (t - 3) · (t - 6,3)    |    Endabstand: 0 km    |    v(7) = 9,8 km/h",
    transform=ax.transAxes,
)
save(fig, "01_geschwindigkeit_mit_flaechen.png")


# 1b. Clean velocity plot without filled areas.
fig, ax = plt.subplots(figsize=(11, 6.3))
ax.plot(t, v(t), color="#005f73", linewidth=2.6)
ax.scatter([0, r, s, 7], [0, 0, 0, v(7)], color="#111111", s=38, zorder=5)
for x, y, label, dx, dy in [
    (0, 0, "Start", 0.08, 0.6),
    (r, 0, "1. Richtungswechsel", 0.08, 0.6),
    (s, 0, "2. Richtungswechsel", -1.18, 0.6),
    (7, v(7), "Ende", -0.45, 0.7),
]:
    ax.text(x + dx, y + dy, label)
for x in special_t:
    label = "lokaler Hochpunkt" if v(x) > 0 else "lokaler Tiefpunkt"
    ax.scatter([x], [v(x)], color="#111111", s=38, zorder=5)
    ax.text(x + 0.08, v(x) + (0.7 if v(x) > 0 else -1.0), label)
style_axes(ax, ylim=(-8, 12))
ax.set_title("Geschwindigkeitsfunktion ohne Flaechenmarkierung")
ax.set_xlabel("Zeit t in Stunden")
ax.set_ylabel("Geschwindigkeit v(t) in km/h")
ax.text(
    0.02,
    -0.18,
    "v(t) = 0,5 · t · (t - 3) · (t - 6,3)",
    transform=ax.transAxes,
)
save(fig, "01b_geschwindigkeit_ohne_flaechen.png")


# 2. Antiderivative / horizontal position.
fig, ax = plt.subplots(figsize=(11, 6.3))
ax.plot(t, V(t), color="#7b3294", linewidth=2.6)
ax.scatter([0, 7], [V(0), V(7)], color="#111111", s=38, zorder=5)
ax.text(0.08, V(0) + 0.8, "Startpunkt")
ax.text(6.28, V(7) + 0.8, "Landepunkt")
style_axes(ax, ylim=(-4, 13))
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
ax.plot(t, a(t), color="#d95f02", linewidth=2.6)
for x in special_t:
    ax.scatter([x], [0], color="#111111", s=38, zorder=5)
    ax.text(x + 0.08, 0.55, f"t = {x:.2f}")
style_axes(ax, ylim=(-6, 11))
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
ax.plot(t, j(t), color="#1b9e77", linewidth=2.6)
zero_second = (r + s) / 3
ax.scatter([zero_second], [0], color="#111111", s=38, zorder=5)
ax.text(zero_second + 0.08, 0.45, f"Wendestelle von v: t = {zero_second:.2f}")
style_axes(ax, ylim=(-10, 13))
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
    ax.plot(t, y, color=color, linewidth=2.2)
    ax.set_title(title)
    ax.set_xlabel("t in h")
    ax.set_ylabel(ylabel)
    pad = max(1, (float(np.max(y)) - float(np.min(y))) * 0.12)
    style_axes(ax, ylim=(float(np.min(y)) - pad, float(np.max(y)) + pad))
fig.suptitle("Ballonfahrt: Funktion, Stammfunktion und Ableitungen", fontsize=17)
fig.tight_layout()
save(fig, "00_uebersicht_alle_graphen.png")
