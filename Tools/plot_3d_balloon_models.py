import os

import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


OUT_DIR = r"C:\Users\leona\Documents\PL Mathe\Grafiken"
os.makedirs(OUT_DIR, exist_ok=True)

# Chosen final model:
# v(t) = k * t * (t - 3.4) * (t - s)
# s is calculated from integral_0^7 v(t) dt = 0.
# k is chosen so that the local maximum is 25 km/h.
r = 3.4
s = ((343 * r / 3) - (2401 / 4)) / ((49 * r / 2) - (343 / 3))


def local_max_scale(target_max=25):
    coeff = [3, -2 * (r + s), r * s]
    roots = sorted(float(x.real) for x in np.roots(coeff) if abs(x.imag) < 1e-9 and 0 <= x.real <= 7)
    t_max = roots[0]
    raw = t_max * (t_max - r) * (t_max - s)
    return target_max / raw


k = local_max_scale(25)


def S(t):
    return k * (t**4 / 4 - (r + s) * t**3 / 3 + r * s * t**2 / 2)


def H(t):
    # Zusatzmodell fuer die Hoehe: Start und Landung am Boden,
    # maximale Hoehe ca. 1.2 km in der Mitte der Fahrt.
    return 1.2 * 4 * t * (7 - t) / 49


def landing_triangle(center=(0, 0, 0), radius=0.55):
    # radius is the distance from center to each vertex.
    angles = np.deg2rad([90, 210, 330])
    cx, cy, cz = center
    return [(cx + radius * np.cos(a), cy + radius * np.sin(a), cz) for a in angles]


def side_lengths(vertices):
    points = np.array(vertices)
    return [
        float(np.linalg.norm(points[0] - points[1])),
        float(np.linalg.norm(points[1] - points[2])),
        float(np.linalg.norm(points[2] - points[0])),
    ]


def draw_custom_axes(ax):
    # GeoGebra-like axes: all three axes start at the common origin.
    ax.set_axis_off()
    xlim = (-5, 58)
    ylim = (-1.4, 1.4)
    zlim = (0, 1.35)
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_zlim(*zlim)

    # Ground grid in z=0: x-y plane.
    for x in np.arange(-5, 59, 5):
        ax.plot([x, x], [ylim[0], ylim[1]], [0, 0], color="#dddddd", linewidth=0.7, zorder=1)
    for y in np.arange(-1.2, 1.21, 0.4):
        ax.plot([xlim[0], xlim[1]], [y, y], [0, 0], color="#eeeeee", linewidth=0.6, zorder=1)

    # Vertical grid in y=0: x-z plane.
    for x in np.arange(-5, 59, 5):
        ax.plot([x, x], [0, 0], [zlim[0], zlim[1]], color="#e2e2e2", linewidth=0.6, zorder=1)
    for z in np.arange(0, 1.31, 0.3):
        ax.plot([xlim[0], xlim[1]], [0, 0], [z, z], color="#e2e2e2", linewidth=0.6, zorder=1)

    # Main axes from the origin.
    ax.plot([xlim[0], xlim[1]], [0, 0], [0, 0], color="#222222", linewidth=1.8)
    ax.plot([0, 0], [ylim[0], ylim[1]], [0, 0], color="#222222", linewidth=1.8)
    ax.plot([0, 0], [0, 0], [zlim[0], zlim[1]], color="#222222", linewidth=1.8)

    # Arrowheads.
    ax.quiver(xlim[1] - 0.25, 0, 0, 0.25, 0, 0, color="#222222", arrow_length_ratio=0.6)
    ax.quiver(0, ylim[1] - 0.08, 0, 0, 0.08, 0, color="#222222", arrow_length_ratio=0.6)
    ax.quiver(0, 0, zlim[1] - 0.12, 0, 0, 0.12, color="#222222", arrow_length_ratio=0.6)

    # Axis labels and a few ticks, kept sparse so the origin remains readable.
    ax.text(xlim[1] - 1.2, -0.16, 0, "x: S(t)", fontsize=10)
    ax.text(-0.35, ylim[1] + 0.05, 0, "y", fontsize=10)
    ax.text(0.08, 0.03, zlim[1] + 0.05, "z: Hoehe", fontsize=10)
    ax.text(0.4, -0.18, 0.05, "O(0|0|0)", fontsize=9)

    for x in [0, 15, 30, 45, 55]:
        ax.plot([x, x], [-0.03, 0.03], [0, 0], color="#222222", linewidth=1)
        ax.text(x, -0.10, 0, str(x), fontsize=8, ha="center")
    for y in [-1, 0, 1]:
        ax.plot([-0.10, 0.10], [y, y], [0, 0], color="#222222", linewidth=1)
        ax.text(-0.35, y, 0, str(y).replace(".", ","), fontsize=8, ha="right")
    for z in [0, 0.6, 1.2]:
        ax.plot([-0.08, 0.08], [0, 0], [z, z], color="#222222", linewidth=1)
        ax.text(-0.18, 0, z, str(z).replace(".", ","), fontsize=8, ha="right")


