'use strict';

const fs = require('fs');
const path = require('path');
const sharp = require(path.join(__dirname, '_sharp', 'node_modules', 'sharp'));

const root = path.join(__dirname, '..');
const svg = fs.readFileSync(path.join(root, 'icons', 'icon.svg'));

async function writePng(size, file, extraPad) {
  let img = sharp(svg, { density: 384 }).resize(size, size, {
    fit: 'contain',
    background: { r: 247, g: 248, b: 250, alpha: 1 }
  });
  if (extraPad) {
    const inner = Math.round(size * 0.78);
    img = sharp(svg, { density: 384 })
      .resize(inner, inner, { fit: 'contain', background: { r: 247, g: 248, b: 250, alpha: 1 } })
      .extend({
        top: Math.floor((size - inner) / 2),
        bottom: Math.ceil((size - inner) / 2),
        left: Math.floor((size - inner) / 2),
        right: Math.ceil((size - inner) / 2),
        background: { r: 247, g: 248, b: 250, alpha: 1 }
      });
  }
  const out = path.join(root, 'icons', file);
  await img.png().toFile(out);
  console.log('wrote', out, fs.statSync(out).size);
}

(async () => {
  await writePng(180, 'icon-180.png', false);
  await writePng(192, 'icon-192.png', false);
  await writePng(512, 'icon-512.png', false);
  await writePng(192, 'icon-192-maskable.png', true);
  await writePng(512, 'icon-512-maskable.png', true);
})().catch((err) => {
  console.error(err);
  process.exit(1);
});
