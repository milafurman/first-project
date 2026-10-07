// Rasterise the lockups to PNG, and build the specimen sheet.
//
// These outputs used to be made by hand, which is why
// truemg-lockup-light-1200.png and -dark-1200.png sat in this folder carrying
// both the old Gila drawing and the stretched LABS for a day after the SVGs
// they are supposedly exports of had been fixed. The README points at them as
// "the ones to upload in the Lapis admin", so a stale pair here is a stale logo
// on the storefront. Rendering them from the SVGs in a script means they cannot
// disagree with the SVGs again.
//
//   node render_png.mjs
//
// The 1200px pair is the markless web lockup on purpose: the Gila mark belongs
// on the browser tab and the vial, not in the site header.

import pkg from '/opt/node-tools/node_modules/playwright/index.js';
const { chromium } = pkg;
import fs from 'fs';
import path from 'path';

const DIR = path.dirname(new URL(import.meta.url).pathname);
process.chdir(DIR);

const WIDTH = 1200;
const PNGS = [
  ['truemg-lockup-web.svg', 'truemg-lockup-light-1200.png'],
  ['truemg-lockup-web-onink.svg', 'truemg-lockup-dark-1200.png'],
];

// name, file, ground — the specimen sheet's rows
const SPECIMEN = [
  ['the mark', 'truemg-mark-brand.svg', 'light'],
  ['site header', 'truemg-lockup-web.svg', 'light'],
  ['site footer', 'truemg-lockup-web-onink.svg', 'dark'],
  ['with the mark, for print', 'truemg-lockup-header.svg', 'light'],
  ['with the mark, on ink', 'truemg-lockup-onink.svg', 'dark'],
];

const vb = (f) => fs.readFileSync(f, 'utf8').match(/viewBox="0 0 ([\d.]+) ([\d.]+)"/).slice(1).map(Number);

const b = await chromium.launch({ args: ['--no-sandbox'] });

for (const [svg, png] of PNGS) {
  const [w, h] = vb(svg);
  const height = Math.round(WIDTH * h / w);
  const ctx = await b.newContext({ viewport: { width: WIDTH, height }, deviceScaleFactor: 1 });
  const p = await ctx.newPage();
  await p.setContent(
    `<style>html,body{margin:0;height:100%}img{width:100%;display:block}</style>` +
    `<img src="data:image/svg+xml;base64,${fs.readFileSync(svg).toString('base64')}">`);
  await p.waitForTimeout(350);
  await p.screenshot({ path: png, omitBackground: true });
  await ctx.close();
  console.log(`  ${png.padEnd(32)} ${WIDTH}x${height}  ${fs.statSync(png).size} bytes`);
}

const rows = SPECIMEN.map(([label, f, ground]) => {
  const [w, h] = vb(f);
  const scale = Math.min(620 / w, 150 / h);
  return `<div class="r ${ground}"><div class="l">${label}<br><span>${f}</span></div>
   <img style="width:${Math.round(w * scale)}px" src="data:image/svg+xml;base64,${fs.readFileSync(f).toString('base64')}"></div>`;
}).join('');

const ctx = await b.newContext({ viewport: { width: 1000, height: 900 }, deviceScaleFactor: 2 });
const p = await ctx.newPage();
await p.setContent(`<style>
 body{margin:0;font:14px ui-monospace,monospace}
 h1{font:600 20px system-ui;margin:0;padding:20px 26px;background:#17181a;color:#fff}
 .r{display:flex;align-items:center;gap:24px;padding:22px 26px;border-bottom:1px solid #e6e7ea}
 .light{background:#fff;color:#111}.dark{background:#0A0A0B;color:#e8e8ea}
 .l{width:210px;flex:none}.l span{color:#8b8f95;font-size:12px}
</style><h1>TrueMG Labs — current logo set</h1>${rows}`);
await p.waitForTimeout(600);
await p.screenshot({ path: 'lockup-preview.jpg', fullPage: true, type: 'jpeg', quality: 92 });
fs.copyFileSync('lockup-preview.jpg', 'labs-lockup-preview.jpg');
console.log(`  lockup-preview.jpg               ${fs.statSync('lockup-preview.jpg').size} bytes`);
console.log('  labs-lockup-preview.jpg          (same sheet; the README names both)');

await b.close();