def add_triangle_3d(ax, vertices):
    tri = Poly3DCollection([vertices], facecolor="#f2c94c", edgecolor="#7a5a00", alpha=0.50, linewidth=1.8)
    ax.add_collection3d(tri)
    xs, ys, zs = zip(*vertices)
    ax.plot(list(xs) + [xs[0]], list(ys) + [ys[0]], list(zs) + [zs[0]], color="#7a5a00", linewidth=2)
    ax.scatter(xs, ys, zs, color="#7a5a00", s=28, depthshade=False)


t = np.linspace(0, 7, 600)
x = S(t)
y = np.zeros_like(t)
z = H(t)
triangle = landing_triangle((0, 0, 0), radius=0.55)
lengths = side_lengths(triangle)


# Final 3D view.
fig = plt.figure(figsize=(10.5, 7))
ax = fig.add_subplot(111, projection="3d")
draw_custom_axes(ax)

ax.plot(x, y, z, color="#005f73", linewidth=3.0)
ax.scatter([0], [0], [0], color="#d62728", s=70, depthshade=False)
ax.text(1.5, -0.65, 0.18, "Start = Landepunkt\nZentrum", fontsize=9)
add_triangle_3d(ax, triangle)

ax.set_title("3D-Modell ohne zusaetzliche Seitenbewegung", pad=12)
ax.view_init(elev=22, azim=-54)
ax.set_box_aspect((2.0, 0.85, 0.65))
fig.text(
    0.08,
    0.03,
    "Die Zeit ist Parameter der Kurve. Die Landeflaeche liegt in z = 0; Start- und Landepunkt sind ihr Zentrum.",
    fontsize=10,
)
path = os.path.join(OUT_DIR, "07_3d_variante_b2_ohne_seitendrift.png")
fig.savefig(path, dpi=220, facecolor="white")
plt.close(fig)
print(path)


# Time-distance-height version.
fig = plt.figure(figsize=(10.5, 7))
ax = fig.add_subplot(111, projection="3d")
ax.plot(t, S(t), H(t), color="#005f73", linewidth=2.8)
ax.scatter([0, 7], [S(0), S(7)], [H(0), H(7)], color="#d62728", s=55, depthshade=False)
ax.text(0, S(0), H(0) + 0.08, "Start", fontsize=9)
ax.text(7, S(7), H(7) + 0.08, "Endpunkt", fontsize=9)
ax.set_title("Zeit, horizontaler Abstand und Hoehe", pad=12)
ax.set_xlabel("x: Zeit t in h", labelpad=8)
ax.set_ylabel("y: horizontaler Abstand S(t) in km", labelpad=8)
ax.set_zlabel("z: Hoehe in km", labelpad=8)
ax.grid(True)
ax.view_init(elev=24, azim=-55)
ax.set_box_aspect((1.15, 1.8, 0.55))
path = os.path.join(OUT_DIR, "09_3d_zeit_abstand_hoehe.png")
fig.savefig(path, dpi=220, facecolor="white")
plt.close(fig)
print(path)


# Exact top view of the landing area with equal x/y scale.
fig, ax = plt.subplots(figsize=(7.5, 7.5))
tri_2d = np.array([(x, y) for x, y, z in triangle])
closed = np.vstack([tri_2d, tri_2d[0]])

ax.fill(tri_2d[:, 0], tri_2d[:, 1], color="#f2c94c", alpha=0.45, edgecolor="#7a5a00", linewidth=2.2)
ax.plot(closed[:, 0], closed[:, 1], color="#7a5a00", linewidth=2.2)
ax.scatter(tri_2d[:, 0], tri_2d[:, 1], color="#7a5a00", s=55, zorder=4)
ax.scatter([0], [0], color="#d62728", s=75, zorder=5)

for i, (vx, vy) in enumerate(tri_2d, start=1):
    ax.text(vx + 0.035, vy + 0.035, f"P{i}", fontsize=12)
    ax.plot([0, vx], [0, vy], color="#d62728", linestyle="--", linewidth=1.1, alpha=0.75)

ax.text(0, -0.08, "Start = Landepunkt\nZentrum der Landeflaeche", ha="center", va="top", fontsize=11)
ax.set_title("Landeflaeche: gleichseitiges Dreieck um Start- und Landepunkt")
ax.set_xlabel("x: horizontaler Abstand in km")
ax.set_ylabel("y: seitlicher Abstand in km")
ax.set_aspect("equal", adjustable="box")
ax.set_xlim(-0.75, 0.75)
ax.set_ylim(-0.75, 0.75)
ax.axhline(0, color="#333333", linewidth=1)
ax.axvline(0, color="#333333", linewidth=1)
ax.grid(True, color="#d0d0d0", linewidth=0.8)
ax.text(
    -0.72,
    -0.70,
    f"Alle Seitenlaengen: {lengths[0]:.3f} km = {lengths[1]:.3f} km = {lengths[2]:.3f} km",
    fontsize=10,
)
path = os.path.join(OUT_DIR, "08_landeflaeche_gleichseitiges_dreieck_draufsicht.png")
fig.savefig(path, dpi=220, bbox_inches="tight", facecolor="white")
plt.close(fig)
print(path)


