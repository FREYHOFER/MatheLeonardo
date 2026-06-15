import os

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


OUT_DIR = r"C:\Users\leona\Documents\PL Mathe\Grafiken"
os.makedirs(OUT_DIR, exist_ok=True)

k = 0.5
r = 3.0
s = 6.3


def v(t):
    return k * t * (t - r) * (t - s)


def S(t):
    return k * (t**4 / 4 - (r + s) * t**3 / 3 + r * s * t**2 / 2)


def H(t):
    # Simple height model: takeoff and landing at ground level,
    # maximum height about 1.2 km after half the flight.
    return 1.2 * 4 * t * (7 - t) / 49


def N(t):
    # Optional sideways drift for the spatial version.
    # It starts and ends at 0, so the final landing point stays at the start.
    return 0.55 * np.sin(2 * np.pi * t / 7)


def landing_triangle(center, radius=0.55, plane="ground"):
    angles = np.deg2rad([90, 210, 330])
    cx, cy, cz = center
    if plane == "ground":
        return [(cx + radius * np.cos(a), cy + radius * np.sin(a), cz) for a in angles]
    if plane == "time":
        return [(cx, cy + radius * np.cos(a), cz + radius * np.sin(a)) for a in angles]
    raise ValueError(plane)


def style_3d(ax):
    ax.grid(True)
    for axis in [ax.xaxis, ax.yaxis, ax.zaxis]:
        axis.pane.set_facecolor((1, 1, 1, 1))
        axis.pane.set_edgecolor((0.85, 0.85, 0.85, 1))
    ax.tick_params(labelsize=9)


def add_triangle(ax, vertices, color="#f2c94c"):
    tri = Poly3DCollection([vertices], facecolor=color, edgecolor="#7a5a00", alpha=0.55, linewidth=1.5)
    ax.add_collection3d(tri)
    xs, ys, zs = zip(*vertices)
    ax.scatter(xs, ys, zs, color="#7a5a00", s=35, depthshade=False)
    for i, point in enumerate(vertices, start=1):
        ax.text(point[0], point[1], point[2] + 0.04, f"P{i}", fontsize=9)


t = np.linspace(0, 7, 500)
end_t = 7
end_distance = float(S(7))
end_height = float(H(7))
end_north = float(N(7))


# Variant A: time-distance-height.
fig = plt.figure(figsize=(10.5, 7))
ax = fig.add_subplot(111, projection="3d")
ax.plot(t, S(t), H(t), color="#005f73", linewidth=2.6)
ax.scatter([0, end_t], [S(0), S(7)], [H(0), H(7)], color="#111111", s=45, depthshade=False)
ax.text(0, S(0), H(0) + 0.08, "Start", fontsize=10)
ax.text(end_t, S(7), H(7) + 0.08, "Endpunkt", fontsize=10)

tri_a = landing_triangle((end_t, end_distance, end_height), radius=0.55, plane="time")
add_triangle(ax, tri_a)

ax.set_title("Variante A: Zeit, horizontaler Abstand und Hoehe", pad=16)
ax.set_xlabel("x: Zeit t in h", labelpad=9)
ax.set_ylabel("y: horizontaler Abstand S(t) in km", labelpad=9)
ax.set_zlabel("z: Hoehe in km", labelpad=9)
ax.view_init(elev=23, azim=-55)
ax.set_box_aspect((1.4, 1.2, 0.55))
style_3d(ax)
fig.text(
    0.08,
    0.03,
    "Hinweis: Diese Darstellung zeigt den Zeitverlauf gut. Die Dreiecksfläche liegt aber in einer Zeit-Ebene und ist daher physikalisch weniger sinnvoll.",
    fontsize=10,
)
path = os.path.join(OUT_DIR, "05_3d_variante_a_zeit_abstand_hoehe.png")
fig.savefig(path, dpi=220, bbox_inches="tight", facecolor="white")
plt.close(fig)
print(path)


# Variant B: spatial model. Time is only the parameter along the curve.
fig = plt.figure(figsize=(10.5, 7))
ax = fig.add_subplot(111, projection="3d")
x = S(t)
y = N(t)
z = H(t)
ax.plot(x, y, z, color="#005f73", linewidth=2.6)
ax.scatter([S(0), S(7)], [N(0), N(7)], [H(0), H(7)], color="#111111", s=45, depthshade=False)
ax.text(S(0), N(0), H(0) + 0.08, "Start", fontsize=10)
ax.text(S(7), N(7), H(7) + 0.08, "Landepunkt", fontsize=10)

tri_b = landing_triangle((end_distance, end_north, 0), radius=0.55, plane="ground")
add_triangle(ax, tri_b)

ax.set_title("Variante B: raeumliche Darstellung der Ballonfahrt", pad=16)
ax.set_xlabel("x: Ost-West-Abstand in km", labelpad=9)
ax.set_ylabel("y: Nord-Sued-Abstand in km", labelpad=9)
ax.set_zlabel("z: Hoehe in km", labelpad=9)
ax.view_init(elev=26, azim=-45)
ax.set_box_aspect((1.7, 0.75, 0.45))
style_3d(ax)
fig.text(
    0.08,
    0.03,
    "Zeit wird hier nicht als Achse gezeichnet, sondern parametrisiert die Kurve. Die Landeflaeche liegt realistisch in der Bodenebene z = 0.",
    fontsize=10,
)
path = os.path.join(OUT_DIR, "06_3d_variante_b_raumkurve_landeflaeche.png")
fig.savefig(path, dpi=220, bbox_inches="tight", facecolor="white")
plt.close(fig)
print(path)


# Variant B without sideways drift, if a stricter interpretation is preferred.
fig = plt.figure(figsize=(10.5, 7))
ax = fig.add_subplot(111, projection="3d")
x = S(t)
y = np.zeros_like(t)
z = H(t)
ax.plot(x, y, z, color="#005f73", linewidth=2.6)
ax.scatter([S(0), S(7)], [0, 0], [H(0), H(7)], color="#111111", s=45, depthshade=False)
ax.text(S(0), 0, H(0) + 0.08, "Start", fontsize=10)
ax.text(S(7), 0, H(7) + 0.08, "Landepunkt", fontsize=10)
tri_c = landing_triangle((end_distance, 0, 0), radius=0.55, plane="ground")
add_triangle(ax, tri_c)
ax.set_title("Variante B2: raeumlich, ohne zusaetzliche Seitenbewegung", pad=16)
ax.set_xlabel("x: horizontaler Abstand S(t) in km", labelpad=9)
ax.set_ylabel("y: seitlicher Abstand in km", labelpad=9)
ax.set_zlabel("z: Hoehe in km", labelpad=9)
ax.view_init(elev=25, azim=-48)
ax.set_box_aspect((1.7, 0.75, 0.45))
style_3d(ax)
fig.text(
    0.08,
    0.03,
    "Strengere Variante: Die berechnete Bewegung bleibt eindimensional horizontal; die y-Achse dient nur dazu, die Landeflaeche am Boden zu zeigen.",
    fontsize=10,
)
path = os.path.join(OUT_DIR, "07_3d_variante_b2_ohne_seitendrift.png")
fig.savefig(path, dpi=220, bbox_inches="tight", facecolor="white")
plt.close(fig)
print(path)
