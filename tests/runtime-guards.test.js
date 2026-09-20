'use strict';

const { describe, it } = require('node:test');
const assert = require('node:assert/strict');

const {
  ensureStateShape,
  parseRequiredNumber,
  nextEntityId,
  latestOdometerSafe,
  canComputeFuelSegment,
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