# Interactive HTML version of the chosen spatial model.
html_dir = r"C:\Users\leona\Documents\PL Mathe\HTML"
os.makedirs(html_dir, exist_ok=True)

tri_closed = triangle + [triangle[0]]
fig = go.Figure()
fig.add_trace(
    go.Scatter3d(
        x=x,
        y=y,
        z=z,
        mode="lines",
        line=dict(color="#005f73", width=7),
        name="Ballonfahrt",
        hovertemplate="x=%{x:.2f} km<br>y=%{y:.2f} km<br>z=%{z:.2f} km<extra></extra>",
    )
)
fig.add_trace(
    go.Mesh3d(
        x=[p[0] for p in triangle],
        y=[p[1] for p in triangle],
        z=[p[2] for p in triangle],
        i=[0],
        j=[1],
        k=[2],
        color="#f2c94c",
        opacity=0.55,
        name="Landeflaeche",
        hoverinfo="skip",
    )
)
fig.add_trace(
    go.Scatter3d(
        x=[p[0] for p in tri_closed],
        y=[p[1] for p in tri_closed],
        z=[p[2] for p in tri_closed],
        mode="lines+markers+text",
        line=dict(color="#7a5a00", width=5),
        marker=dict(color="#7a5a00", size=5),
        text=["P1", "P2", "P3", ""],
        textposition="top center",
        name="Dreieck",
        hovertemplate="x=%{x:.3f} km<br>y=%{y:.3f} km<br>z=%{z:.3f} km<extra></extra>",
    )
)
fig.add_trace(
    go.Scatter3d(
        x=[0],
        y=[0],
        z=[0],
        mode="markers+text",
        marker=dict(color="#d62728", size=7),
        text=["Start = Landepunkt<br>Zentrum"],
        textposition="top right",
        name="Zentrum",
        hovertemplate="O(0|0|0)<extra></extra>",
    )
)

fig.update_layout(
    title="Interaktives 3D-Modell der Ballonfahrt",
    scene=dict(
        xaxis=dict(title="x: horizontaler Abstand S(t) in km", range=[-5, 58], gridcolor="#d0d0d0", zeroline=True, zerolinecolor="#222222"),
        yaxis=dict(title="y: seitlicher Abstand in km", range=[-1.4, 1.4], gridcolor="#d0d0d0", zeroline=True, zerolinecolor="#222222"),
        zaxis=dict(title="z: Hoehe in km", range=[0, 1.35], gridcolor="#d0d0d0", zeroline=True, zerolinecolor="#222222"),
        aspectratio=dict(x=2.2, y=0.65, z=0.5),
        camera=dict(eye=dict(x=1.55, y=-1.55, z=0.9)),
    ),
    margin=dict(l=0, r=0, t=50, b=0),
)
path = os.path.join(html_dir, "ballonfahrt_3d_interaktiv.html")
fig.write_html(path, include_plotlyjs=True, full_html=True)
print(path)


# Interactive HTML version of the time-distance-height model.
fig = go.Figure()
fig.add_trace(
    go.Scatter3d(
        x=t,
        y=S(t),
        z=H(t),
        mode="lines",
        line=dict(color="#005f73", width=7),
        name="Zeit-Abstand-Hoehe",
        hovertemplate="t=%{x:.2f} h<br>S(t)=%{y:.2f} km<br>Hoehe=%{z:.2f} km<extra></extra>",
    )
)
fig.add_trace(
    go.Scatter3d(
        x=[0, 7],
        y=[S(0), S(7)],
        z=[H(0), H(7)],
        mode="markers+text",
        marker=dict(color="#d62728", size=7),
        text=["Start", "Endpunkt"],
        textposition=["top right", "top left"],
        name="Start/Ende",
        hovertemplate="t=%{x:.2f} h<br>S=%{y:.2f} km<br>Hoehe=%{z:.2f} km<extra></extra>",
    )
)
fig.update_layout(
    title="Interaktiv: Zeit, horizontaler Abstand und Hoehe",
    scene=dict(
        xaxis=dict(title="x: Zeit t in h", range=[0, 7], gridcolor="#d0d0d0", zeroline=True, zerolinecolor="#222222"),
        yaxis=dict(title="y: horizontaler Abstand S(t) in km", range=[-5, 58], gridcolor="#d0d0d0", zeroline=True, zerolinecolor="#222222"),
        zaxis=dict(title="z: Hoehe in km", range=[0, 1.35], gridcolor="#d0d0d0", zeroline=True, zerolinecolor="#222222"),
        aspectratio=dict(x=1.1, y=1.8, z=0.55),
        camera=dict(eye=dict(x=1.45, y=-1.7, z=0.9)),
    ),
    margin=dict(l=0, r=0, t=50, b=0),
)
path = os.path.join(html_dir, "ballonfahrt_zeit_abstand_hoehe_interaktiv.html")
fig.write_html(path, include_plotlyjs=True, full_html=True)
print(path)
