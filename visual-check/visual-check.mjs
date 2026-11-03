// Visual and text regression check for riselabs.at (Phase Q).
//
//   node visual-check.mjs shoot   <base-url> <out-dir>
//   node visual-check.mjs compare <before-dir> <after-dir> <report-dir>
//   NOJS=1 node visual-check.mjs shoot …   (same, with JavaScript turned off)
//
// "shoot" takes a full-page screenshot of every path in visual-pages.txt at
// 1440 px and 390 px, in the dark and the light theme, with motion turned off,
// and records what a visitor and a search engine read: the <title>, the
// description and Open Graph tags, the canonical link and the visible text.
// "compare" reports, page by page, the share of pixels that differ and any
// change in that text, and writes a diff image for every page that moved.
// A refactoring step passes when the report lists no changes other than the
// ones the step was meant to make.
import { chromium } from "playwright";
import fs from "node:fs";
import path from "node:path";
import { PNG } from "pngjs";
import pixelmatch from "pixelmatch";

const here = path.dirname(new URL(import.meta.url).pathname);
const VIEWS = [
  { name: "desktop", width: 1440, height: 900 },
  { name: "phone", width: 390, height: 844 },
];
const THEMES = ["dark", "light"];
const slug = (p) => (p.replace(/[^a-z0-9]+/gi, "-").replace(/^-|-$/g, "") || "home");

function pages() {
  return fs.readFileSync(path.join(here, "visual-pages.txt"), "utf8")
    .split("\n").map((l) => l.trim()).filter((l) => l && !l.startsWith("#"));
}

// Read through Playwright's own handles, which work with page scripts turned off.
async function readText(page) {
  const attr = async (sel, name) => (await page.locator(sel).count()) ? await page.locator(sel).first().getAttribute(name) : null;
  return {
    title: await page.title(),
    description: await attr('meta[name="description"]', "content"),
    ogTitle: await attr('meta[property="og:title"]', "content"),
    ogImage: await attr('meta[property="og:image"]', "content"),
    canonical: await attr('link[rel="canonical"]', "href"),
    text: (await page.locator("body").innerText()).replace(/\s+/g, " ").trim(),
  };
}

async function shoot(base, out) {
  fs.mkdirSync(out, { recursive: true });
  const browser = await chromium.launch();
  const text = {};
  for (const theme of THEMES) {
    for (const v of VIEWS) {
      const ctx = await browser.newContext({
        viewport: { width: v.width, height: v.height },
        reducedMotion: "reduce",
        colorScheme: theme,
        // NOJS=1 checks the pages as a visitor without JavaScript sees them.
        // The theme toggle needs JavaScript, so both "themes" then show the default.
        javaScriptEnabled: process.env.NOJS !== "1",
      });
      // The site keeps the visitor's choice under this key; set it before any script runs.
      await ctx.addInitScript((t) => { try { localStorage.setItem("rise-theme", t); } catch (e) {} }, theme);
      const page = await ctx.newPage();
      for (const p of pages()) {
        const url = base.replace(/\/$/, "") + p;
        await page.goto(url, { waitUntil: "networkidle" });
        if (process.env.NOJS !== "1") await page.addStyleTag({ content: "*,*::before,*::after{animation:none!important;transition:none!important;caret-color:transparent!important}" });
        if (process.env.NOJS === "1") {
          // No page scripts run, so wait for the load event instead of polling the images.
          await page.waitForLoadState("load");
        } else {
          await page.evaluate(async () => {
            const cap = (p) => Promise.race([p, new Promise((r) => setTimeout(r, 5000))]);
            document.querySelectorAll("img[loading=lazy]").forEach((i) => (i.loading = "eager"));
            await cap(document.fonts.ready);
            await cap(Promise.all([...document.images].map((i) => i.complete ? 0 : new Promise((r) => { i.onload = i.onerror = r; }))));
          });
        }
        await page.waitForTimeout(300);
        const key = `${slug(p)}__${v.name}__${theme}`;
        await page.screenshot({ path: path.join(out, key + ".png"), fullPage: true });
        if (theme === THEMES[0] && v.name === "desktop") {
          text[p] = await readText(page);
        }
        process.stdout.write(".");
      }
      await ctx.close();
    }
  }
  await browser.close();
  fs.writeFileSync(path.join(out, "text.json"), JSON.stringify(text, null, 1));
  console.log(`\n${Object.keys(text).length} pages, ${pages().length * VIEWS.length * THEMES.length} screenshots in ${out}`);
}

function compare(a, b, reportDir) {
  fs.mkdirSync(reportDir, { recursive: true });
  const rows = [];
  let changed = 0;
  for (const f of fs.readdirSync(a).filter((x) => x.endsWith(".png")).sort()) {
    const pb = path.join(b, f);
    if (!fs.existsSync(pb)) { rows.push(`| ${f} | missing after | |`); changed++; continue; }
    const A = PNG.sync.read(fs.readFileSync(path.join(a, f)));
    const B = PNG.sync.read(fs.readFileSync(pb));
    if (A.width !== B.width || A.height !== B.height) {
      rows.push(`| ${f} | size ${A.width}x${A.height} → ${B.width}x${B.height} | |`); changed++; continue;
    }
    const diff = new PNG({ width: A.width, height: A.height });
    const n = pixelmatch(A.data, B.data, diff.data, A.width, A.height, { threshold: 0.1 });
    if (n > 0) {
      const share = (100 * n / (A.width * A.height)).toFixed(3);
      fs.writeFileSync(path.join(reportDir, f.replace(".png", ".diff.png")), PNG.sync.write(diff));
      rows.push(`| ${f} | ${n} px (${share}%) | ${f.replace(".png", ".diff.png")} |`); changed++;
    }
  }
  const ta = JSON.parse(fs.readFileSync(path.join(a, "text.json"), "utf8"));
  const tb = JSON.parse(fs.readFileSync(path.join(b, "text.json"), "utf8"));
  const textRows = [];
  for (const p of Object.keys(ta)) {
    for (const k of Object.keys(ta[p])) {
      if (JSON.stringify(ta[p][k]) !== JSON.stringify(tb[p]?.[k])) {
        const show = (s) => (s == null ? "–" : String(s).slice(0, 120).replace(/\|/g, "\\|"));
        textRows.push(`| ${p} | ${k} | ${k === "text" ? "visible text changed" : show(ta[p][k]) + " → " + show(tb[p]?.[k])} |`);
      }
    }
  }
  const md = [
    `# Visual check: ${path.basename(a)} → ${path.basename(b)}`,
    "",
    changed ? `## Screenshots that differ (${changed})\n\n| Shot | Difference | Diff image |\n| --- | --- | --- |\n${rows.join("\n")}` : "## Screenshots\n\nNo differences.",
    "",
    textRows.length ? `## Text that differs (${textRows.length})\n\n| Page | Field | Change |\n| --- | --- | --- |\n${textRows.join("\n")}` : "## Text\n\nNo differences in titles, descriptions, Open Graph tags, canonical links or visible text.",
    "",
  ].join("\n");
  fs.writeFileSync(path.join(reportDir, "report.md"), md);
  console.log(md);
  process.exitCode = changed || textRows.length ? 1 : 0;
}

const [cmd, x, y, z] = process.argv.slice(2);
if (cmd === "shoot" && x && y) await shoot(x, y);
else if (cmd === "compare" && x && y && z) compare(x, y, z);
else console.log("usage:\n  node visual-check.mjs shoot <base-url> <out-dir>\n  node visual-check.mjs compare <before-dir> <after-dir> <report-dir>");
