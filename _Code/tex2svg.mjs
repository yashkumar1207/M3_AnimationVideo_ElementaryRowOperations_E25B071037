// Converts LaTeX math expressions to self-contained path-only SVGs for Manim.
import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";
import { mathjax } from "mathjax-full/js/mathjax.js";
import { TeX } from "mathjax-full/js/input/tex.js";
import { SVG } from "mathjax-full/js/output/svg.js";
import { liteAdaptor } from "mathjax-full/js/adaptors/liteAdaptor.js";
import { RegisterHTMLHandler } from "mathjax-full/js/handlers/html.js";
import { AllPackages } from "mathjax-full/js/input/tex/AllPackages.js";

const adaptor = liteAdaptor();
RegisterHTMLHandler(adaptor);

const tex = new TeX({ packages: AllPackages });
const svg = new SVG({ fontCache: "none" });
const html = mathjax.document("", { InputJax: tex, OutputJax: svg });

const texString = process.argv[2];
const outDir = process.argv[3] || path.resolve(".tex_cache");

if (!texString) {
  console.error("Usage: node tex2svg.mjs '<latex>' [outDir]");
  process.exit(1);
}

fs.mkdirSync(outDir, { recursive: true });
const hash = crypto.createHash("sha256").update(texString).digest("hex").slice(0, 16);
const outFile = path.join(outDir, `${hash}.svg`);

if (!fs.existsSync(outFile)) {
  const node = html.convert(texString, { display: true });
  let svgText = adaptor.innerHTML(node);
  svgText = svgText.replace(/currentColor/g, "#FFFFFF");
  fs.writeFileSync(outFile, svgText, "utf8");
}

process.stdout.write(outFile);
