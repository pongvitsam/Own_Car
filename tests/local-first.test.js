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
});
