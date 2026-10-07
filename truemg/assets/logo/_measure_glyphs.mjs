// Measure each LABS glyph's bounding box. Done in a browser because the glyphs are
// potrace curve data: the path's first M is not its left edge (on the A it is the
// apex), and spacing laid out from that point leaves the word reading "LA BS".
import pkg from '/opt/node-tools/node_modules/playwright/index.js';
const { chromium } = pkg; import fs from 'fs';
const b = await chromium.launch({ args: ['--no-sandbox'] });
const p = await (await b.newContext()).newPage();
await p.goto('file://' + fs.realpathSync(process.argv[2]));
console.log(JSON.stringify(await p.evaluate(() =>
  [...document.querySelectorAll('path')].map((e, i) => {
    const b = e.getBBox();
    return { i, x: +b.x.toFixed(2), w: +b.width.toFixed(2), h: +b.height.toFixed(2) };
  }))));
await b.close();
