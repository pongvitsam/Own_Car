'use strict';

const { describe, it } = require('node:test');
const assert = require('node:assert/strict');

const {
  ensureStateShape,
  parseRequiredNumber,
  nextEntityId,
  latestOdometerSafe,
  canComputeFuelSegment,
  odometerBoundsForDate,
} = require('../lib/runtime-guards');

describe('runtime guards: corrupted state', () => {
  it('fills missing arrays so filter/map never throw', () => {
    const restored = ensureStateShape({ selectedVehicleId: 'V-001' });
    assert.deepEqual(restored.vehicles, []);
    assert.deepEqual(restored.fuelLogs, []);
    assert.deepEqual(restored.maintenanceLogs, []);
    assert.deepEqual(restored.alerts, []);
    assert.deepEqual(restored.lineLogs, []);
    assert.deepEqual(restored.categories, []);
  });

  it('accepts null/undefined state', () => {
    assert.ok(Array.isArray(ensureStateShape(null).vehicles));
    assert.ok(Array.isArray(ensureStateShape(undefined).categories));
  });
});

describe('runtime guards: form numbers', () => {
  it('rejects empty and NaN odometer values that would previously save', () => {
    assert.equal(parseRequiredNumber('', 'เลขไมล์', { integer: true, min: 0 }).ok, false);
    assert.equal(parseRequiredNumber('abc', 'เลขไมล์', { integer: true, min: 0 }).ok, false);
    assert.equal(Number.isFinite(parseInt('', 10)), false);
  });

  it('rejects empty cost that would previously save as NaN', () => {
    assert.equal(parseRequiredNumber('', 'ราคา', { min: 0 }).ok, false);
    assert.equal(parseRequiredNumber('2500', 'ราคา', { min: 0 }).value, 2500);
  });
});

describe('runtime guards: ids and odometer', () => {
  it('does not reuse a deleted vehicle id hole', () => {
    const items = [{ id: 'V-001' }, { id: 'V-003' }];
    assert.equal(nextEntityId('V-', items), 'V-002');
  });

  it('latest odometer stays 0 when log arrays are missing', () => {
    assert.equal(latestOdometerSafe('V-001', undefined, undefined), 0);
    assert.equal(latestOdometerSafe('V-001', [{ vehicleId: 'V-001', odo: 100 }], [{ vehicleId: 'V-001', odo: 250 }]), 250);
  });

  it('does not divide fuel efficiency by zero liters', () => {
    assert.equal(canComputeFuelSegment(400, 0), false);
    assert.equal(canComputeFuelSegment(400, 35), true);
  });
});

describe('runtime guards: inline copies in the app match lib', () => {
  const fs = require('fs');
  const path = require('path');
  const vm = require('node:vm');
  const html = fs.readFileSync(path.join(__dirname, '../mockup/MyHome-CarCare-v1.8.html'), 'utf8');

  function extract(name) {
    const start = html.indexOf('function ' + name + '(');
    assert.ok(start >= 0, name + ' missing from app');
    let depth = 0;
    for (let i = html.indexOf('{', start); i < html.length; i++) {
      if (html[i] === '{') depth++;
      else if (html[i] === '}' && --depth === 0) return html.slice(start, i + 1);
    }
    throw new Error('unterminated ' + name);
  }

  const ctx = { state: { vehicles: [], maintenanceLogs: [], fuelLogs: [] } };
  vm.createContext(ctx);
  ['ensureStateShape', 'parseRequiredNumber', 'nextEntityId', 'odometerBoundsForDate', 'findPreviousSameTypeFullTank', 'enrichFuelLogsWithMetrics'].forEach((n) => {
    vm.runInContext(extract(n), ctx);
  });

  it('parseRequiredNumber and nextEntityId agree', () => {
    const cases = [['', { integer: true, min: 0 }], ['12', { integer: true, min: 0 }], ['-1', { min: 0 }], ['0', { gt: 0 }]];
    cases.forEach(([raw, opts]) => {
      assert.deepEqual(JSON.parse(JSON.stringify(ctx.parseRequiredNumber(raw, 'x', opts))), parseRequiredNumber(raw, 'x', opts));
    });
    const items = [{ id: 'V-001' }, { id: 'V-003' }];
    assert.equal(ctx.nextEntityId('V-', items), nextEntityId('V-', items));
  });

  it('odometer bounds keep an entry between its dated neighbours', () => {
    const maint = [{ vehicleId: 'V', odo: 1000, date: '2026-01-01' }];
    const fuel = [
      { id: 'F1', vehicleId: 'V', odo: 1500, date: '2026-02-01' },
      { id: 'F2', vehicleId: 'V', odo: 2000, date: '2026-03-01' },
    ];
    ctx.state.maintenanceLogs = maint;
    ctx.state.fuelLogs = fuel;
    const fromApp = JSON.parse(JSON.stringify(ctx.odometerBoundsForDate('V', 'F1', '2026-02-01')));
    assert.deepEqual(fromApp, odometerBoundsForDate('V', 'F1', '2026-02-01', maint, fuel));
    assert.deepEqual(fromApp, { min: 1000, max: 2000 });
  });

  it('fuel segment metrics match lib/car-logic computeFuelLogMetrics', () => {
    const { computeFuelLogMetrics } = require('../lib/car-logic');
    const logs = [
      { id: 'a', vehicleId: 'V', date: '2026-01-01', odo: 1000, liters: 30, totalCost: 900, fullTank: true, fuelType: 'oil' },
      { id: 'b', vehicleId: 'V', date: '2026-01-10', odo: 1400, liters: 35, totalCost: 1050, fullTank: true, fuelType: 'oil' },
      { id: 'c', vehicleId: 'V', date: '2026-01-20', odo: 1900, liters: 0, totalCost: 0, fullTank: true, fuelType: 'oil' },
      { id: 'd', vehicleId: 'V', date: '2026-02-01', odo: 2300, liters: 40, totalCost: 1200, fullTank: true, fuelType: 'oil' },
    ];
    const fromApp = JSON.parse(JSON.stringify(ctx.enrichFuelLogsWithMetrics(logs)));
    const fromLib = computeFuelLogMetrics('V', logs).enriched || computeFuelLogMetrics('V', logs).logs;
    assert.ok(Array.isArray(fromLib), 'lib must expose the enriched logs');
    fromApp.forEach((row) => {
      const ref = fromLib.find((l) => l.id === row.id);
      assert.equal(row.segmentDistance, ref.segmentDistance, row.id);
      assert.equal(row.costPerKm, ref.costPerKm, row.id);
      assert.equal(row.calculatedEfficiency, ref.calculatedEfficiency, row.id);
    });
  });
});
