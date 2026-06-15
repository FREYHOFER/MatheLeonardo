from PIL import Image, ImageDraw, ImageFont
import math
import os


OUT_DIR = r"C:\Users\leona\Documents\PL Mathe\Grafiken"
OUT_FILE = os.path.join(OUT_DIR, "ballonfahrt_geschwindigkeit.png")

# Velocity model:
# v(t) = k * t * (t - r) * (t - s), 0 <= t <= 7
# r and s are the two direction changes during the flight.
r = 3.3

# The second direction change s is calculated from the condition
# integral from 0 to 7 of v(t) dt = 0.
# For v(t) = k*t*(t-r)*(t-s), k does not matter for this condition.
s = ((343 * r / 3) - (2401 / 4)) / ((49 * r / 2) - (343 / 3))


def raw_v(t):
    return t * (t - r) * (t - s)


def raw_v_prime_roots():
    # derivative of t(t-r)(t-s) = t^3 - (r+s)t^2 + rs t
    # is 3t^2 - 2(r+s)t + rs
    a = 3
    b = -2 * (r + s)
    c = r * s
    disc = b * b - 4 * a * c
    return [(-b - math.sqrt(disc)) / (2 * a), (-b + math.sqrt(disc)) / (2 * a)]


max_t, min_t = raw_v_prime_roots()
k = 25 / raw_v(max_t)


def v(t):
    return k * raw_v(t)


def antiderivative(t):
    # Integral of k * (t^3 - (r+s)t^2 + rs*t)
    return k * (t**4 / 4 - (r + s) * t**3 / 3 + r * s * t**2 / 2)


width, height = 1600, 1000
scale = 2
img = Image.new("RGB", (width * scale, height * scale), "#ffffff")
draw = ImageDraw.Draw(img)


def font(size, bold=False):
    candidates = [
        r"C:\Windows\Fonts\arialbd.ttf" if bold else r"C:\Windows\Fonts\arial.ttf",
        r"C:\Windows\Fonts\segoeuib.ttf" if bold else r"C:\Windows\Fonts\segoeui.ttf",
    ]
    for path in candidates:
        if os.path.exists(path):
            return ImageFont.truetype(path, size * scale)
    return ImageFont.load_default()


title_font = font(40, True)
subtitle_font = font(24)
label_font = font(20)
small_font = font(17)
formula_font = font(22, True)

margin_l, margin_r, margin_t, margin_b = 155 * scale, 90 * scale, 170 * scale, 235 * scale
plot_w = width * scale - margin_l - margin_r
plot_h = height * scale - margin_t - margin_b
x_min, x_max = 0, 7
y_min, y_max = -32, 32


def px(t):
    return margin_l + (t - x_min) / (x_max - x_min) * plot_w


def py(y):
    return margin_t + (y_max - y) / (y_max - y_min) * plot_h


def line(points, fill, width_px=3):
    draw.line([(int(x), int(y)) for x, y in points], fill=fill, width=width_px * scale, joint="curve")


# Background panel.
draw.rounded_rectangle(
    [45 * scale, 45 * scale, (width - 45) * scale, (height - 45) * scale],
    radius=26 * scale,
    fill="#ffffff",
    outline="#d9d9d9",
    width=2 * scale,
)

draw.text((80 * scale, 62 * scale), "Horizontalgeschwindigkeit einer 7-stuendigen Ballonfahrt", fill="#1e2528", font=title_font)
draw.text(
    (80 * scale, 113 * scale),
    "Modell mit zwei Richtungswechseln und exakt ausgeglichener Flaechenbilanz",
    fill="#596166",
    font=subtitle_font,
)

# Grid and axes.
for x in range(0, 8):
    color = "#dddddd" if x else "#777777"
    line([(px(x), py(y_min)), (px(x), py(y_max))], color, 1)
    draw.text((px(x) - 8 * scale, py(0) + 12 * scale), str(x), fill="#3d4448", font=small_font)

for y in range(-30, 31, 10):
    color = "#dddddd" if y else "#333333"
    line([(px(x_min), py(y)), (px(x_max), py(y))], color, 1 if y else 2)
    draw.text((px(0) - 58 * scale, py(y) - 10 * scale), str(y), fill="#3d4448", font=small_font)

