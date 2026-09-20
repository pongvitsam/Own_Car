'use strict';

const { describe, it } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('fs');
const path = require('path');
const { spawnSync } = require('child_process');

const {
  mergeRecordsById,
  restoreSeedIfEmpty,
  shouldSkipRemoteApply,
} = require('../lib/sync-logic');

describe('local-first merge', () => {
  it('keeps local-only records when remote is stale', () => {
    const local = [{ id: 'FUEL-1', liters: 10 }, { id: 'FUEL-NEW', liters: 20 }];
    const remote = [{ id: 'FUEL-1', liters: 9 }];
    const merged = mergeRecordsById(local, remote, true);
    const ids = merged.map((x) => x.id).sort();
    assert.deepEqual(ids, ['FUEL-1', 'FUEL-NEW']);
    assert.equal(merged.find((x) => x.id === 'FUEL-1').liters, 10);
  });

  it('lets remote update shared ids when local is not preferred', () => {
    const local = [{ id: 'V-001', name: 'Old' }];
    const remote = [{ id: 'V-001', name: 'Mazda' }, { id: 'V-002', name: 'Click' }];
    const merged = mergeRecordsById(local, remote, false);
    assert.equal(merged.find((x) => x.id === 'V-001').name, 'Mazda');
    assert.equal(merged.length, 2);
  });

  it('restores seed vehicles when localStorage was emptied', () => {
    const seed = {
      vehicles: [{ id: 'V-001', name: 'Mazda' }],
      categories: [{ id: 'CAT-001', name: 'น้ำมันเครื่อง' }],
      maintenanceLogs: [{ id: 'LOG-001' }],
      fuelLogs: [{ id: 'FUEL-001' }],
      alerts: [],
    };
    const restored = restoreSeedIfEmpty({ vehicles: [], categories: [], maintenanceLogs: [] }, seed);
    assert.equal(restored.vehicles.length, 1);
    assert.equal(restored.categories.length, 1);
    assert.equal(restored.maintenanceLogs.length, 1);
  });

  it('skips remote apply while local saves are still syncing', () => {
    assert.equal(shouldSkipRemoteApply(1, 0), true);
    assert.equal(shouldSkipRemoteApply(0, 2), true);
    assert.equal(shouldSkipRemoteApply(0, 0), false);
  });
});

describe('built app script', () => {
  it('parses without syntax errors', () => {
    const html = fs.readFileSync(path.join(__dirname, '../index.html'), 'utf8');
    const scripts = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map((m) => m[1]);
    assert.ok(scripts.length >= 1, 'expected inline scripts');
    const app = scripts.reduce((a, b) => (a.length >= b.length ? a : b), '');
    const tmp = path.join(__dirname, '_app-syntax-check.js');
    fs.writeFileSync(tmp, app);
    const result = spawnSync(process.execPath, ['--check', tmp], { encoding: 'utf8' });
    fs.unlinkSync(tmp);
    assert.equal(result.status, 0, result.stderr || result.stdout);
  });

  it('starts on DOMContentLoaded instead of waiting for window.onload', () => {
    const html = fs.readFileSync(path.join(__dirname, '../index.html'), 'utf8');
    assert.match(html, /DOMContentLoaded/);
    assert.doesNotMatch(html, /window\.onload\s*=/);
    assert.match(html, /skipRefresh/);
    assert.match(html, /runWhenIdle/);
  });

  it('does not compile Tailwind in the browser', () => {
    const html = fs.readFileSync(path.join(__dirname, '../index.html'), 'utf8');
    assert.doesNotMatch(html, /cdn\.tailwindcss\.com/);
    const cssPath = path.join(__dirname, '../assets/tailwind.min.css');
    assert.equal(fs.existsSync(cssPath), true);
    assert.ok(fs.statSync(cssPath).size > 500);
  });

  it('gates the app behind a remembered device login', () => {
    const html = fs.readFileSync(path.join(__dirname, '../index.html'), 'utf8');
    assert.match(html, /id="app-login-screen"/);
    assert.match(html, /myhome_carcare_device_login_v1/);
    assert.match(html, /submitAppLogin/);
    assert.match(html, /carcare-authed/);
  });

  it('ships a multi-device installable PWA', () => {
    const html = fs.readFileSync(path.join(__dirname, '../index.html'), 'utf8');
    const manifest = fs.readFileSync(path.join(__dirname, '../manifest.webmanifest'), 'utf8');
    assert.match(html, /beforeinstallprompt/);
    assert.match(html, /installPwaApp/);
    assert.match(html, /apple-touch-icon/);
    assert.match(manifest, /icon-192\.png/);
    assert.match(manifest, /icon-512\.png/);
    assert.match(manifest, /"display": "standalone"/);
    assert.doesNotMatch(manifest, /portrait-primary/);
    ['icon-180.png', 'icon-192.png', 'icon-512.png'].forEach((name) => {
      const iconPath = path.join(__dirname, '../icons', name);
      assert.equal(fs.existsSync(iconPath), true, name);
      assert.ok(fs.statSync(iconPath).size > 1000, name);
    });
  });
});
