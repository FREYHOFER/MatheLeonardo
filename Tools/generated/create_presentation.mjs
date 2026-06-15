import fs from "node:fs/promises";
import { Presentation, PresentationFile } from "file:///C:/Users/leona/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/@oai/artifact-tool/dist/artifact_tool.mjs";

const OUT = "C:/Users/leona/Documents/PL Mathe/Abgabe/Ballonfahrt_Modell_Praesentation_Leonardo_Freyhofer.pptx";
const PREVIEW = "C:/Users/leona/Documents/PL Mathe/Render/Praesentation";
const G = "C:/Users/leona/Documents/PL Mathe/Grafiken";
const HTML = "C:/Users/leona/Documents/PL Mathe/HTML";

async function ensureDir(path) {
  await fs.mkdir(path, { recursive: true });
}

async function readImageBlob(path) {
  const bytes = await fs.readFile(path);
  return bytes.buffer.slice(bytes.byteOffset, bytes.byteOffset + bytes.byteLength);
}

async function writeBlob(path, blob) {
  await fs.writeFile(path, new Uint8Array(await blob.arrayBuffer()));
}

const W = 1280;
const H = 720;
const page = { left: 64, top: 52, width: 1152, height: 616 };
const ink = "slate-950";
const muted = "slate-600";
const teal = "cyan-900";
const teal2 = "cyan-700";
const pale = "slate-50";
const accent = "amber-600";

function box(slide, position, fill = "white", line = "slate-200") {
  return slide.shapes.add({
    geometry: "roundRect",
    position,
    fill,
    line: { style: "solid", fill: line, width: 1 },
    borderRadius: "rounded-lg",
  });
}

function text(slide, content, position, style = {}) {
  const shape = slide.shapes.add({
    geometry: "textbox",
    position,
    fill: "none",
    line: { style: "solid", fill: "none", width: 0 },
  });
  shape.text = content;
  shape.text.style = {
    typeface: "Aptos",
    fontSize: style.fontSize ?? 22,
    bold: style.bold ?? false,
    color: style.color ?? ink,
  };
  return shape;
}

async function image(slide, name, position, alt, fit = "contain") {
  const blob = await readImageBlob(`${G}/${name}`);
  slide.images.add({
    blob,
    contentType: "image/png",
    alt,
    fit,
    position,
  });
}

function title(slide, heading, kicker = "") {
  text(slide, kicker.toUpperCase(), { left: page.left, top: 32, width: 820, height: 24 }, { fontSize: 12, bold: true, color: teal2 });
  text(slide, heading, { left: page.left, top: 58, width: 1040, height: 56 }, { fontSize: 34, bold: true, color: teal });
}

function footer(slide, num) {
  text(slide, `Ballonfahrt-Modell · Leonardo Freyhofer · ${num}`, { left: 64, top: 684, width: 500, height: 22 }, { fontSize: 10, color: "slate-500" });
}

function bulletList(slide, items, x, y, w, size = 21, gap = 43) {
  items.forEach((item, i) => {
    text(slide, "•", { left: x, top: y + i * gap, width: 24, height: 28 }, { fontSize: size, bold: true, color: teal2 });
    text(slide, item, { left: x + 30, top: y + i * gap, width: w - 30, height: 34 }, { fontSize: size, color: ink });
  });
}

function formulaCard(slide, formula, caption, x, y, w, h) {
  box(slide, { left: x, top: y, width: w, height: h }, "slate-50", "slate-200");
  text(slide, formula, { left: x + 24, top: y + 20, width: w - 48, height: 44 }, { fontSize: 27, bold: true, color: teal });
  if (caption) text(slide, caption, { left: x + 24, top: y + 74, width: w - 48, height: h - 88 }, { fontSize: 17, color: muted });
}