line([(px(0), py(y_min)), (px(0), py(y_max))], "#333333", 2)
line([(px(x_min), py(0)), (px(x_max), py(0))], "#333333", 2)

draw.text((px(7) - 20 * scale, py(0) + 44 * scale), "t in h", fill="#252b2e", font=label_font)
draw.text((82 * scale, 143 * scale), "v(t) in km/h", fill="#252b2e", font=label_font)

# Area fills.
samples = 900
points = []
for i in range(samples + 1):
    t = x_min + (x_max - x_min) * i / samples
    points.append((t, v(t)))

positive_poly = [(px(0), py(0))]
for t, y in points:
    if y >= 0:
        positive_poly.append((px(t), py(y)))
    else:
        positive_poly.append((px(t), py(0)))
positive_poly.append((px(7), py(0)))
draw.polygon([(int(x), int(y)) for x, y in positive_poly], fill="#8fd19e")

negative_poly = [(px(0), py(0))]
for t, y in points:
    if y <= 0:
        negative_poly.append((px(t), py(y)))
    else:
        negative_poly.append((px(t), py(0)))
negative_poly.append((px(7), py(0)))
draw.polygon([(int(x), int(y)) for x, y in negative_poly], fill="#ef8f82")

# Curve.
curve = [(px(t), py(y)) for t, y in points]
line(curve, "#0f5f73", 4)

# Mark special points.
special = [
    (0, 0, "Start"),
    (r, 0, "Richtungswechsel"),
    (s, 0, "Richtungswechsel"),
    (7, v(7), "Ende"),
    (max_t, v(max_t), "Hochpunkt"),
    (min_t, v(min_t), "Tiefpunkt"),
]

for t, y, label in special:
    x, yy = px(t), py(y)
    draw.ellipse([x - 8 * scale, yy - 8 * scale, x + 8 * scale, yy + 8 * scale], fill="#1e2528")
    if label == "Tiefpunkt":
        tx, ty = x + 12 * scale, yy + 12 * scale
    elif label == "Ende":
        tx, ty = x - 135 * scale, yy - 34 * scale
    elif label == "Hochpunkt":
        tx, ty = x + 14 * scale, yy - 34 * scale
    else:
        tx, ty = x + 12 * scale, yy - 30 * scale
    draw.text((tx, ty), label, fill="#1e2528", font=small_font)

# Formula and key values.
formula = f"v(t) = {k:.3f} * t * (t - {r:.1f}) * (t - {s:.5f})"
draw.rounded_rectangle(
    [785 * scale, 800 * scale, 1495 * scale, 935 * scale],
    radius=12 * scale,
    fill="#ffffff",
    outline="#cccccc",
    width=2 * scale,
)
draw.text((810 * scale, 815 * scale), formula, fill="#17343d", font=formula_font)
draw.text((810 * scale, 858 * scale), f"Hochpunkt: t = {max_t:.2f} h, v = {v(max_t):.1f} km/h", fill="#27434b", font=small_font)
draw.text((1160 * scale, 858 * scale), f"Tiefpunkt: t = {min_t:.2f} h, v = {v(min_t):.1f} km/h", fill="#27434b", font=small_font)
draw.text((810 * scale, 895 * scale), f"Endgeschwindigkeit: v(7) = {v(7):.1f} km/h", fill="#27434b", font=small_font)
end_distance = 0 if abs(antiderivative(7)) < 1e-9 else antiderivative(7)
draw.text((1160 * scale, 895 * scale), f"Endabstand: {end_distance:.6f} km", fill="#27434b", font=small_font)

draw.text((195 * scale, 835 * scale), "Gruen: Fahrt in positive Richtung", fill="#1f7a3a", font=small_font)
draw.text((195 * scale, 872 * scale), "Rot: Fahrt in Gegenrichtung", fill="#b63d31", font=small_font)
draw.text((195 * scale, 909 * scale), "Die Flaechen sind gleich gross: Landung exakt am Start.", fill="#596166", font=small_font)

# Resize for anti-aliasing.
img = img.resize((width, height), Image.Resampling.LANCZOS)
os.makedirs(OUT_DIR, exist_ok=True)
img.save(OUT_FILE, quality=95)
print(OUT_FILE)