async function main() {
  console.log("start deck build");
  await ensureDir("C:/Users/leona/Documents/PL Mathe/Abgabe");
  await ensureDir(PREVIEW);

  const presentation = Presentation.create({ slideSize: { width: W, height: H } });

  // 1
  {
    const slide = presentation.slides.add();
    slide.background.fill = "white";
    text(slide, "Ballonfahrt-Modell", { left: 72, top: 112, width: 850, height: 70 }, { fontSize: 54, bold: true, color: teal });
    text(slide, "Entwicklung einer realistischen Horizontalgeschwindigkeit mit einer Funktion dritten Grades", { left: 76, top: 194, width: 920, height: 70 }, { fontSize: 25, color: muted });
    formulaCard(slide, "v(t) ≈ 1,648 · t · (t - 3,4) · (t - 6,81579)", "Finale Funktion für 0 ≤ t ≤ 7 Stunden", 76, 338, 850, 132);
    text(slide, "Leitfrage: Wie entsteht ein Modell, das mathematisch nachvollziehbar und zugleich realistisch ist?", { left: 76, top: 526, width: 950, height: 42 }, { fontSize: 21, color: ink });
    footer(slide, 1);
    console.log("slide 1");
  }

  // 2
  {
    const slide = presentation.slides.add();
    slide.background.fill = "white";
    title(slide, "Aufgabe und Bedingungen", "Ausgangspunkt");
    bulletList(slide, [
      "Fahrtzeit: 7 Stunden",
      "Horizontalgeschwindigkeit soll durch eine kubische Funktion beschrieben werden",
      "Die Fahrtrichtung soll sich zweimal umkehren",
      "Der Landepunkt soll horizontal exakt beim Startpunkt liegen",
      "Endgeschwindigkeit darf nicht 0 km/h sein",
      "Zusätzlich: z-Achse und gleichseitige Landefläche"
    ], 92, 152, 930, 22, 54);
    footer(slide, 2);
    console.log("slide 2");
  }

  // 3
  {
    const slide = presentation.slides.add();
    slide.background.fill = "white";
    title(slide, "Ansatz der Funktion", "Modellidee");
    formulaCard(slide, "v(t) = k · t · (t - r) · (t - s)", "Drei Faktoren liefern drei Nullstellen: Start und zwei Richtungswechsel.", 90, 145, 710, 140);
    const cards = [
      ["t = 0", "Start der Ballonfahrt"],
      ["r und s", "Zeitpunkte der Richtungswechsel"],
      ["k", "Skalierung der Geschwindigkeit"]
    ];
    cards.forEach((c, i) => {
      box(slide, { left: 90 + i * 370, top: 360, width: 320, height: 120 }, i === 0 ? "cyan-50" : "slate-50", "slate-200");
      text(slide, c[0], { left: 115 + i * 370, top: 382, width: 270, height: 34 }, { fontSize: 28, bold: true, color: teal });
      text(slide, c[1], { left: 115 + i * 370, top: 426, width: 270, height: 44 }, { fontSize: 18, color: muted });
    });
    footer(slide, 3);
    console.log("slide 3");
  }

  // 4
  {
    const slide = presentation.slides.add();
    slide.background.fill = "white";
    title(slide, "Warum die glatte Variante nicht reicht", "Modellentscheidung");
    await image(slide, "10_modellentscheidung_vergleich.png", { left: 80, top: 128, width: 760, height: 460 }, "Vergleich der glatten und finalen Funktion");
    box(slide, { left: 880, top: 156, width: 300, height: 300 }, "slate-50", "slate-200");
    text(slide, "r = 3 führt zu s = 6,3", { left: 906, top: 184, width: 250, height: 52 }, { fontSize: 23, bold: true, color: teal });
    text(slide, "Das ist rechnerisch schön, aber nach Skalierung auf 25 km/h landet der Ballon mit ca. 44,3 km/h.", { left: 906, top: 250, width: 245, height: 120 }, { fontSize: 19, color: ink });
    text(slide, "→ zu schnell für eine realistische Landung", { left: 906, top: 386, width: 250, height: 42 }, { fontSize: 19, bold: true, color: accent });
    footer(slide, 4);
    console.log("slide 4");
  }

  // 5
  {
    const slide = presentation.slides.add();
    slide.background.fill = "white";
    title(slide, "Finale Modellentscheidung", "Herleitung");
    formulaCard(slide, "r = 3,4", "Der erste Richtungswechsel wird etwas später gewählt, damit die Landegeschwindigkeit sinkt.", 82, 142, 360, 150);
    formulaCard(slide, "∫₀⁷ v(t) dt = 0", "Diese Bedingung erzwingt, dass der horizontale Endabstand 0 km ist.", 462, 142, 360, 150);
    formulaCard(slide, "s ≈ 6,81579", "Der zweite Richtungswechsel wird daraus berechnet, nicht geraten.", 842, 142, 360, 150);
    formulaCard(slide, "k ≈ 1,648", "Danach wird k so gewählt, dass der lokale Hochpunkt 25 km/h beträgt.", 272, 386, 360, 150);
    formulaCard(slide, "v(7) ≈ 7,6 km/h", "Die Landegeschwindigkeit bleibt deutlich unter der Höchstgeschwindigkeit.", 652, 386, 360, 150);
    footer(slide, 5);
    console.log("slide 5");
  }

  // 6
  {
    const slide = presentation.slides.add();
    slide.background.fill = "white";
    title(slide, "Geschwindigkeitsgraph", "Finale Funktion");
    await image(slide, "01_geschwindigkeit_mit_flaechen.png", { left: 65, top: 122, width: 805, height: 475 }, "Geschwindigkeitsgraph mit positiver und negativer Fläche");
    bulletList(slide, [
      "Grün: Bewegung in positive Richtung",
      "Rot: Bewegung in Gegenrichtung",
      "Gleiche Flächenbilanz: horizontaler Endabstand 0 km",
      "Endgeschwindigkeit: ca. 7,6 km/h"
    ], 910, 175, 300, 19, 70);
    footer(slide, 6);
    console.log("slide 6");
  }

  // 7
  {
    const slide = presentation.slides.add();
    slide.background.fill = "white";
    title(slide, "Stammfunktion als Abstand", "Auswertung");
    await image(slide, "02_stammfunktion_abstand.png", { left: 78, top: 126, width: 805, height: 475 }, "Stammfunktion als horizontaler Abstand");
    formulaCard(slide, "S(t) = ∫ v(t) dt", "Die Stammfunktion beschreibt den horizontalen Abstand vom Startpunkt. Weil S(7)=0 gilt, landet der Ballon horizontal wieder am Startpunkt.", 910, 180, 300, 232);
    footer(slide, 7);
    console.log("slide 7");
  }

  // 8
  {
    const slide = presentation.slides.add();
    slide.background.fill = "white";
    title(slide, "Ableitungen", "Kontrolle");
    await image(slide, "03_erste_ableitung.png", { left: 70, top: 134, width: 545, height: 395 }, "Erste Ableitung");
    await image(slide, "04_zweite_ableitung.png", { left: 665, top: 134, width: 545, height: 395 }, "Zweite Ableitung");
    text(slide, "v'(t)=0 liefert Hoch- und Tiefpunkt. v''(t) zeigt den Wechsel der Krümmung.", { left: 108, top: 574, width: 980, height: 36 }, { fontSize: 22, bold: true, color: teal });
    footer(slide, 8);
    console.log("slide 8");
  }

  // 9
  {
    const slide = presentation.slides.add();
    slide.background.fill = "white";
    title(slide, "3D-Erweiterung und Landefläche", "Raummodell");
    await image(slide, "07_3d_variante_b2_ohne_seitendrift.png", { left: 58, top: 122, width: 570, height: 390 }, "3D-Modell ohne Seitenbewegung");
    await image(slide, "08_landeflaeche_gleichseitiges_dreieck_draufsicht.png", { left: 688, top: 122, width: 455, height: 455 }, "Draufsicht auf gleichseitige Landefläche");
    text(slide, "Zeit ist Parameter der Kurve. Die Landefläche liegt in z = 0; Start und Landepunkt sind ihr Zentrum.", { left: 90, top: 595, width: 1030, height: 34 }, { fontSize: 20, bold: true, color: teal });
    footer(slide, 9);
    console.log("slide 9");
  }

  // 10
  {
    const slide = presentation.slides.add();
    slide.background.fill = "white";
    title(slide, "Fazit und Medien-Backup", "Abschluss");
    bulletList(slide, [
      "Die Funktion erfüllt alle Aufgabenbedingungen.",
      "Die Richtungswechsel und die Integralbedingung erklären die Form des Graphen.",
      "Die glatte Variante wurde verworfen, weil die Landegeschwindigkeit zu hoch war.",
      "Die finale Variante landet horizontal am Startpunkt und hat v(7) ≈ 7,6 km/h.",
      "Interaktive HTMLs werden gezeigt; alle Aussagen sind zusätzlich als PNG-Folien abgesichert."
    ], 92, 145, 820, 22, 58);
    box(slide, { left: 940, top: 170, width: 270, height: 265 }, "slate-50", "slate-200");
    text(slide, "HTML-Dateien", { left: 962, top: 194, width: 220, height: 30 }, { fontSize: 22, bold: true, color: teal });
    text(slide, "ballonfahrt_zeit_abstand_hoehe_interaktiv.html\n\nballonfahrt_3d_interaktiv.html", { left: 962, top: 244, width: 220, height: 112 }, { fontSize: 15, color: ink });
    text(slide, "Backup: statische Grafiken in der PowerPoint", { left: 962, top: 374, width: 220, height: 45 }, { fontSize: 16, bold: true, color: accent });
    footer(slide, 10);
    console.log("slide 10");
  }

  const pptx = await PresentationFile.exportPptx(presentation);
  await pptx.save(OUT);
  console.log(OUT);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
